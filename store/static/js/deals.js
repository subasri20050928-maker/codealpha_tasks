// Flash Deals Countdown Timer
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
