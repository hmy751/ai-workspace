"""재배치와 무관하게 유지하는 Maintain 계약·설정 파일의 기준 경로."""

from pathlib import Path


MAINTAIN_ROOT = Path(__file__).resolve().parent
