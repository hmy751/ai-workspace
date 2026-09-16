"""출력 chunk 경계·문자 수 제한·읽기 오류의 직접 계약을 검증한다."""

from __future__ import annotations

import io
import unittest

from context.work.harness.verify.output import (
    BoundedStreamCapture,
    PROJECT_ROOT_TOKEN,
    capture_result,
)


class BoundedStreamCaptureTests(unittest.TestCase):
    def test_root_normalization_survives_every_chunk_boundary(self) -> None:
        text = "앞:/project/root/뒤:/project/root/끝"
        expected = f"앞:{PROJECT_ROOT_TOKEN}/뒤:{PROJECT_ROOT_TOKEN}/끝"
        for split in range(len(text) + 1):
            with self.subTest(split=split):
                capture = BoundedStreamCapture(1000, "/project/root")
                capture.add(text[:split])
                capture.add(text[split:])
                capture.finish()
                output, metadata, replacements = capture_result(capture)
                self.assertEqual(output, expected)
                self.assertEqual(replacements, 2)
                self.assertEqual(metadata["observed_chars"], len(text))
                self.assertFalse(metadata["truncated"])

    def test_capture_keeps_draining_after_the_unicode_prefix_limit(self) -> None:
        stream = io.StringIO("가나다라마바사" * 1000)
        capture = BoundedStreamCapture(3, "/root")
        capture.drain(stream)
        output, metadata, replacements = capture_result(capture)
        self.assertEqual(output, "가나다")
        self.assertEqual(metadata["observed_chars"], 7000)
        self.assertEqual(metadata["persisted_chars"], 3)
        self.assertTrue(metadata["truncated"])
        self.assertEqual(replacements, 0)
        self.assertTrue(stream.closed)

    def test_exact_limit_is_not_reported_as_truncation(self) -> None:
        capture = BoundedStreamCapture(3, "/root")
        capture.add("abc")
        capture.finish()
        output, metadata, _ = capture_result(capture)
        self.assertEqual(output, "abc")
        self.assertFalse(metadata["truncated"])

    def test_read_failure_is_recorded_and_normalized_without_leaking_root(self) -> None:
        class BrokenStream:
            closed = False

            def read(self, size: int) -> str:
                raise OSError("/private/project/read failed")

            def close(self) -> None:
                self.closed = True

        stream = BrokenStream()
        capture = BoundedStreamCapture(100, "/private/project")
        capture.drain(stream)
        output, metadata, _ = capture_result(capture)
        self.assertEqual(output, "")
        self.assertEqual(metadata["read_error"], f"{PROJECT_ROOT_TOKEN}/read failed")
        self.assertTrue(stream.closed)
