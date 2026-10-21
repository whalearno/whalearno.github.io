#!/usr/bin/env python3
"""
test_citation.py — 引用模組、citation meta 與 JSON-LD 的建置測試（只用標準函式庫）

用法（在 Personal_Website/ 內）：
  python tools/test_citation.py

做法：
  1. 把網站複製到暫存資料夾，加入測試用文章（含測試 DOI、版本、格式錯誤的值、含引號的標題）。
     測試文章只存在於暫存資料夾，不會進入 content/，也不會被發布。
  2. 建置暫存網站，逐項檢查引用文字、meta、JSON-LD、canonical、hreflang。
  3. 另外建置真正的網站，檢查每頁 canonical 唯一、JSON-LD 有效、沒有測試值外洩。

結束碼：0 全部通過；1 有失敗。需要 PATH 中有 hugo。
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COPY = ["hugo.toml", "archetypes", "assets", "content", "i18n", "layouts", "static", "themes"]
TEST_DOI = "10.5555/fixture.v4"          # 10.5555 為 Crossref 測試用前綴
TEST_CONCEPT_DOI = "10.5555/fixture"
QUOTED_TITLE = '測試 "引號" 與 <角括號> & \'單引號\''

FIXTURES = {
    "zh-tw/notes/fixture-full": f'''---
title: {json.dumps(QUOTED_TITLE, ensure_ascii=False)}
date: 2025-03-04
draft: false
tags: ["Test"]
summary: "fixture"
math: false
version: "v0.4"
doi: "https://doi.org/{TEST_DOI}"
concept_doi: "{TEST_CONCEPT_DOI}"
zenodo: "https://zenodo.org/records/0000000"
license: "CC BY 4.0"
license_url: "https://creativecommons.org/licenses/by/4.0/"
review_status: "Working draft, not peer-reviewed"
pdf_url: "https://example.org/fixture.pdf"
---
內文。
''',
    "en/notes/fixture-full": f'''---
title: "Fixture \\"Quoted\\" Title"
date: 2025-03-04
draft: false
tags: ["Test"]
summary: "fixture"
math: false
version: "v0.4"
doi: "{TEST_DOI}"
---
Body.
''',
    "zh-tw/notes/fixture-version": '''---
title: "只有版本"
date: 2024-12-31
draft: false
tags: ["Test"]
summary: "fixture"
math: false
version: "v1.2"
---
內文。
''',
    "zh-tw/notes/fixture-bad": f'''---
title: "格式錯誤的欄位"
date: 2026-01-01
draft: false
tags: ["Test"]
summary: "fixture"
math: false
doi: "10.1234"
concept_doi: "not-a-doi"
zenodo: "https://sandbox.zenodo.org/records/1"
license_url: "creativecommons"
pdf_url: "missing.pdf"
---
內文。
''',
    "zh-tw/essays/fixture-essay": '''---
title: "觀點文章"
date: 2026-02-02
draft: false
tags: ["Test"]
summary: "fixture"
math: false
---
內文。
''',
    "zh-tw/essays/fixture-off": '''---
title: "關閉引用"
date: 2026-02-02
draft: false
tags: ["Test"]
summary: "fixture"
math: false
citation: false
---
內文。
''',
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical, self.hreflang, self.meta, self.ldjson = [], {}, {}, []
        self.cite_text, self.cite_boxes, self.copy_buttons = None, 0, 0
        self._in_ld, self._ld_buf = False, []
        self._in_cite, self._cite_buf = 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a.get("href"))
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang[a["hreflang"]] = a.get("href")
        if tag == "meta" and (a.get("name") or "").startswith("citation_"):
            self.meta.setdefault(a["name"], []).append(a.get("content"))
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._ld_buf = True, []
        if tag == "section" and "cite-box" in (a.get("class") or ""):
            self.cite_boxes += 1
        if tag == "button" and "data-cite-copy" in a:
            self.copy_buttons += 1
        if tag == "p" and a.get("class") == "cite-text":
            self._in_cite, self._cite_buf = 1, []
        elif self._in_cite:
            self._in_cite += 1

    def handle_endtag(self, tag):
        if tag == "script" and self._in_ld:
            self._in_ld = False
            self.ldjson.append("".join(self._ld_buf))
        if self._in_cite:
            self._in_cite -= 1
            if self._in_cite == 0:
                self.cite_text = "".join(self._cite_buf)

    def handle_data(self, data):
        if self._in_ld:
            self._ld_buf.append(data)
        if self._in_cite:
            self._cite_buf.append(data)


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    p.ld = []
    for raw in p.ldjson:
        p.ld.append(json.loads(raw))  # 無效 JSON 直接拋出例外
    p.article = [o for o in p.ld if o.get("@type") not in ("BreadcrumbList", "Person", "Organization")]
    return p


failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
    print(("  ok    " if cond else "  FAIL  ") + msg)


def build(src, dest):
    r = subprocess.run(["hugo", "build", "--minify", "-s", str(src), "-d", str(dest)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or "ERROR" in r.stdout + r.stderr:
        print(r.stdout + r.stderr)
        sys.exit("hugo build 失敗")


def site_wide_checks(public, label):
    print(f"\n[{label}] 全站檢查")
    pages = [p for p in public.rglob("*.html")]
    bad_canonical, bad_json = [], []
    for f in pages:
        try:
            p = parse(f)
        except json.JSONDecodeError as e:
            bad_json.append(f"{f.relative_to(public)}: {e}")
            continue
        if len(p.canonical) != 1:
            bad_canonical.append(f"{f.relative_to(public)} ({len(p.canonical)})")
        if len(p.article) > 1:
            bad_json.append(f"{f.relative_to(public)}: {len(p.article)} 個文章物件")
        for lang, href in p.hreflang.items():
            rel = href.split("://", 1)[-1].split("/", 1)[-1] if "/" in href.split("://", 1)[-1] else ""
            target = public / rel if rel.endswith(".html") else public / rel / "index.html"
            if not target.exists():
                bad_canonical.append(f"{f.relative_to(public)} hreflang {lang} 指向不存在頁面 {href}")
        text = f.read_text(encoding="utf-8")
        if p.cite_text is not None and ("undefined" in p.cite_text or ". . " in p.cite_text):
            bad_json.append(f"{f.relative_to(public)}: 引用文字有空欄位")
        if "cite-box" in text and p.cite_boxes != 1:
            bad_json.append(f"{f.relative_to(public)}: 引用區塊數量 {p.cite_boxes}")
    check(not bad_canonical, f"{len(pages)} 頁 canonical 唯一、hreflang 目標存在" + ("" if not bad_canonical else f"：{bad_canonical[:5]}"))
    check(not bad_json, "JSON-LD 皆為有效 JSON、每頁最多一個文章物件" + ("" if not bad_json else f"：{bad_json[:5]}"))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="citation-test-") as tmp:
        tmp = Path(tmp)
        site = tmp / "site"
        site.mkdir()
        for name in COPY:
            src = ROOT / name
            if src.is_dir():
                shutil.copytree(src, site / name)
            elif src.exists():
                shutil.copy2(src, site / name)
        for rel, body in FIXTURES.items():
            d = site / "content" / rel
            d.mkdir(parents=True)
            (d / "index.md").write_text(body, encoding="utf-8")

        out = tmp / "fixture-public"
        build(site, out)

        print("[fixture] 完整欄位（中文）")
        p = parse(out / "notes/fixture-full/index.html")
        expected = f"Chih-Ming Wang. (2025). {QUOTED_TITLE} (v0.4). 研究札記與觀點. https://doi.org/{TEST_DOI}"
        check(p.cite_text == expected, f"引用文字 = {p.cite_text!r}")
        check(p.copy_buttons == 1, "有複製按鈕")
        check(p.meta.get("citation_doi") == [TEST_DOI], "citation_doi 去除 https://doi.org/ 前綴")
        check(p.meta.get("citation_title") == [QUOTED_TITLE], "citation_title 保留引號")
        check(p.meta.get("citation_publication_date") == ["2025/03/04"], "citation_publication_date")
        check(p.meta.get("citation_pdf_url") == ["https://example.org/fixture.pdf"], "citation_pdf_url")
        a = p.article[0] if p.article else {}
        check(a.get("@type") == "ScholarlyArticle", "notes 為 ScholarlyArticle")
        check(a.get("headline") == QUOTED_TITLE, "JSON-LD headline 含引號仍正確")
        check(a.get("version") == "v0.4", "JSON-LD version")
        ids = {i.get("name", "version"): i["value"] for i in a.get("identifier", [])}
        check(ids == {"version": TEST_DOI, "Concept DOI": TEST_CONCEPT_DOI}, f"JSON-LD identifier 分開版本與 concept DOI：{ids}")
        check(a.get("archivedAt") == "https://zenodo.org/records/0000000", "JSON-LD archivedAt = Zenodo")
        check(a.get("license") == "https://creativecommons.org/licenses/by/4.0/", "JSON-LD license 只用正式網址")
        check(a.get("inLanguage") == "zh-TW" and a.get("url", "").endswith("/notes/fixture-full/"), "inLanguage 與 url")
        check(len(p.canonical) == 1 and p.canonical[0] == a.get("url"), "canonical 唯一且等於 JSON-LD url")
        check(set(p.hreflang) == {"zh-tw", "en"}, f"有翻譯時輸出 hreflang：{sorted(p.hreflang)}")

        print("[fixture] 英文翻譯")
        p = parse(out / "en/notes/fixture-full/index.html")
        check(p.cite_text == f'Chih-Ming Wang. (2025). Fixture "Quoted" Title (v0.4). Research Notes & Perspectives. https://doi.org/{TEST_DOI}',
              f"英文引用文字 = {p.cite_text!r}")

        print("[fixture] 只有版本")
        p = parse(out / "notes/fixture-version/index.html")
        check(re.fullmatch(r"Chih-Ming Wang\. \(2024\)\. 只有版本 \(v1\.2\)\. 研究札記與觀點\. \S+/notes/fixture-version/", p.cite_text or ""),
              f"引用文字使用 permalink = {p.cite_text!r}")
        check("citation_doi" not in p.meta and "identifier" not in p.article[0], "沒有 DOI 時不輸出 DOI")
        check(set(p.hreflang) == {"zh-tw"}, "沒有翻譯時不輸出其他語言 hreflang")

        print("[fixture] 格式錯誤的欄位")
        p = parse(out / "notes/fixture-bad/index.html")
        text = (out / "notes/fixture-bad/index.html").read_text(encoding="utf-8")
        check((p.cite_text or "").endswith("/notes/fixture-bad/"), "無效 DOI 不取代 permalink")
        check("citation_doi" not in p.meta and "citation_pdf_url" not in p.meta, "無效 DOI、不存在的 PDF 不輸出 meta")
        a = p.article[0]
        check(not any(k in a for k in ("identifier", "archivedAt", "license")), "無效 DOI、sandbox Zenodo、無效授權網址皆不輸出")
        check("sandbox.zenodo" not in text and "10.1234<" not in text, "頁面上不顯示無效值")

        print("[fixture] essays")
        p = parse(out / "essays/fixture-essay/index.html")
        check(p.article[0].get("@type") == "BlogPosting" and p.cite_boxes == 1, "essays 維持 BlogPosting，並有引用區塊")
        p = parse(out / "essays/fixture-off/index.html")
        check(p.cite_boxes == 0 and not p.meta, "citation: false 時不顯示引用區塊與 meta")

        print("[fixture] 非文章頁面")
        for rel in ("about/index.html", "citation-reuse/index.html", "en/citation-reuse/index.html"):
            p = parse(out / rel)
            check(p.cite_boxes == 0 and not p.meta, f"{rel} 沒有引用區塊")

        site_wide_checks(out, "fixture")

        real = tmp / "real-public"
        build(ROOT, real)
        site_wide_checks(real, "正式網站")
        leaked = [str(f.relative_to(real)) for f in real.rglob("*") if f.is_file()
                  and f.suffix in (".html", ".xml", ".json", ".txt")
                  and ("10.5555" in f.read_text(encoding="utf-8", errors="ignore") or "fixture" in f.name)]
        check(not leaked, "正式網站沒有測試 DOI 或測試文章" + ("" if not leaked else f"：{leaked}"))

    print(f"\n{'全部通過' if not failures else f'失敗 {len(failures)} 項'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
