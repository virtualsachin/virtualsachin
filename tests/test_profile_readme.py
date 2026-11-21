"""Brand and security contract tests for the public GitHub profile repository."""

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"

FENCED_CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
MARKDOWN_LINK_TARGET_RE = re.compile(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HTTP_URL_RE = re.compile(r"http://", re.IGNORECASE)
PRIVATE_IP_RE = re.compile(
    r"(?<!\d)(?:"
    r"100\.100\.100\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|"
    r"100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}"
    r")(?!\d)"
)
TOKEN_PATTERNS = (
    ("ghp_", re.compile(r"ghp_")),
    ("github_pat_", re.compile(r"github_pat_")),
    ("sk-", re.compile(r"(?<![A-Za-z0-9])sk-")),
    ("PRIVATE KEY", re.compile(r"PRIVATE KEY")),
)
INTERNAL_HOSTNAME_RE = re.compile(r"\.virtualsach\.home\b", re.IGNORECASE)


class TestProfileReadme(unittest.TestCase):
    """Verify brand invariants, link integrity, secret hygiene, and governance files."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.readme_text = README_PATH.read_text(encoding="utf-8")

    def test_canonical_titles_and_positioning_present(self) -> None:
        required_phrases = (
            "Agentic Infrastructure Architect",
            "Director — Cloud & Infrastructure Architecture",
            "Principal Agentic AI Architect",
            "Complexity is the Enemy. Always.",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.readme_text)

    def test_canonical_links_and_badges_valid(self) -> None:
        body_without_code = FENCED_CODE_BLOCK_RE.sub("", self.readme_text)
        targets = MARKDOWN_LINK_TARGET_RE.findall(body_without_code)
        self.assertGreater(len(targets), 0, "Expected markdown links/badges in README.md")

        for target in targets:
            with self.subTest(target=target):
                is_valid = target.startswith("https://") or target == "mailto:sachin@virtualsach.in"
                self.assertTrue(
                    is_valid,
                    f"Disallowed link or badge URL in README.md: {target!r}",
                )

        self.assertIsNone(
            HTTP_URL_RE.search(body_without_code),
            "README.md must not contain insecure http:// URLs",
        )

        for required_url in (
            "https://virtualsach.in",
            "https://virtualsach.in/llms.txt",
            "https://virtualsach.in/blog/",
        ):
            with self.subTest(required_url=required_url):
                self.assertIn(required_url, self.readme_text)

    def test_no_secrets_or_private_ips_leaked(self) -> None:
        self.assertNotIn("100.100.100.", self.readme_text)
        self.assertNotIn("192.168.", self.readme_text)
        self.assertIsNone(
            PRIVATE_IP_RE.search(self.readme_text),
            "README.md must not contain RFC 1918 or CGNAT internal IPs",
        )

        for label, pattern in TOKEN_PATTERNS:
            with self.subTest(pattern=label):
                self.assertIsNone(
                    pattern.search(self.readme_text),
                    f"README.md must not contain secret/token pattern {label!r}",
                )

        self.assertIsNone(
            INTERNAL_HOSTNAME_RE.search(self.readme_text),
            "README.md must not contain internal *.virtualsach.home hostnames",
        )

    def test_repo_governance_files_exist(self) -> None:
        required_files = (
            "README.md",
            "AGENTS.md",
            "CONTRIBUTING.md",
            "LICENSE",
            ".github/PULL_REQUEST_TEMPLATE.md",
            "bin/verify",
        )
        for rel_path in required_files:
            file_path = REPO_ROOT / rel_path
            with self.subTest(path=rel_path):
                self.assertTrue(file_path.is_file(), f"Missing required file: {rel_path}")
                self.assertGreater(
                    file_path.stat().st_size,
                    0,
                    f"Required file is empty: {rel_path}",
                )


if __name__ == "__main__":
    unittest.main()
