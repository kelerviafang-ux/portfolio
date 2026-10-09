"""Behavior and submission checks for the Boolean Expressions notebook."""

import contextlib
import io
import json
from pathlib import Path
import unittest

import yaml


NOTEBOOK = Path(__file__).resolve().parents[1] / "_notebooks/HW/2026-10-08-python-boolean-expressionsHW.ipynb"
TASK_CELLS = {
    "fields": "8f9d8aab",
    "create": "b0ddfd3d",
    "search": "c468669d",
    "homework": "be864974",
}


class BooleanPopcornTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK.read_text())
        cls.cells = {cell["id"]: cell for cell in cls.notebook["cells"]}
        cls.solutions = {}
        cls.outputs = {}
        for task, cell_id in TASK_CELLS.items():
            namespace = {}
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exec("".join(cls.cells[cell_id]["source"]), namespace)
            cls.solutions[task] = namespace
            cls.outputs[task] = output.getvalue()

    def test_submission_metadata_and_three_distinct_popcorn_sections(self):
        first = self.notebook["cells"][0]
        self.assertEqual(first["cell_type"], "raw")
        metadata = yaml.safe_load("".join(first["source"]).split("---", 2)[1])
        expected = {
            "title": "3.05 Boolean Expressions HW",
            "categories": ["Python"],
            "lesson_language": "Python",
            "lesson_topic": "Boolean-Expressions HW",
            "lesson_part": "interactive",
            "lesson_type": "lesson",
            "permalink": "/python/boolean-hw",
            "author": "kelerviafang-ux",
        }
        for field, value in expected.items():
            self.assertEqual(metadata[field], value)
        text = "\n".join("".join(cell["source"]) for cell in self.notebook["cells"] if cell["cell_type"] == "markdown")
        for number in [1, 2, 3]:
            self.assertEqual(text.count(f"## Popcorn Hack {number}:"), 1)
        self.assertIn("## In-class MCQ Result", text)
        self.assertIn("## College Board Pseudocode Check", text)

    def test_completeness_reports_each_field_and_a_missing_date(self):
        for requirement in ["Product name present", "Category accepted", "Spec number present", "Effective date present", "Record complete"]:
            self.assertIn(f"{requirement}: True", self.outputs["fields"])
        self.assertIn("After clearing the effective date: False", self.outputs["fields"])

    def test_create_and_homework_rules_reject_each_failed_requirement(self):
        valid = {
            "product_name": "Test Flywheel",
            "category": "Auto Racing",
            "spec_number": "1.2",
            "effective_date": "2026-10-08",
        }
        for task, function_name in [("create", "can_create_sfi_record"), ("homework", "validate_sfi_record")]:
            solution = self.solutions[task]
            validate = solution[function_name]
            categories = solution["valid_categories"]
            existing = solution["existing_spec_numbers"]
            self.assertTrue(validate(valid, categories, existing))
            self.assertFalse(validate({**valid, "spec_number": "1.1"}, categories, existing))
            self.assertFalse(validate({**valid, "category": "Street Car"}, categories, existing))
            for field in ["product_name", "category", "spec_number", "effective_date"]:
                for value in ["", "   ", None, 42]:
                    with self.subTest(task=task, field=field, value=value):
                        self.assertFalse(validate({**valid, field: value}, categories, existing))
                missing = {key: value for key, value in valid.items() if key != field}
                self.assertFalse(validate(missing, categories, existing))

    def test_search_requires_valid_categories_for_both_match_options(self):
        solution = self.solutions["search"]
        search = solution["search_sfi_records"]
        records = solution["records"]
        categories = solution["valid_categories"]
        self.assertEqual([part["spec_number"] for part in search(records, "1.2", categories)], ["1.2"])
        self.assertEqual([part["spec_number"] for part in search(records, " FLYWHEEL ", categories)], ["1.1", "2.1"])
        for query in ["", "   ", "no match", "1."]:
            self.assertEqual(search(records, query, categories), [])
        rejected = [{**records[1], "category": "Street Car"}]
        for query in ["1.2", "multiple"]:
            self.assertEqual(search(rejected, query, categories), [])
        self.assertEqual(search([{}], "1.2", categories), [])
        with self.assertRaisesRegex(ValueError, "must be a string"):
            search(records, None, categories)

    def test_homework_cell_runs_independently_with_six_reported_decisions(self):
        output = self.outputs["homework"]
        self.assertIn("Record 1: ACCEPTED", output)
        for number in range(2, 7):
            self.assertIn(f"Record {number}: REJECTED", output)
        self.assertEqual(len(output.splitlines()), 6)

    def test_saved_and_published_outputs_match_the_completed_code(self):
        for task, output in self.outputs.items():
            saved = "".join(self.cells[TASK_CELLS[task]]["outputs"][0]["text"])
            self.assertEqual(saved, output)
            evidence = "".join(self.cells[TASK_CELLS[task] + "-observed"]["source"])
            self.assertIn(output.rstrip(), evidence)


if __name__ == "__main__":
    unittest.main()
