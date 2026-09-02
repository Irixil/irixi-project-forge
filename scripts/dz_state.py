#!/usr/bin/env python3
"""Small, dependency-free project ledger for DZ workflows.

The JSON snapshot is the source of truth. Every accepted mutation is also
written to an append-only journal with a full snapshot so an interrupted write
can be recovered without reconstructing state from chat.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


SCHEMA_VERSION = "1.1"
WORKFLOW_VERSION = "2026-09-02"

RUN_STATUSES = {
    "active",
    "waiting_user",
    "waiting_authorization",
    "blocked",
    "paused",
    "finished",
}
STAGES = {
    "discovery",
    "intent_draft",
    "intent_accepted",
    "spec_draft",
    "spec_accepted",
    "plan_draft",
    "plan_accepted",
    "design",
    "build",
    "test",
    "deploy",
    "maintain",
}
DECISION_STAGES = {
    "discovery",
    "intent_draft",
    "intent_accepted",
    "spec_draft",
    "spec_accepted",
    "plan_draft",
    "plan_accepted",
}
DELIVERY_STAGES = {"design", "build", "test", "deploy", "maintain"}
DELIVERY_STAGE_TRANSITIONS = {
    "plan_accepted": {"design"},
    "design": {"build"},
    "build": {"design", "test"},
    "test": {"design", "build", "deploy"},
    "deploy": {"build", "test", "maintain"},
    "maintain": {"design", "build", "test", "deploy"},
}
PRODUCT_VERDICTS = {
    "not_assessed",
    "implemented_unverified",
    "partially_verified",
    "verified",
    "cancelled",
}
VERDICT_RANK = {
    "not_assessed": 0,
    "implemented_unverified": 1,
    "partially_verified": 2,
    "verified": 3,
}
DECISION_STATUSES = {"not_created", "draft", "accepted", "superseded"}
DECISION_TRANSITIONS = {
    "not_created": {"draft"},
    "draft": {"accepted", "superseded"},
    "accepted": {"superseded"},
    "superseded": {"draft"},
}
WORK_STATUSES = {
    "pending",
    "in_progress",
    "implemented_unverified",
    "verified",
    "waiting_user",
    "blocked",
    "deferred",
    "cancelled",
}
WORK_TRANSITIONS = {
    "pending": {"in_progress", "waiting_user", "blocked", "deferred", "cancelled"},
    "in_progress": {"implemented_unverified", "waiting_user", "blocked", "cancelled"},
    "implemented_unverified": {"in_progress", "verified", "blocked", "deferred", "cancelled"},
    "waiting_user": {"in_progress", "deferred", "cancelled"},
    "blocked": {"in_progress", "deferred", "cancelled"},
    "verified": {"in_progress"},
    "deferred": {"pending"},
    "cancelled": {"pending"},
}
RISK_LEVELS = {"low", "medium", "high", "critical"}
RISK_DECISIONS = {"open", "accepted", "mitigated", "declined"}
RISK_ACTION_STATUSES = {
    "not_applicable",
    "pending_authorization",
    "authorized",
    "completed",
    "failed",
    "cancelled",
    "declined",
}
RISK_ACTION_KINDS = {
    "informational",
    "spend",
    "external_write",
    "delete",
    "migration",
    "public_release",
    "production_access",
    "sensitive_data",
    "other_action",
}
AUTHORIZATION_ACTION_KINDS = RISK_ACTION_KINDS - {"informational"}
TARGET_BOUND_ACTION_KINDS = {"public_release", "production_access"}
EVIDENCE_RESULTS = {"passed", "failed", "unverified"}
BLOCKER_KINDS = {
    "missing_capability",
    "missing_authority",
    "missing_external_condition",
    "host_denial",
    "rights_missing",
}
DIGEST_LENGTH = 64
GUIDANCE_START = "<!-- DZ-PROJECT-CONTINUITY:START -->"
GUIDANCE_END = "<!-- DZ-PROJECT-CONTINUITY:END -->"
PROJECT_GUIDANCE_TEMPLATE = (
    Path(__file__).resolve().parents[1] / "assets" / "project" / "AGENTS.md"
)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
    if size == 0:
        raise ValueError(f"Evidence or decision artifact is empty: {path}")
    return digest.hexdigest()


def project_file(project: Path, value: str, label_name: str) -> tuple[str, Path]:
    relative = Path(value)
    if relative.is_absolute():
        raise ValueError(f"{label_name} must be a path inside the project")
    project_root = project.resolve()
    resolved = (project_root / relative).resolve()
    try:
        normalized = resolved.relative_to(project_root).as_posix()
    except ValueError as exc:
        raise ValueError(f"{label_name} must stay inside the project") from exc
    if not resolved.is_file():
        raise ValueError(f"{label_name} does not exist: {normalized}")
    return normalized, resolved


def stored_file_matches(project: Path, path_value: Any, digest_value: Any) -> bool:
    if not isinstance(path_value, str) or not isinstance(digest_value, str):
        return False
    try:
        _, path = project_file(project, path_value, "stored artifact")
        return sha256_file(path) == digest_value
    except (OSError, ValueError):
        return False


def project_paths(project: Path) -> dict[str, Path]:
    dz_dir = project / ".dz"
    return {
        "state": dz_dir / "state.json",
        "journal": dz_dir / "journal.jsonl",
        "dashboard": project / "PROJECT.md",
        "work_items": project / "docs" / "sdlc" / "work-items.md",
    }


def empty_target() -> dict[str, None]:
    return {
        "id": None,
        "contract_sha256": None,
        "revision": None,
        "environment": None,
        "source": None,
        "artifact_path": None,
        "artifact_sha256": None,
        "set_at": None,
    }


def parse_utc_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def initial_state(name: str, language: str) -> dict[str, Any]:
    timestamp = now()
    return {
        "schema_version": SCHEMA_VERSION,
        "workflow_version": WORKFLOW_VERSION,
        "project": {"name": name, "language": language},
        "run": {
            "status": "active",
            "product_verdict": "not_assessed",
            "stage": "discovery",
            "next_action": "Clarify the next product decision",
            "waiting_for": None,
            "pending_risk_id": None,
            "authorized_risk_id": None,
            "blocker": None,
            "blocker_kind": None,
            "resume_when": None,
            "finish_reason": None,
            "updated_at": timestamp,
        },
        "decisions": {
            "intent": {
                "status": "not_created",
                "path": "docs/sdlc/intent.md",
                "artifact_sha256": None,
                "accepted_by": None,
                "acceptance_reference": None,
                "accepted_at": None,
            },
            "spec": {
                "status": "not_created",
                "path": "docs/sdlc/spec.md",
                "artifact_sha256": None,
                "accepted_by": None,
                "acceptance_reference": None,
                "accepted_at": None,
            },
            "plan": {
                "status": "not_created",
                "path": "docs/sdlc/plan.md",
                "artifact_sha256": None,
                "accepted_by": None,
                "acceptance_reference": None,
                "accepted_at": None,
            },
        },
        "target": empty_target(),
        "work_items": [],
        "evidence": [],
        "risks": [],
    }


def load_state(project: Path) -> dict[str, Any]:
    path = project_paths(project)["state"]
    if not path.is_file():
        raise ValueError(f"DZ state not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read DZ state: {exc}") from exc


def duplicate_ids(items: list[dict[str, Any]]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if item_id in seen:
            duplicates.add(item_id)
        seen.add(item_id)
    return duplicates


def is_canonical_id(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and value == value.strip()
        and not any(character.isspace() for character in value)
    )


def accepted_decision_chain(decisions: dict[str, Any]) -> bool:
    return all(decisions.get(name, {}).get("status") == "accepted" for name in ("intent", "spec", "plan"))


def accepted_contract_sha256(decisions: dict[str, Any]) -> str | None:
    if not accepted_decision_chain(decisions):
        return None
    digests = [decisions[name].get("artifact_sha256") for name in ("intent", "spec", "plan")]
    if not all(isinstance(value, str) and len(value) == DIGEST_LENGTH for value in digests):
        return None
    return hashlib.sha256("\0".join(digests).encode("ascii")).hexdigest()


def current_target(state: dict[str, Any]) -> tuple[str, str, str] | None:
    target = state.get("target")
    if not isinstance(target, dict):
        return None
    if target.get("contract_sha256") != accepted_contract_sha256(
        state.get("decisions", {})
    ):
        return None
    target_id = target.get("id")
    revision = target.get("revision")
    environment = target.get("environment")
    if not is_canonical_id(target_id):
        return None
    if not isinstance(revision, str) or not revision.strip():
        return None
    if not isinstance(environment, str) or not environment.strip():
        return None
    return target_id, revision, environment


def invalidate_verification_target(state: dict[str, Any]) -> None:
    state["target"] = empty_target()
    for item in state.get("work_items", []):
        if isinstance(item, dict) and item.get("status") == "verified":
            item["status"] = "implemented_unverified"
            item["updated_at"] = now()


def risk_context_matches(state: dict[str, Any], risk: dict[str, Any]) -> bool:
    if risk.get("lease_contract_sha256") != accepted_contract_sha256(
        state.get("decisions", {})
    ):
        return False
    target = current_target(state)
    recorded_target = (
        risk.get("lease_target_id"),
        risk.get("lease_revision"),
        risk.get("lease_environment"),
    )
    if target is None:
        return recorded_target == (None, None, None)
    return recorded_target == target


def authorized_action(state: dict[str, Any]) -> dict[str, Any] | None:
    risk_id = state.get("run", {}).get("authorized_risk_id")
    if risk_id is None:
        return None
    for risk in state.get("risks", []):
        if isinstance(risk, dict) and risk.get("id") == risk_id:
            return risk
    return None


def action_lease_is_expired(
    risk: dict[str, Any], reference_time: datetime | None = None
) -> bool:
    expires_at = parse_utc_timestamp(risk.get("expires_at"))
    return expires_at is None or expires_at <= (
        reference_time or datetime.now(timezone.utc)
    )


def active_authorized_lease_errors(state: Any) -> list[str]:
    if not isinstance(state, dict):
        return []
    run = state.get("run")
    if not isinstance(run, dict) or run.get("status") != "active":
        return []
    risks = state.get("risks")
    if not isinstance(risks, list):
        return []
    risk_id = run.get("authorized_risk_id")
    for risk in risks:
        if (
            isinstance(risk, dict)
            and risk.get("id") == risk_id
            and risk.get("action_status") == "authorized"
            and risk.get("action_kind") in AUTHORIZATION_ACTION_KINDS
            and action_lease_is_expired(risk)
        ):
            return [
                f"{risk_id}: active authorized action lease has expired; "
                "cancel it and request fresh authorization"
            ]
    return []


def derive_product_verdict(
    work_items: list[dict[str, Any]], decisions: dict[str, Any]
) -> str:
    if not accepted_decision_chain(decisions):
        return "not_assessed"
    current_contract = accepted_contract_sha256(decisions)
    relevant = [
        item
        for item in work_items
        if item.get("required") is True
        and item.get("contract_sha256") == current_contract
    ]
    if not relevant:
        return "not_assessed"
    statuses = [item.get("status") for item in relevant]
    verified_count = sum(status == "verified" for status in statuses)
    if verified_count == len(statuses) and accepted_decision_chain(decisions):
        return "verified"
    if verified_count:
        return "partially_verified"
    if any(status in {"in_progress", "implemented_unverified"} for status in statuses):
        return "implemented_unverified"
    return "not_assessed"


def current_plan_work(
    state: dict[str, Any], phases: set[str] | None = None
) -> list[dict[str, Any]]:
    contract_digest = accepted_contract_sha256(state.get("decisions", {}))
    return [
        item
        for item in state.get("work_items", [])
        if isinstance(item, dict)
        and item.get("required") is True
        and item.get("contract_sha256") == contract_digest
        and (phases is None or item.get("phase") in phases)
    ]


def stage_transition_errors(
    state: dict[str, Any], old_stage: str, new_stage: str
) -> list[str]:
    errors: list[str] = []
    if (old_stage, new_stage) == ("design", "build"):
        items = current_plan_work(state, {"design"})
        if not items or any(item.get("status") != "verified" for item in items):
            errors.append("Design must have required verified work before Build")
    elif (old_stage, new_stage) == ("build", "test"):
        design = current_plan_work(state, {"design"})
        build = current_plan_work(state, {"build"})
        if not design or any(item.get("status") != "verified" for item in design):
            errors.append("Required Design work must be verified before Test")
        if not build or any(
            item.get("status") not in {"implemented_unverified", "verified"}
            for item in build
        ):
            errors.append("Build must have required implemented work before Test")
    elif (old_stage, new_stage) == ("test", "deploy"):
        items = current_plan_work(state, {"design", "build", "test"})
        phases = {item.get("phase") for item in items}
        if not {"design", "build", "test"}.issubset(phases) or any(
            item.get("status") != "verified" for item in items
        ):
            errors.append("Required Design, Build, and Test work must be verified before Deploy")
        if current_target(state) is None:
            errors.append("An observed verification target is required before Deploy")
    elif (old_stage, new_stage) == ("deploy", "maintain"):
        items = current_plan_work(state, {"design", "build", "test", "deploy"})
        phases = {item.get("phase") for item in items}
        if not {"design", "build", "test", "deploy"}.issubset(phases) or any(
            item.get("status") != "verified" for item in items
        ):
            errors.append("Required release work must be verified before Maintain")
    return errors


def work_verification_support(
    work_item: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    evidence_ids: list[str],
    project_path: Path | None,
    target: tuple[str, str, str] | None,
) -> tuple[set[tuple[Any, Any]], list[str]]:
    if not evidence_ids or target is None:
        return set(), []
    current_target = target
    passed = [
        entry
        for entry in evidence_ids
        if evidence_by_id[entry].get("result") == "passed"
        and (
            evidence_by_id[entry].get("target_id"),
            evidence_by_id[entry].get("revision"),
            evidence_by_id[entry].get("environment"),
        )
        == current_target
        and (
            project_path is None
            or stored_file_matches(
                project_path,
                evidence_by_id[entry].get("artifact_path"),
                evidence_by_id[entry].get("artifact_sha256"),
            )
        )
    ]
    accepted_criteria = set(work_item.get("acceptance", []))
    complete_targets = (
        {current_target}
        if accepted_criteria.issubset(
            {evidence_by_id[entry].get("acceptance") for entry in passed}
        )
        else set()
    )
    resolved = {
        resolved_id
        for entry in passed
        for resolved_id in evidence_by_id[entry].get("resolves") or []
    }
    unresolved = [
        entry
        for entry in evidence_ids
        if (
            evidence_by_id[entry].get("target_id"),
            evidence_by_id[entry].get("revision"),
            evidence_by_id[entry].get("environment"),
        )
        == current_target
        and evidence_by_id[entry].get("result") != "passed"
        and entry not in resolved
    ]
    return complete_targets, unresolved


def reconcile_stale_artifacts(project: Path, state: dict[str, Any]) -> None:
    decisions = state["decisions"]
    invalidated_decision: str | None = None
    for index, name in enumerate(("intent", "spec", "plan")):
        decision = decisions[name]
        if decision.get("status") == "accepted" and not stored_file_matches(
            project, decision.get("path"), decision.get("artifact_sha256")
        ):
            decision["status"] = "superseded"
            for downstream in ("intent", "spec", "plan")[index + 1 :]:
                if decisions[downstream]["status"] != "not_created":
                    decisions[downstream]["status"] = "superseded"
            invalidated_decision = name
            break

    if invalidated_decision is not None:
        state["run"]["stage"] = {
            "intent": "discovery",
            "spec": "intent_accepted",
            "plan": "spec_accepted",
        }[invalidated_decision]
        invalidate_verification_target(state)

    target = state.get("target")
    if (
        isinstance(target, dict)
        and target.get("id") is not None
        and (
            current_target(state) is None
            or not stored_file_matches(
                project, target.get("artifact_path"), target.get("artifact_sha256")
            )
        )
    ):
        invalidate_verification_target(state)

    evidence_by_id = {
        item["id"]: item
        for item in state["evidence"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for item in state["work_items"]:
        if item.get("status") != "verified":
            continue
        evidence_ids = [
            evidence_id
            for evidence_id in item.get("evidence_ids", [])
            if evidence_id in evidence_by_id
        ]
        complete_revisions, unresolved = work_verification_support(
            item, evidence_by_id, evidence_ids, project, current_target(state)
        )
        if not complete_revisions or unresolved:
            item["status"] = "implemented_unverified"
            item["updated_at"] = now()

    run = state["run"]
    lease = authorized_action(state)
    if (
        run.get("status") == "active"
        and lease is not None
        and not risk_context_matches(state, lease)
    ):
        run.update(
            {
                "status": "paused",
                "next_action": None,
                "waiting_for": None,
                "pending_risk_id": None,
                "blocker": None,
                "blocker_kind": None,
                "resume_when": "Record the old authorized action outcome, then request fresh authorization for the current contract and target",
                "finish_reason": None,
            }
        )
    derived_verdict = derive_product_verdict(state["work_items"], decisions)
    if (
        run.get("status") == "finished"
        and run.get("product_verdict") in VERDICT_RANK
        and VERDICT_RANK[run["product_verdict"]] > VERDICT_RANK[derived_verdict]
    ):
        if derived_verdict == "not_assessed":
            run.update(
                {
                    "status": "paused",
                    "product_verdict": derived_verdict,
                    "next_action": None,
                    "waiting_for": None,
                    "pending_risk_id": None,
                    "blocker": None,
                    "blocker_kind": None,
                    "resume_when": "Reconfirm the changed decision or restore fresh evidence before resuming",
                    "finish_reason": None,
                }
            )
        else:
            run["product_verdict"] = derived_verdict


def _validate_state(state: dict[str, Any], project_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(state, dict):
        return ["state must be an object"]

    root_fields = {
        "schema_version",
        "workflow_version",
        "project",
        "run",
        "decisions",
        "target",
        "work_items",
        "evidence",
        "risks",
    }
    unknown_root = set(state) - root_fields
    missing_root = root_fields - set(state)
    if unknown_root:
        errors.append(f"unknown root fields: {', '.join(sorted(unknown_root))}")
    if missing_root:
        errors.append(f"missing root fields: {', '.join(sorted(missing_root))}")
    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if not isinstance(state.get("workflow_version"), str) or not state.get(
        "workflow_version", ""
    ).strip():
        errors.append("workflow_version is required")

    project = state.get("project")
    if not isinstance(project, dict):
        errors.append("project must be an object")
        project = {}
    else:
        unknown = set(project) - {"name", "language"}
        if unknown:
            errors.append(f"unknown project fields: {', '.join(sorted(unknown))}")
    if not isinstance(project.get("name"), str) or not project.get("name", "").strip():
        errors.append("project.name is required")
    if project.get("language") not in {"zh", "en"}:
        errors.append("project.language must be zh or en")

    run = state.get("run")
    run_fields = {
        "status",
        "product_verdict",
        "stage",
        "next_action",
        "waiting_for",
        "pending_risk_id",
        "authorized_risk_id",
        "blocker",
        "blocker_kind",
        "resume_when",
        "finish_reason",
        "updated_at",
    }
    if not isinstance(run, dict):
        errors.append("run must be an object")
        run = {}
    else:
        unknown = set(run) - run_fields
        missing = run_fields - set(run)
        if unknown:
            errors.append(f"unknown run fields: {', '.join(sorted(unknown))}")
        if missing:
            errors.append(f"missing run fields: {', '.join(sorted(missing))}")
    for field in (
        "next_action",
        "waiting_for",
        "pending_risk_id",
        "authorized_risk_id",
        "blocker",
        "blocker_kind",
        "resume_when",
        "finish_reason",
    ):
        if run.get(field) is not None and not isinstance(run.get(field), str):
            errors.append(f"run.{field} must be a string or null")
    if run.get("pending_risk_id") is not None and not is_canonical_id(
        run.get("pending_risk_id")
    ):
        errors.append("run.pending_risk_id must be a canonical ID without whitespace")
    if run.get("authorized_risk_id") is not None and not is_canonical_id(
        run.get("authorized_risk_id")
    ):
        errors.append("run.authorized_risk_id must be a canonical ID without whitespace")
    status = run.get("status")
    verdict = run.get("product_verdict")
    if status not in RUN_STATUSES:
        errors.append(f"invalid run.status: {status}")
    if verdict not in PRODUCT_VERDICTS:
        errors.append(f"invalid run.product_verdict: {verdict}")
    stage = run.get("stage")
    if stage not in STAGES:
        errors.append(f"invalid run.stage: {stage}")
    if not isinstance(run.get("updated_at"), str) or not run.get(
        "updated_at", ""
    ).strip():
        errors.append("run.updated_at is required")
    if status == "active" and not str(run.get("next_action") or "").strip():
        errors.append("active run requires next_action")
    if status in {"waiting_user", "waiting_authorization"} and not str(
        run.get("waiting_for") or ""
    ).strip():
        errors.append(f"{status} requires waiting_for")
    if status == "waiting_authorization" and not str(
        run.get("pending_risk_id") or ""
    ).strip():
        errors.append("waiting_authorization requires pending_risk_id")
    if status != "waiting_authorization" and run.get("pending_risk_id") is not None:
        errors.append("pending_risk_id is valid only while waiting_authorization")
    if status == "blocked":
        if not str(run.get("blocker") or "").strip():
            errors.append("blocked run requires blocker")
        if run.get("blocker_kind") not in BLOCKER_KINDS:
            errors.append("blocked run requires a valid blocker_kind")
        if not str(run.get("resume_when") or "").strip():
            errors.append("blocked run requires resume_when")
    elif run.get("blocker_kind") is not None:
        errors.append("blocker_kind is valid only while blocked")
    if status == "paused" and not str(run.get("resume_when") or "").strip():
        errors.append("paused run requires resume_when")
    if status == "finished":
        if verdict in {None, "not_assessed"}:
            errors.append("finished run requires a final product_verdict")
        if not str(run.get("finish_reason") or "").strip():
            errors.append("finished run requires finish_reason")

    null_fields_by_status = {
        "active": (
            "waiting_for",
            "pending_risk_id",
            "blocker",
            "blocker_kind",
            "resume_when",
            "finish_reason",
        ),
        "waiting_user": (
            "pending_risk_id",
            "blocker",
            "blocker_kind",
            "resume_when",
            "finish_reason",
        ),
        "waiting_authorization": (
            "next_action",
            "authorized_risk_id",
            "blocker",
            "blocker_kind",
            "resume_when",
            "finish_reason",
        ),
        "blocked": ("waiting_for", "pending_risk_id", "finish_reason"),
        "paused": (
            "waiting_for",
            "pending_risk_id",
            "blocker",
            "blocker_kind",
            "finish_reason",
        ),
        "finished": ("waiting_for", "pending_risk_id", "blocker", "blocker_kind"),
    }
    for field in null_fields_by_status.get(status, ()):
        if run.get(field) is not None:
            errors.append(f"run.{field} must be null while run.status is {status}")
    if status not in {"blocked", "paused", "finished"} and run.get("resume_when") is not None:
        errors.append(f"run.resume_when is not valid while run.status is {status}")
    if status != "finished" and run.get("finish_reason") is not None:
        errors.append("run.finish_reason is valid only while finished")

    decisions = state.get("decisions")
    if not isinstance(decisions, dict):
        errors.append("decisions must be an object")
        decisions = {}
    else:
        unknown = set(decisions) - {"intent", "spec", "plan"}
        missing = {"intent", "spec", "plan"} - set(decisions)
        if unknown:
            errors.append(f"unknown decisions: {', '.join(sorted(unknown))}")
        if missing:
            errors.append(f"missing decisions: {', '.join(sorted(missing))}")
    for name in ("intent", "spec", "plan"):
        decision = decisions.get(name)
        if not isinstance(decision, dict):
            errors.append(f"decisions.{name} must be an object")
            continue
        decision_fields = {
            "status",
            "path",
            "artifact_sha256",
            "accepted_by",
            "acceptance_reference",
            "accepted_at",
        }
        unknown = set(decision) - decision_fields
        missing = decision_fields - set(decision)
        if unknown:
            errors.append(
                f"unknown decisions.{name} fields: {', '.join(sorted(unknown))}"
            )
        if missing:
            errors.append(
                f"missing decisions.{name} fields: {', '.join(sorted(missing))}"
            )
        if decision.get("status") not in DECISION_STATUSES:
            errors.append(f"decisions.{name} has an invalid status")
        if not isinstance(decision.get("path"), str) or not decision.get(
            "path", ""
        ).strip():
            errors.append(f"decisions.{name}.path is required")
        digest = decision.get("artifact_sha256")
        digest_valid = (
            isinstance(digest, str)
            and len(digest) == DIGEST_LENGTH
            and all(character in "0123456789abcdef" for character in digest)
        )
        metadata = (
            decision.get("accepted_by"),
            decision.get("acceptance_reference"),
            decision.get("accepted_at"),
        )
        metadata_present = all(
            isinstance(value, str) and value.strip() for value in metadata
        )
        metadata_empty = all(value is None for value in metadata)
        decision_status = decision.get("status")
        if decision_status == "not_created":
            if digest is not None or not metadata_empty:
                errors.append(f"decisions.{name}: not_created cannot contain artifact or acceptance metadata")
        elif decision_status == "draft":
            if not digest_valid:
                errors.append(f"decisions.{name}: draft requires an artifact digest")
            if not metadata_empty:
                errors.append(f"decisions.{name}: draft cannot contain acceptance metadata")
        elif decision_status == "accepted":
            if not digest_valid:
                errors.append(f"decisions.{name}: accepted requires an artifact digest")
            if not metadata_present:
                errors.append(f"decisions.{name}: accepted requires owner, reference, and time")
        elif decision_status == "superseded":
            if not digest_valid:
                errors.append(f"decisions.{name}: superseded requires its prior artifact digest")
            if not (metadata_empty or metadata_present):
                errors.append(f"decisions.{name}: superseded acceptance metadata must be complete or empty")
        if (
            project_path is not None
            and decision_status in {"draft", "accepted"}
            and digest_valid
            and not stored_file_matches(project_path, decision.get("path"), digest)
        ):
            errors.append(f"decisions.{name}: artifact is missing, empty, or changed")
    if decisions.get("spec", {}).get("status") in {"draft", "accepted"} and decisions.get(
        "intent", {}
    ).get("status") != "accepted":
        errors.append("specification requires accepted intent")
    if decisions.get("plan", {}).get("status") in {"draft", "accepted"}:
        if decisions.get("intent", {}).get("status") != "accepted":
            errors.append("plan requires accepted intent")
        if decisions.get("spec", {}).get("status") != "accepted":
            errors.append("plan requires accepted specification")
    if stage in DELIVERY_STAGES and not accepted_decision_chain(decisions):
        errors.append("delivery stages require accepted intent, specification, and plan")

    target = state.get("target")
    target_fields = {
        "id",
        "contract_sha256",
        "revision",
        "environment",
        "source",
        "artifact_path",
        "artifact_sha256",
        "set_at",
    }
    if not isinstance(target, dict):
        errors.append("target must be an object")
        target = {}
    else:
        unknown = set(target) - target_fields
        missing = target_fields - set(target)
        if unknown:
            errors.append(f"unknown target fields: {', '.join(sorted(unknown))}")
        if missing:
            errors.append(f"missing target fields: {', '.join(sorted(missing))}")
    target_values = tuple(target.get(field) for field in target_fields)
    if all(value is None for value in target_values):
        pass
    elif any(value is None for value in target_values):
        errors.append("target fields must be all present or all null")
    else:
        for field in ("id", "contract_sha256", "revision", "environment", "source", "artifact_path", "set_at"):
            if not isinstance(target.get(field), str) or not target.get(field, "").strip():
                errors.append(f"target.{field} is required")
        if not is_canonical_id(target.get("id")):
            errors.append("target.id must be a canonical ID without whitespace")
        contract_digest = target.get("contract_sha256")
        if not (
            isinstance(contract_digest, str)
            and len(contract_digest) == DIGEST_LENGTH
            and all(character in "0123456789abcdef" for character in contract_digest)
        ):
            errors.append("target.contract_sha256 is invalid")
        if str(target.get("source") or "").strip().lower() in {
            "self assertion",
            "model claim",
            "trust me",
            "unknown",
            "n/a",
        }:
            errors.append("target.source is not inspectable evidence")
        digest = target.get("artifact_sha256")
        digest_valid = (
            isinstance(digest, str)
            and len(digest) == DIGEST_LENGTH
            and all(character in "0123456789abcdef" for character in digest)
        )
        if not digest_valid:
            errors.append("target.artifact_sha256 is invalid")
        if project_path is not None and digest_valid and not stored_file_matches(
            project_path, target.get("artifact_path"), digest
        ):
            errors.append("target proof is missing, empty, or changed")

    raw_work_items = state.get("work_items")
    raw_evidence = state.get("evidence")
    raw_risks = state.get("risks")
    if not isinstance(raw_work_items, list):
        errors.append("work_items must be an array")
        raw_work_items = []
    if not isinstance(raw_evidence, list):
        errors.append("evidence must be an array")
        raw_evidence = []
    if not isinstance(raw_risks, list):
        errors.append("risks must be an array")
        raw_risks = []

    work_items: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    risks: list[dict[str, Any]] = []
    for label, raw_items, valid_items in (
        ("work item", raw_work_items, work_items),
        ("evidence", raw_evidence, evidence),
        ("risk", raw_risks, risks),
    ):
        for index, item in enumerate(raw_items):
            if not isinstance(item, dict):
                errors.append(f"{label} at index {index} must be an object")
            else:
                valid_items.append(item)
        duplicates = duplicate_ids(valid_items)
        if duplicates:
            errors.append(f"duplicate {label} ids: {', '.join(sorted(duplicates))}")

    work_fields = {
        "id",
        "title",
        "required",
        "contract_sha256",
        "phase",
        "status",
        "acceptance",
        "evidence_ids",
        "note",
        "blocker",
        "updated_at",
    }
    in_progress = 0
    work_by_id: dict[str, dict[str, Any]] = {}
    for item in work_items:
        item_id = item.get("id") if is_canonical_id(item.get("id")) else ""
        unknown = set(item) - work_fields
        missing = work_fields - set(item)
        if unknown:
            errors.append(f"{item_id or 'work item'}: unknown fields: {', '.join(sorted(unknown))}")
        if missing:
            errors.append(f"{item_id or 'work item'}: missing fields: {', '.join(sorted(missing))}")
        if not item_id:
            errors.append("every work item ID must be non-empty and contain no whitespace")
        if not isinstance(item.get("title"), str) or not item.get(
            "title", ""
        ).strip():
            errors.append(f"{item_id or 'work item'}: title is required")
        if item_id:
            work_by_id[item_id] = item
        if not isinstance(item.get("required"), bool):
            errors.append(f"{item_id or 'work item'}: required must be boolean")
        plan_digest = item.get("contract_sha256")
        if not (
            isinstance(plan_digest, str)
            and len(plan_digest) == DIGEST_LENGTH
            and all(character in "0123456789abcdef" for character in plan_digest)
        ):
            errors.append(f"{item_id or 'work item'}: contract_sha256 is invalid")
        if item.get("phase") not in DELIVERY_STAGES:
            errors.append(f"{item_id or 'work item'}: invalid work phase")
        if item.get("status") not in WORK_STATUSES:
            errors.append(f"{item_id or 'work item'}: invalid work status")
        if item.get("status") == "in_progress":
            in_progress += 1
        acceptance = item.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance or any(
            not isinstance(entry, str) or not entry.strip() for entry in acceptance
        ):
            errors.append(f"{item_id or 'work item'}: acceptance must contain text")
        elif len(acceptance) != len(set(acceptance)):
            errors.append(f"{item_id or 'work item'}: duplicate acceptance criteria")
        evidence_ids = item.get("evidence_ids")
        if not isinstance(evidence_ids, list) or any(
            not is_canonical_id(entry) for entry in (evidence_ids or [])
        ):
            errors.append(
                f"{item_id or 'work item'}: evidence_ids must contain canonical IDs without whitespace"
            )
        elif len(evidence_ids) != len(set(evidence_ids)):
            errors.append(f"{item_id or 'work item'}: duplicate evidence_ids")
        if item.get("note") is not None and not isinstance(item.get("note"), str):
            errors.append(f"{item_id or 'work item'}: note must be string or null")
        if item.get("blocker") is not None and not isinstance(item.get("blocker"), str):
            errors.append(f"{item_id or 'work item'}: blocker must be string or null")
        if item.get("status") == "blocked" and not str(item.get("blocker") or "").strip():
            errors.append(f"{item_id or 'work item'}: blocked work requires blocker")
        if not isinstance(item.get("updated_at"), str) or not item.get(
            "updated_at", ""
        ).strip():
            errors.append(f"{item_id or 'work item'}: updated_at is required")
    if in_progress > 1:
        errors.append("only one work item may be in_progress")
    evidence_fields = {
        "id",
        "work_item_id",
        "contract_sha256",
        "target_id",
        "acceptance",
        "kind",
        "claim",
        "source",
        "artifact_path",
        "artifact_sha256",
        "revision",
        "environment",
        "result",
        "resolves",
        "recorded_at",
    }
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for item in evidence:
        item_id = item.get("id") if is_canonical_id(item.get("id")) else ""
        unknown = set(item) - evidence_fields
        missing = evidence_fields - set(item)
        if unknown:
            errors.append(f"{item_id or 'evidence'}: unknown fields: {', '.join(sorted(unknown))}")
        if missing:
            errors.append(f"{item_id or 'evidence'}: missing fields: {', '.join(sorted(missing))}")
        if not item_id:
            errors.append("every evidence ID must be non-empty and contain no whitespace")
        else:
            evidence_by_id[item_id] = item
        for field in (
            "work_item_id",
            "kind",
            "claim",
            "source",
            "artifact_path",
            "revision",
            "environment",
            "recorded_at",
        ):
            if not isinstance(item.get(field), str) or not item.get(field, "").strip():
                errors.append(f"{item_id or 'evidence'}: {field} is required")
        if not is_canonical_id(item.get("work_item_id")):
            errors.append(
                f"{item_id or 'evidence'}: work_item_id must be a canonical ID without whitespace"
            )
        if not is_canonical_id(item.get("target_id")):
            errors.append(
                f"{item_id or 'evidence'}: target_id must be a canonical ID without whitespace"
            )
        plan_digest = item.get("contract_sha256")
        if not (
            isinstance(plan_digest, str)
            and len(plan_digest) == DIGEST_LENGTH
            and all(character in "0123456789abcdef" for character in plan_digest)
        ):
            errors.append(f"{item_id or 'evidence'}: contract_sha256 is invalid")
        if not isinstance(item.get("acceptance"), str) or not item.get(
            "acceptance", ""
        ).strip():
            errors.append(f"{item_id or 'evidence'}: acceptance is required")
        if str(item.get("source") or "").strip().lower() in {
            "self assertion",
            "model claim",
            "trust me",
            "unknown",
            "n/a",
        }:
            errors.append(f"{item_id or 'evidence'}: source is not inspectable evidence")
        if item.get("result") not in EVIDENCE_RESULTS:
            errors.append(f"{item_id or 'evidence'}: invalid result")
        artifact_digest = item.get("artifact_sha256")
        if not (
            isinstance(artifact_digest, str)
            and len(artifact_digest) == DIGEST_LENGTH
            and all(character in "0123456789abcdef" for character in artifact_digest)
        ):
            errors.append(f"{item_id or 'evidence'}: artifact_sha256 is invalid")
        resolves = item.get("resolves")
        if not isinstance(resolves, list) or any(
            not is_canonical_id(entry) for entry in (resolves or [])
        ):
            errors.append(
                f"{item_id or 'evidence'}: resolves must contain canonical IDs without whitespace"
            )
        elif len(resolves) != len(set(resolves)):
            errors.append(f"{item_id or 'evidence'}: duplicate resolves ids")

    evidence_for_work: dict[str, list[str]] = {item_id: [] for item_id in work_by_id}
    for item_id, item in evidence_by_id.items():
        work_item_id = item.get("work_item_id")
        if work_item_id not in work_by_id:
            errors.append(f"{item_id}: unknown work_item_id: {work_item_id}")
            continue
        if item.get("contract_sha256") != work_by_id[work_item_id].get("contract_sha256"):
            errors.append(f"{item_id}: evidence must use its work item's decision contract digest")
        criterion = item.get("acceptance")
        if criterion not in work_by_id[work_item_id].get("acceptance", []):
            errors.append(f"{item_id}: evidence must name an exact acceptance criterion")
        evidence_for_work[work_item_id].append(item_id)
        for resolved_id in item.get("resolves") or []:
            resolved = evidence_by_id.get(resolved_id)
            if resolved is None:
                errors.append(f"{item_id}: unknown resolved evidence: {resolved_id}")
            elif resolved.get("work_item_id") != work_item_id:
                errors.append(f"{item_id}: cannot resolve evidence for another work item")
            elif resolved.get("acceptance") != criterion:
                errors.append(f"{item_id}: cannot resolve a different acceptance criterion")
            elif (
                resolved.get("target_id"),
                resolved.get("revision"),
                resolved.get("environment"),
            ) != (
                item.get("target_id"),
                item.get("revision"),
                item.get("environment"),
            ):
                errors.append(
                    f"{item_id}: may resolve evidence only in the same target epoch"
                )
            elif resolved.get("result") == "passed":
                errors.append(f"{item_id}: passed evidence does not need resolution")
            elif item.get("result") != "passed":
                errors.append(f"{item_id}: only passed evidence may resolve a gap")

    for item_id, item in work_by_id.items():
        linked = item.get("evidence_ids") if isinstance(item.get("evidence_ids"), list) else []
        actual = evidence_for_work.get(item_id, [])
        if set(linked) != set(actual):
            errors.append(f"{item_id}: evidence_ids must match append-only evidence history")
        if item.get("status") == "verified":
            complete_revisions, unresolved = work_verification_support(
                item, evidence_by_id, actual, project_path, current_target(state)
            )
            if not complete_revisions:
                errors.append(
                    f"{item_id}: verified work needs intact passed evidence for every acceptance criterion at one revision"
                )
            if unresolved:
                errors.append(
                    f"{item_id}: verified work has unresolved evidence: {', '.join(unresolved)}"
                )

    risk_fields = {
        "id",
        "title",
        "level",
        "action_kind",
        "consequence",
        "safer_option",
        "recovery",
        "scope",
        "lease_contract_sha256",
        "lease_target_id",
        "lease_revision",
        "lease_environment",
        "amount_limit",
        "expires_at",
        "authorization_pending",
        "decision",
        "action_status",
        "action_reference",
        "action_at",
        "decision_by",
        "decision_reference",
        "decided_at",
    }
    risk_by_id: dict[str, dict[str, Any]] = {}
    for risk in risks:
        risk_id = risk.get("id") if is_canonical_id(risk.get("id")) else ""
        unknown = set(risk) - risk_fields
        missing = risk_fields - set(risk)
        if unknown:
            errors.append(f"{risk_id or 'risk'}: unknown fields: {', '.join(sorted(unknown))}")
        if missing:
            errors.append(f"{risk_id or 'risk'}: missing fields: {', '.join(sorted(missing))}")
        if not risk_id:
            errors.append("every risk ID must be non-empty and contain no whitespace")
        else:
            risk_by_id[risk_id] = risk
        for field in ("title", "consequence", "safer_option", "recovery", "scope"):
            if not isinstance(risk.get(field), str) or not risk.get(field, "").strip():
                errors.append(f"{risk_id or 'risk'}: {field} is required")
        if risk.get("level") not in RISK_LEVELS:
            errors.append(f"{risk_id or 'risk'}: invalid level")
        if risk.get("action_kind") not in RISK_ACTION_KINDS:
            errors.append(f"{risk_id or 'risk'}: invalid action_kind")
        requires_authorization = risk.get("action_kind") in AUTHORIZATION_ACTION_KINDS
        lease_contract = risk.get("lease_contract_sha256")
        if lease_contract is not None and not (
            isinstance(lease_contract, str)
            and len(lease_contract) == DIGEST_LENGTH
            and all(character in "0123456789abcdef" for character in lease_contract)
        ):
            errors.append(f"{risk_id or 'risk'}: invalid lease_contract_sha256")
        lease_target = (
            risk.get("lease_target_id"),
            risk.get("lease_revision"),
            risk.get("lease_environment"),
        )
        if any(value is not None for value in lease_target):
            if any(
                not isinstance(value, str) or not value.strip()
                for value in lease_target
            ):
                errors.append(
                    f"{risk_id or 'risk'}: lease target fields must be all present or all null"
                )
            elif not is_canonical_id(risk.get("lease_target_id")):
                errors.append(
                    f"{risk_id or 'risk'}: lease_target_id must be canonical"
                )
        if risk.get("amount_limit") is not None and (
            not isinstance(risk.get("amount_limit"), str)
            or not risk.get("amount_limit", "").strip()
        ):
            errors.append(f"{risk_id or 'risk'}: amount_limit must be text or null")
        if risk.get("action_kind") == "spend" and not str(
            risk.get("amount_limit") or ""
        ).strip():
            errors.append(f"{risk_id or 'risk'}: spending risk requires amount_limit")
        expires_at = risk.get("expires_at")
        if requires_authorization and parse_utc_timestamp(expires_at) is None:
            errors.append(
                f"{risk_id or 'risk'}: actionable risk requires a timezone-aware expires_at"
            )
        if not requires_authorization and expires_at is not None:
            errors.append(
                f"{risk_id or 'risk'}: informational risk cannot create an action expiry"
            )
        if not isinstance(risk.get("authorization_pending"), bool):
            errors.append(f"{risk_id or 'risk'}: authorization_pending must be boolean")
        decision = risk.get("decision")
        if decision not in RISK_DECISIONS:
            errors.append(f"{risk_id or 'risk'}: invalid decision")
        if risk.get("action_status") not in RISK_ACTION_STATUSES:
            errors.append(f"{risk_id or 'risk'}: invalid action_status")
        if decision == "open":
            if any(risk.get(field) is not None for field in ("decision_by", "decision_reference", "decided_at")):
                errors.append(f"{risk_id or 'risk'}: open risk cannot contain decision metadata")
            expected_action_status = (
                "pending_authorization"
                if risk.get("authorization_pending") is True
                else "not_applicable"
            )
            if risk.get("action_status") != expected_action_status:
                errors.append(f"{risk_id or 'risk'}: open risk has an inconsistent action_status")
        else:
            if risk.get("authorization_pending") is not False:
                errors.append(f"{risk_id or 'risk'}: decided risk cannot remain pending")
            for field in ("decision_by", "decision_reference", "decided_at"):
                if not isinstance(risk.get(field), str) or not risk.get(field, "").strip():
                    errors.append(f"{risk_id or 'risk'}: {field} required after risk decision")
        if decision == "declined" and risk.get("action_status") != "declined":
            errors.append(f"{risk_id or 'risk'}: declined risk must retain declined action status")
        if requires_authorization:
            if decision == "open" and (
                risk.get("authorization_pending") is not True
                or risk.get("action_status") != "pending_authorization"
            ):
                errors.append(
                    f"{risk_id or 'risk'}: actionable risk must remain pending until a decision"
                )
            if decision in {"accepted", "mitigated"} and risk.get(
                "action_status"
            ) not in {"authorized", "completed", "failed", "cancelled"}:
                errors.append(
                    f"{risk_id or 'risk'}: an accepted actionable risk requires an action lease or outcome"
                )
        elif risk.get("action_kind") == "informational":
            expected_informational_status = (
                "declined" if decision == "declined" else "not_applicable"
            )
            if (
                risk.get("authorization_pending") is not False
                or risk.get("action_status") != expected_informational_status
            ):
                errors.append(
                    f"{risk_id or 'risk'}: informational risk cannot create an action authorization"
                )
        if risk.get("action_status") in {"completed", "failed", "cancelled"}:
            for field in ("action_reference", "action_at"):
                if not isinstance(risk.get(field), str) or not risk.get(field, "").strip():
                    errors.append(f"{risk_id or 'risk'}: {field} required after action completion")
        elif risk.get("action_reference") is not None or risk.get("action_at") is not None:
            errors.append(f"{risk_id or 'risk'}: action outcome metadata is premature")

    pending_risk_id = run.get("pending_risk_id")
    pending_authorizations = [
        risk
        for risk in risks
        if risk.get("authorization_pending") is True and risk.get("decision") == "open"
    ]
    if len(pending_authorizations) > 1:
        errors.append("only one risk authorization may be pending at a time")
    if status == "active" and pending_authorizations:
        errors.append("active run cannot bypass a pending risk authorization")
    if status == "active":
        declined_scopes = {
            risk.get("scope")
            for risk in risks
            if risk.get("decision") == "declined"
        }
        if run.get("next_action") in declined_scopes:
            errors.append("active next_action cannot repeat an explicitly declined risk scope")
    if status == "waiting_authorization" and pending_risk_id:
        pending_risk = risk_by_id.get(pending_risk_id)
        if pending_risk is None:
            errors.append(f"unknown pending_risk_id: {pending_risk_id}")
        elif pending_risk.get("decision") != "open":
            errors.append("pending risk must still be open")
        elif pending_risk.get("authorization_pending") is not True:
            errors.append("pending risk must retain its authorization obligation")
        if pending_authorizations and pending_authorizations[0].get("id") != pending_risk_id:
            errors.append("run points to a different pending risk authorization")
    authorized_risk_id = run.get("authorized_risk_id")
    authorized_actions = [
        risk for risk in risks if risk.get("action_status") == "authorized"
    ]
    if len(authorized_actions) > 1:
        errors.append("only one authorized risk action may be active at a time")
    if authorized_actions and authorized_risk_id != authorized_actions[0].get("id"):
        errors.append("an authorized risk action must remain bound to the run until completion")
    if authorized_risk_id is not None:
        authorized_risk = risk_by_id.get(authorized_risk_id)
        if authorized_risk is None:
            errors.append(f"unknown authorized_risk_id: {authorized_risk_id}")
        elif authorized_risk.get("action_status") != "authorized":
            errors.append("authorized risk lease must point to an authorized action")
        elif status == "active" and run.get("next_action") != authorized_risk.get("scope"):
            errors.append("active next_action must match the unconsumed authorized risk scope")
        elif status == "active" and not risk_context_matches(state, authorized_risk):
            errors.append("active authorized risk lease no longer matches the current contract and target")

    derived_verdict = derive_product_verdict(work_items, decisions)
    if status != "finished" and verdict in PRODUCT_VERDICTS and verdict != derived_verdict:
        errors.append(
            f"active product_verdict must match current records: {derived_verdict}"
        )
    if (
        status == "finished"
        and verdict in VERDICT_RANK
        and VERDICT_RANK[verdict] > VERDICT_RANK[derived_verdict]
    ):
        errors.append(
            f"finished product_verdict overstates current records: {derived_verdict}"
        )

    if status == "finished" and verdict == "verified":
        if pending_authorizations or authorized_actions:
            errors.append(
                "verified verdict requires every risk authorization and action lease to have an observed outcome"
            )
        if not accepted_decision_chain(decisions):
            errors.append("verified verdict requires accepted intent, spec, and plan")
        current_plan = accepted_contract_sha256(decisions)
        required_work = [
            item
            for item in work_items
            if item.get("required") is True
            and item.get("contract_sha256") == current_plan
        ]
        if not required_work:
            errors.append("verified verdict requires at least one required work item")
        unfinished = [
            item.get("id") for item in required_work if item.get("status") != "verified"
        ]
        if unfinished:
            errors.append(
                "verified verdict requires every required work item to be verified: "
                + ", ".join(str(item) for item in unfinished)
            )
    return errors


def validate_state(state: dict[str, Any], project_path: Path | None = None) -> list[str]:
    """Return validation errors even when a JSON value has the wrong nested type."""
    try:
        return _validate_state(state, project_path)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        return [f"state structure is invalid: {exc}"]


def latest_valid_journal_state(project: Path) -> dict[str, Any] | None:
    journal = project_paths(project)["journal"]
    if not journal.is_file():
        return None
    latest = None
    with journal.open("rb") as handle:
        for raw_line in handle:
            try:
                record = json.loads(raw_line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            candidate = record.get("state") if isinstance(record, dict) else None
            if isinstance(candidate, dict):
                try:
                    candidate_errors = validate_state(candidate)
                except Exception:
                    continue
                if not candidate_errors:
                    latest = candidate
    return copy.deepcopy(latest)


def latest_legacy_v1_state(project: Path) -> dict[str, Any] | None:
    journal = project_paths(project)["journal"]
    latest = None
    if journal.is_file():
        with journal.open("rb") as handle:
            for raw_line in handle:
                try:
                    record = json.loads(raw_line.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
                candidate = record.get("state") if isinstance(record, dict) else None
                if isinstance(candidate, dict) and candidate.get(
                    "schema_version"
                ) == "1.0":
                    try:
                        migrated = migrate_legacy_v1_state(candidate)
                        candidate_errors = validate_state(migrated)
                    except (AttributeError, KeyError, TypeError, ValueError):
                        continue
                    if not candidate_errors:
                        latest = candidate
    if latest is not None:
        return copy.deepcopy(latest)
    try:
        candidate = load_state(project)
    except ValueError:
        return None
    if candidate.get("schema_version") == "1.0":
        try:
            migrated = migrate_legacy_v1_state(candidate)
            candidate_errors = validate_state(migrated)
        except (AttributeError, KeyError, TypeError, ValueError):
            return None
        if not candidate_errors:
            return copy.deepcopy(candidate)
    return None


def migrate_legacy_v1_state(state: dict[str, Any]) -> dict[str, Any]:
    migrated = copy.deepcopy(state)
    migrated["schema_version"] = SCHEMA_VERSION
    run = migrated["run"]
    run["authorized_risk_id"] = None
    migrated["target"] = empty_target()
    decisions = migrated["decisions"]
    chain_accepted = accepted_decision_chain(decisions)
    for item in migrated["work_items"]:
        if not isinstance(item, dict):
            continue
        item["contract_sha256"] = "0" * DIGEST_LENGTH
        item["phase"] = "build"
        if item.get("status") == "verified":
            item["status"] = "implemented_unverified"
        if not chain_accepted and item.get("status") in {
            "in_progress",
            "implemented_unverified",
        }:
            item["status"] = "pending"
        legacy_note = "Migrated from DZ 1.0 without a decision-contract binding; review or recreate under the current accepted contract."
        item["note"] = (
            f"{item.get('note')} | {legacy_note}" if item.get("note") else legacy_note
        )
    for item in migrated["evidence"]:
        if isinstance(item, dict):
            item["contract_sha256"] = "0" * DIGEST_LENGTH
            item["target_id"] = "legacy-unbound"
    legacy_risk_needs_review = False
    for risk in migrated["risks"]:
        if not isinstance(risk, dict):
            continue
        pending = risk.get("authorization_pending") is True and risk.get("decision") == "open"
        if pending or risk.get("decision") in {"accepted", "mitigated"}:
            legacy_risk_needs_review = True
        risk["action_kind"] = "informational"
        risk["lease_contract_sha256"] = None
        risk["lease_target_id"] = None
        risk["lease_revision"] = None
        risk["lease_environment"] = None
        risk["amount_limit"] = None
        risk["expires_at"] = None
        risk["authorization_pending"] = False
        risk["action_status"] = (
            "declined" if risk.get("decision") == "declined" else "not_applicable"
        )
        risk["action_reference"] = None
        risk["action_at"] = None

    if chain_accepted:
        run["stage"] = "plan_accepted"
    elif decisions.get("spec", {}).get("status") == "accepted":
        run["stage"] = "spec_accepted"
    elif decisions.get("intent", {}).get("status") == "accepted":
        run["stage"] = "intent_accepted"
    else:
        run["stage"] = "discovery"
    run["product_verdict"] = "not_assessed"
    if run.get("status") == "finished":
        if state.get("run", {}).get("product_verdict") == "cancelled":
            run["product_verdict"] = "cancelled"
        else:
            run.update(
                {
                    "status": "paused",
                    "next_action": None,
                    "waiting_for": None,
                    "pending_risk_id": None,
                    "blocker": None,
                    "blocker_kind": None,
                    "resume_when": "Review migrated work and bind it to the current decision contract and observed target",
                    "finish_reason": None,
                }
            )
    if legacy_risk_needs_review and run.get("status") in {
        "active",
        "waiting_authorization",
        "waiting_user",
    }:
        run.update(
            {
                "status": "waiting_user",
                "next_action": None,
                "waiting_for": "Review migrated risk history and create a fresh exact action authorization before any material action",
                "pending_risk_id": None,
                "authorized_risk_id": None,
                "blocker": None,
                "blocker_kind": None,
                "resume_when": None,
                "finish_reason": None,
            }
        )
    return migrated


def journal_consistency_errors(project: Path, state: dict[str, Any]) -> list[str]:
    latest = latest_valid_journal_state(project)
    if latest is None:
        return ["DZ journal is missing or has no valid snapshot; recover or reinitialize before continuing"]
    if latest != state:
        return ["DZ state differs from the latest journal snapshot; run recover before continuing"]
    return []


def append_only_evidence_errors(project: Path, state: dict[str, Any]) -> list[str]:
    latest = latest_valid_journal_state(project)
    if latest is None:
        return []
    previous = latest.get("evidence")
    current = state.get("evidence")
    if not isinstance(previous, list) or not isinstance(current, list):
        return ["DZ evidence history is invalid"]
    if len(current) < len(previous) or current[: len(previous)] != previous:
        return ["DZ evidence is append-only and cannot be deleted, changed, or reordered"]
    return []


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def project_guidance_block() -> str:
    if not PROJECT_GUIDANCE_TEMPLATE.is_file():
        raise ValueError(
            f"DZ project guidance template not found: {PROJECT_GUIDANCE_TEMPLATE}"
        )
    template = PROJECT_GUIDANCE_TEMPLATE.read_text(encoding="utf-8").strip()
    return f"{GUIDANCE_START}\n{template}\n{GUIDANCE_END}\n"


def install_project_guidance(project: Path) -> Path:
    target = project / "AGENTS.md"
    existing = target.read_text(encoding="utf-8") if target.is_file() else ""
    start_count = existing.count(GUIDANCE_START)
    end_count = existing.count(GUIDANCE_END)
    if start_count != end_count or start_count > 1:
        raise ValueError(
            "AGENTS.md has a damaged DZ continuity section; repair its markers first"
        )

    block = project_guidance_block()
    if start_count == 1:
        before, remainder = existing.split(GUIDANCE_START, 1)
        _, after = remainder.split(GUIDANCE_END, 1)
        content = before.rstrip()
        if content:
            content += "\n\n"
        content += block.rstrip()
        if after.strip():
            content += "\n\n" + after.strip()
        content += "\n"
    else:
        content = existing.rstrip()
        if content:
            content += "\n\n"
        content += block

    atomic_write(target, content)
    return target


def write_journal(path: Path, event: str, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"at": now(), "event": event, "state": state}
    encoded = (
        json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    with path.open("ab+") as handle:
        handle.seek(0, os.SEEK_END)
        if handle.tell() > 0:
            handle.seek(-1, os.SEEK_END)
            if handle.read(1) != b"\n":
                handle.seek(0, os.SEEK_END)
                handle.write(b"\n")
        handle.seek(0, os.SEEK_END)
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def label(value: str, language: str) -> str:
    labels = {
        "zh": {
            "active": "正在继续",
            "waiting_user": "等用户决定",
            "waiting_authorization": "等用户确认一个具体动作",
            "blocked": "缺少执行条件",
            "paused": "已暂停",
            "finished": "本轮已收尾",
            "not_assessed": "尚未判断",
            "implemented_unverified": "已经做出，但还没完整检查",
            "partially_verified": "一部分已经检查",
            "verified": "已经按约定检查",
            "cancelled": "已取消",
            "discovery": "先把想法说清楚",
            "intent_draft": "正在整理想解决的事",
            "intent_accepted": "想解决的事已确认",
            "spec_draft": "正在整理这次做什么",
            "spec_accepted": "这次做什么已确认",
            "plan_draft": "正在整理怎么做",
            "plan_accepted": "怎么做已确认",
            "design": "把做法说清楚",
            "build": "动手制作",
            "test": "实际检查",
            "deploy": "准备或执行上线",
            "maintain": "上线后观察和改进",
            "pending_authorization": "等这次动作的确认",
            "authorized": "这次动作已获确认",
            "completed": "动作已完成",
            "failed": "动作失败",
            "not_applicable": "不需要执行动作",
            "declined": "用户没有同意",
        },
        "en": {},
    }
    return labels.get(language, {}).get(value, value.replace("_", " "))


def markdown_cell(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r\n", "<br>").replace("\n", "<br>")


def render(project: Path, state: dict[str, Any]) -> None:
    paths = project_paths(project)
    language = state["project"]["language"]
    run = state["run"]
    work_items = state["work_items"]
    risks = state["risks"]
    evidence = state["evidence"]
    target = state.get("target") or {}
    target_summary = (
        f"{target.get('revision')} / {target.get('environment')} / {str(target.get('id'))[:12]}"
        if target.get("id")
        else None
    )
    contract_digest = accepted_contract_sha256(state.get("decisions", {}))

    if language == "zh":
        dashboard = [
            f"# {state['project']['name']}",
            "",
            "> 本页由 DZ 项目账本生成；真实记录保存在 `.dz/state.json`。",
            "",
            "## 现在做到哪",
            f"- 当前情况：{label(run['status'], language)}",
            f"- 产品情况：{label(run['product_verdict'], language)}",
            f"- 当前阶段：{label(run['stage'], language)}",
            f"- 当前约定指纹：{contract_digest[:12] if contract_digest else '无'}",
            f"- 当前检查对象：{target_summary or '无'}",
            f"- 下一步：{run.get('next_action') or '无'}",
            f"- 等待内容：{run.get('waiting_for') or '无'}",
            f"- 等待决定的风险：{run.get('pending_risk_id') or '无'}",
            f"- 正在使用的动作通行条：{run.get('authorized_risk_id') or '无'}",
            f"- 阻塞原因：{run.get('blocker') or '无'}",
            f"- 阻塞类型：{run.get('blocker_kind') or '无'}",
            f"- 恢复条件：{run.get('resume_when') or '无'}",
            f"- 最后更新：{run['updated_at']}",
            "",
            "## 工作概览",
            f"- 共 {len(work_items)} 项；已检查 {sum(i['status'] == 'verified' for i in work_items)} 项；待检查 {sum(i['status'] == 'implemented_unverified' for i in work_items)} 项。",
            "- 详细记录：[docs/sdlc/work-items.md](docs/sdlc/work-items.md)",
            "",
            "## 已知风险",
        ]
        if risks:
            dashboard.extend(
                f"- {item['id']}：{item['title']}（{item['level']}，{item['decision']}，{label(item['action_status'], language)}）"
                for item in risks
            )
        else:
            dashboard.append("- 暂无记录。")
        dashboard.extend(["", "## 最近证据"])
        if evidence:
            dashboard.extend(
                f"- {item['id']}：{item['claim']} — {item['result']}"
                for item in evidence[-5:]
            )
        else:
            dashboard.append("- 暂无记录。")
    else:
        dashboard = [
            f"# {state['project']['name']}",
            "",
            "> Generated from the DZ project ledger; `.dz/state.json` is the source of truth.",
            "",
            "## Current position",
            f"- Run: {label(run['status'], language)}",
            f"- Product: {label(run['product_verdict'], language)}",
            f"- Stage: {run['stage']}",
            f"- Decision contract: {contract_digest[:12] if contract_digest else 'none'}",
            f"- Verification target: {target_summary or 'none'}",
            f"- Next action: {run.get('next_action') or 'none'}",
            f"- Waiting for: {run.get('waiting_for') or 'none'}",
            f"- Pending risk: {run.get('pending_risk_id') or 'none'}",
            f"- Authorized action lease: {run.get('authorized_risk_id') or 'none'}",
            f"- Blocker: {run.get('blocker') or 'none'}",
            f"- Blocker kind: {run.get('blocker_kind') or 'none'}",
            f"- Resume when: {run.get('resume_when') or 'none'}",
            f"- Updated: {run['updated_at']}",
            "",
            "## Work overview",
            f"- {len(work_items)} total; {sum(i['status'] == 'verified' for i in work_items)} verified; {sum(i['status'] == 'implemented_unverified' for i in work_items)} implemented but unverified.",
            "- Details: [docs/sdlc/work-items.md](docs/sdlc/work-items.md)",
            "",
            "## Known risks",
        ]
        dashboard.extend(
            [
                f"- {item['id']}: {item['title']} ({item['level']}, {item['decision']}, {item['action_status']})"
                for item in risks
            ]
            or ["- None recorded."]
        )
        dashboard.extend(["", "## Recent evidence"])
        dashboard.extend(
            [f"- {item['id']}: {item['claim']} — {item['result']}" for item in evidence[-5:]]
            or ["- None recorded."]
        )

    work_doc = [
        "# 工作账本" if language == "zh" else "# Work ledger",
        "",
        "> 由 `.dz/state.json` 生成，请不要在这里维护第二套状态。"
        if language == "zh"
        else "> Generated from `.dz/state.json`; do not maintain a second source of truth here.",
        "",
        "| ID | 必须完成 | 所属阶段 | 当前情况 | 要做的事 | 检查标准 | 证据 | 备注 |"
        if language == "zh"
        else "| ID | Required | Phase | Status | Work | Acceptance | Evidence | Note |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for item in work_items:
        acceptance = "<br>".join(markdown_cell(value) for value in item.get("acceptance", [])) or "—"
        evidence_text = ", ".join(markdown_cell(value) for value in item.get("evidence_ids", [])) or "—"
        note = markdown_cell(item.get("note") or item.get("blocker") or "—")
        work_doc.append(
            f"| {markdown_cell(item['id'])} | {'yes' if item.get('required', True) else 'no'} | {label(item['phase'], language)} | {item['status']} | {markdown_cell(item['title'])} | {acceptance} | {evidence_text} | {note} |"
        )
    if not work_items:
        work_doc.append("| — | — | — | — | — | — | — | — |")

    atomic_write(paths["dashboard"], "\n".join(dashboard) + "\n")
    atomic_write(paths["work_items"], "\n".join(work_doc) + "\n")


def persist(project: Path, state: dict[str, Any], event: str) -> None:
    if state["run"].get("status") != "finished":
        state["run"]["product_verdict"] = derive_product_verdict(
            state.get("work_items", []), state.get("decisions", {})
        )
    state["run"]["updated_at"] = now()
    errors = validate_state(state, project)
    errors.extend(append_only_evidence_errors(project, state))
    if errors:
        raise ValueError("; ".join(errors))
    paths = project_paths(project)
    write_journal(paths["journal"], event, state)
    atomic_write(paths["state"], json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    render(project, state)


def mutate(project: Path, event: str, change: Callable[[dict[str, Any]], None]) -> None:
    state = copy.deepcopy(load_state(project))
    consistency_errors = journal_consistency_errors(project, state)
    if consistency_errors:
        raise ValueError("; ".join(consistency_errors))
    if state.get("run", {}).get("status") == "finished" and not event.startswith(
        ("set_run:", "complete_risk_action:")
    ):
        raise ValueError(
            "This DZ run is finished; explicitly resume it before changing project state"
        )
    change(state)
    persist(project, state, event)


def find_by_id(items: list[dict[str, Any]], item_id: str, label_name: str) -> dict[str, Any]:
    if not is_canonical_id(item_id):
        raise ValueError(f"Invalid {label_name} ID: IDs cannot contain whitespace")
    for item in items:
        if item.get("id") == item_id:
            return item
    raise ValueError(f"Unknown {label_name}: {item_id}")


def init_command(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    paths = project_paths(project)
    if paths["state"].exists() or paths["journal"].exists():
        raise ValueError(
            "DZ state or recovery journal already exists; inspect or recover it instead of reinitializing"
        )
    project.mkdir(parents=True, exist_ok=True)
    persist(project, initial_state(args.name or project.name, args.language), "init")
    install_project_guidance(project)
    print(paths["state"])


def install_guidance_command(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    project.mkdir(parents=True, exist_ok=True)
    print(install_project_guidance(project))


def check_command(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    state = load_state(project)
    errors = validate_state(state, project)
    errors.extend(active_authorized_lease_errors(state))
    errors.extend(journal_consistency_errors(project, state))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("DZ state is valid")


def show_command(args: argparse.Namespace) -> None:
    state = load_state(args.project.resolve())
    print(json.dumps(state, ensure_ascii=False, indent=2))


def recover_command(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    journal = project_paths(project)["journal"]
    if not journal.is_file():
        raise ValueError(f"DZ journal not found: {journal}")
    recovered = latest_valid_journal_state(project)
    if recovered is None:
        raise ValueError("No valid snapshot found in journal")
    reconcile_stale_artifacts(project, recovered)
    persist(project, recovered, "recover")
    print("Recovered DZ state from the journal")


def migrate_command(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    legacy = latest_legacy_v1_state(project)
    if legacy is None:
        current = load_state(project)
        if current.get("schema_version") == SCHEMA_VERSION:
            raise ValueError("DZ state is already on the current schema")
        raise ValueError("No recoverable DZ 1.0 snapshot was found")
    paths = project_paths(project)
    stamp = now().replace(":", "-")
    migration_dir = project / ".dz" / "migrations" / stamp
    state_backup = migration_dir / "state.v1.0.json"
    journal_backup = migration_dir / "journal.v1.0.jsonl"
    if paths["state"].is_file():
        atomic_write(state_backup, paths["state"].read_text(encoding="utf-8"))
    if paths["journal"].is_file():
        atomic_write(journal_backup, paths["journal"].read_text(encoding="utf-8"))
    migrated = migrate_legacy_v1_state(legacy)
    persist(project, migrated, "migrate:1.0:1.1")
    print(f"Migrated DZ state to {SCHEMA_VERSION}; backup: {migration_dir}")


def set_run_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        run = state["run"]
        lease = authorized_action(state)
        pending = [
            risk
            for risk in state["risks"]
            if risk.get("authorization_pending") is True
            and risk.get("decision") == "open"
        ]
        if args.status == "active" and pending:
            raise ValueError(
                "Resolve the pending risk authorization before returning to active work"
            )
        if args.status == "active" and lease is not None:
            if args.next_action != lease.get("scope"):
                raise ValueError(
                    "The next action must exactly match the unconsumed authorized risk scope"
                )
            if not risk_context_matches(state, lease):
                raise ValueError(
                    "The authorized action no longer matches the current decision contract and target"
                )
            if action_lease_is_expired(lease):
                raise ValueError(
                    "The authorized action lease expired; record its outcome and request fresh authorization"
                )
        if args.status == "waiting_authorization":
            if not args.pending_risk:
                raise ValueError("waiting_authorization requires --pending-risk")
            risk = find_by_id(state["risks"], args.pending_risk, "risk")
            if risk.get("decision") != "open":
                raise ValueError("Only an open risk can wait for authorization")
            if risk.get("action_kind") not in AUTHORIZATION_ACTION_KINDS:
                raise ValueError(
                    "An informational risk does not authorize an action; record a new exact actionable risk"
                )
            if pending and pending[0].get("id") != args.pending_risk:
                raise ValueError("Resolve the current pending risk before requesting another")
            risk["authorization_pending"] = True
        requested_stage = args.stage or run["stage"]
        if requested_stage != run["stage"]:
            if requested_stage in DECISION_STAGES:
                raise ValueError(
                    "Decision stages change only through set-decision so their confirmation cannot be skipped"
                )
            if not accepted_decision_chain(state["decisions"]):
                raise ValueError(
                    "Accept intent, specification, and plan before entering delivery work"
                )
            allowed = DELIVERY_STAGE_TRANSITIONS.get(run["stage"], set())
            if requested_stage not in allowed:
                raise ValueError(
                    f"Invalid stage transition: {run['stage']} -> {requested_stage}"
                )
            gate_errors = stage_transition_errors(state, run["stage"], requested_stage)
            if gate_errors:
                raise ValueError("; ".join(gate_errors))
        run.update(
            {
                "status": args.status,
                "stage": requested_stage,
                "next_action": args.next_action,
                "waiting_for": args.waiting_for,
                "pending_risk_id": args.pending_risk,
                "blocker": args.blocker,
                "blocker_kind": args.blocker_kind,
                "resume_when": args.resume_when,
                "finish_reason": None,
            }
        )

    mutate(args.project.resolve(), f"set_run:{args.status}", change)


def close_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        reconcile_stale_artifacts(args.project.resolve(), state)
        run = state["run"]
        run.update(
            {
                "status": "finished",
                "product_verdict": args.verdict,
                "next_action": args.next_action,
                "waiting_for": None,
                "pending_risk_id": None,
                "blocker": None,
                "blocker_kind": None,
                "resume_when": args.resume_when,
                "finish_reason": args.reason,
            }
        )

    mutate(args.project.resolve(), f"close:{args.verdict}", change)


def set_decision_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        if authorized_action(state) is not None:
            raise ValueError(
                "Complete or cancel the authorized action before changing a product decision"
            )
        decision = state["decisions"][args.name]
        current = decision["status"]
        if current == "accepted" and args.status == "accepted":
            raise ValueError("An accepted decision is immutable; supersede it before a new draft")
        if args.path and args.status != "draft":
            raise ValueError("A decision path may be supplied only while preparing a draft")
        if args.status == "accepted" and (not args.by or not args.reference):
            raise ValueError("Acceptance requires --by and --reference")
        if args.status != "accepted" and (args.by or args.reference):
            raise ValueError("Acceptance metadata is valid only with --status accepted")
        if args.status != current and args.status not in DECISION_TRANSITIONS[current]:
            raise ValueError(f"Invalid decision transition: {current} -> {args.status}")
        if args.name == "spec" and args.status in {"draft", "accepted"}:
            if state["decisions"]["intent"]["status"] != "accepted":
                raise ValueError("Specification requires accepted intent")
        if args.name == "plan" and args.status in {"draft", "accepted"}:
            if state["decisions"]["intent"]["status"] != "accepted":
                raise ValueError("Plan requires accepted intent")
            if state["decisions"]["spec"]["status"] != "accepted":
                raise ValueError("Plan requires accepted specification")
        if args.status == "draft":
            selected_path = args.path or decision["path"]
            normalized, artifact = project_file(
                args.project.resolve(), selected_path, f"{args.name} decision artifact"
            )
            decision.update(
                {
                    "status": "draft",
                    "path": normalized,
                    "artifact_sha256": sha256_file(artifact),
                    "accepted_by": None,
                    "acceptance_reference": None,
                    "accepted_at": None,
                }
            )
        elif args.status == "accepted":
            if not stored_file_matches(
                args.project.resolve(),
                decision.get("path"),
                decision.get("artifact_sha256"),
            ):
                raise ValueError("The decision artifact changed after its recorded draft")
            decision.update(
                {
                    "status": "accepted",
                    "accepted_by": args.by,
                    "acceptance_reference": args.reference,
                    "accepted_at": now(),
                }
            )
        else:
            decision["status"] = args.status
        if args.status == "superseded" and args.name == "intent":
            for downstream in ("spec", "plan"):
                if state["decisions"][downstream]["status"] != "not_created":
                    state["decisions"][downstream]["status"] = "superseded"
        if args.status == "superseded" and args.name == "spec":
            if state["decisions"]["plan"]["status"] != "not_created":
                state["decisions"]["plan"]["status"] = "superseded"
        if args.status == "superseded":
            invalidate_verification_target(state)
        stage_map = {
            ("intent", "draft"): "intent_draft",
            ("intent", "accepted"): "intent_accepted",
            ("intent", "superseded"): "discovery",
            ("spec", "draft"): "spec_draft",
            ("spec", "accepted"): "spec_accepted",
            ("spec", "superseded"): "intent_accepted",
            ("plan", "draft"): "plan_draft",
            ("plan", "accepted"): "plan_accepted",
            ("plan", "superseded"): "spec_accepted",
        }
        state["run"]["stage"] = stage_map[(args.name, args.status)]

    mutate(args.project.resolve(), f"set_decision:{args.name}:{args.status}", change)


def set_target_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        if authorized_action(state) is not None:
            raise ValueError(
                "Complete or cancel the authorized action before changing the observed target"
            )
        if not accepted_decision_chain(state["decisions"]):
            raise ValueError(
                "Accept intent, specification, and plan before setting a verification target"
            )
        normalized_artifact, artifact = project_file(
            args.project.resolve(), args.artifact, "target proof"
        )
        artifact_digest = sha256_file(artifact)
        target_id = hashlib.sha256(
            (
                args.revision
                + "\0"
                + args.environment
                + "\0"
                + args.source
                + "\0"
                + artifact_digest
                + "\0"
                + now()
            ).encode("utf-8")
            + os.urandom(16)
        ).hexdigest()
        invalidate_verification_target(state)
        state["target"] = {
            "id": target_id,
            "contract_sha256": accepted_contract_sha256(state["decisions"]),
            "revision": args.revision,
            "environment": args.environment,
            "source": args.source,
            "artifact_path": normalized_artifact,
            "artifact_sha256": artifact_digest,
            "set_at": now(),
        }

    mutate(
        args.project.resolve(),
        f"set_target:{args.revision}:{args.environment}",
        change,
    )


def add_work_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        if not accepted_decision_chain(state["decisions"]):
            raise ValueError(
                "Accept intent, specification, and plan before creating delivery work"
            )
        if any(item.get("id") == args.id for item in state["work_items"]):
            raise ValueError(f"Work item already exists: {args.id}")
        state["work_items"].append(
            {
                "id": args.id,
                "title": args.title,
                "required": not args.optional,
                "contract_sha256": accepted_contract_sha256(state["decisions"]),
                "phase": args.phase,
                "status": "pending",
                "acceptance": args.acceptance or [],
                "evidence_ids": [],
                "note": None,
                "blocker": None,
                "updated_at": now(),
            }
        )

    mutate(args.project.resolve(), f"add_work:{args.id}", change)


def update_work_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        item = find_by_id(state["work_items"], args.id, "work item")
        if args.status:
            current = item["status"]
            if args.status != current and args.status not in WORK_TRANSITIONS[current]:
                raise ValueError(f"Invalid work transition: {current} -> {args.status}")
            if args.status in {
                "in_progress",
                "implemented_unverified",
                "verified",
            } and not accepted_decision_chain(state["decisions"]):
                raise ValueError(
                    "Accept intent, specification, and plan before starting implementation work"
                )
            if args.status in {
                "in_progress",
                "implemented_unverified",
                "verified",
            } and item.get("contract_sha256") != accepted_contract_sha256(
                state["decisions"]
            ):
                raise ValueError(
                    "This work belongs to an older decision contract; create a new current-contract work item with a new ID and link the old ID in its note"
                )
            if args.status == "in_progress" and args.status != current:
                if authorized_action(state) is not None:
                    raise ValueError(
                        "Complete or cancel the authorized action before reopening implementation work"
                    )
                invalidate_verification_target(state)
            item["status"] = args.status
            if args.status != "blocked" and args.blocker is None:
                item["blocker"] = None
        if args.note is not None:
            item["note"] = args.note
        if args.blocker is not None:
            item["blocker"] = args.blocker
        item["updated_at"] = now()

    mutate(args.project.resolve(), f"update_work:{args.id}", change)


def add_evidence_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        if any(item.get("id") == args.id for item in state["evidence"]):
            raise ValueError(f"Evidence already exists: {args.id}")
        work_item = find_by_id(state["work_items"], args.work_item, "work item")
        current_plan = accepted_contract_sha256(state["decisions"])
        if (
            not accepted_decision_chain(state["decisions"])
            or work_item.get("contract_sha256") != current_plan
        ):
            raise ValueError(
                "Evidence can be added only to work under the accepted current plan"
            )
        selected_target = current_target(state)
        if selected_target is None:
            raise ValueError(
                "Set the observed verification target before recording evidence"
            )
        if selected_target[1:] != (args.revision, args.environment):
            raise ValueError(
                "Evidence revision and environment must match the current observed target"
            )
        if args.acceptance not in work_item["acceptance"]:
            raise ValueError("Evidence must name an exact acceptance criterion")
        normalized_artifact, artifact = project_file(
            args.project.resolve(), args.artifact, "evidence artifact"
        )
        artifact_digest = sha256_file(artifact)
        resolves = list(dict.fromkeys(args.resolves or []))
        for resolved_id in resolves:
            resolved = find_by_id(state["evidence"], resolved_id, "evidence")
            if resolved.get("work_item_id") != args.work_item:
                raise ValueError("Cannot resolve evidence for another work item")
            if resolved.get("acceptance") != args.acceptance:
                raise ValueError("Cannot resolve a different acceptance criterion")
            if (
                resolved.get("target_id"),
                resolved.get("revision"),
                resolved.get("environment"),
            ) != (selected_target[0], args.revision, args.environment):
                raise ValueError(
                    "Evidence may resolve a gap only in the same target epoch; rerun every criterion for a new target"
                )
            if resolved.get("result") == "passed":
                raise ValueError("Passed evidence does not need resolution")
        if resolves and args.result != "passed":
            raise ValueError("Only passed evidence may resolve a gap")
        state["evidence"].append(
            {
                "id": args.id,
                "work_item_id": args.work_item,
                "contract_sha256": work_item["contract_sha256"],
                "target_id": selected_target[0],
                "acceptance": args.acceptance,
                "kind": args.kind,
                "claim": args.claim,
                "source": args.source,
                "artifact_path": normalized_artifact,
                "artifact_sha256": artifact_digest,
                "revision": args.revision,
                "environment": args.environment,
                "result": args.result,
                "resolves": resolves,
                "recorded_at": now(),
            }
        )
        work_item["evidence_ids"].append(args.id)
        if work_item["status"] == "verified":
            evidence_by_id = {item["id"]: item for item in state["evidence"]}
            complete_targets, unresolved = work_verification_support(
                work_item,
                evidence_by_id,
                work_item["evidence_ids"],
                args.project.resolve(),
                current_target(state),
            )
            if not complete_targets or unresolved:
                work_item["status"] = "implemented_unverified"
        work_item["updated_at"] = now()

    mutate(args.project.resolve(), f"add_evidence:{args.id}", change)


def add_risk_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        if any(item.get("id") == args.id for item in state["risks"]):
            raise ValueError(f"Risk already exists: {args.id}")
        requires_authorization = args.action_kind in AUTHORIZATION_ACTION_KINDS
        expiry = parse_utc_timestamp(args.expires_at)
        if requires_authorization:
            if expiry is None:
                raise ValueError(
                    "An actionable risk requires --expires-at with a timezone"
                )
            if expiry <= datetime.now(timezone.utc):
                raise ValueError("Risk authorization must expire in the future")
        elif args.expires_at is not None:
            raise ValueError("An informational risk does not create an action expiry")
        if args.action_kind == "spend" and not str(args.amount_limit or "").strip():
            raise ValueError("A spending action requires --amount-limit")
        if requires_authorization and state["run"].get("authorized_risk_id") is not None:
            raise ValueError(
                "Complete or cancel the current authorized action before requesting another"
            )
        if requires_authorization and any(
            risk.get("authorization_pending") is True
            and risk.get("decision") == "open"
            for risk in state["risks"]
        ):
            raise ValueError(
                "Resolve the current risk authorization before requesting another"
            )
        target = current_target(state)
        state["risks"].append(
            {
                "id": args.id,
                "title": args.title,
                "level": args.level,
                "action_kind": args.action_kind,
                "consequence": args.consequence,
                "safer_option": args.safer_option,
                "recovery": args.recovery,
                "scope": args.scope,
                "lease_contract_sha256": accepted_contract_sha256(
                    state["decisions"]
                ),
                "lease_target_id": target[0] if target else None,
                "lease_revision": target[1] if target else None,
                "lease_environment": target[2] if target else None,
                "amount_limit": args.amount_limit,
                "expires_at": args.expires_at,
                "authorization_pending": requires_authorization,
                "decision": "open",
                "action_status": (
                    "pending_authorization"
                    if requires_authorization
                    else "not_applicable"
                ),
                "action_reference": None,
                "action_at": None,
                "decision_by": None,
                "decision_reference": None,
                "decided_at": None,
            }
        )
        if requires_authorization:
            state["run"].update(
                {
                    "status": "waiting_authorization",
                    "next_action": None,
                    "waiting_for": (
                        "Decide whether to continue this exact risk scope: "
                        + args.scope
                    ),
                    "pending_risk_id": args.id,
                    "blocker": None,
                    "blocker_kind": None,
                    "resume_when": None,
                    "finish_reason": None,
                }
            )

    mutate(args.project.resolve(), f"add_risk:{args.id}", change)


def decide_risk_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        risk = find_by_id(state["risks"], args.id, "risk")
        if risk["decision"] != "open":
            raise ValueError("Risk already has a decision; create a new risk record to reopen it")
        run = state["run"]
        if run["status"] != "waiting_authorization" or run.get(
            "pending_risk_id"
        ) != args.id:
            raise ValueError("Risk decision requires a matching waiting_authorization state")
        if args.decision in {"accepted", "mitigated"}:
            if args.next_action != risk["scope"]:
                raise ValueError(
                    "The next action must exactly match the risk scope the user reviewed"
                )
            if not risk_context_matches(state, risk):
                raise ValueError(
                    "The decision contract or observed target changed; decline this stale request and create a new exact risk authorization"
                )
            if action_lease_is_expired(risk):
                raise ValueError(
                    "This risk authorization request expired; decline it and create a current request"
                )
            if (
                risk.get("action_kind") in TARGET_BOUND_ACTION_KINDS
                and risk.get("lease_target_id") is None
            ):
                raise ValueError(
                    "Release and production actions require an explicit observed target before authorization"
                )
        elif args.next_action is not None:
            raise ValueError("A declined action cannot be copied into the next action")
        risk.update(
            {
                "authorization_pending": False,
                "decision": args.decision,
                "decision_by": args.by,
                "decision_reference": args.reference,
                "decided_at": now(),
                "action_status": (
                    "declined" if args.decision == "declined" else "authorized"
                ),
            }
        )
        if args.decision == "declined":
            run.update(
                {
                    "status": "waiting_user",
                    "next_action": None,
                    "waiting_for": (
                        "Choose a different action; the declined scope remains recorded: "
                        + risk["scope"]
                    ),
                    "pending_risk_id": None,
                    "authorized_risk_id": None,
                    "blocker": None,
                    "blocker_kind": None,
                    "resume_when": None,
                    "finish_reason": None,
                }
            )
        else:
            run.update(
                {
                    "status": "active",
                    "next_action": risk["scope"],
                    "waiting_for": None,
                    "pending_risk_id": None,
                    "authorized_risk_id": args.id,
                    "blocker": None,
                    "blocker_kind": None,
                    "resume_when": None,
                    "finish_reason": None,
                }
            )

    mutate(args.project.resolve(), f"decide_risk:{args.id}:{args.decision}", change)


def complete_risk_action_command(args: argparse.Namespace) -> None:
    def change(state: dict[str, Any]) -> None:
        risk = find_by_id(state["risks"], args.id, "risk")
        run = state["run"]
        if run.get("authorized_risk_id") != args.id:
            raise ValueError("No matching authorized action lease is active")
        if risk.get("action_status") != "authorized":
            raise ValueError("The risk action is not awaiting an outcome")
        if action_lease_is_expired(risk) and args.outcome != "cancelled":
            raise ValueError(
                "The authorized action lease expired; only cancellation may close it before fresh authorization"
            )
        risk.update(
            {
                "action_status": args.outcome,
                "action_reference": args.reference,
                "action_at": now(),
            }
        )
        original_status = run["status"]
        if original_status == "active":
            if not str(args.next_action or "").strip():
                raise ValueError(
                    "An active run needs --next-action after recording the action outcome"
                )
            run.update(
                {
                    "next_action": args.next_action,
                    "waiting_for": None,
                    "pending_risk_id": None,
                    "authorized_risk_id": None,
                    "blocker": None,
                    "blocker_kind": None,
                    "resume_when": None,
                    "finish_reason": None,
                }
            )
        else:
            run["authorized_risk_id"] = None

    mutate(
        args.project.resolve(),
        f"complete_risk_action:{args.id}:{args.outcome}",
        change,
    )


def can_stop_command(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    state = load_state(project)
    errors = validate_state(state, project)
    errors.extend(journal_consistency_errors(project, state))
    if errors:
        raise ValueError("; ".join(errors))
    lease_errors = active_authorized_lease_errors(state)
    if lease_errors:
        print("continue: " + "; ".join(lease_errors))
        raise SystemExit(2)
    status = state["run"]["status"]
    if status == "active":
        print("continue: active work must first continue, pause, wait, block, or close")
        raise SystemExit(2)
    print(f"stop allowed: {status}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain a durable DZ project ledger")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def project_arg(command: argparse.ArgumentParser) -> None:
        command.add_argument("project", type=Path)

    command = subparsers.add_parser("init")
    project_arg(command)
    command.add_argument("--name")
    command.add_argument("--language", choices=("zh", "en"), default="zh")
    command.set_defaults(handler=init_command)

    for name, handler in (
        ("check", check_command),
        ("show", show_command),
        ("recover", recover_command),
        ("migrate", migrate_command),
        ("can-stop", can_stop_command),
        ("install-guidance", install_guidance_command),
    ):
        command = subparsers.add_parser(name)
        project_arg(command)
        command.set_defaults(handler=handler)

    command = subparsers.add_parser("set-run")
    project_arg(command)
    command.add_argument("--status", required=True, choices=sorted(RUN_STATUSES - {"finished"}))
    command.add_argument("--stage", choices=sorted(STAGES))
    command.add_argument("--next-action")
    command.add_argument("--waiting-for")
    command.add_argument("--pending-risk")
    command.add_argument("--blocker")
    command.add_argument("--blocker-kind", choices=sorted(BLOCKER_KINDS))
    command.add_argument("--resume-when")
    command.set_defaults(handler=set_run_command)

    command = subparsers.add_parser("close")
    project_arg(command)
    command.add_argument("--verdict", required=True, choices=sorted(PRODUCT_VERDICTS - {"not_assessed"}))
    command.add_argument("--reason", required=True)
    command.add_argument("--next-action")
    command.add_argument("--resume-when")
    command.set_defaults(handler=close_command)

    command = subparsers.add_parser("set-decision")
    project_arg(command)
    command.add_argument("name", choices=("intent", "spec", "plan"))
    command.add_argument(
        "--status", required=True, choices=sorted(DECISION_STATUSES - {"not_created"})
    )
    command.add_argument("--path")
    command.add_argument("--by")
    command.add_argument("--reference")
    command.set_defaults(handler=set_decision_command)

    command = subparsers.add_parser("set-target")
    project_arg(command)
    command.add_argument("--revision", required=True)
    command.add_argument("--environment", required=True)
    command.add_argument("--source", required=True)
    command.add_argument("--artifact", required=True)
    command.set_defaults(handler=set_target_command)

    command = subparsers.add_parser("add-work")
    project_arg(command)
    command.add_argument("--id", required=True)
    command.add_argument("--title", required=True)
    command.add_argument("--optional", action="store_true")
    command.add_argument("--phase", required=True, choices=sorted(DELIVERY_STAGES))
    command.add_argument("--acceptance", action="append", required=True)
    command.set_defaults(handler=add_work_command)

    command = subparsers.add_parser("update-work")
    project_arg(command)
    command.add_argument("id")
    command.add_argument("--status", choices=sorted(WORK_STATUSES))
    command.add_argument("--note")
    command.add_argument("--blocker")
    command.set_defaults(handler=update_work_command)

    command = subparsers.add_parser("add-evidence")
    project_arg(command)
    command.add_argument("--id", required=True)
    command.add_argument("--work-item", required=True)
    command.add_argument("--acceptance", required=True)
    command.add_argument("--kind", required=True)
    command.add_argument("--claim", required=True)
    command.add_argument("--source", required=True)
    command.add_argument("--artifact", required=True)
    command.add_argument("--revision", required=True)
    command.add_argument("--environment", required=True)
    command.add_argument("--result", required=True, choices=sorted(EVIDENCE_RESULTS))
    command.add_argument("--resolves", action="append")
    command.set_defaults(handler=add_evidence_command)

    command = subparsers.add_parser("add-risk")
    project_arg(command)
    command.add_argument("--id", required=True)
    command.add_argument("--title", required=True)
    command.add_argument("--level", required=True, choices=sorted(RISK_LEVELS))
    command.add_argument(
        "--action-kind", required=True, choices=sorted(RISK_ACTION_KINDS)
    )
    command.add_argument("--consequence", required=True)
    command.add_argument("--safer-option", required=True)
    command.add_argument("--recovery", default="unknown")
    command.add_argument("--scope", required=True)
    command.add_argument("--amount-limit")
    command.add_argument("--expires-at")
    command.set_defaults(handler=add_risk_command)

    command = subparsers.add_parser("decide-risk")
    project_arg(command)
    command.add_argument("id")
    command.add_argument("--decision", required=True, choices=sorted(RISK_DECISIONS - {"open"}))
    command.add_argument("--by", required=True)
    command.add_argument("--reference", required=True)
    command.add_argument("--next-action")
    command.set_defaults(handler=decide_risk_command)

    command = subparsers.add_parser("complete-risk-action")
    project_arg(command)
    command.add_argument("id")
    command.add_argument(
        "--outcome", required=True, choices=("completed", "failed", "cancelled")
    )
    command.add_argument("--reference", required=True)
    command.add_argument("--next-action")
    command.set_defaults(handler=complete_risk_action_command)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.handler(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
