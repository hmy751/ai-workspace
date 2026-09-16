"""Claude 연결의 공개 import·모듈 실행 진입점."""

from .adapters.claude import ClaudeHookAdapter, main

__all__ = ["ClaudeHookAdapter", "main"]
if __name__ == "__main__":
    raise SystemExit(main())
