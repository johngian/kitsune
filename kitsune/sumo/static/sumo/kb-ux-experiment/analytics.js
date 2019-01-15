document.addEventListener('DOMContentLoaded', function() {

  var helpful = document.querySelector("input[name='helpful']");
  var not_helpful = document.querySelector("input[name='not-helpful']");

  function trackEvent(category, action, label, value) {
    if (window.gtag) {
      window.gtag('event', action, {
        'event_category': category,
        'event_label': label,
        'value': value
      });
    }
  }

  helpful.addEventListener('click', function() {
    trackEvent('UX experiment 1', 'helpful article');
  });

  not_helpful.addEventListener('click', function() {
    trackEvent('UX experiment 1', 'not helpful article');
  });
});
