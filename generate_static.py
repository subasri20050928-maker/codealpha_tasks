# generate_static.py
import os

css_content = """/* NEXORA Modern Startup CSS */
:root {
  --font-main: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --bg-body: #0a0c14;
  --bg-surface: #111422;
  --bg-card: rgba(22, 27, 44, 0.75);
  --bg-card-hover: rgba(30, 37, 60, 0.9);
  --bg-glass: rgba(17, 20, 34, 0.85);
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-accent: rgba(99, 102, 241, 0.35);
  --border-focus: #6366f1;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  --primary: #6366f1;
  --primary-hover: #4f46e5;
  --primary-glow: rgba(99, 102, 241, 0.4);
  --secondary: #8b5cf6;
  --accent: #ec4899;
  --accent-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  --hero-gradient: radial-gradient(circle at 50% -20%, rgba(99, 102, 241, 0.3), transparent 70%);
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.6);
  --shadow-glow: 0 0 25px rgba(99, 102, 241, 0.3);
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 22px;
  --radius-full: 9999px;
  --header-height: 76px;
  --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-theme="light"] {
  --bg-body: #f8fafc;
  --bg-surface: #ffffff;
  --bg-card: #ffffff;
  --bg-card-hover: #f1f5f9;
  --bg-glass: rgba(255, 255, 255, 0.9);
  --border-subtle: rgba(0, 0, 0, 0.08);
  --border-accent: rgba(99, 102, 241, 0.25);
  --border-focus: #6366f1;
  --text-main: #0f172a;
  --text-muted: #475569;
  --text-dim: #94a3b8;
  --primary: #4f46e5;
  --primary-hover: #4338ca;
  --primary-glow: rgba(79, 70, 229, 0.2);
  --hero-gradient: radial-gradient(circle at 50% -20%, rgba(99, 102, 241, 0.12), transparent 70%);
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.12);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font-main);
  background-color: var(--bg-body);
  color: var(--text-main);
  line-height: 1.6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease, color 0.3s ease;
}
a { color: inherit; text-decoration: none; transition: var(--transition); }
img { max-width: 100%; height: auto; display: block; }
button, input, select, textarea { font-family: inherit; font-size: 1rem; }

.container { width: 100%; max-width: 1280px; margin: 0 auto; padding: 0 1.5rem; }

/* Navbar */
.navbar {
  position: sticky; top: 0; z-index: 1000;
  height: var(--header-height);
  background: var(--bg-glass);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border-subtle);
}
.navbar .container {
  height: 100%; display: flex; align-items: center; justify-content: space-between; gap: 1.5rem;
}
.brand-logo {
  display: flex; align-items: center; gap: 0.5rem;
  font-weight: 800; font-size: 1.6rem; letter-spacing: -0.5px;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.nav-links { display: flex; align-items: center; gap: 1.75rem; list-style: none; }
.nav-link { font-size: 0.95rem; font-weight: 500; color: var(--text-muted); padding: 0.5rem 0; position: relative; }
.nav-link:hover, .nav-link.active { color: var(--text-main); }
.nav-link.active::after {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
  background: var(--primary); border-radius: var(--radius-full);
}

/* Nav Search */
.nav-search-box { position: relative; flex: 1; max-width: 380px; }
.nav-search-input {
  width: 100%; padding: 0.6rem 1rem 0.6rem 2.6rem;
  background: var(--bg-surface); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-full); color: var(--text-main); font-size: 0.9rem; outline: none;
}
.nav-search-input:focus { border-color: var(--border-focus); box-shadow: 0 0 0 3px var(--primary-glow); }
.nav-search-icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); color: var(--text-dim); }

.search-dropdown {
  position: absolute; top: calc(100% + 8px); left: 0; right: 0;
  background: var(--bg-surface); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
  overflow: hidden; display: none; z-index: 1050;
}
.search-dropdown.active { display: block; }
.search-result-item {
  display: flex; align-items: center; gap: 1rem; padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-subtle);
}
.search-result-item:hover { background: var(--bg-card-hover); }
.search-result-thumb { width: 42px; height: 42px; border-radius: var(--radius-sm); object-fit: cover; }

/* Nav Actions */
.nav-actions { display: flex; align-items: center; gap: 0.75rem; }
.action-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 42px; height: 42px; border-radius: var(--radius-full);
  background: var(--bg-surface); border: 1px solid var(--border-subtle);
  color: var(--text-main); position: relative; cursor: pointer; transition: var(--transition);
}
.action-btn:hover { background: var(--bg-card-hover); border-color: var(--border-accent); transform: translateY(-1px); }
.badge-count {
  position: absolute; top: -4px; right: -4px;
  background: var(--primary); color: #fff; font-size: 0.7rem; font-weight: 700;
  width: 19px; height: 19px; border-radius: var(--radius-full);
  display: flex; align-items: center; justify-content: center;
  transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.badge-count.pulse { transform: scale(1.35); }

/* Buttons */
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 0.5rem; padding: 0.75rem 1.5rem; font-weight: 600; font-size: 0.95rem;
  border-radius: var(--radius-full); cursor: pointer; border: none; transition: var(--transition);
}
.btn-primary {
  background: var(--accent-gradient); color: #ffffff;
  box-shadow: 0 4px 14px var(--primary-glow);
}
.btn-primary:hover { opacity: 0.95; transform: translateY(-2px); box-shadow: 0 6px 20px var(--primary-glow); }
.btn-secondary {
  background: var(--bg-surface); color: var(--text-main);
  border: 1px solid var(--border-subtle);
}
.btn-secondary:hover { background: var(--bg-card-hover); border-color: var(--border-accent); }
.btn-sm { padding: 0.5rem 1rem; font-size: 0.85rem; }
.btn-block { width: 100%; }

/* Hero */
.hero-section {
  position: relative; padding: 5rem 0 4rem;
  background: var(--hero-gradient); overflow: hidden;
}
.hero-grid {
  display: grid; grid-template-columns: 1.15fr 0.85fr; align-items: center; gap: 3.5rem;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.4rem 1rem; background: rgba(99, 102, 241, 0.15);
  border: 1px solid var(--border-accent); border-radius: var(--radius-full);
  color: var(--primary); font-size: 0.85rem; font-weight: 600; margin-bottom: 1.5rem;
}
.hero-title {
  font-size: 3.75rem; font-weight: 800; line-height: 1.1; letter-spacing: -1.5px; margin-bottom: 1.25rem;
}
.hero-title .gradient-text {
  background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-desc { font-size: 1.2rem; color: var(--text-muted); max-width: 520px; margin-bottom: 2rem; }
.hero-buttons { display: flex; gap: 1rem; flex-wrap: wrap; }
.hero-visual { position: relative; display: flex; justify-content: center; }
.hero-img-card {
  position: relative; border-radius: var(--radius-lg); overflow: hidden;
  box-shadow: var(--shadow-lg), var(--shadow-glow); border: 1px solid var(--border-subtle);
  transform: perspective(1000px) rotateY(-5deg) rotateX(3deg);
  transition: transform 0.5s ease;
}
.hero-img-card:hover { transform: perspective(1000px) rotateY(0deg) rotateX(0deg) scale(1.02); }
.hero-img { width: 100%; height: 460px; object-fit: cover; }
.floating-pill {
  position: absolute; padding: 0.75rem 1.25rem; background: var(--bg-glass);
  backdrop-filter: blur(12px); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md); box-shadow: var(--shadow-md);
  display: flex; align-items: center; gap: 0.75rem;
  animation: floatSlow 4s ease-in-out infinite alternate;
}
.pill-1 { top: 8%; left: -8%; }
.pill-2 { bottom: 10%; right: -6%; animation-delay: 2s; }
@keyframes floatSlow {
  0% { transform: translateY(0px); }
  100% { transform: translateY(-12px); }
}

/* Sections */
.section { padding: 5rem 0; }
.section-header { text-align: center; max-width: 650px; margin: 0 auto 3.5rem; }
.section-tag {
  text-transform: uppercase; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px;
  color: var(--primary); margin-bottom: 0.5rem;
}
.section-title { font-size: 2.35rem; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 0.75rem; }
.section-subtitle { color: var(--text-muted); font-size: 1.05rem; }

/* Categories Grid */
.category-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.5rem;
}
.category-card {
  position: relative; height: 240px; border-radius: var(--radius-md);
  overflow: hidden; border: 1px solid var(--border-subtle);
  display: flex; align-items: flex-end; padding: 1.5rem; transition: var(--transition);
}
.category-card:hover { transform: translateY(-6px); border-color: var(--border-accent); box-shadow: var(--shadow-md); }
.category-bg {
  position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1); filter: brightness(0.6);
}
.category-card:hover .category-bg { transform: scale(1.1); filter: brightness(0.45); }
.category-info { position: relative; z-index: 2; }
.category-name { font-size: 1.25rem; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 0.5rem; }

/* Product Cards */
.product-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.75rem;
}
.product-card {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md); overflow: hidden; display: flex;
  flex-direction: column; transition: var(--transition); position: relative;
}
.product-card:hover { transform: translateY(-6px); border-color: var(--border-accent); box-shadow: var(--shadow-md); }
.product-thumb-wrap { position: relative; height: 260px; background: var(--bg-surface); overflow: hidden; }
.product-thumb { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.product-card:hover .product-thumb { transform: scale(1.06); }
.discount-badge {
  position: absolute; top: 12px; left: 12px; background: var(--accent);
  color: #fff; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.65rem;
  border-radius: var(--radius-full); z-index: 2;
}
.wishlist-btn {
  position: absolute; top: 12px; right: 12px; width: 36px; height: 36px;
  border-radius: var(--radius-full); background: var(--bg-glass);
  backdrop-filter: blur(8px); border: 1px solid var(--border-subtle);
  color: var(--text-muted); display: flex; align-items: center; justify-content: center;
  cursor: pointer; z-index: 2; transition: var(--transition);
}
.wishlist-btn:hover, .wishlist-btn.active { color: var(--accent); background: rgba(236, 72, 153, 0.15); border-color: var(--accent); }
.product-content { padding: 1.25rem; display: flex; flex-direction: column; flex: 1; }
.product-category-tag { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--primary); margin-bottom: 0.35rem; }
.product-name { font-size: 1.05rem; font-weight: 700; margin-bottom: 0.5rem; line-height: 1.35; }
.product-rating { display: flex; align-items: center; gap: 0.35rem; font-size: 0.85rem; color: var(--warning); margin-bottom: 0.75rem; }
.product-price-row { display: flex; align-items: baseline; gap: 0.75rem; margin-top: auto; margin-bottom: 1rem; }
.current-price { font-size: 1.35rem; font-weight: 800; color: var(--text-main); }
.original-price { font-size: 0.95rem; text-decoration: line-through; color: var(--text-dim); }
.product-card-actions { display: flex; gap: 0.5rem; }
.product-card-actions .btn { flex: 1; padding: 0.65rem 1rem; font-size: 0.88rem; }

/* Showcase Section */
.showcase-box {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.06) 100%);
  border: 1px solid var(--border-accent); border-radius: var(--radius-lg);
  padding: 3.5rem; display: grid; grid-template-columns: 1fr 1fr;
  align-items: center; gap: 3.5rem;
}
.showcase-visual { border-radius: var(--radius-md); overflow: hidden; box-shadow: var(--shadow-lg); }
.showcase-visual img { width: 100%; height: 420px; object-fit: cover; }

/* Flash Deals */
.flash-deals-banner {
  background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
  border: 1px solid rgba(236, 72, 153, 0.35); border-radius: var(--radius-lg);
  padding: 2.5rem; color: #fff; margin-bottom: 2.5rem; display: flex;
  justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.5rem;
}
.countdown-timer { display: flex; align-items: center; gap: 0.75rem; }
.countdown-unit {
  background: rgba(0, 0, 0, 0.5); border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-sm); padding: 0.6rem 0.9rem; min-width: 58px; text-align: center;
}
.countdown-val { font-size: 1.6rem; font-weight: 800; color: #fff; font-variant-numeric: tabular-nums; }
.countdown-label { font-size: 0.65rem; text-transform: uppercase; color: var(--text-dim); }
.countdown-sep { font-size: 1.5rem; font-weight: 700; color: var(--accent); }

/* AI Assistant */
.ai-assistant-wrapper {
  background: var(--bg-card); border: 1px solid var(--border-accent);
  border-radius: var(--radius-lg); padding: 3rem; box-shadow: var(--shadow-glow);
}
.ai-header-badge {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: linear-gradient(135deg, #6366f1, #ec4899);
  color: #fff; font-size: 0.8rem; font-weight: 700;
  padding: 0.35rem 0.9rem; border-radius: var(--radius-full); margin-bottom: 1rem;
}
.ai-chips-wrap { display: flex; gap: 0.75rem; flex-wrap: wrap; margin: 1.5rem 0; }
.ai-chip {
  background: var(--bg-surface); border: 1px solid var(--border-subtle);
  color: var(--text-muted); padding: 0.45rem 1rem; border-radius: var(--radius-full);
  font-size: 0.85rem; cursor: pointer; transition: var(--transition);
}
.ai-chip:hover {
  background: var(--bg-card-hover); border-color: var(--border-focus);
  color: var(--text-main); transform: translateY(-2px);
}
.ai-input-group { display: flex; gap: 0.75rem; margin-top: 1.5rem; }
.ai-input {
  flex: 1; padding: 0.9rem 1.4rem; background: var(--bg-surface);
  border: 1px solid var(--border-subtle); border-radius: var(--radius-full);
  color: var(--text-main); font-size: 1rem; outline: none;
}
.ai-input:focus { border-color: var(--border-focus); box-shadow: 0 0 0 3px var(--primary-glow); }
.ai-results-area { margin-top: 2rem; display: none; }
.ai-reply-bubble {
  background: rgba(99, 102, 241, 0.1); border-left: 4px solid var(--primary);
  padding: 1.25rem 1.5rem; border-radius: var(--radius-sm);
  color: var(--text-main); font-size: 1.05rem; margin-bottom: 1.75rem;
}

/* Flying ghost element for add to cart */
.flying-ghost {
  position: fixed; z-index: 9999; border-radius: var(--radius-md);
  object-fit: cover; pointer-events: none; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  transition: all 0.8s cubic-bezier(0.19, 1, 0.22, 1);
}

/* Timeline */
.timeline-track { display: flex; justify-content: space-between; position: relative; margin: 3rem 0; }
.timeline-track::before {
  content: ''; position: absolute; top: 22px; left: 0; right: 0;
  height: 4px; background: var(--border-subtle); z-index: 1;
}
.timeline-progress-bar {
  position: absolute; top: 22px; left: 0; height: 4px;
  background: var(--accent-gradient); z-index: 2; transition: width 0.6s ease;
}
.timeline-step {
  position: relative; z-index: 3; display: flex; flex-direction: column;
  align-items: center; text-align: center; gap: 0.75rem; width: 100px;
}
.timeline-node {
  width: 44px; height: 44px; border-radius: var(--radius-full);
  background: var(--bg-surface); border: 2px solid var(--border-subtle);
  color: var(--text-dim); display: flex; align-items: center;
  justify-content: center; font-weight: 700; transition: var(--transition);
}
.timeline-step.completed .timeline-node {
  background: var(--primary); border-color: var(--primary); color: #fff;
  box-shadow: 0 0 15px var(--primary-glow);
}
.timeline-step.active .timeline-node {
  background: var(--accent); border-color: var(--accent); color: #fff;
  box-shadow: 0 0 20px rgba(236, 72, 153, 0.5);
}

/* Tables & Forms */
.table-card {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md); overflow: hidden;
}
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-subtle); text-align: left; }
.table th { background: var(--bg-surface); font-weight: 700; color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; }

.form-group { margin-bottom: 1.25rem; }
.form-label { display: block; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-main); }
.form-control {
  width: 100%; padding: 0.8rem 1rem; background: var(--bg-surface);
  border: 1px solid var(--border-subtle); border-radius: var(--radius-sm);
  color: var(--text-main); outline: none; transition: var(--transition);
}
.form-control:focus { border-color: var(--border-focus); box-shadow: 0 0 0 3px var(--primary-glow); }

/* Footer */
.footer {
  background: var(--bg-surface); border-top: 1px solid var(--border-subtle);
  padding: 4.5rem 0 2rem; margin-top: auto;
}
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 3rem; margin-bottom: 3rem; }
.footer-desc { color: var(--text-muted); max-width: 320px; margin: 1rem 0 1.5rem; }
.footer-title { font-size: 1rem; font-weight: 700; margin-bottom: 1.25rem; }
.footer-links { list-style: none; display: flex; flex-direction: column; gap: 0.75rem; }
.footer-link { color: var(--text-muted); font-size: 0.9rem; }
.footer-link:hover { color: var(--primary); }
.footer-bottom {
  padding-top: 2rem; border-top: 1px solid var(--border-subtle);
  display: flex; align-items: center; justify-content: space-between;
  color: var(--text-dim); font-size: 0.85rem; flex-wrap: wrap; gap: 1rem;
}

/* Toast */
.toast-container {
  position: fixed; bottom: 2rem; right: 2rem; z-index: 10000;
  display: flex; flex-direction: column; gap: 0.75rem;
}
.toast {
  padding: 1rem 1.5rem; border-radius: var(--radius-md);
  background: var(--bg-surface); border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-lg); color: var(--text-main);
  display: flex; align-items: center; gap: 0.75rem; min-width: 280px;
}
.toast-success { border-left: 4px solid var(--success); }
.toast-error { border-left: 4px solid var(--danger); }

@media (max-width: 992px) {
  .hero-grid, .showcase-box { grid-template-columns: 1fr; gap: 2.5rem; }
  .hero-title { font-size: 2.8rem; }
  .footer-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 768px) {
  .nav-links, .nav-search-box { display: none; }
  .hero-title { font-size: 2.25rem; }
  .footer-grid { grid-template-columns: 1fr; }
}
"""

with open("store/static/css/main.css", "w", encoding="utf-8") as f:
    f.write(css_content)
print("✓ store/static/css/main.css written")

# Theme JS
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
print("✓ store/static/js/theme.js written")

# Cart JS
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
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3500);
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
  ghost.style.left = `${startRect.left}px`;
  ghost.style.top = `${startRect.top}px`;
  ghost.style.width = `${startRect.width}px`;
  ghost.style.height = `${startRect.height}px`;
  document.body.appendChild(ghost);

  requestAnimationFrame(() => {
    ghost.style.left = `${endRect.left + 10}px`;
    ghost.style.top = `${endRect.top + 10}px`;
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
  .catch(err => {
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
        if (data.added) {
          btnElement.classList.add('active');
        } else {
          btnElement.classList.remove('active');
        }
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
print("✓ store/static/js/cart.js written")

# Flash Deals Countdown JS
deals_js = """// Flash Deals Countdown Timer
function initFlashDeals(deadlineStr) {
  const targetDate = new Date(deadlineStr).getTime();

  function update() {
    const now = new Date().getTime();
    const distance = targetDate - now;

    if (distance <= 0) {
      const timerEl = document.getElementById('flashCountdown');
      if (timerEl) timerEl.innerHTML = '<span style="color:var(--accent);font-weight:700">Deals Just Refreshed!</span>';
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
print("✓ store/static/js/deals.js written")

# AI Assistant JS
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
    replyBubble.innerHTML = `<em>Scanning NEXORA inventory for \"${promptText}\"...</em>`;
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
          html += `
            <div class=\"product-card\">
              <div class=\"product-thumb-wrap\">
                <img src=\"${p.image}\" alt=\"${p.name}\" class=\"product-thumb\">
                ${p.discount_percentage ? `<span class=\"discount-badge\">-${p.discount_percentage}%</span>` : ''}
              </div>
              <div class=\"product-content\">
                <div class=\"product-category-tag\">${p.category}</div>
                <h4 class=\"product-name\"><a href=\"${p.detail_url}\">${p.name}</a></h4>
                <div class=\"product-rating\">★ ${p.rating} (${p.reviews_count} reviews)</div>
                <div class=\"product-price-row\">
                  <span class=\"current-price\">₹${p.current_price.toLocaleString('en-IN')}</span>
                  ${p.price > p.current_price ? `<span class=\"original-price\">₹${p.price.toLocaleString('en-IN')}</span>` : ''}
                </div>
                <div class=\"product-card-actions\">
                  <a href=\"${p.detail_url}\" class=\"btn btn-secondary btn-sm\">View</a>
                  <button onclick=\"addToCart(${p.id}, 1, this)\" class=\"btn btn-primary btn-sm\">Add to Cart</button>
                </div>
              </div>
            </div>
          `;
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
print("✓ store/static/js/assistant.js written")

print("All static assets generated successfully.")
