(function () {
    function _hideIfEmpty() {
        var banner = document.getElementById("announcements-banner");
        if (!banner) return;
        var items = banner.querySelectorAll("[data-announcement-id]");
        for (var i = 0; i < items.length; i++) {
            if (items[i].style.display !== "none") return;
        }
        banner.style.display = "none";
    }

    document.addEventListener("DOMContentLoaded", function () {
        var items = document.querySelectorAll("[data-announcement-id]");
        items.forEach(function (item) {
            var id = item.getAttribute("data-announcement-id");
            var key = "dismissed_announcement_" + id;
            if (localStorage.getItem(key)) {
                item.style.display = "none";
                return;
            }
            var closeBtn = item.querySelector("[data-announcement-dismiss]");
            if (closeBtn) {
                closeBtn.addEventListener("click", function () {
                    localStorage.setItem(key, Date.now().toString());
                    item.style.display = "none";
                    _hideIfEmpty();
                });
            }
        });
        _hideIfEmpty();
    });
})();
