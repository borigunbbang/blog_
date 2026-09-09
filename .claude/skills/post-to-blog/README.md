# post-to-blog

[borigunbbang/blog_](https://github.com/borigunbbang/blog_) 학습 기록 블로그에 글을 올리는 반복 작업을 자동화하는 **Claude Code 스킬**입니다.

## 이 스킬 점검

좋은 스킬인지 스스로 확인한 기준입니다.

- [x] **매번 반복하던 일에서 나왔는가?** — 8/31 ~ 9/4까지 총 5번, docx를 열어서 내용 확인 → 손으로 Jekyll 포스트 형식으로 옮겨 적기 → 원본 정리 → git add/commit/push를 매일 똑같이 반복한 뒤에 스킬로 만들었습니다. 한 번 해보고 만든 게 아니라, 실제로 여러 번 반복한 다음에 뽑아낸 패턴입니다.
- [x] **`description`만 봐도 언제 쓰는지 아는가?** — [SKILL.md](SKILL.md) frontmatter에 있는 실제 설명:

  > Convert a raw learning-log file (.docx or .txt) that the user dropped into this Jekyll blog's `_posts/` folder into a properly formatted Jekyll markdown post, archive the original source file, and commit + push to GitHub Pages (borigunbbang/blog_). Use this whenever the user says they added a docx/txt file to `_post(s)` or `_posts` and want it turned into a post ("포스팅해줘", "마크다운으로 만들어줘"), or asks to publish/push a new day's learning-log entry for this blog — even if they don't name this skill directly.

  실제로 사용자가 쓸 법한 트리거 문구("포스팅해줘")를 그대로 넣어뒀기 때문에, 이 설명만 보고도 언제 쓰이는 스킬인지 바로 알 수 있습니다.
- [x] **README에 '왜'가 불편에서 해결로 적혀 있는가?** — 아래 [왜 만들었나](#왜-만들었나) 참고. 불편했던 4단계 과정을 먼저 적고, 그걸 한마디로 없앤다는 걸 명시했습니다.
- [x] **다른 대화에서 한마디로 발동시켜 보았는가?** — 검증함, 그리고 실패도 기록함. 스킬 이름을 전혀 언급하지 않고 "`_post`에 파일 추가했어 포스팅해줘" 한 줄만 준 별도 대화(독립된 에이전트)에서 테스트한 결과, **자동으로 트리거되지 않았습니다.** 원인은 그 세션의 작업 폴더(cwd)가 `blog_`가 아니라 그 부모 폴더였기 때문 — 아래 [알려진 제약](#알려진-제약-작업-폴더)에 그대로 남겨둡니다. "일단 만들었으니 됐다"가 아니라 실제로 다른 맥락에서 던져보고, 안 되면 왜 안 되는지까지 확인하는 게 이 항목의 요지라고 생각해서 결과를 숨기지 않았습니다.

## 알려진 제약 — 작업 폴더

이 스킬은 **프로젝트 스킬**이라 `blog_` 폴더 자체가 Claude Code의 작업 폴더(working directory)일 때만 자동 인식됩니다. `blog_`를 담고 있는 상위 폴더(예: 여러 프로젝트가 모여 있는 폴더)에서 세션을 열면, 그 하위에 `blog_/.claude/skills/`가 있어도 스킬 목록에 나타나지 않습니다.

```bash
# 이렇게 열면 트리거됨
cd "<...>/blog_"
claude

# 이렇게 열면 안 됨 (blog_는 하위 폴더일 뿐)
cd "<...>"          # blog_의 부모 폴더
claude
```

## 왜 만들었나

**불편했던 점**: 매일 학습한 내용을 docx/txt로 대충 적어두고, 그걸 블로그에 올리려면 매번 아래 4단계를 반복해야 했습니다.

1. 문서 열어서 내용 확인
2. Jekyll 포스트 형식(front matter, 섹션 구성)으로 손으로 옮겨 적기
3. 원본 파일 정리
4. `git add` → `commit` → `push`

**해결**: 이 스킬은 "`_posts`에 원본 파일 추가했어, 포스팅해줘" 한마디로 위 4단계 전체를 대신 처리합니다.

## 무엇을 하는지

`_posts/` 폴더에 `.docx` 또는 `.txt` 원본 파일을 넣고 요청하면:

1. **내용 추출** — docx는 pandoc/`python-docx` 없이도 안전하게 문단·표를 뽑아내는 `scripts/extract_docx.py`를 사용
2. **재구성** — 날짜순으로 정리되지 않은 메모를 주제별 `##`/`###` 섹션으로 묶고, 표는 마크다운 표로, ASCII 다이어그램은 코드블록으로, Notion 스타일 콜아웃(`<aside>💡...</aside>`)은 인용문으로 변환. 원문 표현은 그대로 살립니다 (요약하지 않음)
3. **파일 생성** — `_posts/YYYY-MM-DD-day-N.md` 형식으로 저장 (기존 글 중 가장 큰 `day-N`에서 +1, front matter 자동 작성)
4. **원본 아카이브** — 변환에 쓴 원본 파일은 `_source/`로 이동 (Jekyll이 빌드 시 무시하는 폴더라 저장소에 원본 기록만 남기고 사이트엔 노출되지 않음)
5. **배포** — `git add -A` → `commit` → `push origin main`까지 한 번에

자세한 규칙은 [SKILL.md](SKILL.md)에 있습니다.

## 설치

Claude Code가 자동으로 인식하려면 `.claude/skills/post-to-blog/` 경로에 이 저장소 내용이 있어야 합니다.

**개인 스킬로 설치 (어느 프로젝트에서 작업하든 인식):**

```bash
git clone git@github.com:borigunbbang/My-skill_-blog-post.git ~/.claude/skills/post-to-blog
```

**blog_ 프로젝트 안에만 설치 (이미 blog_ 저장소 안에 동일한 스킬이 포함되어 있음):**

```bash
git clone git@github.com:borigunbbang/My-skill_-blog-post.git <blog_ 저장소 경로>/.claude/skills/post-to-blog
```

> 이 스킬은 내용상 `borigunbbang/blog_` 저장소 구조(`_posts`, `_source`, `git push origin main`)를 전제로 동작합니다. 개인 스킬로 설치해도 실제로는 그 저장소 폴더에서 작업할 때만 트리거 조건에 맞습니다.

## 사용법

`blog_` 저장소 폴더에서 Claude Code로 대화하며:

```
_post에 9월 5일 학습.docx 추가했어 포스팅해줘
```

이렇게만 말하면 스킬이 자동으로 트리거되어 위 5단계를 전부 처리합니다. 스킬 이름을 몰라도 되고, 명령어를 외울 필요도 없습니다.

## 요구사항

- Python 3 (표준 라이브러리만 사용 — 추가 설치 불필요)
- git (원격 저장소에 push 권한 필요)

## 관련 도구

- `blog_` 저장소의 [`bin/blogpost`](https://github.com/borigunbbang/blog_/blob/main/bin/blogpost) — 원본 파일 변환이 아니라 **직접 글을 쓸 때** 쓰는 CLI (`new`, `publish`). 이 스킬과는 역할이 다릅니다.
