# Personal_Website — Agent 工作規則

這份檔案是 Claude Code 在本專案工作時必須遵守的規則。
本專案是個人公開網站（Hugo + PaperMod，發布到 GitHub Pages）。
**這是公開儲存庫：任何推送到 GitHub 的內容都視為已公開，且會永久留在 Git 歷史中。**

## 1. 路徑

| 用途 | 路徑 |
|---|---|
| 網站專案（本儲存庫） | `D:/Personal_Website` |
| 收件匣（待整理稿件，不在儲存庫內） | `D:/Website_Inbox` |
| 已處理的原稿 | `D:/Website_Inbox/_processed/YYYY-MM-DD/` |
| 暫緩發布的原稿 | `D:/Website_Inbox/_held/` |
| 敏感詞清單（不在儲存庫內） | `D:/Website_Inbox/_config/sensitive_terms.txt` |

敏感詞清單絕不可以複製、引用或摘錄到本儲存庫的任何檔案、commit 訊息或 PR 說明中。
回報命中結果時，只能在對話中告訴使用者，不能寫進會推送的內容。

## 2. 絕對禁止

1. 推送到 `main`，或合併任何 Pull Request。合併只由使用者在 GitHub 上操作。
2. `git push --force`、`git reset --hard`、改寫已推送的歷史。
3. 刪除 `content/`、`static/`、`themes/` 中既有的檔案（除非使用者在當次對話明確要求）。
4. 修改 `themes/PaperMod/` 內的任何檔案。樣式調整只能放在 `assets/css/extended/`，版面擴充只能放在 `layouts/`。
5. 改寫文章正文的內容與論述。允許的修改只有第 5 節列出的格式修正。
6. 把收件匣以外的檔案（例如研究主稿目錄）搬進網站，除非使用者明確指定。
7. 檢查有任何 ERROR 或 Hugo 建置失敗時，仍然 commit 或推送。
8. 自行翻譯文章並設為公開。翻譯只在使用者要求時進行，且一律 `draft: true`。

## 3. 內容結構

```
content/<語言>/<分類>/<網址名稱>/index.md   ← 每篇文章一個資料夾（Page Bundle）
content/<語言>/<分類>/<網址名稱>/*.png      ← 圖片與文章放在一起
```

- 語言：`zh-tw`（繁體中文，預設）或 `en`
- 分類：
  - `notes/` 研究札記：數學、物理、AI 的觀察、推導、計算，篇幅可長可短
  - `essays/` 觀點文章：完整論述的思想、方法論、評論，以文字論證為主
  - `publications/` 研究成果：已有或即將有 DOI／arXiv 的固定版本，網站只放介紹與連結
- 網址名稱：小寫英文、數字、連字號，例如 `tensor-rigidity`。發布後不可更改。
- 中英文翻譯版本使用相同的分類與網址名稱，Hugo 會自動連結兩者。

分類判斷不確定時，在報告中說明理由並請使用者確認，不要自行決定。

## 4. Front matter 規範（YAML）

```yaml
---
title: "文章標題"
date: 2026-10-19
lastmod: 2026-10-19          # 選填，修訂時更新
draft: false
tags: ["Tensor", "Geometry"]
summary: "一到兩句摘要。"
math: true                   # 內文有公式時必須為 true
# 以下僅 publications 使用
doi: ""
zenodo: ""
arxiv: ""
version: ""
---
```

- `tags` 一律使用英文，首字大寫，專有名詞照原寫法（例如 `MST-EUT`、`AI`）。優先沿用網站已有的 tags（用 `grep -rh "^tags:" content/` 查看）。
- `date` 用原稿中的日期；原稿沒有時用整理當天日期，並在報告中註明。
- `summary` 原稿沒有時，可以從內文擷取或濃縮一到兩句，並在報告中標示為「agent 草擬」。

## 5. 允許的格式修正

整理文章時只能做以下修改，而且每一項都要列在報告中：

- 補齊或修正 front matter 欄位
- 行內公式 `$...$` 改為 `\( ... \)`（本站不支援單一 `$`）
- 圖片路徑改為相對路徑，並把圖片複製到文章資料夾
- 圖片檔名改為小寫英文與連字號
- 移除原稿中第一個與 `title` 重複的 `# 標題`
- 原始 HTML 標籤改為等效的 Markdown（無法等效時保留並回報）

錯字、語句、論點、段落順序一律不改；發現疑似問題時在報告中提出建議即可。

## 6. 數學公式規範

- 行內：`\( ... \)`
- 獨立：`$$ ... $$` 或 `\[ ... \]`
- 不使用單一 `$ ... $`；一般文字中的 `$` 會被當作普通符號
- 有公式的文章 `math: true`

## 7. 檢查與建置指令

```bash
# 發布前檢查（Windows 若 python 無效，改用 py）
python tools/check_post.py <文章資料夾> --terms D:/Website_Inbox/_config/sensitive_terms.txt

# 建置檢查（必須無 ERROR）
hugo build --gc --minify -d D:/Website_Inbox/_build_check

# 本機預覽（含草稿）
hugo server -D
```

建置檢查輸出到收件匣下的 `_build_check`，不要在儲存庫內產生 `public/`。

## 8. Git 與發布流程

- 每次發布建立新分支：`publish/YYYYMMDD-<網址名稱>`；一次多篇時用 `publish/YYYYMMDD-batch`
- commit 訊息格式：`publish: <文章標題>` 或 `publish: N 篇文章`
- 推送分支後用 `gh pr create` 建立 PR，PR 說明附上第 9 節的報告（不含敏感詞內容）
- `gh` 不可用時，推送分支後停止，告訴使用者到 GitHub 手動建立 PR
- PR 建立後切回 `main`

## 9. 報告格式

每次整理完成後，以表格向使用者報告：

| 原稿 | 目的位置 | 語言 | 分類 | tags | draft | 檢查 |
|---|---|---|---|---|---|---|

接著列出：
- 每篇做了哪些格式修正（第 5 節）
- 哪些欄位是 agent 草擬的
- 檢查的 WARN 項目
- 需要使用者決定的事項

## 10. 常用指令

- `/publish-inbox`：整理收件匣並建立 Pull Request（詳見 `.claude/skills/publish-inbox/SKILL.md`）
