#!/usr/bin/env python3
"""
Generador automático de CV en PDF para Nicolás Muñoz (catstudio.cl)
Genera un documento A4 profesional, ATS-friendly, con tipografía TrueType 100% embebida
y sincronizado con los datos, proyectos y certificaciones del portafolio.
"""
import os
import sys
import cairo

PAGE_W = 595.28
PAGE_H = 841.89
MARGIN_L = 46.0
MARGIN_R = 549.0
USABLE_W = MARGIN_R - MARGIN_L

def wrap_text(ctx, text, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        w = ctx.text_extents(test_line).x_advance
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_bullet(ctx, x, y, bold_prefix, text, max_w, line_h=11.3, font_size=8.3):
    ctx.save()
    ctx.set_source_rgb(0.3, 0.35, 0.42)
    ctx.arc(x + 3.5, y - 3, 1.8, 0, 2 * 3.14159)
    ctx.fill()
    
    text_x = x + 12
    avail_w1 = max_w - 12
    
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    prefix_w = ctx.text_extents(bold_prefix + ' ').x_advance if bold_prefix else 0
    
    words = text.strip().split(' ')
    first_line_words = []
    rem_words = []
    
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(font_size)
    
    curr_w = prefix_w
    for i, w in enumerate(words):
        test_w = ctx.text_extents((' ' if first_line_words else '') + w).x_advance
        if curr_w + test_w <= avail_w1:
            first_line_words.append(w)
            curr_w += test_w
        else:
            rem_words = words[i:]
            break
            
    curr_y = y
    if bold_prefix:
        ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_source_rgb(0.06, 0.09, 0.15)
        ctx.move_to(text_x, curr_y)
        ctx.show_text(bold_prefix + ' ')
        
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0.16, 0.2, 0.26)
    ctx.move_to(text_x + prefix_w, curr_y)
    ctx.show_text(' '.join(first_line_words))
    curr_y += line_h
    
    curr_line = []
    for w in rem_words:
        test_line = (' '.join(curr_line + [w]))
        if ctx.text_extents(test_line).x_advance <= avail_w1:
            curr_line.append(w)
        else:
            ctx.move_to(text_x, curr_y)
            ctx.show_text(' '.join(curr_line))
            curr_y += line_h
            curr_line = [w]
    if curr_line:
        ctx.move_to(text_x, curr_y)
        ctx.show_text(' '.join(curr_line))
        curr_y += line_h
        
    ctx.restore()
    return curr_y

def draw_header(ctx, y):
    # Top Tag
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(7.5)
    ctx.set_source_rgb(0.42, 0.48, 0.56)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('ÚLTIMA ACTUALIZACIÓN: NOVIEMBRE 2026 • SINCRONIZADO CON PORTAFOLIO')
    y += 18.0

    # Name
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(20.0)
    ctx.set_source_rgb(0.05, 0.08, 0.14)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('Nicolás Alexsander Muñoz Méndez')
    y += 15.0

    # Subtitle / Headline
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(10.0)
    ctx.set_source_rgb(0.18, 0.24, 0.32)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('Desarrollador Full-Stack Junior | Egresando de Ingeniería en Informática (2026)')
    y += 15.0

    # Contact Bar with interactive clickable links
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.4)
    
    cur_x = MARGIN_L
    def add_contact_item(text, link=None, sep='  •  '):
        nonlocal cur_x, y
        if link:
            ctx.set_source_rgb(0.1, 0.35, 0.75)
            ctx.move_to(cur_x, y)
            ctx.tag_begin(cairo.TAG_LINK, f"uri='{link}'")
            ctx.show_text(text)
            ctx.tag_end(cairo.TAG_LINK)
            cur_x += ctx.text_extents(text).x_advance
        else:
            ctx.set_source_rgb(0.28, 0.34, 0.42)
            ctx.move_to(cur_x, y)
            ctx.show_text(text)
            cur_x += ctx.text_extents(text).x_advance
        if sep:
            ctx.set_source_rgb(0.55, 0.6, 0.68)
            ctx.move_to(cur_x, y)
            ctx.show_text(sep)
            cur_x += ctx.text_extents(sep).x_advance
            
    add_contact_item('Valparaíso, Chile')
    add_contact_item('nico.alexander.m.m@gmail.com', 'mailto:nico.alexander.m.m@gmail.com')
    add_contact_item('+56 9 6878 7862', 'tel:+56968787862')
    add_contact_item('catstudio.cl', 'https://deralexsander.github.io/deralexsander/')
    add_contact_item('github.com/deralexsander', 'https://github.com/deralexsander', sep=None)
    y += 11.0

    # Divider Line
    ctx.set_source_rgb(0.8, 0.84, 0.9)
    ctx.set_line_width(0.75)
    ctx.move_to(MARGIN_L, y)
    ctx.line_to(MARGIN_R, y)
    ctx.stroke()
    y += 15.0
    return y

def draw_section_title(ctx, y, title):
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(10.2)
    ctx.set_source_rgb(0.06, 0.1, 0.16)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text(title)
    y += 4.0
    ctx.set_source_rgb(0.68, 0.73, 0.8)
    ctx.set_line_width(0.5)
    ctx.move_to(MARGIN_L, y)
    ctx.line_to(MARGIN_R, y)
    ctx.stroke()
    y += 13.0
    return y

def draw_footer(ctx, page_num, total_pages=2):
    ctx.set_source_rgb(0.82, 0.86, 0.9)
    ctx.set_line_width(0.5)
    ctx.move_to(MARGIN_L, 810)
    ctx.line_to(MARGIN_R, 810)
    ctx.stroke()

    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(7.8)
    ctx.set_source_rgb(0.45, 0.5, 0.58)
    ctx.move_to(MARGIN_L, 822)
    ctx.show_text('Nicolás Alexsander Muñoz Méndez — Currículum Vitae')
    
    right_text = f'Página {page_num} de {total_pages}  •  '
    ctx.move_to(MARGIN_R - 120, 822)
    ctx.show_text(right_text)
    w_rt = ctx.text_extents(right_text).x_advance
    
    ctx.move_to(MARGIN_R - 120 + w_rt, 822)
    ctx.set_source_rgb(0.1, 0.35, 0.75)
    ctx.tag_begin(cairo.TAG_LINK, "uri='https://deralexsander.github.io/deralexsander/'")
    ctx.show_text('catstudio.cl')
    ctx.tag_end(cairo.TAG_LINK)

def draw_project(ctx, y, p):
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(9.2)
    ctx.set_source_rgb(0.06, 0.09, 0.15)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text(p['title'])
    
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.2)
    ctx.set_source_rgb(0.4, 0.46, 0.54)
    date_w = ctx.text_extents(p['date']).x_advance
    ctx.move_to(MARGIN_R - date_w, y)
    ctx.show_text(p['date'])
    y += 10.5
    
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.1)
    ctx.set_source_rgb(0.24, 0.28, 0.35)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text(p['sub_prefix'])
    sub_w = ctx.text_extents(p['sub_prefix']).x_advance
    
    if 'link_text' in p and p['link_text']:
        ctx.set_source_rgb(0.1, 0.35, 0.75)
        ctx.move_to(MARGIN_L + sub_w, y)
        ctx.tag_begin(cairo.TAG_LINK, f"uri='{p['link_url']}'")
        ctx.show_text(p['link_text'])
        ctx.tag_end(cairo.TAG_LINK)
    y += 11.5
    
    for b_prefix, b_text in p['bullets']:
        y = draw_bullet(ctx, MARGIN_L, y, b_prefix, b_text, USABLE_W, line_h=11.2, font_size=8.2)
        y += 1.2
    y += 4.0
    return y

def generate_pdf(output_path):
    surface = cairo.PDFSurface(output_path, PAGE_W, PAGE_H)
    ctx = cairo.Context(surface)

    # ================= PAGE 1 =================
    y = draw_header(ctx, 48.0)

    # 1. PERFIL PROFESIONAL
    y = draw_section_title(ctx, y, 'PERFIL PROFESIONAL')
    profile_text = (
        'Desarrollador con sólida formación en ingeniería de software, arquitectura de sistemas y diseño de interfaces UI/UX. '
        'Experiencia comprobada en despliegue de soluciones SaaS en producción, desarrollo frontend reactivo con HTMX y CSS3 modular, '
        'infraestructura cloud (Railway, Cloudflare, dominios y certificados SSL/TLS), seguridad de sesiones (2FA/OTP transaccional con '
        'Gmail API REST, tokens HMAC) y consumo eficiente de APIs RESTful. Trabajo colaborativo bajo marco ágil Scrum y primer '
        'lugar regional en robótica competitiva y resolución algorítmica.'
    )
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.6)
    ctx.set_source_rgb(0.16, 0.2, 0.26)
    for line in wrap_text(ctx, profile_text, USABLE_W):
        ctx.move_to(MARGIN_L, y)
        ctx.show_text(line)
        y += 11.8
    y += 8.0

    # 2. PROYECTOS DESTACADOS Y CLIENTES REALES (Página 1)
    y = draw_section_title(ctx, y, 'PROYECTOS DESTACADOS Y CLIENTES REALES')

    p1_list = [
        {
            'title': 'SmartBids – SaaS de Inteligencia Comercial y Licitaciones Públicas',
            'date': 'Ago 2025 – Dic 2025',
            'sub_prefix': 'Rol: Team Developer (Frontend, Cloud & Security) | Cliente Real en Producción | ',
            'link_text': 'smartbids.cl',
            'link_url': 'https://smartbids.cl',
            'bullets': [
                ('Frontend & UI/UX:', 'Diseñé e implementé la interfaz responsiva, accesible y de alta velocidad con HTML5, CSS3 modular (Dark Theme) y HTMX, eliminando la sobrecarga de SPAs complejas.'),
                ('Infraestructura Cloud:', 'Despliegue en producción sobre Railway con dominio corporativo propio (smartbids.cl) y aprovisionamiento de certificados SSL/TLS estricto.'),
                ('Seguridad & Identidad:', 'Implementé la capa de autenticación de dos factores (2FA / OTP transaccional con Gmail API REST), control de sesiones seguras y validación de tokens con firmas HMAC.'),
                ('Metodología Ágil:', 'Trabajo en equipo multidisciplinario bajo marco Scrum en iteraciones cortas (Sprints) con control de versiones en GitHub y revisiones de código continuo.')
            ]
        },
        {
            'title': 'G&M Constructora – Plataforma Web Corporativa y Consultoría',
            'date': '2025',
            'sub_prefix': 'Rol: Consultor Web Freelance & Diseñador Full-Stack | Cliente PYME | ',
            'link_text': 'deralexsander.github.io/GMConstructora',
            'link_url': 'https://deralexsander.github.io/GMConstructora/',
            'bullets': [
                ('Consultoría Digital Integral:', 'Levantamiento de requerimientos y desarrollo de presencia digital corporativa orientada a catálogo de obras y captación de clientes.'),
                ('Infraestructura & DNS:', 'Asesoría técnica en adquisición de dominio web (URL), configuración DNS y despliegue a producción sobre GitHub Pages.'),
                ('Rendimiento & Móvil:', 'Maquetación responsive mobile-first, optimización de activos WebP para alta velocidad y enlace directo a canal de ventas vía WhatsApp.')
            ]
        },
        {
            'title': 'Notes & Sillage – Catálogo Digital de Fragancias y E-commerce',
            'date': '2024 – 2025',
            'sub_prefix': 'Rol: Fundador & Desarrollador Web | Emprendimiento Propio | ',
            'link_text': 'notes.cl (Demo en Vivo)',
            'link_url': 'https://deralexsander.github.io/notes-and-sillage/',
            'bullets': [
                ('Catálogo Digital Interactivo:', 'Desarrollo de plataforma web responsiva (mobile-first) para resolver la fricción en ventas de fragancias y automatizar pedidos comerciales.'),
                ('Buscador Reactivo & Checkout:', 'Buscador en tiempo real por familias olfativas y generador dinámico de checkout estructurado hacia la API de WhatsApp.'),
                ('Alta Disponibilidad:', 'Arquitectura estática sobre GitHub Pages y Cloudflare con costo cero de mantenimiento, carga instantánea y disponibilidad 24/7.')
            ]
        },
        {
            'title': 'Servicio CATTECH – Plataforma de Integración y Pagos',
            'date': 'Ago 2024 – Nov 2024',
            'sub_prefix': 'Rol: Líder Técnico / Desarrollador Full-Stack | Proyecto Integrador | ',
            'link_text': 'github.com/deralexsander/Servicio-CATTECH',
            'link_url': 'https://github.com/deralexsander/Servicio-CATTECH',
            'bullets': [
                ('Pasarela de Pagos:', 'Procesé transacciones financieras seguras integrando la API de Mercado Pago y programé un motor de validación para transferencias bancarias directas.'),
                ('Persistencia NoSQL:', 'Migré la capa de persistencia a Cloud Firestore, disminuyendo la latencia de consulta en un 40% y configurando reglas de seguridad NoSQL granulares.')
            ]
        }
    ]

    for p in p1_list:
        y = draw_project(ctx, y, p)

    draw_footer(ctx, 1)
    surface.show_page()

    # ================= PAGE 2 =================
    y = 48.0
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(8.0)
    ctx.set_source_rgb(0.42, 0.48, 0.56)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('NICOLÁS ALEXSANDER MUÑOZ MÉNDEZ  •  CURRÍCULUM VITAE (CONTINUACIÓN)')
    y += 8.0

    ctx.set_source_rgb(0.78, 0.82, 0.88)
    ctx.set_line_width(0.75)
    ctx.move_to(MARGIN_L, y)
    ctx.line_to(MARGIN_R, y)
    ctx.stroke()
    y += 16.0

    # 1. OTROS PROYECTOS TÉCNICOS & DESARROLLO DE SOFTWARE
    y = draw_section_title(ctx, y, 'OTROS PROYECTOS TÉCNICOS & DESARROLLO DE SOFTWARE')
    p2_list = [
        {
            'title': 'FerreMas – E-commerce y Gestión Logística',
            'date': 'Abr 2025 – Jun 2025',
            'sub_prefix': 'Rol: Desarrollador Full-Stack | Proyecto Académico Integrador | ',
            'link_text': 'github.com/deralexsander/web_FerreMas',
            'link_url': 'https://github.com/deralexsander/web_FerreMas',
            'bullets': [
                ('Autenticación Segura:', 'Aseguré el flujo de autenticación mediante Google OAuth 2.0 y Firebase Authentication, eliminando accesos no autorizados.'),
                ('Control de Acceso RBAC:', 'Optimicé la gestión operativa diferenciando perfiles mediante Control de Acceso Basado en Roles entre Clientes y Administradores.'),
                ('Geolocalización & Rutas:', 'Integré la API de Google Maps para geolocalización y cálculo de despachos entre sucursales, reduciendo el error en locales.')
            ]
        },
        {
            'title': 'NekoBeansWeb – Sistema de Administración para PYMES',
            'date': 'Abr 2023 – Jul 2023',
            'sub_prefix': 'Rol: Desarrollador Full-Stack | Proyecto Académico Integrador | ',
            'link_text': 'github.com/deralexsander/web_nekobeans',
            'link_url': 'https://github.com/deralexsander/web_nekobeans',
            'bullets': [
                ('Gestión Comercial:', 'Digitalicé el circuito comercial de ventas y cotizaciones para PYMES mediante formularios dinámicos y segregación de roles (Vendedor/Cliente).'),
                ('Modelo Relacional:', 'Diseñé el esquema relacional en PostgreSQL garantizando integridad transaccional en flujos de pago híbridos (efectivo y transferencia).')
            ]
        }
    ]
    for p in p2_list:
        y = draw_project(ctx, y, p)

    y += 4.0

    # 2. HABILIDADES TÉCNICAS Y STACK
    y = draw_section_title(ctx, y, 'HABILIDADES TÉCNICAS Y STACK TECNOLÓGICO')
    skills = [
        ('Lenguajes de Programación:', 'Python, JavaScript (ES6+), TypeScript, Java, SQL, HTML5, CSS3/SCSS.'),
        ('Backend y APIs:', 'Django, Django REST Framework, Node.js, arquitectura RESTful, microservicios, seguridad 2FA/HMAC.'),
        ('Frontend y Móvil:', 'HTMX, CSS3 Modular (Dark Theme), diseño responsivo accesible (WCAG), Bootstrap, Android Studio.'),
        ('Datos y Machine Learning:', 'PostgreSQL, Cloud Firestore (GCP), Scikit-Learn, XGBoost, modelado relacional y NoSQL indexado.'),
        ('Cloud, DevOps y Seguridad:', 'Railway, Cloudflare, dominios corporativos, certificados SSL/TLS, Git, GitHub, Linux, CI/CD.'),
        ('Metodologías de Trabajo:', 'Scrum, Kanban, Pair Programming, Code Reviews, levantamiento de requerimientos técnicos.')
    ]
    for prefix, desc in skills:
        y = draw_bullet(ctx, MARGIN_L, y, prefix, desc, USABLE_W, line_h=11.6, font_size=8.3)
        y += 1.8

    y += 8.0

    # 3. EDUCACIÓN
    y = draw_section_title(ctx, y, 'EDUCACIÓN SUPERIOR')
    edu = [
        {
            'title': 'Duoc UC – Sede Viña del Mar',
            'date': '2023 – 2026',
            'sub_prefix': 'Carrera: Ingeniería en Informática (Egresando / Cursando último año)',
            'bullets': [
                ('Formación Especializada:', 'Enfoque práctico en ingeniería de software, arquitectura de sistemas, bases de datos relacionales y NoSQL, desarrollo full-stack y gestión ágil de proyectos tecnológicos.')
            ]
        },
        {
            'title': 'Colegio Don Orione',
            'date': '2019 – 2022',
            'sub_prefix': 'Titulación: Técnico de Nivel Medio en Electrónica',
            'bullets': [
                ('Bases Técnicas:', 'Formación en circuitos lógicos, microcontroladores, automatización, diseño de hardware y pensamiento analítico para resolución de problemas complejos.')
            ]
        }
    ]
    for e in edu:
        ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(9.2)
        ctx.set_source_rgb(0.06, 0.09, 0.15)
        ctx.move_to(MARGIN_L, y)
        ctx.show_text(e['title'])
        
        ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(8.2)
        ctx.set_source_rgb(0.4, 0.46, 0.54)
        date_w = ctx.text_extents(e['date']).x_advance
        ctx.move_to(MARGIN_R - date_w, y)
        ctx.show_text(e['date'])
        y += 10.5
        
        ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(8.1)
        ctx.set_source_rgb(0.24, 0.28, 0.35)
        ctx.move_to(MARGIN_L, y)
        ctx.show_text(e['sub_prefix'])
        y += 11.5
        
        for b_prefix, b_text in e['bullets']:
            y = draw_bullet(ctx, MARGIN_L, y, b_prefix, b_text, USABLE_W, line_h=11.2, font_size=8.2)
            y += 1.2
        y += 3.5

    y += 8.0

    # 4. CERTIFICACIONES INTERNACIONALES Y DISTINCIONES
    y = draw_section_title(ctx, y, 'CERTIFICACIONES INTERNACIONALES Y DISTINCIONES')
    certs = [
        ('Cisco Networking Academy & Python Institute:', 'Partner: PCAP – Programming Essentials in Python (Julio 2023).'),
        ('CertiProf International:', 'DevOps Foundation Professional Certificate (DFPC™) – ID: TLZZKDZKTHL-XPXRMHPSH-RLKFTJJHSS.'),
        ('CertiProf International:', 'DevOps Essentials Professional Certificate (DEPC®) – ID: TLZZLLDVDKK-XPWTMQXHS-RLKRJKLLTT.'),
        ('MakeX Robotics Competition:', '1.er Lugar Regional – Medalla de Oro en diseño y programación de algoritmos de navegación autónoma en tiempo real.')
    ]
    for prefix, desc in certs:
        y = draw_bullet(ctx, MARGIN_L, y, prefix, desc, USABLE_W, line_h=11.6, font_size=8.3)
        y += 1.8

    draw_footer(ctx, 2)
    surface.show_page()
    surface.finish()

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_pdf = os.path.join(repo_dir, "assets", "cv-nicolas-munoz.pdf")
    root_pdf = os.path.join(repo_dir, "cv profecional.pdf")
    
    print("⚡ Compilando CV profesional en PDF con Cairo y TrueType...")
    generate_pdf(assets_pdf)
    
    # Copia a la raíz para compatibilidad con accesos previos
    import shutil
    shutil.copy2(assets_pdf, root_pdf)
    
    print(f"✅ CV generado exitosamente con fuentes TrueType embebidas y enlaces activos:")
    print(f"   • {assets_pdf}")
    print(f"   • {root_pdf}")

if __name__ == "__main__":
    main()
