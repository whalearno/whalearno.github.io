---
name: publish-inbox
description: 整理 D:/Website_Inbox 收件匣中的 Markdown 稿件，放入網站正確位置、補齊格式、執行檢查與建置，然後建立發布分支與 Pull Request。只在使用者輸入 /publish-inbox 或明確要求發布收件匣時使用。
disable-model-invocation: true
---

# 發布收件匣

開始前先讀 `CLAUDE.md`，本流程中所有規則以它為準。
**任何步驟失敗都要停下來報告，不要跳過或繞過。**

## 步驟 0：環境檢查

1. 確認目前位於 `D:/Personal_Website`。
2. `git status`：工作目錄必須乾淨。不乾淨時列出變更並停止，請使用者處理。
3. `git checkout main && git pull`：確保是最新版本。
4. 確認 `hugo version` 可執行，並與 `README.md` 記錄的版本一致；不一致時提醒但可繼續。
5. 確認 `D:/Website_Inbox/_config/sensitive_terms.txt` 存在。不存在時停止。

## 步驟 1：盤點收件匣

列出 `D:/Website_Inbox/` 第一層的稿件，略過底線開頭的資料夾（`_config`、`_processed`、`_held`、`_build_check`）與 `README.md`。

稿件可能是：
- 單一 `.md` 檔
- 資料夾，內含一個 `.md` 檔與圖片等附件

收件匣是空的時，告訴使用者並結束。

## 步驟 2：逐篇判斷

讀取每篇稿件，決定：

| 項目 | 判斷方式 |
|---|---|
| 語言 | 原稿 front matter 有 `lang` 時照用；否則依正文主要語言判斷 |
| 分類 | 原稿有 `section` 時照用；否則依 `CLAUDE.md` 第 3 節判斷 |
| 網址名稱 | 原稿有 `slug` 時照用；否則依標題擬一個簡短英文名稱 |
| tags | 原稿有時照用（中文 tag 轉為英文）；否則建議 2～4 個，優先沿用網站既有 tags |
| draft | 原稿有時照用；沒有時預設 `false` |

檢查目的位置是否已存在同名文章：
- 已存在 → 視為**更新**既有文章。保留原 `date`，更新 `lastmod`，並在報告中明確標示「覆寫既有文章」。
- 同名但內容明顯是不同文章 → 停止該篇，請使用者另取網址名稱。

**先向使用者列出判斷結果表格（CLAUDE.md 第 9 節格式），等使用者確認或修改後才繼續。**
使用者不在場、無法確認時，到此停止，不要繼續後續步驟。

## 步驟 3：放置與格式整理

對每篇確認過的稿件：

1. 建立 `content/<語言>/<分類>/<網址名稱>/`。
2. 寫入 `index.md`：front matter 依 `CLAUDE.md` 第 4 節整理，移除 `lang`、`section`、`slug` 這三個收件匣專用欄位。
3. 只做 `CLAUDE.md` 第 5 節允許的格式修正，逐項記錄。
4. 複製圖片與附件到同一資料夾，修正引用路徑。原稿引用了找不到的圖片時，記錄並在報告中提出。

## 步驟 4：檢查

```bash
python tools/check_post.py <每篇的資料夾> --terms D:/Website_Inbox/_config/sensitive_terms.txt
```

- 有 ERROR：能用第 5 節允許的方式修正的就修正後重跑；不能修正的（例如命中敏感詞）把該篇移出本次發布（刪除剛建立的資料夾），原稿移到 `D:/Website_Inbox/_held/`，並在報告中說明原因。
- 命中敏感詞時，只在對話中告訴使用者命中哪個詞、在哪一行，不寫進任何會推送的內容。

## 步驟 5：建置

```bash
hugo build --gc --minify -d D:/Website_Inbox/_build_check
```

建置失敗時停止並回報錯誤訊息，不要 commit。
成功後提醒使用者可以執行 `hugo server -D` 在本機預覽。

## 步驟 6：最終確認

向使用者展示：
- 最終的判斷表格
- 每篇的格式修正清單與 agent 草擬欄位
- WARN 項目
- `git status` 與 `git diff --stat`

**詢問使用者是否建立發布分支與 Pull Request。得到明確同意後才進行步驟 7。**

## 步驟 7：建立分支與 Pull Request

```bash
git checkout -b publish/YYYYMMDD-<網址名稱或 batch>
git add content/
git commit -m "publish: <標題或 N 篇文章>"
git push -u origin <分支名稱>
gh pr create --base main --title "<同 commit 訊息>" --body "<報告，不含敏感詞>"
git checkout main
```

只 `git add` 本次新增或修改的文章資料夾，不要用 `git add .`。
`gh` 不可用或未登入時，推送分支後停止，告訴使用者到 GitHub 手動建立 PR。

## 步驟 8：收尾

1. 已發布的原稿移到 `D:/Website_Inbox/_processed/YYYY-MM-DD/`（不是刪除）。
2. 刪除 `D:/Website_Inbox/_build_check/`。
3. 告訴使用者：PR 的連結；GitHub 上的建置檢查通過後，在 GitHub 上按 Merge 即會發布；發布約需 1～2 分鐘。
