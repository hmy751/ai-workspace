"""기존 두 사례의 자료·의뢰를 보존하고 실행 스킬 판본만 교체한다."""

import hashlib
import json
import math
import shutil
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    root = Path(__file__).resolve().parent
    prior = root.parent / "explain-four-problems-60medium-2026-10-26"
    prototype = root.parents[1] / "prototypes/development-workflow"
    runs = []
    for name in ["case02-access", "case04-investigation"]:
        old = prior / name
        case = root / name
        # 최초 응답이나 이미 준비된 입력을 덮어쓰지 않는다.
        case.mkdir()
        shutil.copytree(old / "input", case / "input")
        for filename in ["prompt.txt", "required.json", "read_material.py"]:
            shutil.copy2(old / filename, case / filename)
        before = json.loads((old / "inventory.json").read_text())
        inventory = {}
        changed = []
        for rel, meta in before.items():
            path = case / "input" / rel
            if rel.startswith("skills/"):
                shutil.copy2(prototype / rel, path)
            data = path.read_bytes()
            text = data.decode()
            inventory[rel] = {
                "sha256": digest(path),
                "bytes": len(data),
                "chars": len(text),
                "chunks": math.ceil(len(text) / 3000),
            }
            if meta["sha256"] != inventory[rel]["sha256"]:
                assert rel.startswith("skills/"), rel
                changed.append(rel)
        images = []
        for image in json.loads((old / "images.json").read_text()):
            rel = Path(image["path"]).relative_to(old)
            path = case / rel
            assert digest(path) == image["sha256"]
            images.append({"path": str(path), "sha256": digest(path)})
        required = json.loads((case / "required.json").read_text())
        # 인덱스에 없는 원문·이미지도 준비 중 변형이 없었는지 대조한다.
        for old_path in (old / "input/materials").rglob("*"):
            if old_path.is_file():
                assert digest(old_path) == digest(case / old_path.relative_to(old))
        assert not list((case / "input/skills").rglob("_background"))
        (case / "output").mkdir()
        write_json(case / "inventory.json", inventory)
        write_json(case / "images.json", images)
        run = {
            "case": name,
            "prior_case": str(old),
            "model": "gpt-6-sol",
            "reasoning_effort": "medium",
            "required": required,
            "required_chunks": sum(inventory[r]["chunks"] for r in required),
            "changed_skill_files": changed,
            "unchanged_materials": True,
            "unchanged_prompt": digest(old / "prompt.txt") == digest(case / "prompt.txt"),
            "prompt_sha256": digest(case / "prompt.txt"),
            "helper_sha256": digest(case / "read_material.py"),
            "text_files": len(inventory),
            "images": len(images),
            "prior_response_sha256": digest(old / "output/response.md"),
        }
        write_json(case / "preparation.json", run)
        runs.append(run)
    write_json(root / "execution-plan.json", {
        "authorization": "좋아 그럼 종합한 방향으로 본체랑 상세, _background까지 반영해봐. 기존 의미 잘 유지됐는지 확인하고 2번이랑 4번 다시 6.0 sol 미디엄으로 테스트해보자",
        "fresh_context": True,
        "first_response_only": True,
        "runs": runs,
        "scope": "이전과 같은 자료·prompt·도구조건, 수정한 실행 스킬만 교체. 형성 자료·평가·기대 답 제외.",
        "isolation": "폴더/지침/로그로 범위 구분. OS 수준 접근 격리는 아님.",
    })
    print(json.dumps(runs, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
