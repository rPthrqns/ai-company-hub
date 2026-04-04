// === Header Scroll Effect ===
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 50);
});

// === Mobile Nav Toggle ===
const navToggle = document.getElementById('navToggle');
const nav = document.querySelector('.nav');
navToggle.addEventListener('click', () => {
  nav.classList.toggle('open');
});
// Close nav on link click
nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));

// === Tabs ===
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
  });
});

// === Phone Auto-Format ===
const phoneInput = document.getElementById('phone');
phoneInput.addEventListener('input', (e) => {
  let val = e.target.value.replace(/\D/g, '');
  if (val.length > 11) val = val.slice(0, 11);
  if (val.length >= 7) {
    e.target.value = val.slice(0, 3) + '-' + val.slice(3, 7) + '-' + val.slice(7);
  } else if (val.length >= 4) {
    e.target.value = val.slice(0, 3) + '-' + val.slice(3);
  } else {
    e.target.value = val;
  }
});

// === Form Submit ===
const form = document.getElementById('applyForm');
const formSuccess = document.getElementById('formSuccess');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  // Validate
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  // Collect data (in production, send to API)
  const data = Object.fromEntries(new FormData(form));
  console.log('지원서 제출:', data);
  // Show success
  form.style.display = 'none';
  formSuccess.style.display = 'block';
  formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

// === Floating CTA visibility ===
const floatingCta = document.getElementById('floatingCta');
const applySection = document.getElementById('apply');
window.addEventListener('scroll', () => {
  if (window.innerWidth <= 768) {
    const applyTop = applySection.getBoundingClientRect().top;
    floatingCta.style.display = applyTop > window.innerHeight ? 'flex' : 'none';
  }
});

// === Smooth scroll for anchor links ===
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', (e) => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
