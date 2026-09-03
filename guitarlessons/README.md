# Guitar lesson file sharing

A private-ish page per student where they can download tabs, charts, backing
tracks, and recordings.

Aidan's page:  https://rooneypitchford.com/guitarlessons/students/aidan/

## Adding files for a student

1. Drop the files into the student's `files/` folder, e.g.
   `guitarlessons/students/aidan/files/`
   Name them the way you want them to read on the page — "Blues Shuffle in
   E.pdf" shows up as **Blues Shuffle in E**. Spaces are fine.

2. From the top of the repo, run:

       python3 tools/update-lesson-files.py

   That rewrites the file list on every student page. Newest files sort to
   the top.

3. Commit and push. GitHub Pages republishes the site in about a minute.

Optional: to show a one-line note under a file, add a line to that student's
`files/_descriptions.txt`:

    Blues Shuffle in E.pdf | Play it slowly first - metronome at 70bpm

## Adding a new student

    cp -r guitarlessons/students/aidan guitarlessons/students/jamie
    rm -f guitarlessons/students/jamie/files/*

Then open `guitarlessons/students/jamie/index.html` and change "Aidan" to the
new name in the two places it appears (the `<title>` tag and the `<h1>`).
Run the script again and push.

## How private is this, honestly

- The page carries a `noindex` tag, so Google and other search engines skip
  it, and nothing on the site links to it. Someone would have to be given the
  link to find it.
- It is **not** password protected. GitHub Pages has no login. Anyone with the
  exact URL can open it.
- This repository is **public**, so the files are also visible by browsing the
  repo on github.com, and GitHub repos do get indexed by search engines.
  Fine for tabs and backing tracks. Do not put anything here you would mind a
  stranger seeing — especially recordings or photos of a student who is a
  minor.

## Size limits

Individual files must be under 100 MB (GitHub's hard limit), and the whole
repository should stay under about 1 GB. Audio is fine. Long video is not —
put video on YouTube as an unlisted link instead and link to it.
