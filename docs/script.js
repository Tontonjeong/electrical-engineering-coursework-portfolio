const projectLinks = document.querySelectorAll("[data-track]");
projectLinks.forEach((link) => {
  link.addEventListener("click", () => {
    document.documentElement.dataset.lastNavigation = link.dataset.track;
  });
});

const yearNodes = document.querySelectorAll("[data-year]");
yearNodes.forEach((node) => {
  node.textContent = new Date().getFullYear();
});
