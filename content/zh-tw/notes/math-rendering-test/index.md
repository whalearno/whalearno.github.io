---
title: "數學公式顯示測試"
date: 2026-10-19
draft: false
tags: ["Test"]
summary: "確認行內與獨立公式、矩陣、對齊式在網站上正確顯示。測試完成後可刪除或改為 draft: true。"
math: true
---

這是一篇測試文章，用來確認公式在本機與線上都能正確顯示。

## 行內公式

黎曼 ζ 函數定義為 \( \zeta(s) = \sum_{n=1}^{\infty} n^{-s} \)，在 \( \operatorname{Re}(s) > 1 \) 時收斂。
含底線與星號的式子：\( a_{ij} * b_{jk} \)、\( x_1^2 + x_2^2 \)。

一般文字中的金額不應被當成公式：這本書售價 $30，運費 $5。

## 獨立公式（`$$ ... $$`）

$$
\zeta(s) = \prod_{p\ \text{prime}} \frac{1}{1 - p^{-s}}
$$

## 獨立公式（`\[ ... \]`）

\[
T_{ijk} = \sum_{a,b,c} \Lambda_{ia}\,\Lambda_{jb}\,\Lambda_{kc}\, T'_{abc}
\]

## 矩陣與對齊

$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{aligned}
$$

$$
A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix}
$$

## 程式碼區塊

```python
def zeta_partial(s, N=1000):
    return sum(n ** -s for n in range(1, N + 1))
```
