"""Check the SASS Container Popcorn Hack's rendered invitation and conversion."""

from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = Path('_notebooks/HW/2026-10-10-sass-containerhw.ipynb')


class InvitationMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []
        self.parents = []

    def handle_starttag(self, tag, attrs):
        element = {'tag': tag, 'attrs': dict(attrs), 'parent': self.parents[-1] if self.parents else None}
        self.elements.append(element)
        self.parents.append(element)

    def handle_endtag(self, tag):
        self.parents.pop()

    def by_class(self, name):
        return [element for element in self.elements if name in element['attrs'].get('class', '').split()]


class SassContainerPopcornTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads((ROOT / NOTEBOOK).read_text())
        source = ''.join(next(cell['source'] for cell in notebook['cells'] if cell['id'] == '441b9a97'))
        cls.source = source
        program = source.split('{% capture sass_container_popcorn_code %}', 1)[1].split('{% endcapture %}', 1)[0]
        # Execute the exact JavaScript supplied to the deployed UI Runner.
        result = subprocess.run(
            ['node', '-e', 'const outputElement = {innerHTML: ""};\n' + program + '\nprocess.stdout.write(outputElement.innerHTML);'],
            capture_output=True, text=True, check=True,
        )
        cls.html = result.stdout
        cls.markup = InvitationMarkup()
        cls.markup.feed(cls.html)

    def test_invitation_uses_one_container_and_card_with_title_and_description(self):
        container, = self.markup.by_class('ocs__container')
        card, = self.markup.by_class('ocs__card')
        title, = self.markup.by_class('ocs__section-title')
        description, = self.markup.by_class('ocs__description')
        self.assertIsNone(container['parent'])
        self.assertIs(card['parent'], container)
        self.assertIs(title['parent'], card)
        self.assertIs(description['parent'], card)
        self.assertIn('Poway Rotary Parade Invite', self.html)
        self.assertIn('Celebrate Poway with local parade floats and community groups.', self.html)

    def test_schedule_uses_three_standard_grid_cells_and_one_accent(self):
        grid, = self.markup.by_class('ocs__grid')
        self.assertEqual(grid['attrs']['class'].split(), ['ocs__grid', 'ocs__grid--standard', 'cols-3'])
        cells = self.markup.by_class('ocs__grid-cell')
        self.assertEqual(len(cells), 3)
        for cell in cells:
            self.assertIs(cell['parent'], grid)
        self.assertEqual(len(self.markup.by_class('ocs__grid-cell--accent')), 1)
        for detail in ['Location: Poway Road', 'Start time: 9:00 AM', 'What you get:']:
            self.assertIn(detail, self.html)

    def test_invitation_has_only_ocs_classes_and_no_inline_styles(self):
        allowed = {'ocs__container', 'ocs__card', 'ocs__section-title', 'ocs__description',
                   'ocs__grid', 'ocs__grid--standard', 'cols-3', 'ocs__grid-cell', 'ocs__grid-cell--accent'}
        for element in self.markup.elements:
            self.assertNotIn('style', element['attrs'])
            self.assertLessEqual(set(element['attrs'].get('class', '').split()), allowed)

    def test_clean_conversion_preserves_the_ui_runner(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory)
            source = build / NOTEBOOK
            source.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / NOTEBOOK, source)
            shutil.copyfile(ROOT / 'Makefile', build / 'Makefile')
            shutil.copytree(ROOT / 'scripts', build / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
            subprocess.run(['make', 'convert-single', f'PYTHON={sys.executable}', f'NOTEBOOK_FILE={NOTEBOOK}'],
                           cwd=build, capture_output=True, text=True, check=True)
            post = (build / '_posts/HW/2026-10-10-sass-containerhw_IPYNB_2_.md').read_text()
            self.assertIn('runner_id="sass-container-popcorn-v1"', post)
            self.assertIn('include runners/ui.html', post)
            self.assertIn(self.source.strip(), post)


if __name__ == '__main__':
    unittest.main()
