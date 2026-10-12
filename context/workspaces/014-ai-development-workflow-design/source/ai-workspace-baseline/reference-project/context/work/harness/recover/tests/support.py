"""Recover receipt 시나리오의 독립된 snapshot 기대값을 준비한다."""

from __future__ import annotations

import hashlib
import json

from context.work.harness.testing import WorkspaceFixture


class ReceiptFixture(WorkspaceFixture):
    def project_snapshot(self, relative_path: str) -> dict[str, object]:
        content = (self.project_root / relative_path).read_bytes()
        return {
            "path": relative_path,
            "sha256": hashlib.sha256(content).hexdigest(),
            "size": len(content),
        }

    def snapshot_sha256(
        self,
        canonical_basis_files: list[dict[str, object]],
        evidence_files: list[dict[str, object]],
    ) -> str:
        serialized = json.dumps(
            {
                "canonical_basis_files": canonical_basis_files,
                "evidence_files": evidence_files,
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()
