"""Fail a Pages build if the JavaScript Runner or its blog entry is missing."""

import argparse
from html.parser import HTMLParser
from pathlib import Path


RUNNER_PATH = "/HW/sass-container-js-runner/"
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
        self.redirect_urls = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.add(attrs.get("href"))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            content = attrs.get("content", "")
            if "url=" in content:
                self.redirect_urls.add(content.split("url=", 1)[1].strip())
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


def verify_python_lesson(site, baseurl, lesson_path, runner_id, legacy_path=None):
    """Reject missing lesson routes, broken runners, and stale blog links."""
    lesson_file = site / lesson_path.strip("/") / "index.html"
    if not lesson_file.is_file():
        raise ValueError(f"Missing generated Python lesson: {lesson_file}")
    lesson = PageMarkup()
    lesson.feed(lesson_file.read_text(encoding="utf-8"))
    if f"runner-{runner_id}" not in lesson.ids or not lesson.has_editor or not lesson.has_run_button:
        raise ValueError("Python lesson runner markup, editor, or Run button is missing")
    module_path = f"{baseurl}/assets/js/pages/runners/index.js"
    if not any(module_path in script and 'pythonRuntime: "browser"' in script
               for script in lesson.module_scripts):
        raise ValueError("Python lesson browser runtime or runner module import is missing")

    url = baseurl + lesson_path
    blogs = PageMarkup()
    blogs.feed((site / "blogs/index.html").read_text(encoding="utf-8"))
    if url not in blogs.links:
        raise ValueError(f"Blog list does not link to the Python lesson: {url}")
    legacy_paths = [legacy_path] if isinstance(legacy_path, str) else (legacy_path or [])
    for path in legacy_paths:
        legacy_file = site / path.strip("/") / "index.html"
        if not legacy_file.is_file():
            raise ValueError(f"Missing compatibility redirect: {legacy_file}")
        legacy = PageMarkup()
        legacy.feed(legacy_file.read_text(encoding="utf-8"))
        if url not in legacy.redirect_urls or url not in legacy.links:
            raise ValueError(f"Compatibility redirect must point to {url}")
        print(f"Verified compatibility redirect: {baseurl}{path}")
    print(f"Verified Python lesson and blog entry: {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--baseurl", default="/portfolio")
    parser.add_argument("--python-lesson-path")
    parser.add_argument("--python-runner-id")
    parser.add_argument("--legacy-path", action="append", help="Compatibility URL; may be repeated")
    args = parser.parse_args()
    try:
        verify(args.site, args.baseurl.rstrip("/"))
        if args.python_lesson_path or args.python_runner_id or args.legacy_path:
            if not args.python_lesson_path or not args.python_runner_id:
                raise ValueError("Python lesson verification requires both its path and runner ID")
            verify_python_lesson(args.site, args.baseurl.rstrip("/"),
                                 args.python_lesson_path, args.python_runner_id, args.legacy_path)
    except ValueError as error:
        parser.exit(1, f"Pages verification failed: {error}\n")
