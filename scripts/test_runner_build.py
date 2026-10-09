"""Regression checks for the Runner notebook and Pages workflow.

Run with: venv/bin/python3 -m unittest discover -s scripts -p 'test_runner_build.py'
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

from scripts.verify_runner_blog import RUNNER_PATH


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = Path("_notebooks/HW/2026-10-03-sasscontainerjshtml-with-runner.ipynb")


class RunnerBuildTests(unittest.TestCase):
    def test_clean_conversion_satisfies_the_workflow_output_check(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/jekyll-gh-pages.yml").read_text())
        steps = workflow["jobs"]["build"]["steps"]
        check = next(step["run"] for step in steps if step["name"] == "Verify Runner notebook conversion")

        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory)
            source = build / NOTEBOOK
            source.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / NOTEBOOK, source)
            shutil.copyfile(ROOT / "Makefile", build / "Makefile")
            shutil.copytree(ROOT / "scripts", build / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
            subprocess.run(
                ["make", "convert-single", f"PYTHON={sys.executable}", f"NOTEBOOK_FILE={NOTEBOOK}"],
                cwd=build, check=True, capture_output=True, text=True,
            )
            subprocess.run(["bash", "-e", "-c", check], cwd=build, check=True)
            output = build / "_posts/HW/2026-10-03-sasscontainerjshtml-with-runner_IPYNB_2_.md"
            self.assertIn("sass-container-js-live-v1", output.read_text())
            self.assertFalse((build / "_posts/HWHacks").exists())

    def test_page_verifier_and_deployment_link_follow_the_notebook_permalink(self):
        notebook = json.loads((ROOT / NOTEBOOK).read_text())
        front_matter = yaml.safe_load("".join(notebook["cells"][0]["source"]).split("---", 2)[1])
        permalink = front_matter["permalink"]
        self.assertEqual(RUNNER_PATH, permalink)

        workflow = yaml.safe_load((ROOT / ".github/workflows/jekyll-gh-pages.yml").read_text())
        steps = workflow["jobs"]["deploy"]["steps"]
        summary = next(step["run"] for step in steps if step.get("name") == "Show published blog links")
        self.assertIn(f"$SITE_URL{permalink}", summary)


if __name__ == "__main__":
    unittest.main()
