#!/usr/bin/env python3
"""
Rebuild the file list on each student's lesson page.

You never edit HTML. You just drop files into
    guitarlessons/students/<student>/files/
and run:
    python3 tools/update-lesson-files.py

Optional: to add a one-line description under a file, create a plain text file
    guitarlessons/students/<student>/files/_descriptions.txt
with one line per file, in the form:
    Blues Shuffle in E.pdf | Practice slowly with a metronome at 70bpm
"""

import html
import os
import sys
import time
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENTS_DIR = os.path.join(REPO, "guitarlessons", "students")

SKIP = {".gitkeep", "_descriptions.txt", ".DS_Store"}

KIND_LABEL = {
    "pdf": "PDF", "mp3": "AUDIO", "wav": "AUDIO", "m4a": "AUDIO",
    "aiff": "AUDIO", "aif": "AUDIO", "flac": "AUDIO",
    "mp4": "VIDEO", "mov": "VIDEO", "m4v": "VIDEO",
    "png": "IMAGE", "jpg": "IMAGE", "jpeg": "IMAGE", "gif": "IMAGE",
    "gp5": "TAB", "gp": "TAB", "gpx": "TAB", "tab": "TAB", "txt": "TEXT",
    "mid": "MIDI", "midi": "MIDI",
}


def human_size(num_bytes):
    if num_bytes < 1024:
        return "%d B" % num_bytes
    for unit in ("KB", "MB", "GB"):
        num_bytes /= 1024.0
        if num_bytes < 1024 or unit == "GB":
            return "%.0f %s" % (num_bytes, unit) if num_bytes >= 10 else "%.1f %s" % (num_bytes, unit)


def read_descriptions(files_dir):
    path = os.path.join(files_dir, "_descriptions.txt")
    notes = {}
    if not os.path.exists(path):
        return notes
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line:
                continue
            name, _, note = line.partition("|")
            notes[name.strip()] = note.strip()
    return notes


def build_rows(files_dir):
    if not os.path.isdir(files_dir):
        return [], 0

    entries = []
    for name in os.listdir(files_dir):
        full = os.path.join(files_dir, name)
        if name in SKIP or name.startswith(".") or not os.path.isfile(full):
            continue
        entries.append((name, full, os.path.getmtime(full)))

    # Newest first.
    entries.sort(key=lambda item: (-item[2], item[0].lower()))

    notes = read_descriptions(files_dir)
    rows = []
    for name, full, mtime in entries:
        stem, dot, ext = name.rpartition(".")
        display = stem if dot else name
        ext = ext.lower() if dot else ""
        kind = KIND_LABEL.get(ext, ext.upper()[:5] or "FILE")
        href = "files/" + urllib.parse.quote(name)
        added = time.strftime("Added %b %-d, %Y", time.localtime(mtime))
        size = human_size(os.path.getsize(full))

        note_html = ""
        if notes.get(name):
            note_html = '\n            <span class="file-note">%s</span>' % html.escape(notes[name])

        rows.append(
            '        <a class="file-row" href="%s">\n'
            '          <span class="file-kind">%s</span>\n'
            '          <span>\n'
            '            <span class="file-name">%s</span>%s\n'
            '          </span>\n'
            '          <span class="file-meta">%s &middot; %s</span>\n'
            '        </a>'
            % (href, html.escape(kind), html.escape(display), note_html,
               html.escape(added), html.escape(size))
        )

    return rows, len(entries)


def splice(text, start_marker, end_marker, replacement, page_path):
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1:
        sys.exit("ERROR: markers %s / %s missing from %s" % (start_marker, end_marker, page_path))
    return text[: start + len(start_marker)] + replacement + text[end:]


def update_student(student_dir):
    student = os.path.basename(student_dir)
    page_path = os.path.join(student_dir, "index.html")
    if not os.path.exists(page_path):
        print("  skipped %s (no index.html)" % student)
        return

    rows, count = build_rows(os.path.join(student_dir, "files"))

    if rows:
        files_block = "\n" + "\n".join(rows) + "\n"
    else:
        files_block = (
            "\n        <div class=\"empty-state\">Nothing here yet &mdash; "
            "files from our next lesson will appear on this page.</div>\n"
        )

    label = "%02d item%s" % (count, "" if count == 1 else "s")

    with open(page_path, "r", encoding="utf-8") as handle:
        text = handle.read()

    original = text
    text = splice(text, "<!-- FILES:START -->", "<!-- FILES:END -->", files_block, page_path)
    text = splice(text, "<!-- COUNT:START -->", "<!-- COUNT:END -->", label, page_path)

    if text == original:
        print("  %-14s %s (no change)" % (student, label))
        return

    with open(page_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    print("  %-14s %s -> updated" % (student, label))


def main():
    if not os.path.isdir(STUDENTS_DIR):
        sys.exit("ERROR: %s not found. Run this from inside the website repo." % STUDENTS_DIR)

    wanted = sys.argv[1:]
    students = sorted(
        name for name in os.listdir(STUDENTS_DIR)
        if os.path.isdir(os.path.join(STUDENTS_DIR, name)) and not name.startswith(".")
    )
    if wanted:
        students = [name for name in students if name in wanted]
        if not students:
            sys.exit("ERROR: no matching student folder in %s" % STUDENTS_DIR)

    print("Rebuilding lesson pages:")
    for name in students:
        update_student(os.path.join(STUDENTS_DIR, name))
    print("Done. Now commit and push to publish.")


if __name__ == "__main__":
    main()
