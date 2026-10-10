/* Styled tooltips for the guide, in place of the browser's own title= tooltips.
   Markup: a trigger with aria-describedby="X" and an element id="X" class="plato-tip"
   role="tooltip". The tip opens on hover and on keyboard focus, stays open while the pointer
   is over it, closes on Esc, and is kept inside the viewport. On a touchscreen the first tap
   on a trigger shows the tip and the second follows the link. The tip is moved to <body> so
   that the sidebar's scrolling and transforms cannot clip or misplace it. */
(() => {
  const GAP = 8, MARGIN = 8;
  let open = null, closeTimer = 0;

  function place(trigger, tip) {
    const r = trigger.getBoundingClientRect();
    const w = tip.offsetWidth, h = tip.offsetHeight;
    const vw = document.documentElement.clientWidth, vh = window.innerHeight;
    let left = Math.min(Math.max(r.left, MARGIN), vw - w - MARGIN);
    let top = r.bottom + GAP;
    if (top + h > vh - MARGIN && r.top - GAP - h >= MARGIN) top = r.top - GAP - h;
    tip.style.left = `${Math.max(left, MARGIN)}px`;
    tip.style.top = `${Math.max(Math.min(top, vh - h - MARGIN), MARGIN)}px`;
  }

  function show(trigger, tip) {
    clearTimeout(closeTimer);
    if (open && open.tip !== tip) hide();
    open = { trigger, tip };
    tip.classList.add("is-open");
    place(trigger, tip);
  }

  function hide() {
    clearTimeout(closeTimer);
    if (!open) return;
    open.tip.classList.remove("is-open");
    open = null;
  }

  const hideSoon = () => { clearTimeout(closeTimer); closeTimer = setTimeout(hide, 150); };

  function init() {
    document.querySelectorAll("[aria-describedby]").forEach((trigger) => {
      const tip = document.getElementById(trigger.getAttribute("aria-describedby"));
      if (!tip || !tip.classList.contains("plato-tip")) return;
      document.body.appendChild(tip);
      let touched = false;
      trigger.addEventListener("pointerenter", (e) => { if (e.pointerType !== "touch") show(trigger, tip); });
      trigger.addEventListener("pointerleave", (e) => { if (e.pointerType !== "touch") hideSoon(); });
      tip.addEventListener("pointerenter", () => clearTimeout(closeTimer));
      tip.addEventListener("pointerleave", hideSoon);
      trigger.addEventListener("focus", () => { if (!touched) show(trigger, tip); });
      trigger.addEventListener("blur", hide);
      trigger.addEventListener("pointerdown", (e) => { touched = e.pointerType === "touch"; });
      trigger.addEventListener("click", (e) => {
        if (touched && !(open && open.tip === tip)) { e.preventDefault(); show(trigger, tip); }
        touched = false;
      });
    });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") hide(); });
    document.addEventListener("pointerdown", (e) => {
      if (open && !open.trigger.contains(e.target) && !open.tip.contains(e.target)) hide();
    });
    const reposition = () => { if (open) place(open.trigger, open.tip); };
    window.addEventListener("resize", reposition);
    document.addEventListener("scroll", reposition, true);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
