"""Fail a Pages build if the JavaScript Runner or its blog entry is missing."""

import argparse
from html.parser import HTMLParser
from pathlib import Path


RUNNER_PATH = "/hwhacks/sass-container-js-runner/"
RUNNER_ID = "sass-container-js-live-v1"


class PageMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()
        self.ids = set()
        self.has_editor = False
        self.has_run_button = False
        self.module_scripts = []
        self.in_module = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.add(attrs.get("href"))
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "textarea" and "editor-textarea" in attrs.get("class", "").split():
            self.has_editor = True
        if tag == "button" and "runBtn" in attrs.get("class", "").split():
            self.has_run_button = True
        if tag == "script":
            self.in_module = attrs.get("type") == "module"

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_module = False

    def handle_data(self, data):
        if self.in_module:
            self.module_scripts.append(data)


def verify(site, baseurl):
    runner_file = site / RUNNER_PATH.strip("/") / "index.html"
    blog_file = site / "blogs/index.html"
    for path in (runner_file, blog_file):
        if not path.is_file():
            raise ValueError(f"Missing generated page: {path}")

    runner = PageMarkup()
    runner.feed(runner_file.read_text(encoding="utf-8"))
    if not {f"ui-runner-{RUNNER_ID}", f"ui-output-{RUNNER_ID}"} <= runner.ids:
        raise ValueError("Runner markup is missing; check notebook conversion and Liquid includes")
    if not runner.has_editor or not runner.has_run_button:
        raise ValueError("Runner editor or Run button is missing")
    module_path = f"{baseurl}/assets/js/pages/runners/index.js"
    if not any(module_path in script for script in runner.module_scripts):
        raise ValueError(f"Runner module import is missing: {module_path}")
    if not (site / "assets/js/pages/runners/index.js").is_file():
        raise ValueError("Runner JavaScript assets were not published")

    blogs = PageMarkup()
    blogs.feed(blog_file.read_text(encoding="utf-8"))
    url = baseurl + RUNNER_PATH
    if url not in blogs.links:
        raise ValueError(f"Blog list does not link to {url}; check post metadata and blog filtering")
    print(f"Verified Runner: {url}")
    print(f"Verified blog entry: {baseurl}/blogs/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--baseurl", default="/portfolio")
    args = parser.parse_args()
    try:
        verify(args.site, args.baseurl.rstrip("/"))
    except ValueError as error:
        parser.exit(1, f"Pages verification failed: {error}\n")
