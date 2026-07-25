/* @ds-bundle: {"format":4,"namespace":"RDPUIDesignSystem_ee4ae1","components":[{"name":"Accordion","sourcePath":"components/data/Accordion.jsx"},{"name":"Card","sourcePath":"components/data/Card.jsx"},{"name":"FilterBar","sourcePath":"components/data/FilterBar.jsx"},{"name":"StatCard","sourcePath":"components/data/StatCard.jsx"},{"name":"Table","sourcePath":"components/data/Table.jsx"},{"name":"Timeline","sourcePath":"components/data/Timeline.jsx"},{"name":"Alert","sourcePath":"components/feedback/Alert.jsx"},{"name":"Confirm","sourcePath":"components/feedback/Confirm.jsx"},{"name":"Drawer","sourcePath":"components/feedback/Drawer.jsx"},{"name":"EmptyState","sourcePath":"components/feedback/EmptyState.jsx"},{"name":"Modal","sourcePath":"components/feedback/Modal.jsx"},{"name":"Toast","sourcePath":"components/feedback/Toast.jsx"},{"name":"ToastContainer","sourcePath":"components/feedback/Toast.jsx"},{"name":"Tooltip","sourcePath":"components/feedback/Tooltip.jsx"},{"name":"Checkbox","sourcePath":"components/forms/Checkbox.jsx"},{"name":"FileUpload","sourcePath":"components/forms/FileUpload.jsx"},{"name":"FormField","sourcePath":"components/forms/FormField.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Radio","sourcePath":"components/forms/Radio.jsx"},{"name":"SearchBox","sourcePath":"components/forms/SearchBox.jsx"},{"name":"Select","sourcePath":"components/forms/Select.jsx"},{"name":"Switch","sourcePath":"components/forms/Switch.jsx"},{"name":"Textarea","sourcePath":"components/forms/Textarea.jsx"},{"name":"BrandMark","sourcePath":"components/layout/BrandMark.jsx"},{"name":"PageHeader","sourcePath":"components/layout/PageHeader.jsx"},{"name":"Sidebar","sourcePath":"components/layout/Sidebar.jsx"},{"name":"Topbar","sourcePath":"components/layout/Topbar.jsx"},{"name":"Breadcrumb","sourcePath":"components/navigation/Breadcrumb.jsx"},{"name":"Dropdown","sourcePath":"components/navigation/Dropdown.jsx"},{"name":"Pagination","sourcePath":"components/navigation/Pagination.jsx"},{"name":"Steps","sourcePath":"components/navigation/Steps.jsx"},{"name":"Tabs","sourcePath":"components/navigation/Tabs.jsx"},{"name":"Avatar","sourcePath":"components/primitives/Avatar.jsx"},{"name":"AvatarGroup","sourcePath":"components/primitives/Avatar.jsx"},{"name":"Badge","sourcePath":"components/primitives/Badge.jsx"},{"name":"Button","sourcePath":"components/primitives/Button.jsx"},{"name":"Icon","sourcePath":"components/primitives/Icon.jsx"},{"name":"Loader","sourcePath":"components/primitives/Loader.jsx"},{"name":"Progress","sourcePath":"components/primitives/Progress.jsx"},{"name":"Rating","sourcePath":"components/primitives/Rating.jsx"},{"name":"Skeleton","sourcePath":"components/primitives/Skeleton.jsx"},{"name":"Spinner","sourcePath":"components/primitives/Spinner.jsx"}],"sourceHashes":{"assets/rdp.js":"cc46c561d7d2","components/data/Accordion.jsx":"4cafb1932fc3","components/data/Card.jsx":"e12e8d0de311","components/data/FilterBar.jsx":"9b1c45d06089","components/data/StatCard.jsx":"3be0f449836f","components/data/Table.jsx":"052fcc9d6f27","components/data/Timeline.jsx":"f9a59006e5df","components/feedback/Alert.jsx":"6256b93f6aaa","components/feedback/Confirm.jsx":"be5cf5a60a3c","components/feedback/Drawer.jsx":"1174169cfdc6","components/feedback/EmptyState.jsx":"c016d1ce9e10","components/feedback/Modal.jsx":"e5aa1ad31ca4","components/feedback/Toast.jsx":"67222bec1708","components/feedback/Tooltip.jsx":"6140ee85e62e","components/forms/Checkbox.jsx":"69bd4f927e96","components/forms/FileUpload.jsx":"dae872d8b3d5","components/forms/FormField.jsx":"9fe0d88bf83c","components/forms/Input.jsx":"175513ae84ed","components/forms/Radio.jsx":"a498f7b038d6","components/forms/SearchBox.jsx":"2dffd04f8716","components/forms/Select.jsx":"45ebf9e471d7","components/forms/Switch.jsx":"077074f9f3b8","components/forms/Textarea.jsx":"035cbe5b2ead","components/layout/BrandMark.jsx":"2752beeeb0c9","components/layout/PageHeader.jsx":"357b662a2294","components/layout/Sidebar.jsx":"ccb7c0af14b1","components/layout/Topbar.jsx":"4a34f4d7d950","components/navigation/Breadcrumb.jsx":"69356ca6dfbf","components/navigation/Dropdown.jsx":"5230fab579de","components/navigation/Pagination.jsx":"ec02b694c32c","components/navigation/Steps.jsx":"18bed6af87aa","components/navigation/Tabs.jsx":"a6c1ac23121a","components/primitives/Avatar.jsx":"97e5af972635","components/primitives/Badge.jsx":"c8b12fbd246c","components/primitives/Button.jsx":"288ba535611b","components/primitives/Icon.jsx":"31dea94da187","components/primitives/Loader.jsx":"f047bf01b114","components/primitives/Progress.jsx":"e83e466a8f1b","components/primitives/Rating.jsx":"f9220e39cd33","components/primitives/Skeleton.jsx":"0e9f9e850693","components/primitives/Spinner.jsx":"43b26a0b4dc1","ui_kits/dashboard/app.jsx":"08f5a86af3f8"},"inlinedExternals":[],"unexposedExports":[{"name":"iconNames","sourcePath":"components/primitives/Icon.jsx"}]} */

(() => {

const __ds_ns = (window.RDPUIDesignSystem_ee4ae1 = window.RDPUIDesignSystem_ee4ae1 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// assets/rdp.js
try { (() => {
(function () {
  const o = document.createElement("link").relList;
  if (o && o.supports && o.supports("modulepreload")) return;
  for (const t of document.querySelectorAll('link[rel="modulepreload"]')) e(t);
  new MutationObserver(t => {
    for (const i of t) if (i.type === "childList") for (const a of i.addedNodes) a.tagName === "LINK" && a.rel === "modulepreload" && e(a);
  }).observe(document, {
    childList: !0,
    subtree: !0
  });
  function s(t) {
    const i = {};
    return t.integrity && (i.integrity = t.integrity), t.referrerPolicy && (i.referrerPolicy = t.referrerPolicy), t.crossOrigin === "use-credentials" ? i.credentials = "include" : t.crossOrigin === "anonymous" ? i.credentials = "omit" : i.credentials = "same-origin", i;
  }
  function e(t) {
    if (t.ep) return;
    t.ep = !0;
    const i = s(t);
    fetch(t.href, i);
  }
})();
(function () {
  const n = window.RDP || {};
  n.openModal = function (o) {
    const s = typeof o == "string" ? document.getElementById(o) : o;
    !s || s.tagName !== "DIALOG" || (s.showModal(), document.body.style.overflow = "hidden", s.dispatchEvent(new CustomEvent("rdp:modal-open", {
      bubbles: !0
    })));
  }, n.closeModal = function (o) {
    const s = typeof o == "string" ? document.getElementById(o) : o;
    !s || s.tagName !== "DIALOG" || (s.close(), document.body.style.overflow = "", s.dispatchEvent(new CustomEvent("rdp:modal-close", {
      bubbles: !0
    })));
  }, window.RDP = n, document.addEventListener("click", function (o) {
    const s = o.target.closest('[data-rdp-action="open-modal"]');
    if (s) {
      o.preventDefault();
      const t = s.getAttribute("data-rdp-target");
      t && n.openModal(t.replace("#", ""));
    }
    const e = o.target.closest('[data-rdp-action="close-modal"]');
    if (e) {
      o.preventDefault();
      const t = e.closest("dialog.rdp-modal");
      t && n.closeModal(t);
    }
    if (o.target.tagName === "DIALOG" && o.target.classList.contains("rdp-modal")) {
      const t = o.target.getBoundingClientRect();
      t.top <= o.clientY && o.clientY <= t.top + t.height && t.left <= o.clientX && o.clientX <= t.left + t.width || n.closeModal(o.target);
    }
  });
})();
(function () {
  const n = window.RDP || {};
  n.showToast = function (o = {}) {
    const {
        title: s,
        message: e,
        type: t = "info",
        duration: i = 5e3,
        position: a = "top-right",
        action: c
      } = o,
      p = `rdp-toast-container--${a}`;
    let d = document.querySelector(`.rdp-toast-container.${p}`);
    d || (d = document.createElement("div"), d.className = `rdp-toast-container ${p}`, document.body.appendChild(d));
    const r = document.createElement("div");
    r.className = `rdp-toast rdp-toast--${t}`, r.setAttribute("role", "alert");
    let m = "";
    i > 0 && (m = `<div class="rdp-toast__progress" style="animation-duration: ${i}ms"></div>`);
    let f = "";
    c && c.text && c.callback && (f = `<button class="rdp-toast__action">${c.text}</button>`), r.innerHTML = `
      <div class="rdp-toast__content">
        ${s ? `<div class="rdp-toast__title">${s}</div>` : ""}
        ${e ? `<div class="rdp-toast__message">${e}</div>` : ""}
        ${f}
      </div>
      <button class="rdp-toast__close" aria-label="Tutup">&times;</button>
      ${m}
    `, d.appendChild(r);
    const u = () => {
      r.classList.add("rdp-toast--hiding"), r.addEventListener("animationend", () => {
        r.remove(), d.children.length === 0 && d.remove();
      }, {
        once: !0
      });
    };
    if (r.querySelector(".rdp-toast__close").addEventListener("click", l => {
      l.preventDefault(), u();
    }), c && c.text && c.callback) {
      const l = r.querySelector(".rdp-toast__action");
      l && l.addEventListener("click", g => {
        g.preventDefault(), c.callback(), u();
      });
    }
    i > 0 && setTimeout(u, i);
  }, window.RDP = n;
})();
(function () {
  const n = window.RDP || {};
  n.setTheme = function (e) {
    const t = document.documentElement;
    e === "auto" ? t.removeAttribute("data-theme") : t.setAttribute("data-theme", e);
    try {
      localStorage.setItem("rdp-theme", e);
    } catch {}
    document.dispatchEvent(new CustomEvent("rdp:theme-change", {
      detail: {
        theme: e
      }
    }));
  }, n.getTheme = function () {
    return document.documentElement.getAttribute("data-theme") || "auto";
  };
  function o() {
    try {
      const e = localStorage.getItem("rdp-theme");
      e && e !== "auto" && document.documentElement.setAttribute("data-theme", e);
    } catch {}
  }
  n.toggleSidebar = function () {
    const e = document.querySelector(".rdp-sidebar"),
      t = document.querySelector(".rdp-sidebar-backdrop");
    if (!e) return;
    e.classList.contains("is-open") ? (e.classList.remove("is-open"), t && t.classList.remove("is-visible"), document.body.style.overflow = "") : (e.classList.add("is-open"), t && t.classList.add("is-visible"), document.body.style.overflow = "hidden");
  }, n.dismissAlert = function (e) {
    e && (e.classList.add("rdp-alert--hiding"), e.addEventListener("animationend", function () {
      e.remove();
    }, {
      once: !0
    }));
  }, n.toggleMobileNav = function () {
    const e = document.querySelector(".rdp-topnav__mobile");
    e && e.classList.toggle("is-open");
  };
  function s() {
    o(), document.addEventListener("click", function (e) {
      const t = e.target.closest("[data-rdp-action]");
      if (!t) return;
      switch (t.getAttribute("data-rdp-action")) {
        case "toggle-sidebar":
          e.preventDefault(), n.toggleSidebar();
          break;
        case "toggle-mobile-nav":
          e.preventDefault(), n.toggleMobileNav();
          break;
        case "dismiss-alert":
          e.preventDefault(), n.dismissAlert(t.closest(".rdp-alert"));
          break;
        case "set-theme":
          e.preventDefault();
          var a = t.getAttribute("data-rdp-theme");
          a && n.setTheme(a);
          break;
      }
    }), document.addEventListener("click", function (e) {
      e.target.classList.contains("rdp-sidebar-backdrop") && n.toggleSidebar();
    }), document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        var t = document.querySelector(".rdp-sidebar.is-open");
        if (t) {
          n.toggleSidebar();
          return;
        }
        var i = document.querySelector(".rdp-topnav__mobile.is-open");
        i && n.toggleMobileNav();
      }
    });
  }
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", s) : s(), window.RDP = n;
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "assets/rdp.js", error: String((e && e.message) || e) }); }

// components/data/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Card({
  title,
  header,
  footer,
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-card"
  }, rest), title || header ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-card__header"
  }, title ? /*#__PURE__*/React.createElement("h3", {
    className: "rdp-card__title"
  }, title) : null, header) : null, children, footer ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-card__footer"
  }, footer) : null);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Card.jsx", error: String((e && e.message) || e) }); }

// components/data/FilterBar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function FilterBar({
  children,
  actions,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-filter-bar"
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: "rdp-filter-bar__filters"
  }, children), actions ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-filter-bar__actions"
  }, actions) : null);
}
Object.assign(__ds_scope, { FilterBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/FilterBar.jsx", error: String((e && e.message) || e) }); }

// components/data/Table.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Table({
  columns,
  rows,
  striped = false,
  hoverable = false,
  compact = false,
  renderCell,
  ...rest
}) {
  const cls = ['rdp-table', striped ? 'rdp-table--striped' : '', hoverable ? 'rdp-table--hoverable' : '', compact ? 'rdp-table--compact' : ''].filter(Boolean).join(' ');
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-table-wrapper"
  }, rest), /*#__PURE__*/React.createElement("table", {
    className: cls
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, columns.map(c => /*#__PURE__*/React.createElement("th", {
    key: c.key
  }, c.label)))), /*#__PURE__*/React.createElement("tbody", null, rows.map((r, i) => /*#__PURE__*/React.createElement("tr", {
    key: i
  }, columns.map(c => /*#__PURE__*/React.createElement("td", {
    key: c.key
  }, renderCell ? renderCell(r, c.key) : r[c.key])))))));
}
Object.assign(__ds_scope, { Table });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Table.jsx", error: String((e && e.message) || e) }); }

// components/data/Timeline.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Timeline({
  items,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("ul", _extends({
    className: "rdp-timeline"
  }, rest), items.map((it, i) => /*#__PURE__*/React.createElement("li", {
    key: i,
    className: "rdp-timeline-item"
  }, /*#__PURE__*/React.createElement("span", {
    className: 'rdp-timeline-item__dot' + (it.active ? ' rdp-timeline-item__dot--active' : '')
  }), /*#__PURE__*/React.createElement("div", {
    className: "rdp-timeline-item__content"
  }, /*#__PURE__*/React.createElement("span", {
    className: "rdp-timeline-item__title"
  }, it.title), it.desc ? /*#__PURE__*/React.createElement("span", {
    className: "rdp-timeline-item__desc"
  }, it.desc) : null, it.time ? /*#__PURE__*/React.createElement("span", {
    className: "rdp-timeline-item__time"
  }, it.time) : null))));
}
Object.assign(__ds_scope, { Timeline });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Timeline.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Confirm.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Confirm({
  title = 'Are you sure?',
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  danger = false,
  onConfirm,
  onCancel,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-confirm-overlay",
    onClick: onCancel
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: "rdp-confirm-modal",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("div", {
    className: "rdp-confirm-modal__header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "rdp-confirm-modal__title"
  }, title)), /*#__PURE__*/React.createElement("div", {
    className: "rdp-confirm-modal__body"
  }, /*#__PURE__*/React.createElement("p", {
    className: "rdp-confirm-modal__message"
  }, message)), /*#__PURE__*/React.createElement("div", {
    className: "rdp-confirm-modal__footer"
  }, /*#__PURE__*/React.createElement("button", {
    className: "rdp-btn rdp-btn--md rdp-btn--outline",
    onClick: onCancel
  }, cancelLabel), /*#__PURE__*/React.createElement("button", {
    className: 'rdp-btn rdp-btn--md ' + (danger ? 'rdp-btn--danger' : 'rdp-btn--primary'),
    onClick: onConfirm
  }, confirmLabel))));
}
Object.assign(__ds_scope, { Confirm });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Confirm.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Drawer.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Drawer({
  side = 'right',
  title,
  footer,
  onClose,
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: 'rdp-drawer-backdrop rdp-drawer-backdrop--' + side,
    onClick: onClose
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: "rdp-drawer is-open",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("div", {
    className: "rdp-drawer__header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "rdp-drawer__title"
  }, title), /*#__PURE__*/React.createElement("button", {
    className: "rdp-modal__close",
    "aria-label": "Close",
    onClick: onClose
  }, '\u00d7')), /*#__PURE__*/React.createElement("div", {
    className: "rdp-drawer__body"
  }, children), footer ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-drawer__footer"
  }, footer) : null));
}
Object.assign(__ds_scope, { Drawer });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Drawer.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Modal.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Modal({
  open = true,
  size = 'md',
  title,
  footer,
  onClose,
  children,
  ...rest
}) {
  if (!open) return null;
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-modal-backdrop",
    onClick: onClose
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: 'rdp-modal rdp-modal--' + size,
    role: "dialog",
    "aria-modal": "true",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("div", {
    className: "rdp-modal__header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "rdp-modal__title"
  }, title), /*#__PURE__*/React.createElement("button", {
    className: "rdp-modal__close",
    "aria-label": "Close",
    onClick: onClose
  }, '\u00d7')), /*#__PURE__*/React.createElement("div", {
    className: "rdp-modal__body"
  }, children), footer ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-modal__footer"
  }, footer) : null));
}
Object.assign(__ds_scope, { Modal });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Modal.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Tooltip.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Tooltip({
  label,
  position = 'top',
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({
    className: 'rdp-tooltip-wrapper rdp-tooltip-wrapper--' + position,
    "data-tooltip": label
  }, rest), children);
}
Object.assign(__ds_scope, { Tooltip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Tooltip.jsx", error: String((e && e.message) || e) }); }

// components/forms/Checkbox.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Checkbox({
  label,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "rdp-checkbox"
  }, /*#__PURE__*/React.createElement("input", _extends({
    type: "checkbox",
    className: "rdp-checkbox__input"
  }, rest)), /*#__PURE__*/React.createElement("span", {
    style: {
      whiteSpace: 'nowrap'
    }
  }, label));
}
Object.assign(__ds_scope, { Checkbox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Checkbox.jsx", error: String((e && e.message) || e) }); }

// components/forms/FormField.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function FormField({
  label,
  required = false,
  help,
  error,
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-form-field"
  }, rest), label ? /*#__PURE__*/React.createElement("label", {
    className: "rdp-form-field__label"
  }, label, required ? /*#__PURE__*/React.createElement("span", {
    className: "rdp-form-field__required"
  }, "*") : null) : null, children, error ? /*#__PURE__*/React.createElement("span", {
    className: "rdp-form-field__error"
  }, error) : help ? /*#__PURE__*/React.createElement("span", {
    className: "rdp-form-field__help"
  }, help) : null);
}
Object.assign(__ds_scope, { FormField });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/FormField.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Input({
  invalid = false,
  className = '',
  ...rest
}) {
  return /*#__PURE__*/React.createElement("input", _extends({
    className: ('rdp-input ' + className).trim(),
    "aria-invalid": invalid ? 'true' : undefined
  }, rest));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Radio.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Radio({
  label,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "rdp-radio"
  }, /*#__PURE__*/React.createElement("input", _extends({
    type: "radio",
    className: "rdp-radio__input"
  }, rest)), /*#__PURE__*/React.createElement("span", null, label));
}
Object.assign(__ds_scope, { Radio });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Radio.jsx", error: String((e && e.message) || e) }); }

// components/forms/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Select({
  invalid = false,
  options,
  className = '',
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("select", _extends({
    className: ('rdp-select ' + className).trim(),
    "aria-invalid": invalid ? 'true' : undefined
  }, rest), options ? options.map(o => /*#__PURE__*/React.createElement("option", {
    key: String(o.value),
    value: o.value
  }, o.label)) : children);
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Select.jsx", error: String((e && e.message) || e) }); }

// components/forms/Switch.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Switch({
  label,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "rdp-switch"
  }, /*#__PURE__*/React.createElement("input", _extends({
    type: "checkbox",
    className: "rdp-switch__input"
  }, rest)), /*#__PURE__*/React.createElement("span", null, label));
}
Object.assign(__ds_scope, { Switch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Switch.jsx", error: String((e && e.message) || e) }); }

// components/forms/Textarea.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Textarea({
  invalid = false,
  className = '',
  ...rest
}) {
  return /*#__PURE__*/React.createElement("textarea", _extends({
    className: ('rdp-textarea ' + className).trim(),
    "aria-invalid": invalid ? 'true' : undefined
  }, rest));
}
Object.assign(__ds_scope, { Textarea });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Textarea.jsx", error: String((e && e.message) || e) }); }

// components/layout/BrandMark.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function BrandMark({
  size = 28,
  withWordmark = true,
  dark = false,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.5rem',
      fontWeight: 700,
      fontSize: '1rem',
      color: dark ? '#fff' : 'var(--rdp-text)'
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      width: size,
      height: size,
      background: 'var(--rdp-primary)',
      borderRadius: 6,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: '#fff',
      fontWeight: 800,
      fontSize: size * 0.55
    }
  }, "R"), withWordmark ? 'RDP-UI' : null);
}
Object.assign(__ds_scope, { BrandMark });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/layout/BrandMark.jsx", error: String((e && e.message) || e) }); }

// components/layout/PageHeader.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function PageHeader({
  title,
  actions,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-page-header"
  }, rest), /*#__PURE__*/React.createElement("h2", {
    className: "rdp-page-header__title"
  }, title), /*#__PURE__*/React.createElement("div", {
    className: "rdp-page-header__actions"
  }, actions));
}
Object.assign(__ds_scope, { PageHeader });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/layout/PageHeader.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Breadcrumb.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Breadcrumb({
  items,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("ol", _extends({
    className: "rdp-breadcrumb"
  }, rest), items.map((it, i) => /*#__PURE__*/React.createElement("li", {
    key: i
  }, it.href && i < items.length - 1 ? /*#__PURE__*/React.createElement("a", {
    href: it.href
  }, it.label) : it.label)));
}
Object.assign(__ds_scope, { Breadcrumb });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Breadcrumb.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Dropdown.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Dropdown({
  trigger,
  items,
  align = 'left',
  open,
  onSelect,
  ...rest
}) {
  const [isOpen, setOpen] = React.useState(false);
  const show = open !== undefined ? open : isOpen;
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-dropdown"
  }, rest), /*#__PURE__*/React.createElement("span", {
    onClick: () => setOpen(!isOpen)
  }, trigger), show ? /*#__PURE__*/React.createElement("div", {
    className: 'rdp-dropdown__menu rdp-dropdown__menu--' + align
  }, items.map((it, i) => it.divider ? /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "rdp-dropdown__divider"
  }) : it.header ? /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "rdp-dropdown__label"
  }, it.header) : /*#__PURE__*/React.createElement("button", {
    key: i,
    className: 'rdp-dropdown__item' + (it.danger ? ' rdp-dropdown__item--danger' : ''),
    onClick: () => {
      setOpen(false);
      onSelect && onSelect(it);
      it.onClick && it.onClick();
    }
  }, it.label))) : null);
}
Object.assign(__ds_scope, { Dropdown });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Dropdown.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Pagination.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Pagination({
  page = 1,
  pages = 1,
  onChange,
  ...rest
}) {
  const go = p => onChange && onChange(Math.min(pages, Math.max(1, p)));
  return /*#__PURE__*/React.createElement("nav", _extends({
    className: "rdp-pagination"
  }, rest), /*#__PURE__*/React.createElement("button", {
    className: 'rdp-pagination__item' + (page <= 1 ? ' disabled' : ''),
    onClick: () => go(page - 1)
  }, '\u2039'), Array.from({
    length: pages
  }, (_, i) => /*#__PURE__*/React.createElement("button", {
    key: i,
    className: 'rdp-pagination__item' + (i + 1 === page ? ' active' : ''),
    onClick: () => go(i + 1)
  }, i + 1)), /*#__PURE__*/React.createElement("button", {
    className: 'rdp-pagination__item' + (page >= pages ? ' disabled' : ''),
    onClick: () => go(page + 1)
  }, '\u203a'));
}
Object.assign(__ds_scope, { Pagination });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Pagination.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Steps.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Steps({
  steps,
  current = 0,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-steps"
  }, rest), steps.map((s, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: 'rdp-steps__item' + (i === current ? ' rdp-steps__item--active' : i < current ? ' rdp-steps__item--completed' : '')
  }, /*#__PURE__*/React.createElement("span", {
    className: "rdp-steps__indicator"
  }, i < current ? '\u2713' : i + 1), /*#__PURE__*/React.createElement("span", {
    className: "rdp-steps__label"
  }, s), i < steps.length - 1 ? /*#__PURE__*/React.createElement("span", {
    className: "rdp-steps__line"
  }) : null)));
}
Object.assign(__ds_scope, { Steps });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Steps.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Tabs.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Tabs({
  tabs,
  active,
  onChange,
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-tabs"
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: "rdp-tabs__list",
    role: "tablist"
  }, tabs.map(t => /*#__PURE__*/React.createElement("button", {
    key: t.id,
    role: "tab",
    "aria-selected": t.id === active,
    className: 'rdp-tabs__tab' + (t.id === active ? ' rdp-tabs__tab--active' : ''),
    onClick: () => onChange && onChange(t.id)
  }, t.label))), children ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-tabs__panel"
  }, children) : null);
}
Object.assign(__ds_scope, { Tabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Tabs.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Avatar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Avatar({
  size,
  src,
  alt = '',
  children,
  ...rest
}) {
  const cls = ['rdp-avatar', size ? 'rdp-avatar--' + size : ''].filter(Boolean).join(' ');
  return /*#__PURE__*/React.createElement("span", _extends({
    className: cls
  }, rest), src ? /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: alt
  }) : children);
}
function AvatarGroup({
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "rdp-avatar-group"
  }, children);
}
Object.assign(__ds_scope, { Avatar, AvatarGroup });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Badge({
  variant = 'default',
  pill = false,
  dot = false,
  outline = false,
  children,
  ...rest
}) {
  const cls = ['rdp-badge', 'rdp-badge--' + variant, pill ? 'rdp-badge--pill' : '', outline ? 'rdp-badge--outline' : ''].filter(Boolean).join(' ');
  return /*#__PURE__*/React.createElement("span", _extends({
    className: cls
  }, rest), dot ? /*#__PURE__*/React.createElement("span", {
    className: "rdp-badge__dot"
  }) : null, children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Badge.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Button({
  variant = 'primary',
  size = 'md',
  iconOnly = false,
  loading = false,
  fullWidth = false,
  className = '',
  children,
  ...rest
}) {
  const cls = ['rdp-btn', 'rdp-btn--' + size, 'rdp-btn--' + variant, iconOnly ? 'rdp-btn--icon-only' : '', fullWidth ? 'rdp-btn--full' : '', className].filter(Boolean).join(' ');
  return /*#__PURE__*/React.createElement("button", _extends({
    className: cls
  }, rest), loading ? /*#__PURE__*/React.createElement("span", {
    className: 'rdp-spinner rdp-spinner--sm'
  }) : null, children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Button.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Icon.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const P = {
  search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
  check: '<path d="M20 6 9 17l-5-5"/>',
  x: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
  'chevron-down': '<path d="m6 9 6 6 6-6"/>',
  'chevron-right': '<path d="m9 18 6-6-6-6"/>',
  'chevron-left': '<path d="m15 18-6-6 6-6"/>',
  info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
  'alert-triangle': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
  'alert-circle': '<circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
  'check-circle': '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>',
  upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/>',
  download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
  bell: '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
  user: '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
  users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  home: '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
  dashboard: '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
  'file-text': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
  folder: '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
  plus: '<path d="M5 12h14"/><path d="M12 5v14"/>',
  'more-horizontal': '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
  'log-out': '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/>',
  calendar: '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
  filter: '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46"/>',
  trash: '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
  pencil: '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>',
  eye: '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
  inbox: '<polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
  mail: '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
  briefcase: '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
  menu: '<line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/>',
  'trending-up': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
  'trending-down': '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/>',
  settings: '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>'
};
function Icon({
  name,
  size = 20,
  strokeWidth = 1.5,
  style,
  ...rest
}) {
  const d = P[name] || P.info;
  return /*#__PURE__*/React.createElement("svg", _extends({
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: strokeWidth,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    style: style,
    "aria-hidden": "true",
    dangerouslySetInnerHTML: {
      __html: d
    }
  }, rest));
}
const iconNames = Object.keys(P);
Object.assign(__ds_scope, { Icon, iconNames });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Icon.jsx", error: String((e && e.message) || e) }); }

// components/data/Accordion.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Accordion({
  items,
  defaultOpen = 0,
  ...rest
}) {
  const [open, setOpen] = React.useState(defaultOpen);
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-accordion"
  }, rest), items.map((it, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: 'rdp-accordion__item' + (open === i ? ' rdp-accordion__item--open' : '')
  }, /*#__PURE__*/React.createElement("button", {
    className: "rdp-accordion__trigger",
    "aria-expanded": open === i,
    onClick: () => setOpen(open === i ? -1 : i)
  }, it.title, /*#__PURE__*/React.createElement("span", {
    className: "rdp-accordion__icon"
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "chevron-down",
    size: 16
  }))), open === i ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-accordion__content"
  }, it.content) : null)));
}
Object.assign(__ds_scope, { Accordion });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Accordion.jsx", error: String((e && e.message) || e) }); }

// components/data/StatCard.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function StatCard({
  label,
  value,
  change,
  direction = 'neutral',
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-stat-card"
  }, rest), /*#__PURE__*/React.createElement("span", {
    className: "rdp-stat-card__label"
  }, label), /*#__PURE__*/React.createElement("span", {
    className: "rdp-stat-card__value",
    style: {
      whiteSpace: 'nowrap'
    }
  }, value), change ? /*#__PURE__*/React.createElement("span", {
    className: 'rdp-stat-card__change rdp-stat-card__change--' + direction
  }, direction === 'up' ? /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "trending-up",
    size: 13
  }) : direction === 'down' ? /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "trending-down",
    size: 13
  }) : null, change) : null);
}
Object.assign(__ds_scope, { StatCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/StatCard.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Alert.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const IK = {
  success: 'check-circle',
  warning: 'alert-triangle',
  danger: 'alert-circle',
  info: 'info'
};
function Alert({
  variant = 'info',
  title,
  dismissible = false,
  onDismiss,
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: 'rdp-alert rdp-alert--' + variant,
    role: "alert"
  }, rest), /*#__PURE__*/React.createElement("span", {
    className: "rdp-alert__icon"
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: IK[variant],
    size: 20
  })), /*#__PURE__*/React.createElement("div", {
    className: "rdp-alert__content"
  }, title ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-alert__title"
  }, title) : null, /*#__PURE__*/React.createElement("div", {
    className: "rdp-alert__desc"
  }, children)), dismissible ? /*#__PURE__*/React.createElement("button", {
    className: "rdp-alert__dismiss",
    "aria-label": "Dismiss",
    onClick: onDismiss
  }, '\u00d7') : null);
}
Object.assign(__ds_scope, { Alert });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Alert.jsx", error: String((e && e.message) || e) }); }

// components/feedback/EmptyState.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function EmptyState({
  icon = 'inbox',
  title,
  description,
  action,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-empty-state"
  }, rest), /*#__PURE__*/React.createElement("span", {
    className: "rdp-empty-state__icon"
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: icon,
    size: 40
  })), /*#__PURE__*/React.createElement("h3", {
    className: "rdp-empty-state__title"
  }, title), description ? /*#__PURE__*/React.createElement("p", {
    className: "rdp-empty-state__desc"
  }, description) : null, action);
}
Object.assign(__ds_scope, { EmptyState });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/EmptyState.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Toast.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const IK = {
  success: 'check-circle',
  warning: 'alert-triangle',
  danger: 'alert-circle',
  info: 'info'
};
const CO = {
  success: 'var(--rdp-success)',
  warning: 'var(--rdp-warning)',
  danger: 'var(--rdp-danger)',
  info: 'var(--rdp-info)'
};
function Toast({
  variant = 'info',
  title,
  message,
  actionLabel,
  onAction,
  onDismiss,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: 'rdp-toast rdp-toast--' + variant
  }, rest), /*#__PURE__*/React.createElement("span", {
    className: "rdp-toast__icon",
    style: {
      color: CO[variant]
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: IK[variant],
    size: 18
  })), /*#__PURE__*/React.createElement("div", {
    className: "rdp-toast__content"
  }, /*#__PURE__*/React.createElement("div", {
    className: "rdp-toast__title"
  }, title), message ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-toast__desc"
  }, message) : null), actionLabel ? /*#__PURE__*/React.createElement("button", {
    className: "rdp-toast__action",
    onClick: onAction
  }, actionLabel) : null, onDismiss ? /*#__PURE__*/React.createElement("button", {
    className: "rdp-toast__close",
    onClick: onDismiss
  }, '\u00d7') : null);
}
function ToastContainer({
  position = 'bottom-right',
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: 'rdp-toast-container rdp-toast-container--' + position
  }, children);
}
Object.assign(__ds_scope, { Toast, ToastContainer });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Toast.jsx", error: String((e && e.message) || e) }); }

// components/forms/FileUpload.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function FileUpload({
  text = 'Click to upload or drag a file here',
  subtext = 'PDF, PNG or JPG up to 10 MB',
  fileName,
  error,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "rdp-file-upload-container"
  }, rest), /*#__PURE__*/React.createElement("label", {
    className: "rdp-file-upload-label"
  }, /*#__PURE__*/React.createElement("input", {
    type: "file",
    className: "rdp-file-upload-input"
  }), /*#__PURE__*/React.createElement("div", {
    className: "rdp-file-upload-dropzone"
  }, /*#__PURE__*/React.createElement("span", {
    className: "rdp-file-upload-icon"
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "upload",
    size: 28
  })), /*#__PURE__*/React.createElement("span", {
    className: "rdp-file-upload-text"
  }, text), /*#__PURE__*/React.createElement("span", {
    className: "rdp-file-upload-subtext"
  }, subtext))), fileName ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-file-upload-info"
  }, fileName) : null, error ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-file-upload-error"
  }, error) : null);
}
Object.assign(__ds_scope, { FileUpload });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/FileUpload.jsx", error: String((e && e.message) || e) }); }

// components/forms/SearchBox.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function SearchBox({
  placeholder = 'Search\u2026',
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "rdp-search-wrapper"
  }, /*#__PURE__*/React.createElement("span", {
    className: "rdp-search-icon"
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "search",
    size: 14
  })), /*#__PURE__*/React.createElement("input", _extends({
    type: "search",
    className: "rdp-input rdp-search-input",
    placeholder: placeholder
  }, rest)));
}
Object.assign(__ds_scope, { SearchBox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/SearchBox.jsx", error: String((e && e.message) || e) }); }

// components/layout/Sidebar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Sidebar({
  brand,
  sections,
  footer,
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("aside", _extends({
    className: "rdp-sidebar is-open",
    style: {
      position: 'relative',
      transform: 'none',
      height: '100%',
      width: 260,
      flexShrink: 0,
      background: '#1C1B18',
      color: 'rgba(255,255,255,0.72)',
      border: 'none',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("a", {
    className: "rdp-sidebar__brand",
    href: "#"
  }, brand), /*#__PURE__*/React.createElement("nav", {
    className: "rdp-sidebar__nav"
  }, sections.map((sec, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "rdp-sidebar__section"
  }, sec.title ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-sidebar__section-title"
  }, sec.title) : null, sec.links.map((l, j) => /*#__PURE__*/React.createElement("a", {
    key: j,
    href: "#",
    onClick: e => {
      e.preventDefault();
      l.onClick && l.onClick();
    },
    className: 'rdp-sidebar__link' + (l.active ? ' active' : '')
  }, l.icon ? /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: l.icon,
    size: 18
  }) : null, /*#__PURE__*/React.createElement("span", {
    className: "rdp-sidebar__link-text"
  }, l.label), l.badge ? /*#__PURE__*/React.createElement("span", {
    className: "rdp-sidebar__badge"
  }, l.badge) : null))))), footer ? /*#__PURE__*/React.createElement("div", {
    className: "rdp-sidebar__footer"
  }, footer) : null);
}
Object.assign(__ds_scope, { Sidebar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/layout/Sidebar.jsx", error: String((e && e.message) || e) }); }

// components/layout/Topbar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Topbar({
  title,
  actions,
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("header", _extends({
    className: "rdp-dashboard-topbar"
  }, rest), /*#__PURE__*/React.createElement("button", {
    className: "rdp-dashboard-topbar__toggle",
    "aria-label": "Menu"
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "menu",
    size: 18
  })), /*#__PURE__*/React.createElement("span", {
    className: "rdp-dashboard-topbar__title"
  }, title), children, /*#__PURE__*/React.createElement("div", {
    className: "rdp-dashboard-topbar__actions"
  }, actions));
}
Object.assign(__ds_scope, { Topbar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/layout/Topbar.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Loader.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Loader({
  size = 'md',
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({
    className: 'rdp-loader rdp-loader--' + size
  }, rest), /*#__PURE__*/React.createElement("span", {
    className: "rdp-loader__spinner"
  }));
}
Object.assign(__ds_scope, { Loader });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Loader.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Progress.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Progress({
  value = 0,
  variant,
  indeterminate = false,
  ...rest
}) {
  const cls = ['rdp-progress', variant ? 'rdp-progress--' + variant : '', indeterminate ? 'rdp-progress--indeterminate' : ''].filter(Boolean).join(' ');
  return /*#__PURE__*/React.createElement("div", _extends({
    className: cls,
    role: "progressbar",
    "aria-valuenow": indeterminate ? undefined : value,
    "aria-valuemin": 0,
    "aria-valuemax": 100
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: "rdp-progress__bar",
    style: indeterminate ? undefined : {
      width: value + '%'
    }
  }));
}
Object.assign(__ds_scope, { Progress });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Progress.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Rating.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Rating({
  value = 0,
  max = 5,
  readonly = false,
  onChange,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({
    className: 'rdp-rating' + (readonly ? ' rdp-rating--readonly' : '')
  }, rest), /*#__PURE__*/React.createElement("span", {
    className: "rdp-rating__stars"
  }, Array.from({
    length: max
  }, (_, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    className: 'rdp-rating__star' + (i < value ? ' rdp-rating__star--active' : ''),
    onClick: readonly ? undefined : () => onChange && onChange(i + 1)
  }, '\u2605'))));
}
Object.assign(__ds_scope, { Rating });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Rating.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Skeleton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Skeleton({
  width = '100%',
  height = 14,
  circle = false,
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({
    className: 'rdp-skeleton' + (circle ? ' rdp-skeleton--circle' : ''),
    style: {
      width,
      height,
      display: 'block',
      ...style
    }
  }, rest));
}
Object.assign(__ds_scope, { Skeleton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Skeleton.jsx", error: String((e && e.message) || e) }); }

// components/primitives/Spinner.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Spinner({
  size = 'md',
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({
    className: 'rdp-spinner rdp-spinner--' + size
  }, rest));
}
Object.assign(__ds_scope, { Spinner });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/primitives/Spinner.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/app.jsx
try { (() => {
const NS = window.RDPUIDesignSystem_ee4ae1;
const {
  Icon,
  Button,
  Badge,
  Avatar,
  AvatarGroup,
  Spinner,
  Progress,
  FormField,
  Input,
  Select,
  Checkbox,
  SearchBox,
  Alert,
  Toast,
  ToastContainer,
  Modal,
  Drawer,
  Tooltip,
  EmptyState,
  Tabs,
  Dropdown,
  Pagination,
  Breadcrumb,
  Card,
  StatCard,
  Table,
  Timeline,
  FilterBar,
  BrandMark,
  Sidebar,
  Topbar,
  PageHeader
} = NS;
const {
  useState
} = React;
const INVOICES = [{
  inv: 'INV-0042',
  client: 'PT Cahaya Abadi',
  issued: 'Jul 12, 2026',
  due: 'Jul 26, 2026',
  amount: 'Rp 12.500.000',
  status: 'paid'
}, {
  inv: 'INV-0041',
  client: 'CV Mitra Jaya',
  issued: 'Jul 10, 2026',
  due: 'Jul 24, 2026',
  amount: 'Rp 4.750.000',
  status: 'pending'
}, {
  inv: 'INV-0040',
  client: 'PT Nusantara Tech',
  issued: 'Jun 28, 2026',
  due: 'Jul 12, 2026',
  amount: 'Rp 21.000.000',
  status: 'overdue'
}, {
  inv: 'INV-0039',
  client: 'PT Sinar Terang',
  issued: 'Jun 25, 2026',
  due: 'Jul 09, 2026',
  amount: 'Rp 8.200.000',
  status: 'paid'
}, {
  inv: 'INV-0038',
  client: 'CV Karya Mandiri',
  issued: 'Jun 20, 2026',
  due: 'Jul 04, 2026',
  amount: 'Rp 3.150.000',
  status: 'pending'
}, {
  inv: 'INV-0037',
  client: 'PT Bumi Sejahtera',
  issued: 'Jun 15, 2026',
  due: 'Jun 29, 2026',
  amount: 'Rp 15.900.000',
  status: 'overdue'
}];
const EMPLOYEES = [{
  name: 'Sari Wulandari',
  init: 'SW',
  role: 'Finance Lead',
  dept: 'Finance',
  status: 'active',
  email: 'sari@radian.web.id',
  joined: 'Mar 2023'
}, {
  name: 'Andi Rahman',
  init: 'AR',
  role: 'Platform Engineer',
  dept: 'Engineering',
  status: 'active',
  email: 'andi@radian.web.id',
  joined: 'Jan 2022'
}, {
  name: 'Dewi Kusuma',
  init: 'DK',
  role: 'Ops Manager',
  dept: 'Operations',
  status: 'leave',
  email: 'dewi@radian.web.id',
  joined: 'Aug 2024'
}, {
  name: 'Budi Santoso',
  init: 'BS',
  role: 'Account Executive',
  dept: 'Sales',
  status: 'active',
  email: 'budi@radian.web.id',
  joined: 'Nov 2023'
}, {
  name: 'Rina Hartati',
  init: 'RH',
  role: 'HR Generalist',
  dept: 'People',
  status: 'inactive',
  email: 'rina@radian.web.id',
  joined: 'Feb 2021'
}];
const SB = {
  paid: ['success', 'Paid'],
  pending: ['warning', 'Pending'],
  overdue: ['danger', 'Overdue'],
  active: ['success', 'Active'],
  leave: ['warning', 'On leave'],
  inactive: ['neutral', 'Inactive']
};
const StatusBadge = ({
  s
}) => /*#__PURE__*/React.createElement(Badge, {
  variant: SB[s][0],
  dot: true
}, SB[s][1]);
const BARS = [42, 58, 50, 74, 66, 88, 80, 95, 72, 105, 98, 118];
const MONTHS = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
function Login({
  onSignIn
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "rdp-layout-blank"
  }, /*#__PURE__*/React.createElement("div", {
    className: "rdp-blank"
  }, /*#__PURE__*/React.createElement("div", {
    className: "rdp-blank__card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "rdp-blank__logo",
    style: {
      display: 'flex',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement(BrandMark, {
    size: 40
  })), /*#__PURE__*/React.createElement("h1", {
    className: "rdp-blank__title"
  }, "Welcome back"), /*#__PURE__*/React.createElement("p", {
    className: "rdp-blank__subtitle"
  }, "Sign in to Radian Data Platform"), /*#__PURE__*/React.createElement("form", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16
    },
    onSubmit: e => {
      e.preventDefault();
      onSignIn();
    }
  }, /*#__PURE__*/React.createElement(FormField, {
    label: "Email"
  }, /*#__PURE__*/React.createElement(Input, {
    type: "email",
    defaultValue: "admin@radian.web.id"
  })), /*#__PURE__*/React.createElement(FormField, {
    label: "Password"
  }, /*#__PURE__*/React.createElement(Input, {
    type: "password",
    defaultValue: "password"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(Checkbox, {
    label: "Remember me",
    defaultChecked: true
  }), /*#__PURE__*/React.createElement("a", {
    className: "rdp-link",
    href: "#",
    style: {
      fontSize: 13
    },
    onClick: e => e.preventDefault()
  }, "Forgot password?")), /*#__PURE__*/React.createElement(Button, {
    fullWidth: true,
    type: "submit"
  }, "Sign in")), /*#__PURE__*/React.createElement("div", {
    className: "rdp-blank__divider"
  }, "or"), /*#__PURE__*/React.createElement(Button, {
    variant: "outline",
    fullWidth: true
  }, "Continue with SSO"), /*#__PURE__*/React.createElement("div", {
    className: "rdp-blank__footer"
  }, "No account? ", /*#__PURE__*/React.createElement("a", {
    href: "#",
    onClick: e => e.preventDefault()
  }, "Contact your administrator")))));
}
function DashboardView({
  toast
}) {
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(PageHeader, {
    title: "Dashboard",
    actions: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Button, {
      variant: "outline",
      size: "sm"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "download",
      size: 14
    }), "Export"), /*#__PURE__*/React.createElement(Button, {
      size: "sm",
      onClick: () => toast('success', 'Report scheduled', 'Monthly summary will be emailed at 07:00.')
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "plus",
      size: 14
    }), "New report"))
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4,1fr)',
      gap: 16,
      marginBottom: 24
    }
  }, /*#__PURE__*/React.createElement(StatCard, {
    label: "Monthly revenue",
    value: "Rp 128,4 jt",
    change: "+12.4% vs last month",
    direction: "up"
  }), /*#__PURE__*/React.createElement(StatCard, {
    label: "Open invoices",
    value: "23",
    change: "Rp 64,2 jt outstanding",
    direction: "neutral"
  }), /*#__PURE__*/React.createElement(StatCard, {
    label: "Overdue",
    value: "7",
    change: "+2 this week",
    direction: "down"
  }), /*#__PURE__*/React.createElement(StatCard, {
    label: "Active clients",
    value: "48",
    change: "+3 this month",
    direction: "up"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '2fr 1fr',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "Revenue",
    header: /*#__PURE__*/React.createElement(Badge, {
      variant: "neutral"
    }, "Last 12 months")
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-end',
      gap: 10,
      height: 180,
      paddingTop: 8
    }
  }, BARS.map((h, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 6
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%',
      height: h,
      background: i === BARS.length - 1 ? 'var(--rdp-primary)' : 'var(--rdp-green-100)',
      borderRadius: '4px 4px 0 0',
      transition: 'background var(--rdp-transition)'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10,
      fontFamily: 'var(--rdp-font-mono)',
      color: 'var(--rdp-text-muted)'
    }
  }, MONTHS[i]))))), /*#__PURE__*/React.createElement(Card, {
    title: "Activity"
  }, /*#__PURE__*/React.createElement(Timeline, {
    items: [{
      title: 'Invoice paid',
      desc: 'INV-0042 · Rp 12.500.000',
      time: '09:41',
      active: true
    }, {
      title: 'New client added',
      desc: 'PT Cahaya Abadi',
      time: '08:15'
    }, {
      title: 'Reminder sent',
      desc: 'INV-0040 · 3rd notice',
      time: 'Yesterday'
    }, {
      title: 'Payroll approved',
      desc: 'July · 5 employees',
      time: 'Jul 18'
    }]
  }))));
}
function InvoicesView({
  toast
}) {
  const [q, setQ] = useState('');
  const [tab, setTab] = useState('all');
  const [page, setPage] = useState(1);
  const [modal, setModal] = useState(false);
  const rows = INVOICES.filter(r => (tab === 'all' || r.status === tab) && (r.inv + r.client).toLowerCase().includes(q.toLowerCase()));
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Breadcrumb, {
    items: [{
      label: 'Workspace',
      href: '#'
    }, {
      label: 'Invoices'
    }]
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 8
    }
  }), /*#__PURE__*/React.createElement(PageHeader, {
    title: "Invoices",
    actions: /*#__PURE__*/React.createElement(Button, {
      size: "sm",
      onClick: () => setModal(true)
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "plus",
      size: 14
    }), "New invoice")
  }), /*#__PURE__*/React.createElement(Tabs, {
    tabs: [{
      id: 'all',
      label: 'All'
    }, {
      id: 'paid',
      label: 'Paid'
    }, {
      id: 'pending',
      label: 'Pending'
    }, {
      id: 'overdue',
      label: 'Overdue'
    }],
    active: tab,
    onChange: setTab
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 16
    }
  }), /*#__PURE__*/React.createElement(FilterBar, {
    actions: /*#__PURE__*/React.createElement(Button, {
      variant: "outline",
      size: "sm",
      onClick: () => toast('info', 'Export started', 'invoices-jul-2026.csv is being prepared.')
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "download",
      size: 14
    }), "Export")
  }, /*#__PURE__*/React.createElement(SearchBox, {
    placeholder: "Search invoices\u2026",
    value: q,
    onChange: e => setQ(e.target.value)
  }), /*#__PURE__*/React.createElement(Select, {
    options: [{
      value: '30',
      label: 'Last 30 days'
    }, {
      value: '90',
      label: 'Last quarter'
    }, {
      value: '365',
      label: 'This year'
    }]
  })), rows.length === 0 ? /*#__PURE__*/React.createElement(EmptyState, {
    icon: "inbox",
    title: "No matching invoices",
    description: "Try a different search or status filter.",
    action: /*#__PURE__*/React.createElement(Button, {
      size: "sm",
      variant: "outline",
      onClick: () => {
        setQ('');
        setTab('all');
      }
    }, "Clear filters")
  }) : /*#__PURE__*/React.createElement(Table, {
    hoverable: true,
    columns: [{
      key: 'inv',
      label: 'Invoice'
    }, {
      key: 'client',
      label: 'Client'
    }, {
      key: 'issued',
      label: 'Issued'
    }, {
      key: 'due',
      label: 'Due'
    }, {
      key: 'amount',
      label: 'Amount'
    }, {
      key: 'status',
      label: 'Status'
    }],
    rows: rows,
    renderCell: (r, k) => k === 'status' ? /*#__PURE__*/React.createElement(StatusBadge, {
      s: r.status
    }) : k === 'amount' ? /*#__PURE__*/React.createElement("span", {
      className: "rdp-numeric",
      style: {
        fontFamily: 'var(--rdp-font-mono)',
        fontSize: 13
      }
    }, r.amount) : r[k]
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginTop: 16
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "rdp-caption"
  }, rows.length, " of ", INVOICES.length, " invoices"), /*#__PURE__*/React.createElement(Pagination, {
    page: page,
    pages: 3,
    onChange: setPage
  })), modal ? /*#__PURE__*/React.createElement(Modal, {
    title: "New invoice",
    onClose: () => setModal(false),
    footer: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Button, {
      variant: "outline",
      onClick: () => setModal(false)
    }, "Cancel"), /*#__PURE__*/React.createElement(Button, {
      onClick: () => {
        setModal(false);
        toast('success', 'Invoice created', 'INV-0043 saved as draft.');
      }
    }, "Create invoice"))
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(FormField, {
    label: "Client",
    required: true
  }, /*#__PURE__*/React.createElement(Select, {
    options: [{
      value: '1',
      label: 'PT Cahaya Abadi'
    }, {
      value: '2',
      label: 'CV Mitra Jaya'
    }, {
      value: '3',
      label: 'PT Nusantara Tech'
    }]
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(FormField, {
    label: "Amount",
    required: true
  }, /*#__PURE__*/React.createElement(Input, {
    placeholder: "Rp 0"
  })), /*#__PURE__*/React.createElement(FormField, {
    label: "Due date",
    required: true
  }, /*#__PURE__*/React.createElement(Input, {
    type: "date",
    defaultValue: "2026-08-04"
  }))), /*#__PURE__*/React.createElement(FormField, {
    label: "Notes",
    help: "Shown on the invoice footer"
  }, /*#__PURE__*/React.createElement(Input, {
    placeholder: "Payment terms, PO number\u2026"
  })))) : null);
}
function EmployeesView({
  toast
}) {
  const [q, setQ] = useState('');
  const [emp, setEmp] = useState(null);
  const rows = EMPLOYEES.filter(r => (r.name + r.role + r.dept).toLowerCase().includes(q.toLowerCase()));
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(PageHeader, {
    title: "Employees",
    actions: /*#__PURE__*/React.createElement(Button, {
      size: "sm",
      onClick: () => toast('info', 'Invite sent', 'An onboarding invite email was sent.')
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "plus",
      size: 14
    }), "Add employee")
  }), /*#__PURE__*/React.createElement(FilterBar, {
    actions: /*#__PURE__*/React.createElement(Button, {
      variant: "outline",
      size: "sm"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "filter",
      size: 14
    }), "Filters")
  }, /*#__PURE__*/React.createElement(SearchBox, {
    placeholder: "Search employees\u2026",
    value: q,
    onChange: e => setQ(e.target.value)
  }), /*#__PURE__*/React.createElement(Select, {
    options: [{
      value: 'all',
      label: 'All departments'
    }, {
      value: 'fin',
      label: 'Finance'
    }, {
      value: 'eng',
      label: 'Engineering'
    }]
  })), /*#__PURE__*/React.createElement(Table, {
    hoverable: true,
    columns: [{
      key: 'name',
      label: 'Name'
    }, {
      key: 'role',
      label: 'Role'
    }, {
      key: 'dept',
      label: 'Department'
    }, {
      key: 'joined',
      label: 'Joined'
    }, {
      key: 'status',
      label: 'Status'
    }, {
      key: 'act',
      label: ''
    }],
    rows: rows,
    renderCell: (r, k) => k === 'status' ? /*#__PURE__*/React.createElement(StatusBadge, {
      s: r.status
    }) : k === 'name' ? /*#__PURE__*/React.createElement("span", {
      style: {
        display: 'inline-flex',
        alignItems: 'center',
        gap: 10
      }
    }, /*#__PURE__*/React.createElement(Avatar, {
      size: "sm"
    }, r.init), /*#__PURE__*/React.createElement("span", {
      style: {
        fontWeight: 500
      }
    }, r.name)) : k === 'act' ? /*#__PURE__*/React.createElement(Button, {
      variant: "ghost",
      size: "sm",
      onClick: () => setEmp(r)
    }, "View") : r[k]
  }), emp ? /*#__PURE__*/React.createElement(Drawer, {
    title: "Employee",
    onClose: () => setEmp(null),
    footer: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Button, {
      variant: "outline",
      onClick: () => setEmp(null)
    }, "Close"), /*#__PURE__*/React.createElement(Button, {
      onClick: () => {
        setEmp(null);
        toast('success', 'Profile updated', 'Changes saved for ' + emp.name + '.');
      }
    }, "Save changes"))
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(Avatar, {
    size: "lg"
  }, emp.init), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontWeight: 700,
      fontSize: 16
    }
  }, emp.name), /*#__PURE__*/React.createElement("div", {
    className: "rdp-caption"
  }, emp.role, " \xB7 ", emp.dept)), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: 'auto'
    }
  }, /*#__PURE__*/React.createElement(StatusBadge, {
    s: emp.status
  }))), /*#__PURE__*/React.createElement(FormField, {
    label: "Email"
  }, /*#__PURE__*/React.createElement(Input, {
    defaultValue: emp.email
  })), /*#__PURE__*/React.createElement(FormField, {
    label: "Department"
  }, /*#__PURE__*/React.createElement(Select, {
    options: [{
      value: emp.dept,
      label: emp.dept
    }, {
      value: 'Engineering',
      label: 'Engineering'
    }, {
      value: 'Finance',
      label: 'Finance'
    }]
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "rdp-form-field__label",
    style: {
      marginBottom: 10
    }
  }, "Recent activity"), /*#__PURE__*/React.createElement(Timeline, {
    items: [{
      title: 'Leave request approved',
      desc: 'Aug 3–7 · Annual leave',
      time: 'Jul 15',
      active: true
    }, {
      title: 'Payroll processed',
      desc: 'June salary',
      time: 'Jul 01'
    }, {
      title: 'Joined ' + emp.dept,
      time: emp.joined
    }]
  })))) : null);
}
function App() {
  const [signedIn, setSignedIn] = useState(false);
  const [view, setView] = useState('dashboard');
  const [toasts, setToasts] = useState([]);
  const toast = (variant, title, message) => {
    const id = Date.now();
    setToasts(t => [...t, {
      id,
      variant,
      title,
      message
    }]);
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), 4500);
  };
  if (!signedIn) return /*#__PURE__*/React.createElement(Login, {
    onSignIn: () => setSignedIn(true)
  });
  const VIEWS = {
    dashboard: DashboardView,
    invoices: InvoicesView,
    employees: EmployeesView
  };
  const View = VIEWS[view];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      height: '100%',
      background: 'var(--rdp-background)'
    }
  }, /*#__PURE__*/React.createElement(Sidebar, {
    brand: /*#__PURE__*/React.createElement(BrandMark, {
      dark: true,
      size: 26
    }),
    sections: [{
      title: 'Workspace',
      links: [{
        label: 'Dashboard',
        icon: 'dashboard',
        active: view === 'dashboard',
        onClick: () => setView('dashboard')
      }, {
        label: 'Invoices',
        icon: 'file-text',
        badge: '7',
        active: view === 'invoices',
        onClick: () => setView('invoices')
      }, {
        label: 'Employees',
        icon: 'users',
        active: view === 'employees',
        onClick: () => setView('employees')
      }, {
        label: 'Reports',
        icon: 'folder',
        onClick: () => toast('info', 'Not in this demo', 'Reports are part of the full RDP suite.')
      }]
    }, {
      title: 'Settings',
      links: [{
        label: 'Team',
        icon: 'user',
        onClick: () => toast('info', 'Not in this demo', 'Team settings are part of the full RDP suite.')
      }, {
        label: 'Preferences',
        icon: 'settings',
        onClick: () => toast('info', 'Not in this demo', 'Preferences are part of the full RDP suite.')
      }]
    }],
    footer: /*#__PURE__*/React.createElement("a", {
      href: "#",
      className: "rdp-sidebar__link",
      onClick: e => {
        e.preventDefault();
        setSignedIn(false);
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "log-out",
      size: 18
    }), /*#__PURE__*/React.createElement("span", {
      className: "rdp-sidebar__link-text"
    }, "Sign out"))
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement(Topbar, {
    title: "Radian Data Platform",
    actions: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Tooltip, {
      label: "Notifications",
      position: "bottom"
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "ghost",
      iconOnly: true,
      size: "sm",
      onClick: () => toast('info', 'You are all caught up', 'No unread notifications.')
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "bell",
      size: 16
    }))), /*#__PURE__*/React.createElement(Avatar, {
      size: "sm"
    }, "AR"))
  }), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      overflowY: 'auto',
      padding: '24px 32px'
    }
  }, /*#__PURE__*/React.createElement(View, {
    toast: toast
  }))), /*#__PURE__*/React.createElement(ToastContainer, {
    position: "bottom-right"
  }, toasts.map(t => /*#__PURE__*/React.createElement(Toast, {
    key: t.id,
    variant: t.variant,
    title: t.title,
    message: t.message,
    onDismiss: () => setToasts(x => x.filter(y => y.id !== t.id))
  }))));
}
ReactDOM.createRoot(document.getElementById('root')).render(/*#__PURE__*/React.createElement(App, null));
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/app.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Accordion = __ds_scope.Accordion;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.FilterBar = __ds_scope.FilterBar;

__ds_ns.StatCard = __ds_scope.StatCard;

__ds_ns.Table = __ds_scope.Table;

__ds_ns.Timeline = __ds_scope.Timeline;

__ds_ns.Alert = __ds_scope.Alert;

__ds_ns.Confirm = __ds_scope.Confirm;

__ds_ns.Drawer = __ds_scope.Drawer;

__ds_ns.EmptyState = __ds_scope.EmptyState;

__ds_ns.Modal = __ds_scope.Modal;

__ds_ns.Toast = __ds_scope.Toast;

__ds_ns.ToastContainer = __ds_scope.ToastContainer;

__ds_ns.Tooltip = __ds_scope.Tooltip;

__ds_ns.Checkbox = __ds_scope.Checkbox;

__ds_ns.FileUpload = __ds_scope.FileUpload;

__ds_ns.FormField = __ds_scope.FormField;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Radio = __ds_scope.Radio;

__ds_ns.SearchBox = __ds_scope.SearchBox;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Switch = __ds_scope.Switch;

__ds_ns.Textarea = __ds_scope.Textarea;

__ds_ns.BrandMark = __ds_scope.BrandMark;

__ds_ns.PageHeader = __ds_scope.PageHeader;

__ds_ns.Sidebar = __ds_scope.Sidebar;

__ds_ns.Topbar = __ds_scope.Topbar;

__ds_ns.Breadcrumb = __ds_scope.Breadcrumb;

__ds_ns.Dropdown = __ds_scope.Dropdown;

__ds_ns.Pagination = __ds_scope.Pagination;

__ds_ns.Steps = __ds_scope.Steps;

__ds_ns.Tabs = __ds_scope.Tabs;

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.AvatarGroup = __ds_scope.AvatarGroup;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Icon = __ds_scope.Icon;

__ds_ns.Loader = __ds_scope.Loader;

__ds_ns.Progress = __ds_scope.Progress;

__ds_ns.Rating = __ds_scope.Rating;

__ds_ns.Skeleton = __ds_scope.Skeleton;

__ds_ns.Spinner = __ds_scope.Spinner;

})();
