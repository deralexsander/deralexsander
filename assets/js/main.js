/**
 * PORTAFOLIO PROFESIONAL - NICOLÁS MUÑOZ (catstudio.cl)
 * Microinteracciones, filtrado fluido y animaciones estilo Apple
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Reveal on scroll (Apple-style smooth fade and translate)
  const revealElements = document.querySelectorAll('.reveal');
  
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        // Unobserve once animated so it doesn't flicker
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    rootMargin: '0px 0px -60px 0px',
    threshold: 0.12
  });

  revealElements.forEach((el, index) => {
    // Add subtle delay to grouped cards for nice cascade effect
    if (el.classList.contains('metric-card') || el.classList.contains('project-card') || el.classList.contains('cert-card')) {
      el.style.transitionDelay = `${(index % 3) * 0.08}s`;
    }
    revealObserver.observe(el);
  });

  // 2. Project Filtering with Smooth Transitions
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active button state
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        
        if (filterValue === 'all' || cardCategory.includes(filterValue)) {
          card.style.display = 'flex';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) scale(1)';
          }, 30);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(12px) scale(0.96)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 250);
        }
      });
    });
  });

  // 3. One-Click Copy Email & Toast Notification
  const copyEmailBtns = document.querySelectorAll('[data-action="copy-email"]');
  const toast = document.getElementById('toast');
  const emailToCopy = 'nico.alexander.m.m@gmail.com';

  function showToast(message) {
    if (!toast) return;
    toast.querySelector('.toast-msg').textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }

  copyEmailBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(emailToCopy).then(() => {
          showToast('¡Correo copiado: ' + emailToCopy + '!');
        }).catch(() => {
          fallbackCopyText(emailToCopy);
        });
      } else {
        fallbackCopyText(emailToCopy);
      }
    });
  });

  function fallbackCopyText(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand('copy');
      showToast('¡Correo copiado: ' + text + '!');
    } catch (err) {
      window.location.href = 'mailto:' + text;
    }
    document.body.removeChild(textArea);
  }

  // 4. Subtle Micro-tilt Effect on Project Cards (Apple-esque 3D touch)
  const cardsToTilt = document.querySelectorAll('.project-card, .metric-card');
  
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    cardsToTilt.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -3;
        const rotateY = ((x - centerX) / centerX) * 3;

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-4px)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }

  // 5. Dynamic Footer Year
  const yearElement = document.getElementById('currentYear');
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }

  // 6. Smooth active state update for navigation
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  }, { passive: true });

  // 7. Live GitHub Activity Fetcher
  async function loadRecentGitHubActivity() {
    const grid = document.getElementById('recent-activity-grid');
    if (!grid) return;

    function getRelativeTime(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffSecs = Math.floor((now - date) / 1000);
      
      if (diffSecs < 60) return 'Hace unos segundos';
      const diffMins = Math.floor(diffSecs / 60);
      if (diffMins < 60) return `Hace ${diffMins} min${diffMins > 1 ? 's' : ''}`;
      const diffHours = Math.floor(diffMins / 60);
      if (diffHours < 24) return `Hace ${diffHours} hora${diffHours > 1 ? 's' : ''}`;
      const diffDays = Math.floor(diffHours / 24);
      if (diffDays === 1) return 'Ayer';
      if (diffDays < 30) return `Hace ${diffDays} días`;
      const diffMonths = Math.floor(diffDays / 30);
      return `Hace ${diffMonths} mes${diffMonths > 1 ? 'es' : ''}`;
    }

    try {
      const res = await fetch('https://api.github.com/users/deralexsander/repos?sort=pushed&per_page=6');
      if (!res.ok) throw new Error('GitHub API offline or rate-limited');
      const repos = await res.json();
      
      // Filter out self-profile and get latest 4 updated repositories
      const filtered = repos.filter(r => r.name !== 'deralexsander').slice(0, 4);

      if (filtered.length > 0) {
        grid.innerHTML = filtered.map(repo => {
          const lang = repo.language || 'Software';
          const timeAgo = getRelativeTime(repo.pushed_at);
          const desc = repo.description || 'Proyecto en desarrollo e integración continua.';
          return `
            <a href="${repo.html_url}" target="_blank" rel="noopener noreferrer" class="activity-card reveal active">
              <div class="activity-card-top">
                <span class="activity-repo-name">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                  ${repo.name}
                </span>
                <span class="activity-lang-pill">${lang}</span>
              </div>
              <p class="activity-desc">${desc}</p>
              <div class="activity-card-footer">
                <span class="activity-time">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  Último push: ${timeAgo}
                </span>
                <span class="activity-link-text">
                  Ver código
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
                </span>
              </div>
            </a>
          `;
        }).join('');
      }
    } catch (err) {
      console.log('GitHub live activity using fallback:', err);
    }
  }

  loadRecentGitHubActivity();

  // 8. Dynamic Live Projects Counter (GitHub Pages + Live Domains)
  async function updateLiveProjectsCount() {
    const counterEl = document.getElementById('liveProjectsCounter');
    if (!counterEl) return;

    try {
      const res = await fetch('https://api.github.com/users/deralexsander/repos?per_page=100');
      if (!res.ok) return;
      const repos = await res.json();
      
      // Count repos with has_pages: true (excluding self-profile deralexsander)
      const pagesRepos = repos.filter(r => r.has_pages && r.name.toLowerCase() !== 'deralexsander');
      
      // External live production domain (SmartBids.cl)
      const externalLiveCount = 1; 
      
      const totalLive = pagesRepos.length + externalLiveCount;
      if (totalLive > 0) {
        counterEl.textContent = totalLive;
      }
    } catch (e) {
      console.log('Using default live projects count:', e);
    }
  }

  updateLiveProjectsCount();
});
