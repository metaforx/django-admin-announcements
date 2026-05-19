'use strict';

(function() {
    const STORAGE_KEY = 'djangoAdminAnnouncements';
    const DISMISSED_PROPERTY = 'dismissedAnnouncements';
    const BANNER_ID = 'announcements-banner';
    const ITEM_ATTRIBUTE = 'data-announcement-id';
    const DISMISS_ATTRIBUTE = 'data-announcement-dismiss';
    const MODAL_ATTRIBUTE = 'data-announcement-modal';
    const ITEM_SELECTOR = '[' + ITEM_ATTRIBUTE + ']';
    const DISMISS_SELECTOR = '[' + DISMISS_ATTRIBUTE + ']';
    const MODAL_SELECTOR = '[' + MODAL_ATTRIBUTE + ']';

    function _modalUrl(href) {
        const url = new URL(href, window.location.href);
        url.searchParams.set('_popup', '1');
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

        if (!window.UnfoldModal || typeof window.UnfoldModal.open !== 'function') {
            return;
        }

        const link = event.currentTarget;
        event.preventDefault();
        window.UnfoldModal.open(
            _modalUrl(link.href),
            'admin_announcement_' + link.getAttribute(MODAL_ATTRIBUTE)
        );
    }

    function _hideIfEmpty() {
        const banner = document.getElementById(BANNER_ID);
        if (!banner) return;
        const items = banner.querySelectorAll(ITEM_SELECTOR);
        for (let i = 0; i < items.length; i++) {
            if (items[i].style.display !== 'none') return;
        }
        banner.style.display = 'none';
    }

    function _getDismissedAnnouncements() {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (!stored) return {};

            const data = JSON.parse(stored);
            const dismissed = data ? data[DISMISSED_PROPERTY] : null;
            if (!dismissed || Array.isArray(dismissed) || typeof dismissed !== 'object') {
                return {};
            }
            return dismissed;
        } catch {
            return {};
        }
    }

    function _setDismissedAnnouncements(dismissed) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                [DISMISSED_PROPERTY]: dismissed,
            }));
        } catch {
            return;
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        const dismissed = _getDismissedAnnouncements();
        const items = document.querySelectorAll(ITEM_SELECTOR);

        items.forEach(function(item) {
            const id = item.getAttribute(ITEM_ATTRIBUTE);
            if (dismissed[id]) {
                item.style.display = 'none';
                return;
            }

            const closeBtn = item.querySelector(DISMISS_SELECTOR);
            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    dismissed[id] = Date.now();
                    _setDismissedAnnouncements(dismissed);
                    item.style.display = 'none';
                    _hideIfEmpty();
                });
            }

            const modalLink = item.querySelector(MODAL_SELECTOR);
            if (modalLink) {
                modalLink.addEventListener('click', _openModal);
            }
        });
        _hideIfEmpty();
    });
})();
