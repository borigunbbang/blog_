---
layout: page
title: 검색
permalink: /search/
---

<input id="search-input" class="search-input" type="search" placeholder="제목, 내용, 태그로 검색 (예: Attention, RLS)" autocomplete="off">
<p id="search-count" class="search-count"></p>
<ul id="search-results" class="tag-post-list"></ul>

<script>
(function () {
  var input = document.getElementById('search-input');
  var list = document.getElementById('search-results');
  var count = document.getElementById('search-count');
  var docs = [];
  fetch('{{ "/search.json" | relative_url }}').then(function (r) { return r.json(); }).then(function (d) {
    docs = d;
    var q = new URLSearchParams(location.search).get('q');
    if (q) { input.value = q; run(); }
  });
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function run() {
    var q = input.value.trim().toLowerCase();
    list.innerHTML = '';
    if (!q) { count.textContent = ''; return; }
    var hits = docs.filter(function (d) {
      return (d.title + ' ' + d.tags.join(' ') + ' ' + d.content).toLowerCase().indexOf(q) !== -1;
    });
    count.textContent = hits.length + '개의 글';
    hits.forEach(function (d) {
      var i = d.content.toLowerCase().indexOf(q);
      var snip = i < 0 ? '' : '…' + d.content.slice(Math.max(0, i - 40), i + 80) + '…';
      var li = document.createElement('li');
      li.innerHTML = '<span>' + d.date + '</span> <a href="' + d.url + '">' + esc(d.title) + '</a>' +
        (snip ? '<p class="search-snippet">' + esc(snip) + '</p>' : '');
      list.appendChild(li);
    });
  }
  input.addEventListener('input', run);
})();
</script>
