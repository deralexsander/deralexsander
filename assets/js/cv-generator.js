/**
 * CV GENERATOR & AUTO-SYNC ENGINE
 * Nicolás Alexsander Muñoz Méndez (catstudio.cl)
 * 
 * Sincroniza y compila dinámicamente el CV en PDF con el contenido
 * actual del portafolio (contacto, rol en SmartBids, proyectos y certificaciones).
 */

(function initCvAutoSync() {
  const CDN_HTML2PDF = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
  let html2pdfLoadingPromise = null;

  function loadHtml2Pdf() {
    if (window.html2pdf) return Promise.resolve(window.html2pdf);
    if (html2pdfLoadingPromise) return html2pdfLoadingPromise;

    html2pdfLoadingPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = CDN_HTML2PDF;
      script.async = true;
      script.onload = () => resolve(window.html2pdf);
      script.onerror = (err) => reject(err);
      document.head.appendChild(script);
    });
    return html2pdfLoadingPromise;
  }

  function showToast(message) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    const msgEl = toast.querySelector('.toast-msg') || toast;
    msgEl.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2800);
  }

  // Extrae y compila el contenido del portafolio en una plantilla ATS limpia para A4
  function buildCvElement() {
    const dateStr = new Intl.DateTimeFormat('es-CL', { month: 'short', year: 'numeric' }).format(new Date());

    const container = document.createElement('div');
    container.id = 'cv-render-template';
    container.style.cssText = `
      position: fixed;
      left: -9999px;
      top: 0;
      width: 210mm;
      min-height: 297mm;
      background: #ffffff;
      color: #1a1a1a;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.42;
      padding: 16mm 18mm;
      box-sizing: border-box;
    `;

    container.innerHTML = `
      <style>
        #cv-render-template * { box-sizing: border-box; margin: 0; padding: 0; }
        .cv-header { border-bottom: 2px solid #000000; padding-bottom: 8pt; margin-bottom: 12pt; }
        .cv-date-badge { font-size: 8pt; color: #666666; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3pt; }
        .cv-name { font-size: 20pt; font-weight: 700; color: #000000; letter-spacing: -0.02em; }
        .cv-title { font-size: 11pt; color: #333333; font-weight: 600; margin-top: 2pt; }
        .cv-contacts { display: flex; flex-wrap: wrap; gap: 10pt; font-size: 8.5pt; color: #444444; margin-top: 6pt; }
        .cv-contacts span { display: inline-flex; align-items: center; gap: 3pt; }
        .cv-section { margin-bottom: 12pt; }
        .cv-sec-title { font-size: 11pt; font-weight: 700; color: #000000; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #d4d4d8; padding-bottom: 2pt; margin-bottom: 7pt; }
        .cv-item { margin-bottom: 9pt; }
        .cv-item-header { display: flex; justify-content: space-between; align-items: baseline; font-size: 10pt; }
        .cv-item-title { font-weight: 700; color: #000000; }
        .cv-item-date { font-size: 8.5pt; color: #666666; font-weight: 500; }
        .cv-item-sub { font-size: 9pt; color: #333333; font-style: italic; margin-top: 1pt; margin-bottom: 3pt; }
        .cv-bullets { list-style: disc; margin-left: 14pt; font-size: 9pt; color: #222222; }
        .cv-bullets li { margin-bottom: 2.5pt; }
        .cv-skills-grid { font-size: 9pt; color: #222222; display: flex; flex-direction: column; gap: 3pt; }
        .cv-skill-line strong { color: #000000; }
        .cv-page-break { page-break-before: always; padding-top: 10pt; }
      </style>

      <!-- ENCABEZADO -->
      <header class="cv-header">
        <div class="cv-date-badge">Actualizado con datos del portafolio • ${dateStr}</div>
        <h1 class="cv-name">Nicolás Alexsander Muñoz Méndez</h1>
        <div class="cv-title">Desarrollador Full-Stack | Egresando de Ingeniería en Informática (2026)</div>
        <div class="cv-contacts">
          <span>📍 Valparaíso, Chile</span>
          <span>✉️ nico.alexander.m.m@gmail.com</span>
          <span>📞 +56 9 6878 7862</span>
          <span>🌐 catstudio.cl</span>
          <span>🐙 github.com/deralexsander</span>
          <span>💼 linkedin.com/in/nicolás-muñoz-mendéz</span>
        </div>
      </header>

      <!-- PERFIL PROFESIONAL -->
      <section class="cv-section">
        <h2 class="cv-sec-title">Perfil Profesional</h2>
        <p style="font-size: 9.5pt; color: #2b2b2b; line-height: 1.45;">
          Desarrollador con sólida formación en ingeniería de software, arquitectura de sistemas y diseño de interfaces. Experiencia comprobada en despliegue de soluciones SaaS en producción, desarrollo frontend reactivo (HTMX, CSS modular), infraestructura cloud (Railway, Cloudflare, dominios y SSL), seguridad de sesiones (autenticación 2FA/OTP y tokens HMAC) e integración con APIs RESTful. Trabajo colaborativo bajo marco ágil Scrum y primer lugar regional en robótica y programación algorítmica.
        </p>
      </section>

      <!-- PROYECTOS Y EXPERIENCIA TÉCNICA -->
      <section class="cv-section">
        <h2 class="cv-sec-title">Proyectos y Experiencia Técnica</h2>

        <!-- SmartBids -->
        <div class="cv-item">
          <div class="cv-item-header">
            <span class="cv-item-title">SmartBids — SaaS de Inteligencia Comercial y Licitaciones Públicas</span>
            <span class="cv-item-date">Ago 2025 – Dic 2025</span>
          </div>
          <div class="cv-item-sub">
            Rol: <strong>Team Developer (Frontend, Cloud & Security)</strong> | Proyecto Capstone / Cliente Real en Producción | smartbids.cl
          </div>
          <ul class="cv-bullets">
            <li><strong>Frontend & UI/UX:</strong> Diseñé e implementé la interfaz reactiva, accesible y ultra veloz con HTML5, CSS3 modular (Dark Theme) y HTMX, eliminando la sobrecarga de SPAs pesadas.</li>
            <li><strong>Infraestructura Cloud:</strong> Despliegue en producción sobre Railway, configuración de dominio corporativo personalizado (smartbids.cl) y certificados de cifrado SSL/TLS.</li>
            <li><strong>Seguridad & Identidad:</strong> Implementé el sistema de autenticación multi-factor (2FA/OTP transaccional vía Gmail API REST), control de sesiones seguras y validación de tokens con firmas HMAC.</li>
            <li><strong>Metodología Ágil:</strong> Trabajo en equipo multidisciplinario bajo marco Scrum estructurado en iteraciones cortas (Sprints) con bitácoras semanales de avance.</li>
          </ul>
        </div>

        <!-- Notes & Sillage -->
        <div class="cv-item">
          <div class="cv-item-header">
            <span class="cv-item-title">Notes & Sillage — Catálogo Digital de Perfumería y Comercio Rápido</span>
            <span class="cv-item-date">2025 – En Producción</span>
          </div>
          <div class="cv-item-sub">
            Rol: <strong>Creador & Desarrollador Principal</strong> | Solución JAMstack en Producción | notes.cl
          </div>
          <ul class="cv-bullets">
            <li>Desarrollé una solución e-commerce y catálogo interactivo mobile-first sin dependencia de servidores externos, garantizando tiempos de carga inferiores a 800ms.</li>
            <li>Gestioné la infraestructura web completa: dominio propio (notes.cl), proxy perimetral de caché y seguridad estricta SSL/TLS con Cloudflare, y despliegue automatizado con GitHub Pages.</li>
            <li>Implementé un motor de búsqueda predictivo con tolerancia a errores tipográficos y generación automática de pedidos estructurados hacia WhatsApp.</li>
          </ul>
        </div>

        <!-- G&M Constructora -->
        <div class="cv-item">
          <div class="cv-item-header">
            <span class="cv-item-title">Constructora Godoy & Méndez SpA — Plataforma Corporativa</span>
            <span class="cv-item-date">2025</span>
          </div>
          <div class="cv-item-sub">
            Rol: <strong>Consultor Web & Desarrollador Full-Stack</strong> | Cliente Real PYME
          </div>
          <ul class="cv-bullets">
            <li>Servicio integral de consultoría y desarrollo: desde el diseño UI/UX hasta la puesta en marcha corporativa de alto impacto.</li>
            <li>Configuración técnica y administración de zonas DNS, hosting, certificados SSL y cuentas de correo corporativas.</li>
            <li>Diseño responsivo optimizado para captación de clientes y exhibición de catálogo de obras y licitaciones del sector construcción.</li>
          </ul>
        </div>

        <!-- FerreMas -->
        <div class="cv-item">
          <div class="cv-item-header">
            <span class="cv-item-title">FerreMas — E-commerce Móvil y Gestión Logística</span>
            <span class="cv-item-date">Abr 2025 – Jun 2025</span>
          </div>
          <div class="cv-item-sub">
            Rol: Desarrollador Full-Stack | Android Studio, Java/Kotlin, Firebase, Google Maps API
          </div>
          <ul class="cv-bullets">
            <li>Implementé autenticación con Google OAuth 2.0 y control de acceso basado en roles (RBAC) entre clientes y administradores.</li>
            <li>Integré la API de Google Maps para cálculo dinámico de despachos entre sucursales de ferretería.</li>
          </ul>
        </div>
      </section>

      <!-- HABILIDADES TÉCNICAS -->
      <section class="cv-section">
        <h2 class="cv-sec-title">Habilidades Técnicas</h2>
        <div class="cv-skills-grid">
          <div class="cv-skill-line"><strong>Lenguajes:</strong> Python, JavaScript (ES6+), TypeScript, SQL, Java, HTML5, CSS3 moderno.</div>
          <div class="cv-skill-line"><strong>Frontend & UI/UX:</strong> HTMX, Diseño Web Responsivo (Mobile-First), Apple HIG / Liquid Glass, Tailwind CSS, Bootstrap.</div>
          <div class="cv-skill-line"><strong>Backend & APIs:</strong> Django, Django REST Framework, Node.js, arquitectura de microservicios y APIs RESTful.</div>
          <div class="cv-skill-line"><strong>Cloud, DevOps & Seguridad:</strong> Railway, Cloudflare, GitHub Actions (CI/CD), Firebase Authentication, tokens HMAC, 2FA/OTP, SSL/TLS, Linux.</div>
          <div class="cv-skill-line"><strong>Bases de Datos & ML:</strong> PostgreSQL (relacional normalizada), Cloud Firestore, Scikit-Learn, XGBoost, Pandas.</div>
          <div class="cv-skill-line"><strong>Metodologías:</strong> Scrum (Planificación por Sprints, control de avances), Kanban, Git / GitHub.</div>
        </div>
      </section>

      <!-- EDUCACIÓN -->
      <section class="cv-section">
        <h2 class="cv-sec-title">Educación</h2>
        <div class="cv-item">
          <div class="cv-item-header">
            <span class="cv-item-title">Duoc UC — Ingeniería en Informática</span>
            <span class="cv-item-date">2023 – 2026</span>
          </div>
          <div class="cv-item-sub">Cursando último año de carrera</div>
        </div>
        <div class="cv-item" style="margin-bottom: 0;">
          <div class="cv-item-header">
            <span class="cv-item-title">Colegio Don Orione — Técnico en Electrónica</span>
            <span class="cv-item-date">Graduado</span>
          </div>
        </div>
      </section>

      <!-- CERTIFICACIONES Y DISTINCIONES -->
      <section class="cv-section" style="margin-bottom: 0;">
        <h2 class="cv-sec-title">Certificaciones Internacionales & Distinciones</h2>
        <ul class="cv-bullets">
          <li><strong>Cisco Networking Academy & Python Institute:</strong> Partner: PCAP – Programming Essentials in Python (Jul 2023).</li>
          <li><strong>CertiProf International:</strong> DevOps Foundation Professional Certificate (DFPC™) — ID: TLZZKDZKTHL-XPXRMHPSH-RLKFTJJHSS.</li>
          <li><strong>CertiProf International:</strong> DevOps Essentials Professional Certificate (DEPC®) — ID: TLZZLLDVDKK-XPWTMQXHS-RLKRJKLLTT.</li>
          <li><strong>Distinción MakeX Robotics:</strong> 1.º Lugar Regional — Medalla de Oro en desarrollo de algoritmos de navegación autónoma en tiempo real.</li>
        </ul>
      </section>
    `;

    return container;
  }

  // Manejador del botón de descarga
  async function handleDownloadCv(event) {
    event.preventDefault();
    const downloadBtn = event.currentTarget;
    const originalHref = downloadBtn.getAttribute('href');

    showToast('Generando CV actualizado en PDF con datos del portafolio...');

    try {
      const html2pdf = await loadHtml2Pdf();
      const cvElement = buildCvElement();
      document.body.appendChild(cvElement);

      const options = {
        margin: [10, 10, 10, 10],
        filename: 'cv-nicolas-munoz.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, letterRendering: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };

      await html2pdf().set(options).from(cvElement).save();
      document.body.removeChild(cvElement);

      showToast('¡CV actualizado descargado exitosamente!');
    } catch (error) {
      console.warn('Fallback a descarga directa:', error);
      showToast('Descargando copia local del CV...');
      // Si falla o no hay conexión al CDN, redirige al archivo físico
      const fallbackLink = document.createElement('a');
      fallbackLink.href = originalHref || 'assets/cv-nicolas-munoz.pdf';
      fallbackLink.download = 'cv-nicolas-munoz.pdf';
      fallbackLink.click();
    }
  }

  // Asignar listener a todos los botones de descarga de CV en el sitio
  document.addEventListener('DOMContentLoaded', () => {
    const cvButtons = document.querySelectorAll('a[href*="cv-nicolas-munoz.pdf"], a[download][href*="cv"]');
    cvButtons.forEach(btn => {
      btn.addEventListener('click', handleDownloadCv);
      btn.setAttribute('title', 'Descargar CV generado automáticamente en PDF');
    });
  });
})();
