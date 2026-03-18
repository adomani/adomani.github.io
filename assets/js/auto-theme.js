// Auto-switch Minimal Mistakes skin based on OS preference.
// This MUST run before the theme loads its CSS.

(function() {
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (prefersDark) {
    // Minimal Mistakes loads dark skin automatically when this attribute is set.
    document.documentElement.setAttribute("data-theme", "dark");
  } else {
    document.documentElement.setAttribute("data-theme", "default");
  }
})();
