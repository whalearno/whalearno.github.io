# Personal_Website

個人研究札記與觀點網站。Hugo + PaperMod，發布到 GitHub Pages。

## 版本記錄

| 元件 | 版本 | 備註 |
|---|---|---|
| Hugo Extended | 0.168.0 | 本機與 `.github/workflows/*.yaml` 必須一致 |
| PaperMod | commit `969bebdc5600a1639158b5ef4eff9cf6cbb511ac`（2026-10-18） | 完整放在 `themes/PaperMod/`，要求 Hugo ≥ 0.158.0 |
| KaTeX | 0.16.11 | 由 `layouts/_partials/extend_head.html` 從 CDN 載入 |

升級任何一項時：先在本機改版本、`hugo server` 確認無誤，再同時更新本表與 workflow 中的 `HUGO_VERSION`。

## 目錄

```
content/zh-tw/   繁體中文（網站根目錄）
content/en/      English（/en/）
  notes/         研究札記
  essays/        觀點文章
  publications/  研究成果（DOI、Zenodo、arXiv）
archetypes/      新文章樣板
layouts/_partials/extend_head.html   數學公式（KaTeX）
assets/css/extended/custom.css       少量樣式調整
tools/check_post.py                  發布前檢查
CLAUDE.md                            Agent 工作規則
.claude/skills/publish-inbox/        /publish-inbox 流程
```

## 首次設定（Windows）

1. 安裝工具（PowerShell）：
   ```
   winget install Git.Git
   winget install Hugo.Hugo.Extended
   winget install GitHub.cli
   winget install Python.Python.3.12
   ```
   安裝後重開終端機，確認 `hugo version` 顯示 `0.168.0` 與 `extended`。
   winget 裝到不同版本時，從 https://github.com/gohugoio/hugo/releases/tag/v0.168.0 下載 `hugo_extended_0.168.0_windows-amd64.zip`。
2. 把 `Personal_Website` 放在 `D:/Personal_Website`，`Website_Inbox` 放在 `D:/Website_Inbox`。兩者都不要放在 OneDrive 等同步資料夾內。
3. 修改 `hugo.toml` 中的 `USERNAME`（兩處）與網站名稱。
4. 本機預覽：
   ```
   cd D:/Personal_Website
   hugo server -D
   ```
   打開 http://localhost:1313 ，確認「數學公式顯示測試」一文正常。
5. 建立 GitHub 儲存庫 `<帳號>.github.io`（Public，不要勾選新增 README）。
6. 第一次推送：
   ```
   git init -b main
   git add .
   git commit -m "init: website skeleton"
   git remote add origin https://github.com/<帳號>/<帳號>.github.io.git
   git push -u origin main
   ```
7. GitHub 儲存庫 → Settings → Pages → Source 選 **GitHub Actions**。
8. Actions 頁面出現綠色勾勾後，打開 `https://<帳號>.github.io/` 確認。
9. 登入 GitHub CLI（給 agent 建立 PR 用）：`gh auth login`
10. 建議：Settings → Branches → 為 `main` 新增保護規則，勾選「Require a pull request before merging」與「Require status checks to pass」（選 PR build check）。設定後所有變更都需經過 PR，包括你自己的。

## 日常發布

**用 agent：**
1. 把寫好的 Markdown（或含圖片的資料夾）放進 `D:/Website_Inbox/`。
2. 在 `D:/Personal_Website` 開啟 Claude Code，輸入 `/publish-inbox`。
3. 確認 agent 列出的分類與 tags，同意後它會建立 Pull Request。
4. 到 GitHub 檢查 PR 內容，建置檢查通過後按 Merge，約 1～2 分鐘後上線。

**手動：**
```
hugo new content notes/my-note/index.md               # 中文札記（預設語言）
hugo new content content/en/notes/my-note/index.md    # 英文需寫完整路徑
python tools/check_post.py content/zh-tw/notes/my-note --terms D:/Website_Inbox/_config/sensitive_terms.txt
```
設有分支保護時，手動發布也要開分支與 PR。

## 撰寫規範

- 行內公式 `\( ... \)`；獨立公式 `$$ ... $$` 或 `\[ ... \]`；不使用單一 `$`
- 有公式的文章設 `math: true`
- tags 用英文
- 網址名稱（資料夾名）用小寫英文與連字號，發布後不改
- 不使用 HTML 標籤（`hugo.toml` 設定為不顯示原始 HTML）
- `draft: true` 不會發布，但**原始檔在公開儲存庫中仍看得到**；不想公開的草稿不要放進本專案

## 測試完成後

「數學公式顯示測試」（`content/zh-tw/notes/math-rendering-test/`）只用於確認公式顯示，正式經營前可刪除或改為 `draft: true`。
