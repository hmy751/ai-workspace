"""실제 임시 파일에서 공통 root·symlink·읽기 계약을 검증한다."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from context.work.harness.workspace import (
    HarnessError,
    read_json_without_symlinks,
    read_text_without_symlinks,
    resolve_directory_without_symlinks,
    resolve_inside_root,
    resolve_regular_file_without_symlinks,
)


class WorkspaceSafeReadTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name)
        self.root = self.base / "root"
        self.root.mkdir()
        (self.root / "docs").mkdir()
        (self.root / "docs/value.json").write_text('{"값": 1}', encoding="utf-8")

    def test_regular_utf8_text_and_json_are_read_inside_the_declared_root(self) -> None:
        self.assertEqual(
            read_text_without_symlinks(self.root, "docs/value.json", "fixture"),
            '{"값": 1}',
        )
        self.assertEqual(
            read_json_without_symlinks(self.root, "docs/value.json", "fixture"),
            {"값": 1},
        )

    def test_file_and_directory_resolution_cannot_exchange_their_roles(self) -> None:
        with self.assertRaisesRegex(HarnessError, "regular file"):
            resolve_regular_file_without_symlinks(self.root, "docs", "fixture")
        with self.assertRaisesRegex(HarnessError, "directory"):
            resolve_directory_without_symlinks(self.root, "docs/value.json", "fixture")

    def test_symlink_components_are_rejected_even_when_the_target_is_inside_root(
        self,
    ) -> None:
        (self.root / "linked").symlink_to(self.root / "docs", target_is_directory=True)
        with self.assertRaisesRegex(HarnessError, "symlink"):
            read_text_without_symlinks(self.root, "linked/value.json", "fixture")

    def test_resolved_path_cannot_escape_root_through_a_symlink(self) -> None:
        outside = self.base / "outside.txt"
        outside.write_text("not selected", encoding="utf-8")
        (self.root / "outside.txt").symlink_to(outside)
        with self.assertRaisesRegex(HarnessError, "outside"):
            resolve_inside_root(self.root, "outside.txt", "fixture")

    def test_json_read_rejects_arrays_malformed_input_and_invalid_utf8(self) -> None:
        path = self.root / "docs/value.json"
        for content, error in (
            (b"[]", "JSON object"),
            (b"{broken", "valid JSON"),
            (b"\xff", "UTF-8"),
        ):
            with self.subTest(error=error):
                path.write_bytes(content)
                with self.assertRaisesRegex(HarnessError, error):
                    read_json_without_symlinks(self.root, "docs/value.json", "fixture")
