#!/usr/bin/env python3
"""
Generador automático de CV en PDF para Nicolás Muñoz (catstudio.cl)
Genera un documento A4 profesional de 1 página, optimizado para ATS (Applicant Tracking Systems),
con tipografía TrueType embebida, enlaces interactivos activos y métricas de impacto reales
sincronizadas desde los repositorios y portafolio de proyectos.
"""
import os
import shutil
import cairo

PAGE_W = 595.28
PAGE_H = 841.89
MARGIN_L = 38.0
MARGIN_R = 557.28
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

def draw_bullet(ctx, x, y, bold_prefix, text, max_w, line_h=10.8, font_size=8.1):
    ctx.save()
    # Bullet dot
    ctx.set_source_rgb(0.28, 0.36, 0.48)
    ctx.arc(x + 3.0, y - 2.8, 1.6, 0, 2 * 3.14159)
    ctx.fill()
    
    text_x = x + 11.5
    avail_w1 = max_w - 11.5
    
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
        ctx.set_source_rgb(0.06, 0.1, 0.18)
        ctx.move_to(text_x, curr_y)
        ctx.show_text(bold_prefix + ' ')
        
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0.18, 0.22, 0.28)
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

def draw_section_title(ctx, y, title):
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(9.8)
    ctx.set_source_rgb(0.06, 0.1, 0.2)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text(title)
    y += 3.5
    ctx.set_source_rgb(0.72, 0.77, 0.85)
    ctx.set_line_width(0.6)
    ctx.move_to(MARGIN_L, y)
    ctx.line_to(MARGIN_R, y)
    ctx.stroke()
    y += 11.5
    return y

def draw_header(ctx, y):
    # Name
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(19.0)
    ctx.set_source_rgb(0.06, 0.09, 0.16)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('Nicolás Alexsander Muñoz Méndez')
    y += 14.0

    # Headline
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(9.8)
    ctx.set_source_rgb(0.18, 0.24, 0.35)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('Desarrollador Full-Stack | Egresando de Ingeniería en Informática | Técnico en Electrónica')
    y += 12.5

    # Contact Bar - 2 balanced lines with clickable tags
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.2)

    def draw_contact_line(items, line_y):
        cur_x = MARGIN_L
        sep = '   •   '
        for i, (label, url) in enumerate(items):
            is_last = (i == len(items) - 1)
            if url:
                ctx.set_source_rgb(0.1, 0.35, 0.75)
                ctx.move_to(cur_x, line_y)
                ctx.tag_begin(cairo.TAG_LINK, f"uri='{url}'")
                ctx.show_text(label)
                ctx.tag_end(cairo.TAG_LINK)
                cur_x += ctx.text_extents(label).x_advance
            else:
                ctx.set_source_rgb(0.25, 0.3, 0.38)
                ctx.move_to(cur_x, line_y)
                ctx.show_text(label)
                cur_x += ctx.text_extents(label).x_advance
            if not is_last:
                ctx.set_source_rgb(0.55, 0.6, 0.68)
                ctx.move_to(cur_x, line_y)
                ctx.show_text(sep)
                cur_x += ctx.text_extents(sep).x_advance

    line1 = [
        ('Valparaíso, Chile', None),
        ('nico.alexander.m.m@gmail.com', 'mailto:nico.alexander.m.m@gmail.com'),
        ('+56 9 6878 7862', 'tel:+56968787862')
    ]
    draw_contact_line(line1, y)
    y += 10.5

    line2 = [
        ('linkedin.com/in/nicolas-munoz-mendez', 'https://www.linkedin.com/in/nicol%C3%A1s-mu%C3%B1oz-mend%C3%A9z-abb791292'),
        ('github.com/deralexsander', 'https://github.com/deralexsander'),
        ('catstudio.cl (Portafolio)', 'https://deralexsander.github.io/deralexsander/')
    ]
    draw_contact_line(line2, y)
    y += 9.0

    # Divider line
    ctx.set_source_rgb(0.8, 0.84, 0.9)
    ctx.set_line_width(0.7)
    ctx.move_to(MARGIN_L, y)
    ctx.line_to(MARGIN_R, y)
    ctx.stroke()
    y += 12.0
    return y

def draw_project(ctx, y, p):
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(9.1)
    ctx.set_source_rgb(0.06, 0.09, 0.16)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text(p['title'])
    
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.0)
    ctx.set_source_rgb(0.4, 0.46, 0.54)
    date_w = ctx.text_extents(p['date']).x_advance
    ctx.move_to(MARGIN_R - date_w, y)
    ctx.show_text(p['date'])
    y += 10.0
    
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.0)
    ctx.set_source_rgb(0.25, 0.3, 0.38)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text(p['sub_prefix'])
    sub_w = ctx.text_extents(p['sub_prefix']).x_advance
    
    if 'link_text' in p and p['link_text']:
        ctx.set_source_rgb(0.1, 0.35, 0.75)
        ctx.move_to(MARGIN_L + sub_w, y)
        ctx.tag_begin(cairo.TAG_LINK, f"uri='{p['link_url']}'")
        ctx.show_text(p['link_text'])
        ctx.tag_end(cairo.TAG_LINK)
    y += 10.5
    
    for b_prefix, b_text in p['bullets']:
        y = draw_bullet(ctx, MARGIN_L, y, b_prefix, b_text, USABLE_W, line_h=10.8, font_size=8.1)
        y += 1.0
    y += 3.0
    return y

def draw_footer(ctx):
    ctx.set_source_rgb(0.82, 0.86, 0.9)
    ctx.set_line_width(0.5)
    ctx.move_to(MARGIN_L, 814)
    ctx.line_to(MARGIN_R, 814)
    ctx.stroke()

    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(7.8)
    ctx.set_source_rgb(0.45, 0.5, 0.58)
    ctx.move_to(MARGIN_L, 825)
    ctx.show_text('Nicolás Alexsander Muñoz Méndez — Currículum Vitae  •  Formato ATS Optimizado')
    
    right_text = 'Página 1 de 1  •  '
    w_rt = ctx.text_extents(right_text).x_advance
    ctx.move_to(MARGIN_R - 120, 825)
    ctx.show_text(right_text)
    
    ctx.move_to(MARGIN_R - 120 + w_rt, 825)
    ctx.set_source_rgb(0.1, 0.35, 0.75)
    ctx.tag_begin(cairo.TAG_LINK, "uri='https://deralexsander.github.io/deralexsander/'")
    ctx.show_text('catstudio.cl')
    ctx.tag_end(cairo.TAG_LINK)

def generate_pdf(output_path):
    surface = cairo.PDFSurface(output_path, PAGE_W, PAGE_H)
    ctx = cairo.Context(surface)

    y = draw_header(ctx, 38.0)

    # 1. PERFIL PROFESIONAL
    y = draw_section_title(ctx, y, 'PERFIL PROFESIONAL')
    profile_text = (
        'Desarrollador Full-Stack con base técnica en electrónica, enfocado en arquitectura de software, APIs '
        'RESTful escalables e integración de Machine Learning aplicado. Experiencia en despliegue de plataformas '
        'SaaS en producción (Railway, Cloudflare), PostgreSQL optimizado (+60.000 registros) y desarrollo frontend '
        'reactivo (HTMX, TypeScript, Angular). Metodología Scrum, doble certificación internacional en DevOps '
        '(CertiProf DFPC™/DEPC®), certificación en Python (Cisco PCAP) y 1.er lugar regional en robótica competitiva.'
    )
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.2)
    ctx.set_source_rgb(0.18, 0.22, 0.28)
    for line in wrap_text(ctx, profile_text, USABLE_W):
        ctx.move_to(MARGIN_L, y)
        ctx.show_text(line)
        y += 11.0
    y += 6.0

    # 2. EXPERIENCIA LABORAL Y PROYECTOS DESTACADOS
    y = draw_section_title(ctx, y, 'EXPERIENCIA LABORAL Y PROYECTOS DESTACADOS')
    projects = [
        {
            'title': 'SmartBids – SaaS de Inteligencia Comercial y Licitaciones Públicas',
            'date': 'Ago 2025 – Dic 2025',
            'sub_prefix': 'Rol: Desarrollador Full-Stack (Backend, Cloud & Seguridad) | SaaS en Producción | ',
            'link_text': 'smartbids.cl',
            'link_url': 'https://smartbids.cl',
            'bullets': [
                ('Backend & Optimización:', 'Diseñé la arquitectura en Django REST y modelo relacional en PostgreSQL con +60.000 licitaciones indexadas, reduciendo en un 75% el tiempo de búsqueda para MiPyMEs.'),
                ('Machine Learning & UI:', 'Entrené modelos predictivos con Scikit-Learn y XGBoost (82% F1-score) en adjudicaciones públicas e implementé interfaz ultrarrápida con HTMX sin sobrecarga de SPA.'),
                ('Cloud & Seguridad:', 'Despliegue en Railway con dominio corporativo y SSL/TLS estricto; implementé autenticación 2FA/OTP con Gmail API REST y control de sesiones con firmas HMAC.')
            ]
        },
        {
            'title': 'Servicio CATTECH – Plataforma de Integración y Pasarela Financiera',
            'date': 'Ago 2024 – Nov 2024',
            'sub_prefix': 'Rol: Desarrollador Full-Stack Principal | Proyecto Integrador | ',
            'link_text': 'github.com/deralexsander/Servicio-CATTECH',
            'link_url': 'https://github.com/deralexsander/Servicio-CATTECH',
            'bullets': [
                ('Pasarela Financiera:', 'Integré el SDK de Mercado Pago para pagos seguros con tarjeta y desarrollé motor de validación transaccional para transferencias bancarias directas.'),
                ('Persistencia NoSQL & Móvil:', 'Migré arquitectura a Cloud Firestore (GCP) reduciendo latencia de consulta en un 40% con reglas de seguridad granulares; empaquetado móvil con Capacitor y Angular/Ionic.')
            ]
        },
        {
            'title': 'Notes & Sillage – E-Commerce Serverless & Catálogo de Fragancias',
            'date': '2024 – 2025',
            'sub_prefix': 'Rol: Fundador & Desarrollador Full-Stack | notes.cl | ',
            'link_text': 'Demo notes.cl',
            'link_url': 'https://notes.cl/',
            'bullets': [
                ('Evolución Serverless & Cloud:', 'Evolucioné el catálogo estático a arquitectura Serverless con Cloud Firestore (GCP) para persistencia transaccional de pedidos, reglas NoSQL y notificaciones push inmediatas (ntfy).'),
                ('Tracción & Nuevo Cliente D&G:', 'Infraestructura Cloudflare SSL/DNS con 100% uptime y costo cero; la tracción comercial generó el encargo directo del catálogo D & G Parfums (deralexsander.github.io/d-and-g-parfums).')
            ]
        },
        {
            'title': 'FerreMas – E-Commerce y Plataforma de Gestión Logística',
            'date': 'Abr 2025 – Jun 2025',
            'sub_prefix': 'Rol: Desarrollador Full-Stack | Proyecto Académico Integrador | ',
            'link_text': 'github.com/deralexsander/web_FerreMas',
            'link_url': 'https://github.com/deralexsander/web_FerreMas',
            'bullets': [
                ('Autenticación & Roles RBAC:', 'Implementé autenticación federada con Google OAuth 2.0 y Firebase Auth con roles RBAC granulares (Clientes, Vendedores, Administradores).'),
                ('Geolocalización & Rutas:', 'Integré Google Maps API para geolocalización de sucursales y cálculo dinámico de costos y despachos logísticos entre regiones.')
            ]
        },
        {
            'title': 'G&M Constructora – Plataforma Corporativa y Consultoría Web',
            'date': '2025',
            'sub_prefix': 'Rol: Consultor Web Freelance & Diseñador Full-Stack | Cliente PYME | ',
            'link_text': 'deralexsander.github.io/GMConstructora',
            'link_url': 'https://deralexsander.github.io/GMConstructora/',
            'bullets': [
                ('Consultoría & Catálogo de Obras:', 'Levantamiento de requerimientos, diseño UI/UX mobile-first de catálogo de servicios/obras reales para alta conversión, gestión de dominio/DNS y despliegue a producción.')
            ]
        }
    ]
    for p in projects:
        y = draw_project(ctx, y, p)

    y += 3.0

    # 3. HABILIDADES TÉCNICAS Y STACK TECNOLÓGICO
    y = draw_section_title(ctx, y, 'HABILIDADES TÉCNICAS Y STACK TECNOLÓGICO')
    skills = [
        ('Lenguajes de Programación:', 'Python, JavaScript (ES6+), TypeScript, SQL, Java, Kotlin, HTML5, CSS3/SCSS.'),
        ('Backend y Arquitectura:', 'Django, Django REST Framework, Node.js, Express, arquitectura RESTful, autenticación 2FA/HMAC, RBAC.'),
        ('Frontend y Móvil:', 'HTMX, Angular, Ionic Framework, TypeScript, Capacitor, CSS3 Modular (Dark Theme), Bootstrap, Android Studio.'),
        ('Datos y Machine Learning:', 'PostgreSQL (consultas complejas, indexación, ACID), Cloud Firestore (GCP), Scikit-Learn, XGBoost, Pandas.'),
        ('Cloud, DevOps y Herramientas:', 'Railway, Cloudflare, Google Cloud (GCP), Git, GitHub, Docker básico, Linux (Bash), CI/CD, Postman.'),
        ('Metodologías de Trabajo:', 'Scrum (iteraciones ágiles), Kanban, Code Reviews, Pair Programming, levantamiento de requerimientos.')
    ]
    for prefix, desc in skills:
        y = draw_bullet(ctx, MARGIN_L, y, prefix, desc, USABLE_W, line_h=10.8, font_size=8.1)
        y += 0.8
    y += 3.5

    # 4. EDUCACIÓN Y FORMACIÓN TÉCNICA
    y = draw_section_title(ctx, y, 'EDUCACIÓN Y FORMACIÓN TÉCNICA')
    
    # 4.1 Duoc UC
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(9.1)
    ctx.set_source_rgb(0.06, 0.09, 0.16)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('Duoc UC – Sede Viña del Mar')
    
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.0)
    ctx.set_source_rgb(0.4, 0.46, 0.54)
    date_w = ctx.text_extents('2023 – 2026').x_advance
    ctx.move_to(MARGIN_R - date_w, y)
    ctx.show_text('2023 – 2026')
    y += 9.5

    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.0)
    ctx.set_source_rgb(0.25, 0.3, 0.38)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('Carrera: Ingeniería en Informática (Egresando / Cursando último año)')
    y += 10.0

    y = draw_bullet(ctx, MARGIN_L, y, 'Formación Especializada:', 'Enfoque práctico en ingeniería de software, arquitectura de sistemas, bases de datos relacionales y NoSQL, desarrollo full-stack, DevOps y gestión ágil.', USABLE_W, line_h=10.4, font_size=8.0)
    y += 3.5

    # 4.2 Colegio Don Orione - Técnico en Electrónica
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(9.1)
    ctx.set_source_rgb(0.06, 0.09, 0.16)
    ctx.move_to(MARGIN_L, y)
    ctx.show_text('Colegio Don Orione – Quintero')
    
    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.0)
    ctx.set_source_rgb(0.4, 0.46, 0.54)
    date_w = ctx.text_extents('Titulado (2022)').x_advance
    ctx.move_to(MARGIN_R - date_w, y)
    ctx.show_text('Titulado (2022)')
    y += 9.5

    ctx.select_font_face('Liberation Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(8.0)
    ctx.set_source_rgb(0.25, 0.3, 0.38)
    ctx.move_to(MARGIN_L, y)
    titulo_label = 'Título: Técnico de Nivel Medio en Electrónica (Reg. Mineduc / SECREDUC Nº 29219)'
    ctx.show_text(titulo_label)
    label_w = ctx.text_extents(titulo_label + ' ').x_advance
    
    # Clickable link to official certificate PDF
    ctx.set_source_rgb(0.1, 0.35, 0.75)
    ctx.move_to(MARGIN_L + label_w, y)
    ctx.tag_begin(cairo.TAG_LINK, "uri='https://deralexsander.github.io/deralexsander/assets/certificates/tecnico-nivel-medio-electronica.pdf'")
    ctx.show_text('[Ver Certificado Oficial PDF]')
    ctx.tag_end(cairo.TAG_LINK)
    y += 10.0

    y = draw_bullet(ctx, MARGIN_L, y, 'Especialidad Técnica:', 'Fundamentos sólidos en circuitos análogos/digitales, microcontroladores, instrumentación, diagnóstico de fallas y soporte integral de hardware electrónico.', USABLE_W, line_h=10.4, font_size=8.0)
    y += 4.5

    # 5. CERTIFICACIONES INTERNACIONALES Y DISTINCIONES
    y = draw_section_title(ctx, y, 'CERTIFICACIONES INTERNACIONALES Y DISTINCIONES')
    certs = [
        ('Cisco Partner & Python Institute:', 'PCAP – Programming Essentials in Python (Julio 2023).'),
        ('CertiProf International:', 'DevOps Foundation (DFPC™: TLZZKDZKTHL-XPXRMHPSH-RLKFTJJHSS) & DevOps Essentials (DEPC®).'),
        ('MakeX Robotics Competition:', '1.er Lugar Regional – Medalla de Oro en diseño y programación de algoritmos de navegación autónoma en tiempo real.')
    ]
    for prefix, desc in certs:
        y = draw_bullet(ctx, MARGIN_L, y, prefix, desc, USABLE_W, line_h=10.6, font_size=8.0)
        y += 0.8

    draw_footer(ctx)
    surface.show_page()
    surface.finish()

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_pdf = os.path.join(repo_dir, "assets", "cv-nicolas-munoz.pdf")
    root_pdf = os.path.join(repo_dir, "cv profecional.pdf")
    
    print("⚡ Compilando CV profesional optimizado (1 página, ATS-friendly) con Cairo y TrueType...")
    generate_pdf(assets_pdf)
    
    # Copia a la raíz para compatibilidad con accesos previos
    shutil.copy2(assets_pdf, root_pdf)
    
    print("✅ CV generado exitosamente con fuentes TrueType embebidas y enlaces activos:")
    print(f"   • {assets_pdf}")
    print(f"   • {root_pdf}")

if __name__ == "__main__":
    main()
