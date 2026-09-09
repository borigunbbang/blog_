---
name: post-to-blog
description: >
  Convert a raw learning-log file (.docx or .txt) that the user dropped into
  this Jekyll blog's _posts/ folder into a properly formatted Jekyll markdown
  post, archive the original source file, and commit + push to GitHub Pages
  (borigunbbang/blog_). Use this whenever the user says they added a docx/txt
  file to _post(s) or _posts and want it turned into a post ("포스팅해줘",
  "마크다운으로 만들어줘"), or asks to publish/push a new day's learning-log
  entry for this blog — even if they don't name this skill directly.
---

# Post to blog

This repo is a Jekyll + GitHub Pages blog of dated learning-log posts
(`_posts/YYYY-MM-DD-day-N.md`, `layout: post`, `categories: [일지]`). The
recurring workflow is: the user drops a raw `.docx`/`.txt` file straight into
`_posts/`, and Claude turns it into a matching markdown post, files the raw
source away, and ships it. Follow these steps in order.

## 1. Find the raw file

List `_posts/` and find the file that does **not** match the
`YYYY-MM-DD-title.md` pattern — that's the raw drop the user just added
(usually named something like `9월 4일 학습.docx` or `8/31 일기.txt`).

## 2. Extract its content

**For `.docx`:** don't rely on pandoc or `python-docx` being installed —
they often aren't. Use the bundled script instead:

```bash
python3 "<this-skill-dir>/scripts/extract_docx.py" "_posts/<file>.docx"
```

It prints JSON: `{"paragraphs": [...], "tables": [[[cell,...],...],...]}`,
with tables already pulled out separately so you can render them as real
markdown tables instead of flattening them into prose. Read the script's
docstring if you need to know why it exists — the short version is that a
naive `<w:t...>` regex silently matches `<w:tab>` elements too and corrupts
the extraction.

**For `.txt`:** just read the file directly.

## 3. Turn it into a Jekyll post

The raw notes are typically dense, dashed-off, and organized by whatever
order the user typed them in (often with a `날짜`/`제목`/`내용` header, ASCII
tree diagrams, Notion-style `<aside>💡...</aside>` callouts, and tables).
Your job is to restructure — not just reformat — that into a readable post:

- Group related paragraphs under `##`/`###` headings that reflect the actual
  topics covered (don't invent structure that isn't there, but do impose it
  where the source is just a flat list of loosely related bullets).
- Convert extracted tables into markdown tables.
- Preserve ASCII-art trees/diagrams inside fenced code blocks so their
  spacing survives.
- Turn `<aside>💡...</aside>` callouts and "AI에게 이렇게 요청하세요" style
  suggested-prompt lines into blockquotes (`> ...`).
- Keep the user's own voice and phrasing — this is their study log, not a
  polished article. Don't smooth over or summarize away content; reorganize
  and reformat it, but say what they said.
- If there's a closing personal note (diary-style reflection, "오늘의 일기"),
  keep it as its own short section near the end rather than folding it into
  the technical notes.

Front matter — match the existing posts exactly:

```markdown
---
layout: post
title: "<from the 제목 field, or a short title matching the day's topic>"
date: <YYYY-MM-DD> 00:00:00 +0900
categories: [일지]
---
```

## 4. Name and place the file

Look at the existing files in `_posts/` to find the highest `day-N` number
used so far, and continue the sequence: `_posts/YYYY-MM-DD-day-<N+1>.md`.
The date comes from the raw file's own `날짜` field (or the filename), not
today's date, if they differ.

## 5. Archive the original

Move the raw source file out of `_posts/` into `_source/` (create it if it
doesn't exist yet) — Jekyll ignores underscore-prefixed folders, so this
keeps the raw notes in the repo as a reference without them being processed
as a page or breaking the build. Keep the original filename (fix obviously
broken characters like a stray `:` from a date typed as `9:4` only if it
would cause shell/path headaches, otherwise leave it as the user wrote it).

## 6. Commit and push

```bash
git add -A
git commit -m "<날짜> 학습 내용(<핵심 주제 1~3개>) 포스팅 추가

- _posts/<new file>: 원본 <docx/txt> 내용을 Jekyll 포스트로 변환
- _source/: 원본 파일 아카이브

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
git push origin main
```

Only push once you're confident the post reads well — if anything about the
source content was ambiguous (illegible fragments, unclear date), ask the
user rather than guessing, since it's about to go live on a public blog.

## After pushing

Tell the user the commit landed and that GitHub Pages will pick it up in a
minute or two at `https://borigunbbang.github.io/blog_/`. Don't poll or
sleep waiting for the deploy unless they ask you to check.
