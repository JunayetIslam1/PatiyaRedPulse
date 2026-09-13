(function () {
    document.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-copy]');
        if (!btn) return;
        e.preventDefault();
        var value = btn.getAttribute('data-copy');
        var restoreHtml = btn.innerHTML;

        function showCopied() {
            btn.innerHTML = '<i class="fas fa-check"></i> ' + (btn.getAttribute('data-copied-label') || 'Copied');
            setTimeout(function () { btn.innerHTML = restoreHtml; }, 1600);
        }

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(value).then(showCopied).catch(function () {
                fallbackCopy(value, showCopied);
            });
        } else {
            fallbackCopy(value, showCopied);
        }
    });

    function fallbackCopy(text, done) {
        var temp = document.createElement('textarea');
        temp.value = text;
        temp.style.position = 'fixed';
        temp.style.opacity = '0';
        document.body.appendChild(temp);
        temp.focus();
        temp.select();
        try { document.execCommand('copy'); } catch (err) { /* no-op */ }
        document.body.removeChild(temp);
        done();
    }
})();
