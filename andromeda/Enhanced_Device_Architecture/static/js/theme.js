document.addEventListener("DOMContentLoaded", () => {
  const selector = document.getElementById("themeSelector");
  const saved = localStorage.getItem("theme") || "dark";
  document.documentElement.className = "theme-" + saved;
  selector.value = saved;

  selector.addEventListener("change", () => {
    const theme = selector.value;
    document.documentElement.className = "theme-" + theme;
    localStorage.setItem("theme", theme);
  });
});