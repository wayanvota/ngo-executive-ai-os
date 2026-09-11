from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
REQUIRED_TOP_LEVEL = {
    "AGENTS.md",
    "CONTRIBUTING.md",
    "DISCLAIMER.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "docs",
    "examples",
    "memory",
    "routines",
    "templates",
}
ROUTINES = sorted((ROOT / "routines").glob("*.md"))
TEMPLATES = sorted((ROOT / "templates").glob("*.md"))


def markdown_links(text: str) -> list[str]:
    return re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", text)


class ExecutiveOsE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="ngo-executive-os-e2e-")
        cls.install = Path(cls.temp.name) / "workspace"
        cls.install.mkdir()
        output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        cls.tracked = [Path(value.decode()) for value in output.split(b"\0") if value]
        for relative in cls.tracked:
            source = ROOT / relative
            destination = cls.install / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def installed_text(self, relative: str) -> str:
        return (self.install / relative).read_text(encoding="utf-8")

    def test_u01_fresh_copy_has_required_structure(self) -> None:
        self.assertTrue(REQUIRED_TOP_LEVEL.issubset({path.name for path in self.install.iterdir()}))

    def test_u02_readme_names_the_existing_license(self) -> None:
        readme = self.installed_text("README.md")
        self.assertIn("`LICENSE`", readme)
        self.assertNotIn("`LICENSE.md`", readme)

    def test_u03_agents_defines_role_and_source_discipline(self) -> None:
        agents = self.installed_text("AGENTS.md")
        self.assertIn("## Role", agents)
        self.assertIn("## Source Discipline", agents)
        self.assertIn("[SOURCE NEEDED]", agents)
        self.assertIn("Do not invent", agents)

    def test_u04_agents_preserves_human_approval(self) -> None:
        agents = self.installed_text("AGENTS.md")
        self.assertIn("Ask for explicit approval before", agents)
        for action in ("sending messages", "publishing anything", "changing calendar events", "using connected private accounts"):
            self.assertIn(action, agents)

    def test_u05_memory_contract_has_every_core_file_and_folder(self) -> None:
        memory = self.install / "memory"
        for name in ("executive-profile.md", "judgment-rules.md", "fundraising-pipeline.md", "commitments.md"):
            self.assertTrue((memory / name).is_file(), name)
        for name in ("donors", "board", "partners", "projects", "private"):
            self.assertTrue((memory / name).is_dir(), name)

    def test_u06_templates_cover_each_profile_and_review_type(self) -> None:
        expected = {"board-brief.md", "board-profile.md", "donor-profile.md", "meeting-note.md", "project-record.md", "weekly-review.md"}
        self.assertEqual({path.name for path in (self.install / "templates").glob("*.md")}, expected)

    def test_u07_morning_brief_inputs_resolve_in_fresh_copy(self) -> None:
        routine = self.installed_text("routines/morning-brief.md")
        references = re.findall(r"`(memory/[^`]+)`", routine)
        self.assertGreaterEqual(len(references), 6)
        for reference in references:
            self.assertTrue((self.install / reference).exists(), reference)
        self.assertIn("Recommend the next action clearly", routine)

    def test_u08_donor_review_preserves_operating_columns(self) -> None:
        routine = self.installed_text("routines/donor-crm-review.md")
        self.assertIn("| Donor | Status | Next Action | Owner | Timing | Risk | Evidence Needed |", routine)
        self.assertIn("Do not infer donor intent", routine)

    def test_u09_meeting_workflows_keep_drafts_approval_gated(self) -> None:
        prep = self.installed_text("routines/meeting-prep.md")
        followup = self.installed_text("routines/meeting-follow-up.md")
        self.assertIn("never sent automatically", prep)
        self.assertIn("Drafts must remain approval-gated", followup)
        self.assertIn("Do not edit memory unless asked", followup)

    def test_u10_decision_routines_require_evidence_and_tradeoffs(self) -> None:
        proposal = self.installed_text("routines/proposal-cockpit.md")
        source = self.installed_text("routines/source-check.md")
        weekly = self.installed_text("routines/weekly-strategy-review.md")
        self.assertIn("Evidence Gaps", proposal)
        self.assertIn("Conflicting sources", source)
        self.assertIn("What To Stop Or Defer", weekly)
        self.assertIn("Recommend tradeoffs", weekly)

    def test_a01_distribution_contains_no_symbolic_links(self) -> None:
        self.assertFalse([path for path in self.install.rglob("*") if path.is_symlink()])

    def test_a02_distribution_contains_no_secret_shaped_values(self) -> None:
        secret_patterns = [
            re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
            re.compile(r"gh[opsu]_[A-Za-z0-9]{20,}"),
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        ]
        for path in self.install.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8", errors="ignore")
                for pattern in secret_patterns:
                    self.assertIsNone(pattern.search(text), str(path.relative_to(self.install)))

    def test_a03_private_memory_publishes_only_its_readme(self) -> None:
        private_root = self.install / "memory/private"
        private_files = [path.relative_to(private_root).as_posix() for path in private_root.rglob("*") if path.is_file()]
        self.assertEqual(private_files, ["README.md"])
        check_ignore = subprocess.run(
            ["git", "check-ignore", "memory/private/hypothetical-secret.md"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(check_ignore.returncode, 0)

    def test_a04_public_markdown_has_no_user_specific_absolute_paths(self) -> None:
        pattern = re.compile(r"(?:/Users/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:\\Users\\)")
        for path in self.install.rglob("*.md"):
            self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")), str(path.relative_to(self.install)))

    def test_a05_relative_markdown_links_resolve(self) -> None:
        for path in self.install.rglob("*.md"):
            for href in markdown_links(path.read_text(encoding="utf-8")):
                if re.match(r"^[a-z]+://", href) or href.startswith(("#", "mailto:")):
                    continue
                target = href.split("#", 1)[0]
                self.assertTrue((path.parent / target).resolve().exists(), f"{path.relative_to(self.install)}: {href}")

    def test_a06_public_markdown_has_no_dangerous_bootstrap_commands(self) -> None:
        pattern = re.compile(r"(?:rm\s+-rf|curl\b[^\n|]*\|\s*(?:sh|bash)|chmod\s+777|\beval\s+)", re.IGNORECASE)
        for path in self.install.rglob("*.md"):
            self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")), str(path.relative_to(self.install)))

    def test_a07_templates_preserve_source_and_decision_placeholders(self) -> None:
        for path in (self.install / "templates").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertGreater(len(text), 180, path.name)
            self.assertRegex(text, r"(?i)(source|evidence)", path.name)
            self.assertRegex(text, r"(?m)^[-|1-3].*(?:\s|:|\|)$", path.name)

    def test_a08_examples_are_explicitly_synthetic_and_source_qualified(self) -> None:
        donor = self.installed_text("examples/sample-donor-profile.md")
        brief = self.installed_text("examples/sample-morning-brief.md")
        self.assertIn("Example Family Foundation", donor)
        self.assertIn("internal notes only", donor)
        self.assertIn("No high-stakes external meetings are in memory", brief)

    def test_a09_every_routine_has_purpose_output_and_rules(self) -> None:
        for path in (self.install / "routines").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for heading in ("## Purpose", "## Output", "## Rules"):
                self.assertIn(heading, text, f"{path.name}: {heading}")

    def test_a10_fresh_copy_excludes_git_state_and_keeps_all_documented_routines(self) -> None:
        self.assertFalse((self.install / ".git").exists())
        readme = self.installed_text("README.md")
        for routine in ROUTINES:
            self.assertTrue((self.install / "routines" / routine.name).is_file())
        self.assertEqual(len(list((self.install / "routines").glob("*.md"))), 7)
        self.assertEqual(len(TEMPLATES), 6)
        self.assertIn("routines/", readme)


if __name__ == "__main__":
    unittest.main()
