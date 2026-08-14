from dataclasses import FrozenInstanceError
import unittest

from src.config_loader import RequestPolicy, load_request_policy


class LoadRequestPolicyTests(unittest.TestCase):
    def test_missing_timeout_uses_5000_ms(self) -> None:
        policy = load_request_policy({})

        self.assertEqual(policy.request_timeout_ms, 5000)

    def test_explicit_timeout_is_preserved(self) -> None:
        policy = load_request_policy({"request_timeout_ms": 1250})

        self.assertEqual(policy.request_timeout_ms, 1250)

    def test_rejects_boolean_timeout(self) -> None:
        for value in (True, False):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    load_request_policy({"request_timeout_ms": value})

    def test_rejects_non_positive_timeout(self) -> None:
        for value in (0, -1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    load_request_policy({"request_timeout_ms": value})

    def test_rejects_non_integer_timeout(self) -> None:
        for value in (5000.0, "5000", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    load_request_policy({"request_timeout_ms": value})

    def test_returns_immutable_policy(self) -> None:
        policy = load_request_policy({})

        self.assertIsInstance(policy, RequestPolicy)
        with self.assertRaises(FrozenInstanceError):
            policy.request_timeout_ms = 1000

    def test_rejects_unknown_keys(self) -> None:
        with self.assertRaises(ValueError):
            load_request_policy({"timeout_ms": 5000})


if __name__ == "__main__":
    unittest.main()
