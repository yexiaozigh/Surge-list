import tempfile
import unittest
from pathlib import Path

from scripts.lint_rules import lint_file


class RuleLintTests(unittest.TestCase):
    def lint(self, content: bytes):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "rules.list"
            path.write_bytes(content)
            return lint_file(path)

    def test_accepts_supported_rules_and_comments(self):
        self.assertEqual([], self.lint(b"# comment\nDOMAIN,example.com\nIP-CIDR,192.0.2.0/24\n"))

    def test_reports_duplicate_glued_type_and_bad_type(self):
        errors = self.lint(
            b"DOMAIN-SUFFIX,example.com\n"
            b"DOMAIN-SUFFIX,example.com\n"
            b"DOMAIN-SUFFIX,example.netDOMAIN,api.example.net\n"
            b"UNKNOWN,example.org\n"
        )
        self.assertTrue(any("完全重复" in error for error in errors))
        self.assertTrue(any("意外粘连" in error for error in errors))
        self.assertTrue(any("非法规则类型" in error for error in errors))

    def test_reports_missing_final_newline_and_invalid_cidr_family(self):
        errors = self.lint(b"IP-CIDR6,192.0.2.0/24")
        self.assertTrue(any("末尾缺少换行" in error for error in errors))
        self.assertTrue(any("IP-CIDR6地址无效" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
