// NEXORA Cart & Wishlist AJAX Engine
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
