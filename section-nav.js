// Product and Developer tools sections have their own sidebar. Add a link back to the main
// docs at the top of it, and mark the section name so it reads as the sidebar's title.
(() => {
  const SECTIONS = [
    "/virtual-accounts/", "/payments/", "/payouts/", "/fx-and-conversion/",
    "/direct-debit/", "/issuing/", "/verification/", "/developer-tools/",
  ];

  const apply = () => {
    const nav = document.getElementById("navigation-items");
    if (!nav) return;
    const inSection = SECTIONS.some((prefix) => window.location.pathname.startsWith(prefix));
    const existing = nav.querySelector(".fincra-back");
    const firstHeader = nav.querySelector(".sidebar-group-header");

    if (!inSection) {
      existing?.remove();
      nav.querySelectorAll(".fincra-section-title").forEach((el) => el.classList.remove("fincra-section-title"));
      return;
    }
    if (firstHeader && !firstHeader.classList.contains("fincra-section-title")) {
      firstHeader.classList.add("fincra-section-title");
    }
    if (!existing && firstHeader) {
      const back = document.createElement("a");
      back.className = "fincra-back";
      back.href = "/";
      back.textContent = "← All documentation";
      firstHeader.parentElement.insertBefore(back, firstHeader);
    }
  };

  new MutationObserver(apply).observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener("DOMContentLoaded", apply);
  apply();
})();
