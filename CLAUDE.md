# CLAUDE.md

이 저장소에서 작업할 때 참고할 컨텍스트입니다.

## 프로젝트 개요

Jekyll + GitHub Pages로 만든 날짜별 학습 기록 블로그입니다. 배포 주소: https://borigunbbang.github.io/blog_/

## 새 글 올리기 — `bin/blogpost` CLI

직접 글을 쓸 때는 저장소에 포함된 간단한 CLI를 사용합니다.

```bash
./bin/blogpost new "제목"
./bin/blogpost publish "메시지"
```

- **`new "제목"`**: `_posts/`에 오늘 날짜 기준 `YYYY-MM-DD-day-N.md` 파일을 생성합니다. `day-N`의 번호는 기존 글 중 가장 큰 번호에서 자동으로 +1됩니다. front matter(`layout: post`, `title`, `date`, `categories: [일지]`)까지 채워진 상태로 생성되므로 바로 본문만 작성하면 됩니다.
- **`publish ["메시지"]`**: `git add -A` → `git commit -m "메시지"`(메시지 생략 시 기본값 `"학습 기록 업데이트"`) → `git push origin main`을 한 번에 실행합니다.

`./bin/` 없이 `blogpost`로 바로 쓰려면 PATH에 등록:

```bash
echo 'export PATH="$PATH:'"$(pwd)"'/bin"' >> ~/.zshrc && source ~/.zshrc
```

## 원본 파일(docx/txt)을 글로 변환할 때

`_posts/`에 원본 docx/txt 파일을 그대로 넣고 "포스팅해줘"라고 요청하면 `.claude/skills/post-to-blog` 스킬이 자동으로 트리거되어: 내용 추출 → 섹션별 마크다운으로 재구성 → 원본은 `_source/`로 이동 → git commit/push까지 처리합니다.

`bin/blogpost`는 직접 글을 쓸 때, `post-to-blog` 스킬은 원본 파일을 변환할 때 — 용도가 다릅니다.

## 디렉터리 구조

- `_posts/` — 게시된 글 (`YYYY-MM-DD-day-N.md`)
- `_source/` — 변환 전 원본 파일 아카이브 (Jekyll이 빌드에서 무시하는 폴더)
- `bin/blogpost` — 글 작성/배포 CLI
- `.claude/skills/post-to-blog/` — docx/txt → 포스트 자동 변환 스킬

## 배포

`main` 브랜치에 push하면 GitHub Pages가 자동으로 빌드합니다. 보통 1~2분 안에 반영됩니다.
