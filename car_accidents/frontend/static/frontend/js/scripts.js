document.querySelector(".js-menu-toggle").addEventListener("click", function (e) {
  document.body.classList.contains("show-sidebar")
    ? (document.body.classList.remove("show-sidebar"), this.classList.remove("active"))
    : (document.body.classList.add("show-sidebar"), this.classList.add("active"));
  e.preventDefault();
});
document.addEventListener("mouseup", function (e) {
  var sidebar_elem = document.querySelector(".sidebar");
  !(sidebar_elem == e.target) &&
    !sidebar_elem.contains(e.target) &&
    document.body.classList.contains("show-sidebar") &&
    (document.body.classList.remove("show-sidebar"),
    document.body.querySelector(".js-menu-toggle").classList.remove("active"));
});
