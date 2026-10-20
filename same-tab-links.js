// The sidebar shortcuts to other sections (Developer Tools, API Reference) are pages on this site,
// but Mintlify opens them in a new browser tab. Keep internal links in the same tab.
document.addEventListener(
  "click",
  (event) => {
    const link = event.target.closest('a[target="_blank"][href^="/"]');
    if (!link || event.metaKey || event.ctrlKey || event.shiftKey) return;
    event.preventDefault();
    event.stopPropagation();
    window.location.assign(link.getAttribute("href"));
  },
  true
);
