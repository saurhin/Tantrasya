// Mobile navigation toggle
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("mobile-nav");
  if (!toggle || !menu) return;

  toggle.addEventListener("click", function () {
    var open = menu.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
})();

// Contact form — submits to Formspree without leaving the page
(function () {
  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = document.getElementById("form-status");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Honeypot check — if filled, silently pretend success (it's a bot)
    var honeypot = form.querySelector('input[name="_gotcha"]');
    if (honeypot && honeypot.value) {
      showStatus("success", "Thank you for reaching out to Tantrasya. Your message has been received.");
      form.reset();
      return;
    }

    var submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";

    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" },
    })
      .then(function (response) {
        if (response.ok) {
          showStatus("success", "Thank you for reaching out to Tantrasya. Your message has been received — we'll be in touch soon.");
          form.reset();
        } else {
          showStatus("error", "Your message could not be sent. Please try again, or email us directly.");
        }
      })
      .catch(function () {
        showStatus("error", "Your message could not be sent. Please check your connection and try again.");
      })
      .finally(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = "Send message";
      });
  });

  function showStatus(type, message) {
    status.textContent = message;
    status.className = "form-status show " + type;
    status.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
})();

// Blog category filter — client-side, no page reload. Filters post cards
// by data-category and hides any year group left with nothing visible.
(function () {
  var filterBar = document.getElementById("blog-filter");
  if (!filterBar) return;

  var buttons = filterBar.querySelectorAll("button");
  var cards = document.querySelectorAll(".post-card");
  var yearGroups = document.querySelectorAll(".blog-year-group");
  var emptyState = document.getElementById("blog-empty-state");

  filterBar.addEventListener("click", function (e) {
    var btn = e.target.closest("button");
    if (!btn) return;

    buttons.forEach(function (b) { b.classList.remove("active"); });
    btn.classList.add("active");

    var filter = btn.getAttribute("data-filter");
    var anyVisible = false;

    cards.forEach(function (card) {
      var match = filter === "all" || card.getAttribute("data-category") === filter;
      card.classList.toggle("is-hidden", !match);
      if (match) anyVisible = true;
    });

    yearGroups.forEach(function (group) {
      var hasVisibleCard = group.querySelector(".post-card:not(.is-hidden)");
      group.hidden = !hasVisibleCard;
    });

    if (emptyState) emptyState.hidden = anyVisible;
  });
})();
