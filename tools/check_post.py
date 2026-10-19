#!/usr/bin/env python3
"""
check_post.py — 發布前檢查（只用 Python 標準函式庫）

用法：
  python tools/check_post.py <文章資料夾或 .md 檔> [...] --terms <敏感詞清單>

範例：
  python tools/check_post.py content/zh-tw/notes/tensor-rigidity --terms ../Website_Inbox/_config/sensitive_terms.txt
  python tools/check_post.py --all --terms ../Website_Inbox/_config/sensitive_terms.txt

結果：
  ERROR  必須修正，有任何 ERROR 時結束碼為 1，不可發布
  WARN   建議確認，不阻擋發布
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = {"zh-tw", "en"}
SECTIONS = {"notes", "essays", "publications"}
REQUIRED = ["title", "date", "draft", "tags", "summary", "math"]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_front_matter(text):
    """解析 YAML front matter 的簡化版本，足以應付本站規範的欄位。"""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    block = text[3:end].strip("\n")
    body = text[end + 4:]
    data, current_list = {}, None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m_item = re.match(r"^\s*-\s+(.*)$", line)
        if m_item and current_list is not None:
            data[current_list].append(m_item.group(1).strip().strip("\"'"))
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        current_list = None
        if val == "":
            data[key] = []
            current_list = key
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [v.strip().strip("\"'") for v in inner.split(",") if v.strip()]
        else:
            data[key] = val.strip("\"'")
    return data, body


def load_terms(path):
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        print(f"ERROR  找不到敏感詞清單：{p}")
        sys.exit(2)
    terms = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def strip_code(body):
    """移除程式碼區塊與行內程式碼，避免誤判公式與 HTML。"""
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    body = re.sub(r"~~~.*?~~~", "", body, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", body)


def check_file(md: Path, terms):
    errors, warns = [], []
    text = md.read_text(encoding="utf-8")
    fm, body = parse_front_matter(text)

    # 位置：content/<lang>/<section>/<slug>/index.md
    try:
        rel = md.resolve().relative_to(ROOT / "content")
        parts = rel.parts
    except ValueError:
        parts = ()
    if parts:
        if len(parts) != 4 or parts[3] != "index.md":
            errors.append("位置應為 content/<語言>/<分類>/<英文網址名稱>/index.md")
        else:
            lang, section, slug = parts[0], parts[1], parts[2]
            if lang not in LANGS:
                errors.append(f"語言資料夾不正確：{lang}（應為 zh-tw 或 en）")
            if section not in SECTIONS:
                errors.append(f"分類不正確：{section}（應為 notes、essays、publications）")
            if not SLUG_RE.match(slug):
                errors.append(f"網址名稱只能用小寫英文、數字與連字號：{slug}")

    # front matter
    if fm is None:
        errors.append("缺少 YAML front matter（開頭需有 --- 區塊）")
        fm = {}
    for key in REQUIRED:
        if key not in fm:
            errors.append(f"front matter 缺少欄位：{key}")
    if "draft" in fm and str(fm["draft"]).lower() not in ("true", "false"):
        errors.append("draft 必須是 true 或 false")
    if "date" in fm and not re.match(r"^\d{4}-\d{2}-\d{2}", str(fm["date"])):
        errors.append(f"date 格式應為 YYYY-MM-DD：{fm['date']}")
    if not str(fm.get("title", "")).strip():
        errors.append("title 不可空白")
    tags = fm.get("tags", [])
    if isinstance(tags, list):
        if not tags:
            warns.append("tags 為空")
        for t in tags:
            if not re.match(r"^[A-Za-z0-9][A-Za-z0-9 .\-]*$", t):
                warns.append(f"tag 建議使用英文：{t}")
    if not str(fm.get("summary", "")).strip():
        warns.append("summary 為空，列表頁會自動截取開頭文字")
    if parts and len(parts) == 4 and parts[1] == "publications":
        if not (fm.get("doi") or fm.get("zenodo") or fm.get("arxiv")):
            warns.append("研究成果尚未填入 doi、zenodo 或 arxiv")

    clean = strip_code(body)

    # 數學公式規範
    has_math = bool(re.search(r"\$\$|\\\[|\\\(", clean))
    if has_math and str(fm.get("math", "false")).lower() != "true":
        errors.append("內文含公式，但 math 不是 true，公式不會被渲染")
    no_block = re.sub(r"\$\$.*?\$\$", "", clean, flags=re.S)
    for m in re.finditer(r"(?<![\\$])\$([^$\n]+?)\$(?!\$)", no_block):
        inner = m.group(1)
        if re.search(r"[\\^_{}]", inner):
            warns.append(f"疑似使用單一 $ 的行內公式（本站不支援，請改用 \\( ... \\)）：${inner[:40]}$")

    # 原始 HTML 會被移除（hugo.toml 設定 unsafe = false）
    if re.search(r"<(div|span|table|iframe|script|style|img)\b", clean, flags=re.I):
        warns.append("內文含 HTML 標籤，網站不會顯示，請改用 Markdown")

    # 圖片與附件路徑
    for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)", clean):
        ref = m.group(1)
        if re.match(r"^(https?:)?//", ref):
            continue
        target = (ROOT / "static" / ref.lstrip("/")) if ref.startswith("/") else (md.parent / ref)
        if not target.exists():
            errors.append(f"找不到圖片：{ref}")
    if re.search(r"!\[[^\]]*\]\([A-Za-z]:[\\/]", clean):
        errors.append("圖片使用了本機絕對路徑（例如 D:\\...），上線後會失效")

    # 敏感詞（全文，含 front matter；同時檢查同資料夾的其他文字檔名）
    low = text.lower()
    for term in terms:
        if term.lower() in low:
            line_no = next((i + 1 for i, l in enumerate(text.splitlines()) if term.lower() in l.lower()), "?")
            errors.append(f"命中敏感詞「{term}」（第 {line_no} 行）")
    for f in md.parent.iterdir():
        for term in terms:
            if term.lower() in f.name.lower():
                errors.append(f"檔名命中敏感詞「{term}」：{f.name}")

    return errors, warns


def collect(paths, check_all):
    files = []
    if check_all:
        files = sorted((ROOT / "content").glob("*/*/*/index.md"))
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files.append(p / "index.md")
        else:
            files.append(p)
    return files


def main():
    ap = argparse.ArgumentParser(description="發布前檢查")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--terms", help="敏感詞清單路徑（每行一個詞，# 開頭為註解）")
    ap.add_argument("--all", action="store_true", help="檢查 content/ 下所有文章")
    args = ap.parse_args()

    terms = load_terms(args.terms)
    if not args.terms:
        print("WARN   未指定 --terms，本次沒有做敏感詞檢查")
    files = collect(args.paths, args.all)
    if not files:
        print("沒有要檢查的文章")
        return 0

    total_err = 0
    for md in files:
        if not md.exists():
            print(f"ERROR  找不到檔案：{md}")
            total_err += 1
            continue
        errors, warns = check_file(md, terms)
        status = "FAIL" if errors else "OK"
        try:
            shown = md.resolve().relative_to(ROOT)
        except ValueError:
            shown = md
        print(f"[{status}] {shown}")
        for e in errors:
            print(f"  ERROR  {e}")
        for w in warns:
            print(f"  WARN   {w}")
        total_err += len(errors)

    print(f"\n檢查 {len(files)} 篇，ERROR {total_err} 項")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
