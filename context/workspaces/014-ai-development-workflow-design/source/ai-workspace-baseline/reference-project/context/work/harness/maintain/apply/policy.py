"""허용 Owner 경로와 Markdown·로컬 링크 정책."""

from __future__ import annotations

from datetime import date
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote

from ...workspace_contract import HarnessError, fail

_RECORD_PATTERN = re.compile(
    r"^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-"
    r"(?P<day>[0-9]{2})-(?P<sequence>[0-9]{2})-"
    r"(?P<slug>[^/\\]+)\.md$"
)

_INLINE_LINK_PATTERN = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]*)\)")

_URI_SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _is_allowed_change_path(relative_path: str) -> tuple[bool, bool]:
    """허용 여부와 새 기록만 추가할 수 있는 경로인지 반환한다."""

    parts = PurePosixPath(relative_path).parts
    if (
        parts[:2] == ("current", "memory")
        and (len(parts) == 3 or (len(parts) == 4 and parts[2] in {"spec", "tickets"}))
        and parts[-1].endswith(".md")
        and parts[-1] not in {".md", "..md"}
    ):
        return True, False
    if parts in {
        ("current", "state", "index.md"),
        ("source", "index.md"),
        ("output", "index.md"),
        ("records", "README.md"),
    }:
        return True, False
    if len(parts) != 2 or parts[0] != "records":
        return False, False
    match = _RECORD_PATTERN.fullmatch(parts[1])
    if match is None or match.group("sequence") == "00":
        return False, False
    try:
        date(
            int(match.group("year")),
            int(match.group("month")),
            int(match.group("day")),
        )
    except ValueError:
        return False, False
    return True, True


def _validate_markdown_text(content: str, label: str) -> bytes:
    if "\x00" in content:
        fail(f"{label} must not contain NUL")
    if not content.endswith("\n"):
        fail(f"{label} must end with a newline")
    for line_number, line in enumerate(content.splitlines(), start=1):
        if line.endswith((" ", "\t")):
            fail(f"{label} has trailing whitespace on line {line_number}")
    return content.encode("utf-8")


def _local_link_destination(raw: str, label: str) -> str | None:
    destination = raw.strip()
    if not destination:
        fail(f"{label} has an empty Markdown link destination")
    if destination.startswith("<"):
        closing = destination.find(">")
        if closing < 0:
            fail(f"{label} has an invalid angle-bracket Markdown link")
        destination = destination[1:closing]
    else:
        destination = destination.split(maxsplit=1)[0]
    if destination.startswith("#"):
        return None
    if destination.startswith("//") or _URI_SCHEME_PATTERN.match(destination):
        return None
    return unquote(destination.split("#", 1)[0].split("?", 1)[0])


def _validate_local_markdown_links(
    project_root: Path,
    document_path: Path,
    content: str,
    planned_targets: set[Path],
    label: str,
) -> None:
    resolved_project_root = project_root.resolve(strict=True)
    for candidate in _local_markdown_targets(document_path, content, label):
        try:
            candidate.relative_to(resolved_project_root)
        except ValueError as exc:
            raise HarnessError(
                f"{label} local Markdown link resolves outside Project root: "
                f"{candidate}"
            ) from exc
        if candidate not in planned_targets and not candidate.exists():
            fail(f"{label} local Markdown link target does not exist: " f"{candidate}")


def _local_markdown_targets(
    document_path: Path,
    content: str,
    label: str,
) -> set[Path]:
    in_fence = False
    visible_lines: list[str] = []
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            visible_lines.append(line)
    visible_content = "\n".join(visible_lines)
    targets: set[Path] = set()
    for match in _INLINE_LINK_PATTERN.finditer(visible_content):
        destination = _local_link_destination(match.group(1), label)
        if destination is None:
            continue
        if not destination or Path(destination).is_absolute():
            fail(f"{label} local Markdown links must be relative paths")
        targets.add((document_path.parent / destination).resolve(strict=False))
    return targets
