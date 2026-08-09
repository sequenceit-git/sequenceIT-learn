"use strict";

// ── Sidebar toggle ─────────────────────────────────
function toggleSidebar() {
  var sideNav = document.getElementById("side-nav");
  var main    = document.getElementById("main");
  var topNav  = document.getElementById("top-navbar");
  if (sideNav) sideNav.classList.toggle("toggle-active");
  if (main)    main.classList.toggle("toggle-active");
  if (topNav)  topNav.classList.toggle("toggle-active");
}

// ── Form validation ────────────────────────────────
var forms = document.getElementsByClassName("needs-validation");
Array.prototype.filter.call(forms, function (form) {
  form.addEventListener("submit", function (event) {
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }
    form.classList.add("was-validated");
  }, false);
});

// ── Popup helper ───────────────────────────────────
var c = 0;
function pop() {
  if (c === 0) {
    document.getElementById("popup-box").style.display = "block";
    c = 1;
  } else {
    document.getElementById("popup-box").style.display = "none";
    c = 0;
  }
}

// ── Expand / Collapse course list ─────────────────
var collapsed = true;
function showCourses(btn) {
  var $btn = $(btn);
  if (collapsed) {
    $btn.html('Collapse <i class="fas fa-angle-up"></i>');
    $(".hide").css("max-height", "unset");
    $(".white-shadow").css({ background: "unset", "z-index": "0" });
  } else {
    $btn.html('Expand <i class="fas fa-angle-down"></i>');
    $(".hide").css("max-height", "150px");
    $(".white-shadow").css({
      background: "linear-gradient(transparent 50%, rgba(255,255,255,.8) 80%)",
      "z-index": "2",
    });
  }
  collapsed = !collapsed;
}

// ── Search focus dim effect ────────────────────────
$(document).ready(function () {
  $("#primary-search").focus(function () {
    $("#top-navbar").addClass("dim");
    $("#side-nav").css("pointer-events", "none");
    $("#main-content").css("pointer-events", "none");
  });
  $("#primary-search").focusout(function () {
    $("#top-navbar").removeClass("dim");
    $("#side-nav").css("pointer-events", "auto");
    $("#main-content").css("pointer-events", "auto");
  });
});
