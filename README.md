# 학습 기록 블로그

Jekyll + GitHub Pages로 만든 날짜별 학습 기록 블로그입니다.

- 배포 주소: https://borigunbbang.github.io/blog_/
- 로컬 미리보기: `bundle exec jekyll serve` (최초 1회 `bundle install` 필요)

## 새 글 쓰는 법

1. `_posts/` 폴더에 아래 형식으로 파일을 만듭니다.

   ```
   _posts/YYYY-MM-DD-제목.md
   ```

2. 파일 맨 위에 아래 형식의 front matter를 넣습니다.

   ```markdown
   ---
   layout: post
   title: "제목"
   date: YYYY-MM-DD 00:00:00 +0900
   categories: [일지]
   ---

   본문 내용
   ```

3. 커밋 후 `main` 브랜치에 push하면 GitHub Pages가 자동으로 빌드/배포합니다.

## 저장소 설정 (최초 1회)

GitHub 저장소 **Settings > Pages** 에서:
- Source: `Deploy from a branch`
- Branch: `main` / `(root)`
