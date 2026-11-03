---
title: "從矩陣指數到非線性函數：傅立葉、雙曲變換與神經學習的共同作用結構"
date: 2026-11-02
lastmod: 2026-11-03
draft: false
tags: ["Matrix Exponential", "Fourier Analysis", "Projective Dynamics", "Neural Networks"]
summary: "由自然指數與矩陣生成元出發，把圓周旋轉、雙曲變換與冪零剪切放進同一條推導，說明線性矩陣流如何經射影讀出呈現 tanh 等非線性函數，並以傅立葉分析與神經學習作為對照，同時標明這些比較的適用界線。"
math: true
---

## ——從圓周模態、線性生成元到射影表示與張量作用


## 摘要

傅立葉級數可以把許多簡單的圓周運動組合成複雜曲線；神經網路也能利用簡單的函數單元組合出豐富的輸入—輸出關係。這兩種現象帶出一個共同問題：一個函數的形狀與複雜性，究竟有多少來自基本作用，有多少來自作用的組合與表示方式？

本文從指數函數作為線性微分方程的解開始，導出矩陣指數 \( e^{tA} \)，以 \( A_\varepsilon^2=\varepsilon I \)（\( \varepsilon=-1,0,+1 \)）的二維生成元，比較圓周旋轉、冪零剪切與雙曲變換。接著觀察軌跡分量之比 \( r=Y/X \)，推導出 \( \dot r=1-\varepsilon r^2 \)，說明線性演化為何在射影座標中呈現 \( \tan t \)、\( t \) 與 \( \tanh t \)。傅立葉模態、Lorentz boost、Logistic 函數與 `tanh` 神經單元在這條推導中分別提供不同的數學觀察窗口。最後再以張量積的誘導生成元、高階導數外積及簡要的梯度更新，辨認維度、張量階數、函數表示與學習動力學之間的關係。

本札記以可逐步驗算的既有數學結果，建立一條跨領域的理解路徑；其核心是**生成元、表示、射影與組合如何改變我們所看到的函數結構**。讀者只需熟悉基本的函數、矩陣乘法與微分；文中的「生成元」會從微分方程引入，「射影」會從斜率 \( Y/X \) 說起，而「張量積」則從兩個向量分量的乘積理解。

---

## 1. 從兩種熟悉的函數組合出發

### 1.1 為什麼圓周運動能畫出複雜曲線？

平面上一個半徑為 \( R \)、角速度為 \( \omega \) 的圓周運動，可以寫成

$$
(x(t),y(t))=(R\cos\omega t,R\sin\omega t).
$$

用複數合併兩個座標，便得到

$$
z(t)=x(t)+iy(t)=Re^{i\omega t}.
\tag{1.1}
$$

現在讓多個旋轉向量的終點首尾相接。若第 \( n \) 個向量有自己的幅度與相位，合成位置就是

$$
z_N(t)=\sum_{n=-N}^{N}c_ne^{int}.
\tag{1.2}
$$

每個單元都只是等速旋轉，合成軌跡卻可以形成細緻的輪廓。複數係數 \( c_n \) 的絕對值決定旋轉向量的長度，幅角決定初始方向；正負整數 \( n \) 則表示相反的旋轉方向。這裡的 \( t \) 是沿著曲線移動的參數，對閉合圖形可自然取為一個週期。對週期平方可積函數，這些傅立葉部分和在均方意義下逼近原函數；對足夠光滑的曲線，可得到更強的收斂性質。若有尖角或不連續的週期接縫，往往需要更多高頻項。

這裡的關鍵並不是「圓周本身很複雜」，而是**簡單模態的組合係數可以承載複雜的形狀資訊**。

### 1.2 一個不同的例子：`tanh` 函數單元

單隱藏層神經網路可以表示為

$$
f_N(\mathbf x)=\sum_{a=1}^{m}v_a\tanh(\mathbf w_a\cdot\mathbf x+b_a)+c.
\tag{1.3}
$$

每一個 `tanh` 單元先用權重選擇輸入方向與尺度，再產生一條平滑的 S 型轉折；許多單元相加，可以組合出複雜的函數形狀。這與傅立葉疊加共享「基本函數加權組合」的形式，但兩者差別同樣明顯：傅立葉使用預先指定的週期頻率，神經網路則能調整 \( \mathbf w_a \)、\( b_a \) 與 \( v_a \)。對適當的緊緻定義域，具有非多項式激活函數的單隱藏層網路具有熟知的普遍逼近結果。[1–3]

兩個例子引導我們回到一個更基本的問題：**為什麼三角函數與雙曲函數都和自然指數密切相關？** 若能先理解指數函數所描述的作用，再觀察不同讀出方式，這兩種函數表示的關係就會清楚許多。

## 2. 從自然指數到矩陣指數：線性作用如何生成

### 2.1 指數函數是最簡單的連續演化解

考慮一個純量隨參數 \( t \) 演化，變化率與當前數值成正比：

$$
\frac{dz}{dt}=az,\qquad z(0)=z_0.
$$

它的解是 \( z(t)=e^{at}z_0 \)。原因在於 \( \frac{d}{dt}e^{at}=ae^{at} \)；更重要的是，時間分段相加對應作用相乘：

$$
e^{a(t+s)}=e^{at}e^{as}.
\tag{2.1}
$$

若狀態不只有一個數，而是向量 \( \mathbf z(t) \)，將常數 \( a \) 換成線性算子（矩陣）\( A \)：

$$
\frac{d\mathbf z}{dt}=A\mathbf z,\qquad \mathbf z(0)=\mathbf z_0.
\tag{2.2}
$$

矩陣指數由冪級數定義：

$$
e^{tA}=I+tA+\frac{t^2A^2}{2!}+\frac{t^3A^3}{3!}+\cdots.
\tag{2.3}
$$

逐項微分得到 \( \frac{d}{dt}e^{tA}=Ae^{tA} \)，所以

$$
\boxed{\mathbf z(t)=e^{tA}\mathbf z_0.}
\tag{2.4}
$$

對固定 \( A \)，仍有 \( e^{(t+s)A}=e^{tA}e^{sA} \)。因此 \( A \) 是這一族連續線性變換的**生成元**；\( e^{tA} \) 則是由它生成的有限變換。這一點讓我們可以先研究簡單的代數關係，再看它產生什麼函數與幾何。矩陣指數及線性微分系統的標準推導可參考文獻 [8, 9]。

### 2.2 三種二維生成元，只差一個平方關係

選擇一族特別簡單的矩陣：

$$
A_\varepsilon=\begin{pmatrix}0&\varepsilon\\1&0\end{pmatrix},
\qquad A_\varepsilon^2=\varepsilon I,
\qquad \varepsilon\in\{-1,0,+1\}.
\tag{2.5}
$$

因為偶數冪變成 \( \varepsilon^nI \)，奇數冪變成 \( \varepsilon^nA_\varepsilon \)，矩陣指數可按偶、奇冪分組：

$$
e^{tA_\varepsilon}=C_\varepsilon(t)I+S_\varepsilon(t)A_\varepsilon
=\begin{pmatrix}C_\varepsilon(t)&\varepsilon S_\varepsilon(t)\\S_\varepsilon(t)&C_\varepsilon(t)\end{pmatrix}.
\tag{2.6}
$$

| \( \varepsilon \) | \( C_\varepsilon(t) \) | \( S_\varepsilon(t) \) | 矩陣作用的樣貌 |
|---:|---|---|---|
| \( -1 \) | \( \cos t \) | \( \sin t \) | 圓周旋轉（橢圓型） |
| \( 0 \) | \( 1 \) | \( t \) | 剪切（冪零／拋物型） |
| \( +1 \) | \( \cosh t \) | \( \sinh t \) | 雙曲變換（雙曲型） |

例如 \( \varepsilon=-1 \) 時，\( A^2=-I \) 讓偶數冪交替出現正負號，因此產生 \( \cos t \) 與 \( \sin t \)；\( \varepsilon=+1 \) 時，偶數冪沒有交替符號，因此產生 \( \cosh t \) 與 \( \sinh t \)。這正是 Euler 公式 \( e^{it}=\cos t+i\sin t \) 在實二維矩陣中的對應結構。

從純量指數來看，這裡還有一個容易被忽略的連結。三角函數與雙曲函數分別可由含虛數與實數的指數組合而成：

$$
\cos t=\frac{e^{it}+e^{-it}}{2},\qquad
\cosh t=\frac{e^t+e^{-t}}{2}.
$$

把變數延伸到複數，就有

$$
\boxed{\cos t=\cosh(it),\qquad
\sin t=-i\sinh(it),\qquad
\tanh(it)=i\tan t.}
$$

因此，兩類函數可以透過**解析延拓**聯繫：在公式中把實參數換成虛參數，可以從雙曲函數走到三角函數。然而，在實數二維空間中，\( A_{-1}^2=-I \) 與 \( A_{+1}^2=I \) 仍對應不同的實矩陣流；前者保持圓周型二次式，後者保持雙曲型二次式。解析公式彼此連通，不等於兩種實幾何作用沒有差別。

### 2.3 不變量使幾何性質變得可見

讓三種矩陣流作用於同一個初始向量：

$$
\begin{pmatrix}X(t)\\Y(t)\end{pmatrix}
=e^{tA_\varepsilon}\begin{pmatrix}1\\0\end{pmatrix}
=\begin{pmatrix}C_\varepsilon(t)\\S_\varepsilon(t)\end{pmatrix}.
\tag{2.7}
$$

由生成元直接讀出：

$$
\dot X=\varepsilon Y,\qquad \dot Y=X.
\tag{2.8}
$$

因此

$$
\frac{d}{dt}(X^2-\varepsilon Y^2)
=2X(\varepsilon Y)-2\varepsilon YX=0.
$$

配合初值，得到

$$
\boxed{X^2-\varepsilon Y^2=1.}
\tag{2.9}
$$

\( \varepsilon=-1 \) 是單位圓，\( \varepsilon=0 \) 是直線 \( X=1 \)，\( \varepsilon=+1 \) 則是雙曲線右支。幾何軌跡的差異，就這樣由生成元平方關係與同一個初始條件導出。三個生成元都具有零跡，所生成的矩陣行列式均為 \( 1 \)，亦可視為 \( SL(2,\mathbb R) \) 單參數子群的基本例子。

## 3. 讓二維線性流變成非線性函數：射影讀出

### 3.1 為什麼要看 \( Y/X \)？

沿著上一節的軌跡，現在改問另一件事：**從原點望向運動中的點 \( (X,Y) \)，這條直線的斜率是多少？**

只要 \( X\ne0 \)，斜率便是

$$
\boxed{r(t)=\frac{Y(t)}{X(t)}.}
\tag{3.1}
$$

把經過原點與 \( (X,Y) \) 的整條直線延伸到 \( X=1 \)，交點是 \( (1,r) \)。這就是射影座標的一個具體幾何圖像。因為從原點望向 \( (X,Y) \)，即使把兩個座標同時乘上非零常數，視線方向也不變；射影表示保留的是「方向」，不再分別記錄兩個分量的大小。這裡用的是**視線直線的斜率**，而非曲線本身的切線斜率。若 \( X=0 \)，此座標暫時失效，可改用另一張射影座標圖。

![圖 1：圓周、直線與雙曲流及其射影讀出](figure-01-generator-flows-projective-readouts.png)

*圖 1．三種矩陣指數流的平面軌跡（上排）及斜率函數 \( r=Y/X \)（下排）。同一個初始條件，經不同生成元得到圓周、直線與雙曲線；射影後分別得到 \( \tan t \)、\( t \) 與 \( \tanh t \)。圖中示意的是原點連線的射影斜率，不是軌跡切線。*

### 3.2 一次商數微分，得到三種非線性方程

利用式 (2.8)，對 \( r=Y/X \) 求導：

$$
\begin{aligned}
\dot r
&=\frac{X\dot Y-Y\dot X}{X^2}\\
&=\frac{X^2-\varepsilon Y^2}{X^2}\\
&=1-\varepsilon r^2.
\end{aligned}
\tag{3.2}
$$

所以：

$$
\boxed{
\begin{array}{c|c|c}
\varepsilon&r(t)&\dot r\\\hline
-1&\tan t&1+r^2\\
0&t&1\\
+1&\tanh t&1-r^2
\end{array}}
\tag{3.3}
$$

原來只要改變線性生成元的平方關係，便會在比值座標中形成三種不同函數。底層的 \( (X,Y) \) 仍滿足**線性**微分方程；所看到的非線性，則來自對分量取比值的表示方式。\( \tan t \) 的極點對應 \( X=0 \)，是這張座標圖的邊界，而非圓周軌跡在平面中爆炸。相對地，雙曲支線上的 \( X(t)=\cosh t\ge1 \) 對所有實數 \( t \) 都不為零，因此 \( \tanh t=Y/X \) 在整條實數軸上都可使用，而且 \( |\tanh t|<1 \)。這個**沒有實極點、輸出有界**的特性，是 `tanh` 適合作為平滑激活函數的理由之一；它也帶來飽和區域梯度變小的另一面，後文 §9 再討論。從 §2.2 的複數解析延拓再往前看，\( \tanh z \) 的極點位於 \( z=i(\pi/2+n\pi) \)（\( n \) 為整數），都在虛軸上；而 \( \tan z \) 的極點位於 \( z=\pi/2+n\pi \)。這讓「實軸上無極點」與兩類函數的解析關係相互呼應。

### 3.3 一般矩陣流與 Riccati 方程

這種現象可以直接推廣。設

$$
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\qquad
\begin{pmatrix}\dot X\\\dot Y\end{pmatrix}=A\begin{pmatrix}X\\Y\end{pmatrix}.
$$

同樣對 \( Y/X \) 求導，得到

$$
\boxed{\dot r=c+(d-a)r-br^2.}
\tag{3.4}
$$

這是 Riccati 型方程。換句話說，**二維線性流在射影直線上的作用，天然給出一類二次非線性方程**。Riccati 微分方程的專門背景可參考 Reid [10]；本文的射影化公式則已由上面的商數微分直接推得。

三種基本函數的參數合成還遵守同一個形式：

$$
\boxed{r(t+s)=\frac{r(t)+r(s)}{1+\varepsilon r(t)r(s)}.}
\tag{3.5}
$$

\( \varepsilon=-1 \)、\( 0 \)、\( +1 \) 分別給出正切加法、普通加法與雙曲正切加法；所有式子均需在所用分母非零的座標區域內理解。

## 4. 同一個雙曲生成元，可以有不同的數學讀法

### 4.1 從 `tanh` 到 Logistic

對 \( \varepsilon=+1 \) 的雙曲流，令 \( K=A_{+1} \)。作用於 \( (1,0)^T \) 後，

$$
(X,Y)=(\cosh u,\sinh u),\qquad \frac{Y}{X}=\tanh u.
\tag{4.1}
$$

神經網路常見的 Logistic 函數與 `tanh` 有精確的仿射關係：

$$
\boxed{\sigma(u)=\frac{1}{1+e^{-u}}=\frac{1+\tanh(u/2)}{2}.}
\tag{4.2}
$$

這個式子可以從同一雙曲流的**本徵座標**理解：在對角化的座標中，兩個獨立分量分別按 \( e^{-u/2} \) 與 \( e^{u/2} \) 伸縮。令 \( z_-(u)=e^{-u/2} \)、\( z_+(u)=e^{u/2} \)，再把這兩個正分量的總和正規化為 \( 1 \)：

$$
\sigma(u)=\frac{z_+(u)}{z_-(u)+z_+(u)},
\qquad \boxed{\sigma'(u)=\sigma(u)[1-\sigma(u)]}.
\tag{4.3}
$$

`Sigmoid` 的輸出區間是 \( (0,1) \)，`tanh` 的輸出區間是 \( (-1,1) \)；兩者可理解為雙曲指數作用在不同射影／正規化座標中的表示，參數尺度相差一個因子 \( 2 \)。這也說明，選擇何種讀出座標，會改變不動點在數軸上的位置：前者在 \( 0,1 \)，後者在 \( -1,1 \)。

### 4.2 Lorentz boost：保存二次型的線性讀法

同一雙曲生成元，在 \( (1+1) \) 維 Minkowski 度規中也有一個熟悉的身分。令

$$
K=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
\eta=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
\Lambda(u)=e^{uK}
=\begin{pmatrix}\cosh u&\sinh u\\\sinh u&\cosh u\end{pmatrix}.
$$

因 \( K^T\eta+\eta K=0 \)，便有

$$
\boxed{\Lambda(u)^T\eta\Lambda(u)=\eta.}
\tag{4.4}
$$

這是以快度 \( u \) 參數化的一維 Lorentz boost（正負方向由慣例決定）。當我們觀察完整矩陣的作用時，看到的是**二次型不變性**；當我們取演化向量的分量比值時，看到的是 **`tanh` 射影函數**。它們共同使用雙曲生成元，卻回答不同的數學問題。

例如預激活參數增加 \( s \)，有

$$
\boxed{\tanh(u+s)=\frac{\tanh u+\tanh s}{1+\tanh u\,\tanh s}.}
\tag{4.5}
$$

這與一維相對論速度合成具有相同的分式線性形式。對一般神經單元而言，\( u \) 只是實數預激活量；這個對照使用的是共同代數結構，不需要替神經輸入賦予物理快度。

## 5. 當作用對象是張量：生成元如何自然升階

前面討論的 \( e^{tA} \) 作用於一個向量，例如二維狀態 \( (X,Y) \)。現在考慮兩個向量的張量積 \( v\otimes w \)。它可以理解為一張由分量乘積 \( v^i w^j \) 排成的表，保留兩個向量之間的雙線性關係；這與把原始平面由二維改成四維物理空間是兩回事。

若我們要觀察**同一個線性作用如何作用在多個張量槽位上**，只需要從最熟悉的乘積微分法則開始。

假設兩個向量各自遵守

$$
\dot v=Av,\qquad\dot w=Aw.
$$

則張量積的導數是

$$
\begin{aligned}
\frac{d}{dt}(v\otimes w)
&=\dot v\otimes w+v\otimes\dot w\\
&=(A\otimes I+I\otimes A)(v\otimes w).
\end{aligned}
\tag{5.1}
$$

因此二階張量積上的生成元是

$$
\boxed{A^{(2)}=A\otimes I+I\otimes A,\qquad
 e^{tA^{(2)}}=e^{tA}\otimes e^{tA}.}
\tag{5.2}
$$

![圖 2：張量積與 Leibniz 法則](figure-02-tensor-product-leibniz-generator.png)

*圖 2．乘積微分法則在張量積上的直接表現：生成元 \( A \) 分別作用於兩個槽位，再將貢獻相加，形成 \( A\otimes I+I\otimes A \)。*

對 \( p \) 個逆變張量槽位，同樣得到

$$
\boxed{A^{(p)}=\sum_{j=1}^{p}I^{\otimes(j-1)}\otimes A\otimes I^{\otimes(p-j)}.}
\tag{5.3}
$$

例如二階逆變張量的分量轉換是 \( T'^{ij}=\Lambda^i{}_{\alpha}\Lambda^j{}_{\beta}T^{\alpha\beta} \)。協變指標則要使用對偶作用；若改變座標或度規，也需按張量類型作適當處理。

這裡可清楚區分：底層向量空間維度 \( d \)、張量階數 \( p \) 與完整張量積空間維度 \( d^p \) 並不是同一個概念。**增加張量階數，改變的是多線性作用的槽位數，不是把原本的幾何空間強行增加維度。**

本節的 \( A^{(p)} \) 作用於**狀態空間的張量積**（例如本篇二維流的 \( V^{\otimes p} \)）。後面 §7 還會出現 \( q^{\otimes p} \)：那是函數對**輸入變數**求 \( p \) 階導數後，屬於輸入空間對偶的對稱張量。這兩者的空間與用途不同；它們的接點是「由矩陣流產生純量函數，再用鏈式法則對輸入求導」，而不是把兩種張量直接視為相等。

## 6. 回到傅立葉：旋轉生成元為什麼適合表示平移？

由式 (2.5) 的 \( \varepsilon=-1 \)，令

$$
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad J^2=-I.
$$

它的矩陣指數就是二維旋轉矩陣：

$$
e^{\theta J}=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}.
\tag{6.1}
$$

若將平面視為複數平面，同一作用可寫為 \( e^{i\theta} \)。這讓 Fourier 模態 \( e^{ikx} \) 具有一項特別簡潔的性質：平移 \( x\mapsto x+a \)，只會帶來相位因子

$$
e^{ik(x+a)}=e^{ika}e^{ikx}.
\tag{6.2}
$$

因此，若定義平移算子 \( \mathsf T_a f(x)=f(x+a) \)，傅立葉模態便是它的**本徵函數**，本徵值為 \( e^{ika} \)：平移輸入只改變複數相位。同樣是把自變量平移 \( a \)，第 4 節的 `tanh` 卻給出另一種形式。這兩種表示可以直接並排觀察：

| 同一件事：\( x\mapsto x+a \) | 傅立葉模態 \( z=e^{ikx} \) | 雙曲射影座標 \( r=\tanh x \) |
|---|---|---|
| 平移後的值 | \( z'=e^{ika}z \) | \( r'=\dfrac{r+\tanh a}{1+r\tanh a} \) |
| 作用形式 | 複數平面中的相位旋轉 | 射影直線上的 Möbius 變換 |
| 參數如何合成 | 相位角 \( ka \) 可相加 | 雙曲參數 \( a \) 可相加 |

兩者都把**實數加法的平移參數**表成一族可連續合成的作用：一者作用於複數振幅，一者作用於射影比值。共同之處是合成律，不是說旋轉與雙曲射影是同一個實線性變換。

傅立葉分析正是利用這些模態，將函數拆為不同頻率的合成。在 \( d \) 維空間，採用轉換慣例

$$
\widehat f(\mathbf k)=\int_{\mathbb R^d}f(\mathbf x)e^{-ik_i x^i}\,d^dx,
\qquad
f(\mathbf x)=\frac{1}{(2\pi)^d}\int_{\mathbb R^d}\widehat f(\mathbf k)e^{ik_i x^i}\,d^dk.
\tag{6.3}
$$

其中 \( k_i x^i \) 是向量與對偶向量的縮併。此處先假設 \( f \) 足夠規則，讓積分與反演有通常的意義；更一般的 \( L^2 \) 或分布情形需採用對應的函數空間架構。

使用核 \( \mathcal K(\mathbf k,\mathbf x)=e^{-ik_i x^i} \)，傅立葉轉換是一個線性積分算子；離散後可表示成 \( \widehat f_m=F_m{}^nf_n \)。更有用的是，在適當邊界與正則條件下：

$$
\boxed{\mathcal F[\partial_i f]=ik_i\widehat f,\qquad
\mathcal F[\partial_i\partial_j f]=-k_i k_j\widehat f.}
\tag{6.4}
$$

所以原本的微分作用，在頻域可轉為頻率向量的乘法與外積。這也說明了傅立葉方法在平移對稱線性微分問題中為何特別有效；若原問題含非線性乘積，頻域一般會出現卷積與模態耦合。

## 7. 函數單元的共同張量骨架

現在將傅立葉模態與 `tanh` 單元放到同一個表示形式中。先設輸入向量 \( \mathbf x \) 屬於 \( E=\mathbb R^d \)，再由每個對偶向量 \( q_a \) 選出一個純量輸入 \( u_a \)：

$$
\boxed{f(\mathbf x)=\sum_{a}c_a\phi_a(u_a),\qquad
u_a=q_{ai}x^i+b_a.}
\tag{7.1}
$$

這時才適合銜接 §5 的兩種張量：§5 的 \( A^{(p)} \) 作用在**狀態空間** \( V \) 的張量積；本節對 \( \mathbf x \) 求導，則產生**輸入空間** \( E \) 上的導數張量。若選擇 \( \phi_a(u_a)=\tanh u_a \)，函數便可依序理解為 \( \mathbf x\to u_a\to(X(u_a),Y(u_a))\to Y(u_a)/X(u_a) \)。矩陣流先提供純量函數，鏈式法則再描述它對輸入的敏感程度。兩種張量由此串接，卻不是同一個對象。

\( \phi_a \) 可以是複數指數、正弦、雙曲正切或其他足夠可微的純量函數。先把輸入沿 \( q_a \) 方向縮併為一個純量，再施加函數映射，最後加權求和。這類結構在函數逼近文獻中與 *ridge functions*（嶺函數）密切相關。[2,4]

由鏈式法則，一階導數是

$$
\partial_i f=\sum_a c_a\phi_a'(u_a)q_{ai},
$$

二階導數（Hessian，描述各個輸入方向的斜率如何改變）則是

$$
\boxed{\partial_i\partial_j f=\sum_a c_a\phi_a''(u_a)q_{ai}q_{aj}.}
\tag{7.2}
$$

所以單一單元對 Hessian 的貢獻，是一個純量係數乘上 \( q_a\otimes q_a \)，其矩陣秩至多為一。繼續微分可得到

$$
\boxed{\partial_{i_1}\cdots\partial_{i_p}f
=\sum_a c_a\phi_a^{(p)}(u_a)
q_{ai_1}\cdots q_{ai_p}.}
\tag{7.3}
$$

這裡 \( q_{ai_1}\cdots q_{ai_p} \) 是輸入空間對偶 \( E^* \) 的 \( p \) 階對稱張量分量。它與 §5 的誘導生成元 \( A^{(p)} \) 不同：前者記錄函數對輸入方向的敏感程度，後者記錄線性變換如何同時作用於多個張量槽位。

更有趣的是，**共同的外積骨架之外，兩類函數各有自己的導數代數**。對 Fourier 單元 \( \phi(u)=e^{iu} \)：

$$
\phi^{(p)}(u)=i^p\phi(u).
$$

一次微分只乘上 \( i \)，因此指數模態對微分作用具有本徵函數性質。對 `tanh`，令 \( h=\tanh u \)，§3 已經給出 \( h'=1-h^2 \)，接著利用鏈式法則：

$$
\begin{aligned}
h''&=-2h(1-h^2),\\
h^{(3)}&=-2(1-h^2)(1-3h^2).
\end{aligned}
$$

每次微分之後仍是 \( h \) 的多項式。若定義 \( P_0(h)=h \)，便可用下列規則逐階計算：

$$
\boxed{P_{p+1}(h)=(1-h^2)\frac{dP_p(h)}{dh},\qquad
\frac{d^p}{du^p}\tanh u=P_p(\tanh u).}
$$

所以傅立葉模態的導數是「**固定模態乘上常數**」，而 `tanh` 的導數是「**由 Riccati 關係封閉生成的多項式**」。兩者都能套用式 (7.3)，但它們如何改變外積前的係數，具有明確差別。這裡所說的封閉，是指多項式代數在這個微分規則下封閉，並不表示所有導數張成固定有限維的線性空間。

應同時分清：輸入維度 \( d \) 是 \( \mathbf x \) 的分量數，張量階數 \( p \) 是導數指標數，單元數 \( m \) 是求和項數。這是在固定仿射座標、常數權重與單層函數合成下的明確結果；多層函數複合或協變微分則需要完整的鏈式法則與相關連接項，不能只沿用式 (7.3)。

## 8. 一個有趣的來回轉換：`tanh` 也有傅立葉表示

`tanh` 是奇函數，對實數 \( x \) 有精確的正弦積分表示：

$$
\boxed{\tanh x=\int_0^\infty\frac{\sin(\omega x)}{\sinh(\pi\omega/2)}\,d\omega.}
\tag{8.1}
$$

這不是把 `tanh` 變成另一個物理機制，而是在另一組函數表示中描述相同的曲線。推導可以先從可積分的導數開始：

$$
\frac{d}{dx}\tanh x=\operatorname{sech}^2x,\qquad
\mathcal F[\operatorname{sech}^2x](\omega)=\frac{\pi\omega}{\sinh(\pi\omega/2)}.
\tag{8.2}
$$

由傅立葉反演再對 \( x \) 積分，便得到式 (8.1)；其正規化係數在附錄 B 核對。平滑轉折的導數具有快速衰減的高頻成分，而把有限區間上的 `tanh` **直接週期延拓**，會在端點形成跳躍，產生較慢衰減的傅立葉係數與 Gibbs 現象。

這個例子清楚提醒我們：**頻譜不只與函數形狀有關，也與定義域、邊界接續方式和分析對象（函數本身或導數）有關。**

## 9. 從函數導數到參數更新：神經學習中的張量例子

回到式 (1.3)，單一神經元的預激活量可寫成 \( u^a=W^a{}_ix^i+b^a \)，輸出是 \( h^a=\tanh u^a \)。從射影方程 (3.2) 立即得到

$$
\boxed{\frac{dh^a}{du^a}=1-(h^a)^2=\operatorname{sech}^2u^a.}
\tag{9.1}
$$

\( |u^a| \) 很大時，導數趨近零，這是 `tanh` 飽和所造成的局部梯度抑制。若令 \( y=v_ah^a+c \)、單筆平方損失 \( L=\tfrac12(y-y_\ast)^2 \)，則

$$
\frac{\partial L}{\partial W^a{}_i}
=(y-y_\ast)v_a[1-(h^a)^2]x^i.
\tag{9.2}
$$

將前面的係數記為 \( \delta_a \)，便得到

$$
\boxed{\nabla_W L=\boldsymbol\delta\otimes\mathbf x.}
\tag{9.3}
$$

對一筆資料，權重梯度矩陣是秩至多為一的外積；小批次時則為外積之和。這讓「參數學習」也呈現了可直接辨認的張量結構。

若以連續梯度流 \( \dot\theta=-\nabla_\theta L \) 描述理想化學習，則

$$
\boxed{\frac{dL}{dt}=-\|\nabla_\theta L\|^2\le0.}
\tag{9.4}
$$

它是損失沿梯度流的下降關係。更深入的 NTK、頻譜偏向與特徵學習問題，可以另外研究；附錄 C 只列出通往這些研究的最基本公式。[5–7]

常見激活函數也說明同一個原則：Sigmoid 是 `tanh` 的仿射變換；SiLU \( u\sigma(u) \) 是線性因子與平滑門控的乘積；ReLU 具有分段線性結構；GELU 精確涉及高斯累積分布。不同函數具有不同的導數與組合特性，適合留給另一篇專門比較生成方式與張量耦合的札記。

## 10. 回到共同的數學結構

這一趟從繪圖、自然指數、矩陣流走到射影與張量，得到的不是把不同領域併成一個理論，而是一套更容易辨認各層次作用的讀法。

| 數學層次 | 代表關係 | 它讓我們看見什麼？ |
|---|---|---|
| 生成元 | \( \dot{\mathbf z}=A\mathbf z \) | 基本線性演化規則 |
| 矩陣指數 | \( e^{tA} \) | 有限參數作用與組合律 |
| 不變結構 | \( X^2-\varepsilon Y^2=1 \) | 作用所保存的二次型或退化拘束 |
| 射影讀出 | \( r=Y/X \) | 線性流的非線性座標表示 |
| 模態疊加 | \( \sum c_a\phi_a \) | 簡單函數如何組合複雜形狀 |
| 張量誘導 | \( A\otimes I+I\otimes A \) | 基本作用如何進入多個槽位 |
| 高階微分 | \( \sum c_a\phi_a^{(p)}q_a^{\otimes p} \) | 函數幾何的對稱外積結構 |
| 參數演化 | \( \dot\theta=-\nabla L \) | 表示單元如何在學習中改變 |

上述每一列都有明確的前提：射影座標需要分母不為零；傅立葉轉換涉及函數空間與邊界條件；誘導張量表示依賴指標類型；梯度下降涉及損失與所採用的動力學。這些條件是數學結構的一部分，也使跨領域的比較保持可檢驗性。

最後值得繼續追問的問題，不是「哪一個領域才是其他領域的真正來源」，而是：**哪些表現差異來自生成元、哪些來自表示與觀測、哪些來自張量組合，哪些又必須依靠額外的動力學與拘束才能決定？**

這些問題可以逐一展開成獨立札記：生成元與射影幾何；函數乘積與複合；傅立葉頻譜與邊界；高階導數張量的參數演化；以及共同對稱、Noether 與李雅普諾夫型拘束。各篇先處理一個數學核心，再逐步建立它們的關係。

---

## 附錄 A｜Riccati 與參數合成的快速驗算

從 \( \dot X=\varepsilon Y \)、\( \dot Y=X \) 與 \( r=Y/X \)，在 \( X\ne0 \) 時直接得

$$
\dot r=(X^2-\varepsilon Y^2)/X^2=1-\varepsilon r^2.
$$

由 \( e^{(t+s)A}=e^{tA}e^{sA} \) 及式 (2.6)，可得

$$
C_\varepsilon(t+s)=C_\varepsilon(t)C_\varepsilon(s)+\varepsilon S_\varepsilon(t)S_\varepsilon(s),
$$

$$
S_\varepsilon(t+s)=S_\varepsilon(t)C_\varepsilon(s)+C_\varepsilon(t)S_\varepsilon(s).
$$

兩式相除即得到式 (3.5)。一般 Riccati 公式 (3.4) 則來自 \( \dot X=aX+bY \)、\( \dot Y=cX+dY \) 的商數微分。

## 附錄 B｜`tanh` 的正弦積分與正規化係數

令 \( g(x)=\operatorname{sech}^2x\in L^1(\mathbb R) \)，並使用式 (6.3) 的傅立葉慣例：

$$
\widehat g(\omega)=\frac{\pi\omega}{\sinh(\pi\omega/2)}.
$$

由 \( \tanh x-\tanh0=\int_0^xg(s)\,ds \)，反演後積分：

$$
\begin{aligned}
\tanh x
&=\frac{1}{2\pi}\int_{\mathbb R}\widehat g(\omega)
\frac{e^{i\omega x}-1}{i\omega}\,d\omega\\
&=\int_0^\infty\frac{\sin(\omega x)}{\sinh(\pi\omega/2)}\,d\omega.
\end{aligned}
$$

偶對稱的實數部分使兩側頻率合併，係數 \( 1/(2\pi) \) 與 \( \widehat g \) 中的 \( \pi \) 及正負頻率因子 \( 2 \) 相消，故積分前係數為 \( 1 \)。作為數值交叉檢查：

| \( x \) | 正弦積分 | \( \tanh x \) |
|---:|---:|---:|
| \( 0.7 \) | \( 0.604367777117 \) | \( 0.604367777117 \) |
| \( 1.5 \) | \( 0.905148253645 \) | \( 0.905148253645 \) |

## 附錄 C｜神經切線核與頻率演化：後續札記的接口

對平方損失

$$
L(\theta)=\frac12\int\bigl[f_\theta(x)-f_\ast(x)\bigr]^2\,d\mu(x),
$$

設 \( \rho_\theta=f_\theta-f_\ast \) 為預測誤差。由梯度流與鏈式法則得到

$$
\partial_t f_\theta(x)=-\int \Theta_\theta(x,x')\rho_\theta(x')\,d\mu(x'),
$$

其中

$$
\Theta_\theta(x,x')=\sum_{\mu}\frac{\partial f_\theta(x)}{\partial\theta_\mu}
\frac{\partial f_\theta(x')}{\partial\theta_\mu}.
$$

若核固定、平移不變、定義域週期化且測度相容，傅立葉模態可以對角化此核算子，得到 \( \partial_t\widehat\rho_n=-\lambda_n\widehat\rho_n \)。一般可學習的有限寬度網路中，核會隨參數改變，也可能使頻率耦合；這是另需研究的學習動力學問題。[5–7]

## 附錄 D｜參考文獻

1. **Cybenko, G. (1989).** “Approximation by Superpositions of a Sigmoidal Function.” *Mathematics of Control, Signals, and Systems*, 2, 303–314. [DOI](https://doi.org/10.1007/BF02551274).
2. **Barron, A. R. (1993).** “Universal Approximation Bounds for Superpositions of a Sigmoidal Function.” *IEEE Transactions on Information Theory*, 39(3), 930–945. [DOI](https://doi.org/10.1109/18.256500).
3. **Leshno, M., Lin, V. Ya., Pinkus, A., & Schocken, S. (1993).** “Multilayer Feedforward Networks with a Nonpolynomial Activation Function Can Approximate Any Function.” *Neural Networks*, 6(6), 861–867. [DOI](https://doi.org/10.1016/S0893-6080(05)80131-5).
4. **Candès, E. J. (1999).** “Harmonic Analysis of Neural Networks.” *Applied and Computational Harmonic Analysis*, 6(2), 197–218. [DOI](https://doi.org/10.1006/acha.1998.0248).
5. **Jacot, A., Gabriel, F., & Hongler, C. (2018).** “Neural Tangent Kernel: Convergence and Generalization in Neural Networks.” *NeurIPS 2018*. [Paper](https://papers.nips.cc/paper_files/paper/2018/hash/5a4be1fa34e62bb8a6ec6b91d2462f5a-Abstract.html).
6. **Rahaman, N., et al. (2019).** “On the Spectral Bias of Neural Networks.” *ICML 2019*. [PMLR](https://proceedings.mlr.press/v97/rahaman19a.html).
7. **Tancik, M., et al. (2020).** “Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains.” *NeurIPS 2020*. [Paper](https://proceedings.neurips.cc/paper_files/paper/2020/hash/55053683268957697aa39fba6f231c68-Abstract.html); **Sitzmann, V., et al. (2020).** “Implicit Neural Representations with Periodic Activation Functions.” *NeurIPS 2020*. [Paper](https://proceedings.neurips.cc/paper_files/paper/2020/hash/53c04118df112c13a8c34b38343b9c10-Abstract.html).
8. **Hall, B. C. (2015).** *Lie Groups, Lie Algebras, and Representations: An Elementary Introduction*, 2nd ed., Graduate Texts in Mathematics 222, Springer. [DOI](https://doi.org/10.1007/978-3-319-13467-3). — 矩陣指數、生成元、李群與表示的基礎參考。
9. **Teschl, G. (2012).** *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in Mathematics 140, American Mathematical Society. [DOI](https://doi.org/10.1090/gsm/140). — 線性微分系統、矩陣指數與動力學的基礎參考。
10. **Reid, W. T. (1972).** *Riccati Differential Equations*, Mathematics in Science and Engineering 86, Academic Press. [出版社](https://shop.elsevier.com/books/riccati-differential-equations/reid/978-0-12-586250-9). — 純量與矩陣 Riccati 微分方程的專門參考文獻。

### 延伸閱讀

11. **Chen, R. T. Q., Rubanova, Y., Bettencourt, J., & Duvenaud, D. (2018).** “Neural Ordinary Differential Equations.” *NeurIPS 2018*. [Paper](https://proceedings.neurips.cc/paper/2018/hash/69386f6bb1dfed68692a24c8686939b9-Abstract.html). — 後續討論連續深度學習時的延伸閱讀。
12. **Ganea, O., Bécigneul, G., & Hofmann, T. (2018).** “Hyperbolic Neural Networks.” *NeurIPS 2018*. [Paper](https://papers.nips.cc/paper/7780-hyperbolic-neural-networks). — 後續比較雙曲幾何神經架構的延伸閱讀；其 Poincaré 幾何方法與本文的雙曲生成元對照並非同一個構造。
