# build_all_templates.py
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Ensure directories
os.makedirs("store/templates/store/auth", exist_ok=True)
os.makedirs("store/static/js", exist_ok=True)

# 1. JS files
theme_js = """// NEXORA Theme Switcher
(function() {
  const savedTheme = localStorage.getItem('nexora_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('themeToggleBtn');
    if (toggleBtn) {
      updateIcon(savedTheme);
      toggleBtn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('nexora_theme', next);
        updateIcon(next);
      });
    }
  });

  function updateIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
      icon.innerHTML = theme === 'dark'
        ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
        : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }
  }
})();
"""
with open("store/static/js/theme.js", "w", encoding="utf-8") as f:
    f.write(theme_js)

cart_js = """// NEXORA Cart & Wishlist AJAX Engine
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = 'toast toast-' + type;
  toast.innerHTML = '<span>' + message + '</span>';
  container.appendChild(toast);
  setTimeout(() => { toast.remove(); }, 3500);
}

function flyToCart(startElement) {
  const cartIcon = document.getElementById('navCartBtn');
  if (!startElement || !cartIcon) return;

  const startRect = startElement.getBoundingClientRect();
  const endRect = cartIcon.getBoundingClientRect();

  const ghost = document.createElement('img');
  ghost.src = startElement.src || (startElement.querySelector('img') ? startElement.querySelector('img').src : '');
  if (!ghost.src) return;

  ghost.className = 'flying-ghost';
  ghost.style.left = startRect.left + 'px';
  ghost.style.top = startRect.top + 'px';
  ghost.style.width = startRect.width + 'px';
  ghost.style.height = startRect.height + 'px';
  document.body.appendChild(ghost);

  requestAnimationFrame(() => {
    ghost.style.left = (endRect.left + 10) + 'px';
    ghost.style.top = (endRect.top + 10) + 'px';
    ghost.style.width = '24px';
    ghost.style.height = '24px';
    ghost.style.opacity = '0.3';
  });

  setTimeout(() => {
    ghost.remove();
    const badge = document.getElementById('cartBadge');
    if (badge) {
      badge.classList.add('pulse');
      setTimeout(() => badge.classList.remove('pulse'), 300);
    }
  }, 800);
}

function addToCart(productId, quantity = 1, triggerBtn = null) {
  const csrftoken = getCookie('csrftoken');
  let thumbImg = null;
  if (triggerBtn) {
    const card = triggerBtn.closest('.product-card') || triggerBtn.closest('.product-detail-grid');
    if (card) thumbImg = card.querySelector('img');
  }

  fetch('/api/cart/add/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ product_id: productId, quantity: quantity })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const badge = document.getElementById('cartBadge');
      if (badge) badge.innerText = data.cart_count;
      if (thumbImg) flyToCart(thumbImg);
      showToast(data.message, 'success');
    } else {
      showToast(data.error || 'Could not add to cart', 'error');
    }
  })
  .catch(() => {
    showToast('Network error while updating cart', 'error');
  });
}

function updateCartItem(itemId, action, quantity = 1) {
  const csrftoken = getCookie('csrftoken');
  fetch('/api/cart/update/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ item_id: itemId, action: action, quantity: quantity })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      location.reload();
    }
  });
}

function removeCartItem(itemId) {
  const csrftoken = getCookie('csrftoken');
  fetch('/api/cart/remove/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ item_id: itemId })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      location.reload();
    }
  });
}

function toggleWishlist(productId, btnElement) {
  const csrftoken = getCookie('csrftoken');
  fetch('/api/wishlist/toggle/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ product_id: productId })
  })
  .then(res => res.json())
  .then(data => {
    if (data.login_required) {
      window.location.href = '/login/?next=' + window.location.pathname;
      return;
    }
    if (data.success) {
      if (btnElement) {
        if (data.added) btnElement.classList.add('active');
        else btnElement.classList.remove('active');
      }
      const badge = document.getElementById('wishlistBadge');
      if (badge) badge.innerText = data.wishlist_count;
      showToast(data.message, 'success');
    }
  });
}
"""
with open("store/static/js/cart.js", "w", encoding="utf-8") as f:
    f.write(cart_js)

deals_js = """// Flash Deals Countdown Timer
function initFlashDeals(deadlineStr) {
  const targetDate = new Date(deadlineStr).getTime();

  function update() {
    const now = new Date().getTime();
    const distance = targetDate - now;

    if (distance <= 0) {
      const timerEl = document.getElementById('flashCountdown');
      if (timerEl) timerEl.innerHTML = '<span style="color:var(--accent);font-weight:700">Deals Refreshed!</span>';
      return;
    }

    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    const hEl = document.getElementById('dealHours');
    const mEl = document.getElementById('dealMins');
    const sEl = document.getElementById('dealSecs');

    if (hEl) hEl.innerText = String(hours).padStart(2, '0');
    if (mEl) mEl.innerText = String(minutes).padStart(2, '0');
    if (sEl) sEl.innerText = String(seconds).padStart(2, '0');
  }

  update();
  setInterval(update, 1000);
}
"""
with open("store/static/js/deals.js", "w", encoding="utf-8") as f:
    f.write(deals_js)

assistant_js = """// NEXORA AI Shopping Assistant
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('aiPromptInput');
  const sendBtn = document.getElementById('aiSendBtn');
  const resultsArea = document.getElementById('aiResultsArea');
  const replyBubble = document.getElementById('aiReplyBubble');
  const productCardsGrid = document.getElementById('aiProductsGrid');
  const chips = document.querySelectorAll('.ai-chip');

  if (!input || !sendBtn) return;

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      input.value = chip.getAttribute('data-prompt');
      submitAIQuery(input.value);
    });
  });

  sendBtn.addEventListener('click', () => {
    if (input.value.trim()) submitAIQuery(input.value.trim());
  });

  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && input.value.trim()) {
      submitAIQuery(input.value.trim());
    }
  });

  function submitAIQuery(promptText) {
    sendBtn.disabled = true;
    sendBtn.innerText = 'Analyzing...';
    resultsArea.style.display = 'block';
    replyBubble.innerHTML = '<em>Scanning NEXORA inventory for "' + promptText + '"...</em>';
    productCardsGrid.innerHTML = '';

    const csrftoken = getCookie('csrftoken');

    fetch('/api/ai-assistant/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ prompt: promptText })
    })
    .then(res => res.json())
    .then(data => {
      sendBtn.disabled = false;
      sendBtn.innerText = 'Ask AI';

      if (data.success) {
        replyBubble.innerHTML = data.message;
        let html = '';
        data.products.forEach(p => {
          html += '<div class="product-card">' +
            '<div class="product-thumb-wrap">' +
              '<img src="' + p.image + '" alt="' + p.name + '" class="product-thumb">' +
              (p.discount_percentage ? '<span class="discount-badge">-' + p.discount_percentage + '%</span>' : '') +
            '</div>' +
            '<div class="product-content">' +
              '<div class="product-category-tag">' + p.category + '</div>' +
              '<h4 class="product-name"><a href="' + p.detail_url + '">' + p.name + '</a></h4>' +
              '<div class="product-rating">★ ' + p.rating + ' (' + p.reviews_count + ' reviews)</div>' +
              '<div class="product-price-row">' +
                '<span class="current-price">₹' + p.current_price.toLocaleString('en-IN') + '</span>' +
                (p.price > p.current_price ? '<span class="original-price">₹' + p.price.toLocaleString('en-IN') + '</span>' : '') +
              '</div>' +
              '<div class="product-card-actions">' +
                '<a href="' + p.detail_url + '" class="btn btn-secondary btn-sm">View</a>' +
                '<button onclick="addToCart(' + p.id + ', 1, this)" class="btn btn-primary btn-sm">Add to Cart</button>' +
              '</div>' +
            '</div>' +
          '</div>';
        });
        productCardsGrid.innerHTML = html;
      } else {
        replyBubble.innerText = data.error || 'No recommendations found. Try another prompt.';
      }
    })
    .catch(() => {
      sendBtn.disabled = false;
      sendBtn.innerText = 'Ask AI';
      replyBubble.innerText = 'Sorry, could not process request right now.';
    });
  }
});
"""
with open("store/static/js/assistant.js", "w", encoding="utf-8") as f:
    f.write(assistant_js)

print("[OK] JS files created")
