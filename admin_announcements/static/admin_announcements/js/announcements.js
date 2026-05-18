(function () {
    function _modalUrl(href) {
        var url = new URL(href, window.location.href);
        url.searchParams.set("_popup", "1");
        return url.toString();
    }

    function _openModal(event) {
        if (
            event.defaultPrevented ||
            event.button !== 0 ||
            event.metaKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey
        ) {
            return;
        }

        if (!window.UnfoldModal || typeof window.UnfoldModal.open !== "function") {
            return;
        }

        var link = event.currentTarget;
        event.preventDefault();
        window.UnfoldModal.open(
            _modalUrl(link.href),
            "admin_announcement_" + link.getAttribute("data-announcement-modal")
        );
    }

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

            var modalLink = item.querySelector("[data-announcement-modal]");
            if (modalLink) {
                modalLink.addEventListener("click", _openModal);
            }
        });
        _hideIfEmpty();
    });
})();
