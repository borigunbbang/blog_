source "https://rubygems.org"

# GitHub Pages가 지원하는 gem 세트를 통째로 사용 (버전 충돌 없이 안전하게 빌드됨)
gem "github-pages", group: :jekyll_plugins

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-seo-tag"
end

# Windows / JRuby 호환용 (없어도 되지만 GitHub Pages 기본 템플릿 관례)
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
