---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: true
tags: []
summary: ""
math: false
# 以下為選填欄位，確實存在時才取消註解填入（詳見 README.md「引用與版本欄位」）
# version: ""        # 版本，例如 "v0.4"
# doi: ""            # 已註冊的版本 DOI，格式 10.xxxx/...，填 Zenodo 給的真實值
# concept_doi: ""    # 已註冊的 concept DOI（所有版本），不可與 doi 相同
# zenodo: ""         # 真實的 https://zenodo.org/records/... 網址
# license: ""        # 作者決定後才填，例如 "CC BY 4.0"；未填即著作權保留
# license_url: ""    # 授權條款正式網址
# review_status: ""  # 研究狀態，例如 "Working draft, not peer-reviewed"
# pdf_url: ""        # 公開 PDF 網址，或同資料夾內的 PDF 檔名
---
