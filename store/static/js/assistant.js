// NEXORA AI Shopping Assistant
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
