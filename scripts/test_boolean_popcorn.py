"""Behavior checks for the Boolean Expressions popcorn hack solutions."""

import contextlib
import io
import json
from pathlib import Path
import unittest


NOTEBOOK = Path(__file__).resolve().parents[1] / "_notebooks/HW/2026-10-08-python-boolean-expressionsHW.ipynb"


class BooleanPopcornTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK.read_text())
        cls.solutions = {}
        cls.outputs = {}
        for index in [2, 4, 6, 10, 12]:
            namespace = {}
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exec("".join(cls.notebook["cells"][index]["source"]), namespace)
            cls.solutions[index] = namespace
            cls.outputs[index] = output.getvalue()

    def test_completeness_reports_each_field_and_a_missing_date(self):
        for requirement in ["Product name present", "Category accepted", "Spec number present", "Effective date present", "Record complete"]:
            self.assertIn(f"{requirement}: True", self.outputs[2])
        self.assertIn("After clearing the effective date: False", self.outputs[2])
        self.assertFalse(self.solutions[4]["can_create_record"])

    def test_create_rule_accepts_only_complete_records_with_a_new_spec(self):
        solution = self.solutions[6]
        create = solution["can_create_sfi_record"]
        valid = {**solution["part"], "spec_number": "1.2"}
        categories = solution["valid_categories"]
        existing = solution["existing_spec_numbers"]
        self.assertTrue(create(valid, categories, existing))
        self.assertFalse(create(solution["part"], categories, existing))
        self.assertFalse(create({**valid, "category": "Street Car"}, categories, existing))
        for field in ["product_name", "category", "spec_number", "effective_date"]:
            for value in ["", "   ", None, 42]:
                with self.subTest(field=field, value=value):
                    self.assertFalse(create({**valid, field: value}, categories, existing))
            missing = {key: value for key, value in valid.items() if key != field}
            self.assertFalse(create(missing, categories, existing))

    def test_search_combines_name_or_exact_spec_with_an_accepted_category(self):
        for index in [10, 12]:
            solution = self.solutions[index]
            search = solution["search_sfi_records"]
            records = solution["records"]
            categories = solution["valid_categories"]
            self.assertEqual([part["spec_number"] for part in search(records, "1.2", categories)], ["1.2"])
            self.assertEqual([part["spec_number"] for part in search(records, " FLYWHEEL ", categories)], ["1.1", "2.1"])
            for query in ["", "   ", "no match", "1."]:
                self.assertEqual(search(records, query, categories), [])
            self.assertEqual(search([{**records[1], "category": "Street Car"}], "1.2", categories), [])
            self.assertEqual(search([{}], "1.2", categories), [])
            with self.assertRaisesRegex(ValueError, "must be a string"):
                search(records, None, categories)

    def test_saved_outputs_match_the_completed_code(self):
        for index, output in self.outputs.items():
            saved = "".join(self.notebook["cells"][index]["outputs"][0]["text"])
            self.assertEqual(saved, output)


if __name__ == "__main__":
    unittest.main()
