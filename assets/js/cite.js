// 「引用本文」複製按鈕。複製的內容就是畫面上 .cite-text 的文字。
// 沒有 JavaScript 時按鈕保持隱藏，引用文字仍可手動選取。
(function () {
  function selectText(el) {
    var range = document.createRange();
    range.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  function legacyCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  document.querySelectorAll("[data-cite-copy]").forEach(function (btn) {
    var box = btn.closest(".cite-box");
    var source = box.querySelector(".cite-text");
    var status = box.querySelector(".cite-status");
    var timer;

    function report(ok) {
      clearTimeout(timer);
      status.textContent = ok ? btn.dataset.ok : btn.dataset.fail;
      status.classList.toggle("cite-status-error", !ok);
      if (ok) {
        timer = setTimeout(function () { status.textContent = ""; }, 3000);
      } else {
        selectText(source);
      }
    }

    btn.addEventListener("click", function () {
      var text = source.textContent.replace(/\s+/g, " ").trim();
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(
          function () { report(true); },
          function () { report(legacyCopy(text)); }
        );
      } else {
        report(legacyCopy(text));
      }
    });

    btn.hidden = false;
  });
})();
