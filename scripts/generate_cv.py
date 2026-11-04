#!/usr/bin/env python3
"""
Generador automático de CV en PDF para Nicolás Muñoz (catstudio.cl)
Compila un documento A4 profesional, ATS-friendly y sincronizado con el portafolio.
"""
import subprocess
import os

def esc(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def generate_postscript():
    # A4 Dimensions in points (1 pt = 1/72 inch): 595.28 x 841.89
    ps = []
    ps.append("%!PS-Adobe-3.0")
    ps.append("%%BoundingBox: 0 0 595 842")
    ps.append("%%Pages: 2")
    ps.append("%%EndComments")
    
    # Procedures
    ps.append("""
    /FTitle { /Helvetica-Bold findfont 18 scalefont setfont } def
    /FSub { /Helvetica-Bold findfont 10 scalefont setfont } def
    /FSec { /Helvetica-Bold findfont 11 scalefont setfont } def
    /FItem { /Helvetica-Bold findfont 9.5 scalefont setfont } def
    /FBody { /Helvetica findfont 9 scalefont setfont } def
    /FBodyB { /Helvetica-Bold findfont 9 scalefont setfont } def
    /FSmall { /Helvetica findfont 8 scalefont setfont } def
    /FDate { /Helvetica findfont 8.5 scalefont setfont } def
    
    /line {
        newpath
        moveto
        lineto
        stroke
    } def
    
    /bullet {
        newpath
        2 sub exch
        2.2 0 360 arc
        fill
    } def
    """)
    
    # -------------------------------------------------------------
    # PAGE 1
    # -------------------------------------------------------------
    ps.append("%%Page: 1 1")
    
    # Header
    ps.append(f"FSmall 0.4 setgray 50 805 moveto ({esc('ULTIMA ACTUALIZACION: NOVIEMBRE 2026 - SINCRONIZADO CON PORTAFOLIO')}) show")
    ps.append(f"FTitle 0 setgray 50 782 moveto ({esc('Nicolas Alexsander Munoz Mendez')}) show")
    ps.append(f"FSub 0.2 setgray 50 766 moveto ({esc('Desarrollador Full-Stack | Egresando de Ingenieria en Informatica (2026)')}) show")
    
    # Contact Row
    ps.append(f"FSmall 0.3 setgray 50 750 moveto ({esc('Valparaiso, Chile   |   nico.alexander.m.m@gmail.com   |   +56 9 6878 7862   |   catstudio.cl   |   github.com/deralexsander')}) show")
    
    # Line divider
    ps.append("0.8 setlinewidth 0.2 setgray 50 740 545 740 line")
    
    # Section: Perfil Profesional
    ps.append(f"FSec 0 setgray 50 722 moveto ({esc('PERFIL PROFESIONAL')}) show")
    ps.append("0.4 setlinewidth 0.7 setgray 50 716 545 716 line")
    
    profile_lines = [
        "Desarrollador con solida formacion en ingenieria de software, arquitectura de sistemas y diseno de interfaces UI/UX.",
        "Experiencia comprobada en despliegue de soluciones SaaS en produccion, desarrollo frontend reactivo con HTMX y CSS3",
        "modular, infraestructura cloud (Railway, Cloudflare, dominios y certificados SSL/TLS), seguridad de sesiones (2FA/OTP con",
        "Gmail API, tokens HMAC) y consumo eficiente de APIs RESTful. Trabajo colaborativo bajo marco agil Scrum y primer",
        "lugar regional en robotica competitiva y resolucion algoritmica."
    ]
    y = 702
    ps.append("FBody 0.15 setgray")
    for l in profile_lines:
        ps.append(f"50 {y} moveto ({esc(l)}) show")
        y -= 12
        
    # Section: Proyectos y Experiencia Tecnica
    y -= 6
    ps.append(f"FSec 0 setgray 50 {y} moveto ({esc('PROYECTOS Y EXPERIENCIA TECNICA')}) show")
    y -= 6
    ps.append(f"0.4 setlinewidth 0.7 setgray 50 {y} 545 {y} line")
    y -= 16
    
    # 1. SmartBids
    ps.append(f"FItem 0 setgray 50 {y} moveto ({esc('SmartBids - SaaS de Inteligencia Comercial y Licitaciones Publicas')}) show")
    ps.append(f"FDate 0.4 setgray 450 {y} moveto ({esc('Ago 2025 - Dic 2025')}) show")
    y -= 12
    ps.append(f"FSmall 0.2 setgray 50 {y} moveto ({esc('Rol: Team Developer - Frontend, Cloud & Security   |   Cliente Real en Produccion   |   smartbids.cl')}) show")
    y -= 13
    
    sb_bullets = [
        "Frontend & UI/UX: Disene e implemente la interfaz responsiva, accesible y ultra veloz con HTML5, CSS3 modular (Dark",
        "Theme) y HTMX, eliminando la sobrecarga de SPAs pesadas y garantizando una experiencia fluida.",
        "Infraestructura Cloud: Despliegue en produccion sobre Railway, configuracion de dominio corporativo propio (smartbids.cl)",
        "y certificados de seguridad estricta SSL/TLS.",
        "Seguridad & Identidad: Implemente la capa de autenticacion de dos factores (2FA / OTP transaccional con Gmail API REST),",
        "control de sesiones seguras y validacion de tokens con firmas HMAC.",
        "Metodologia Agil: Trabajo en equipo multidisciplinario bajo marco Scrum estructurado en iteraciones cortas (Sprints)",
        "con bitacoras semanales de avance y mitigacion de bloqueos."
    ]
    ps.append("FBody 0.15 setgray")
    for b in sb_bullets:
        if not b.startswith("Theme") and not b.startswith("y certificados") and not b.startswith("control de") and not b.startswith("con bitacoras"):
            ps.append(f"56 {y+4} bullet")
            ps.append(f"64 {y} moveto ({esc(b)}) show")
        else:
            ps.append(f"64 {y} moveto ({esc(b)}) show")
        y -= 11.5

    # 2. Notes & Sillage
    y -= 4
    ps.append(f"FItem 0 setgray 50 {y} moveto ({esc('Notes & Sillage - Catalogo Digital de Perfumeria & E-Commerce Ligero')}) show")
    ps.append(f"FDate 0.4 setgray 445 {y} moveto ({esc('2025 - En Produccion')}) show")
    y -= 12
    ps.append(f"FSmall 0.2 setgray 50 {y} moveto ({esc('Rol: Creador & Desarrollador Principal   |   Solucion JAMstack en Produccion   |   notes.cl')}) show")
    y -= 13
    
    ns_bullets = [
        "Disene y desarrolle una plataforma e-commerce y catalogo interactivo mobile-first sin dependencia de servidores",
        "externos, garantizando tiempos de renderizado inferiores a 800ms.",
        "Infraestructura y Redes: Gestion de dominio propio (notes.cl), proxy perimetral de cache y SSL estricto con Cloudflare,",
        "y automatizacion de despliegues (CI/CD) con GitHub Pages.",
        "Buscador predictivo con tolerancia a errores tipograficos y checkout automatizado hacia WhatsApp."
    ]
    ps.append("FBody 0.15 setgray")
    for b in ns_bullets:
        if not b.startswith("externos") and not b.startswith("y automatizacion"):
            ps.append(f"56 {y+4} bullet")
            ps.append(f"64 {y} moveto ({esc(b)}) show")
        else:
            ps.append(f"64 {y} moveto ({esc(b)}) show")
        y -= 11.5

    # 3. GM Constructora
    y -= 4
    ps.append(f"FItem 0 setgray 50 {y} moveto ({esc('Constructora Godoy & Mendez SpA - Plataforma Corporativa')}) show")
    ps.append(f"FDate 0.4 setgray 518 {y} moveto ({esc('2025')}) show")
    y -= 12
    ps.append(f"FSmall 0.2 setgray 50 {y} moveto ({esc('Rol: Consultor Web & Desarrollador Full-Stack   |   Cliente Real PYME')}) show")
    y -= 13
    
    gm_bullets = [
        "Servicio integral de consultoria y desarrollo: desde levantamiento de requerimientos y diseno UI/UX hasta la puesta",
        "en marcha tecnica y corporativa del sitio web.",
        "Administracion de infraestructura: Compra y configuracion de dominios, zonas DNS, SSL y correos corporativos."
    ]
    ps.append("FBody 0.15 setgray")
    for b in gm_bullets:
        if not b.startswith("en marcha"):
            ps.append(f"56 {y+4} bullet")
            ps.append(f"64 {y} moveto ({esc(b)}) show")
        else:
            ps.append(f"64 {y} moveto ({esc(b)}) show")
        y -= 11.5

    # Page 1 Footer
    ps.append(f"FSmall 0.5 setgray 50 35 moveto ({esc('Nicolas Alexsander Munoz Mendez - Pagina 1 de 2')}) show")
    ps.append(f"FSmall 0.5 setgray 440 35 moveto ({esc('catstudio.cl - Portafolio Oficial')}) show")
    ps.append("showpage")
    
    # -------------------------------------------------------------
    # PAGE 2
    # -------------------------------------------------------------
    ps.append("%%Page: 2 2")
    y = 800
    ps.append(f"FTitle 0 setgray 50 {y} moveto ({esc('Nicolas Alexsander Munoz Mendez')}) show")
    y -= 16
    ps.append(f"FSub 0.3 setgray 50 {y} moveto ({esc('Curriculum Vitae Tecnico - Continuacion')}) show")
    y -= 10
    ps.append(f"0.8 setlinewidth 0.2 setgray 50 {y} 545 {y} line")
    y -= 22
    
    # FerreMas & CATTECH
    ps.append(f"FSec 0 setgray 50 {y} moveto ({esc('EXPERIENCIA EN PROYECTOS INTEGRADORES')}) show")
    y -= 6
    ps.append(f"0.4 setlinewidth 0.7 setgray 50 {y} 545 {y} line")
    y -= 16
    
    ps.append(f"FItem 0 setgray 50 {y} moveto ({esc('FerreMas - E-commerce y Gestion Logistica')}) show")
    ps.append(f"FDate 0.4 setgray 450 {y} moveto ({esc('Abr 2025 - Jun 2025')}) show")
    y -= 12
    ps.append(f"FSmall 0.2 setgray 50 {y} moveto ({esc('Rol: Desarrollador Full-Stack   |   Android Studio, Java/Kotlin, Firebase, Google Maps API')}) show")
    y -= 13
    
    fm_bullets = [
        "Asegure el flujo de autenticacion de usuarios mediante Google OAuth 2.0 y control de acceso por roles (RBAC).",
        "Integre la API de Google Maps para geolocalizacion y calculo automatico de despachos entre sucursales."
    ]
    ps.append("FBody 0.15 setgray")
    for b in fm_bullets:
        ps.append(f"56 {y+4} bullet")
        ps.append(f"64 {y} moveto ({esc(b)}) show")
        y -= 12
        
    y -= 4
    ps.append(f"FItem 0 setgray 50 {y} moveto ({esc('Servicio CATTECH - Plataforma de Integracion y Pagos')}) show")
    ps.append(f"FDate 0.4 setgray 448 {y} moveto ({esc('Ago 2024 - Nov 2024')}) show")
    y -= 12
    ps.append(f"FSmall 0.2 setgray 50 {y} moveto ({esc('Rol: Lider Tecnico / Desarrollador Full-Stack   |   Cloud Firestore, Mercado Pago SDK, JavaScript ES6+')}) show")
    y -= 13
    
    cat_bullets = [
        "Procese transacciones financieras integrando la API de Mercado Pago y programe motor de validacion de transferencias.",
        "Coordine a un equipo de 2 desarrolladores, garantizando entregas incrementales bajo metodologia agil."
    ]
    ps.append("FBody 0.15 setgray")
    for b in cat_bullets:
        ps.append(f"56 {y+4} bullet")
        ps.append(f"64 {y} moveto ({esc(b)}) show")
        y -= 12

    # Section: Habilidades Tecnicas
    y -= 10
    ps.append(f"FSec 0 setgray 50 {y} moveto ({esc('HABILIDADES TECNICAS')}) show")
    y -= 6
    ps.append(f"0.4 setlinewidth 0.7 setgray 50 {y} 545 {y} line")
    y -= 16
    
    skills = [
        ("Lenguajes:", "Python, JavaScript (ES6+), TypeScript, SQL, Java, HTML5, CSS3 moderno."),
        ("Frontend & UI/UX:", "HTMX, Diseno Web Responsivo (Mobile-First), Apple HIG / Liquid Glass, Tailwind CSS, Bootstrap."),
        ("Backend & APIs:", "Django, Django REST Framework, Node.js, arquitectura de microservicios y APIs RESTful."),
        ("Cloud & Seguridad:", "Railway, Cloudflare, GitHub Actions (CI/CD), Firebase Authentication, tokens HMAC, 2FA/OTP, SSL/TLS, Linux."),
        ("Bases de Datos & ML:", "PostgreSQL (relacional normalizada), Cloud Firestore, Scikit-Learn, XGBoost, Pandas."),
        ("Metodologias:", "Scrum (Planificacion por Sprints, control de avances en bitacoras), Kanban, Git / GitHub.")
    ]
    for cat, val in skills:
        ps.append(f"FBodyB 0 setgray 50 {y} moveto ({esc(cat)}) show")
        ps.append(f"FBody 0.2 setgray 165 {y} moveto ({esc(val)}) show")
        y -= 13

    # Section: Educacion
    y -= 10
    ps.append(f"FSec 0 setgray 50 {y} moveto ({esc('EDUCACION')}) show")
    y -= 6
    ps.append(f"0.4 setlinewidth 0.7 setgray 50 {y} 545 {y} line")
    y -= 16
    
    ps.append(f"FItem 0 setgray 50 {y} moveto ({esc('Duoc UC - Ingenieria en Informatica')}) show")
    ps.append(f"FDate 0.4 setgray 470 {y} moveto ({esc('2023 - 2026')}) show")
    y -= 11
    ps.append(f"FSmall 0.3 setgray 50 {y} moveto ({esc('Cursando ultimo ano de carrera - Egreso 2026')}) show")
    y -= 16
    
    ps.append(f"FItem 0 setgray 50 {y} moveto ({esc('Colegio Don Orione - Tecnico de Nivel Medio en Electronica')}) show")
    ps.append(f"FDate 0.4 setgray 480 {y} moveto ({esc('Graduado')}) show")
    y -= 18

    # Section: Certificaciones y Distinciones
    ps.append(f"FSec 0 setgray 50 {y} moveto ({esc('CERTIFICACIONES INTERNACIONALES Y DISTINCIONES')}) show")
    y -= 6
    ps.append(f"0.4 setlinewidth 0.7 setgray 50 {y} 545 {y} line")
    y -= 16
    
    certs = [
        "Cisco Networking Academy & Python Institute: Partner: PCAP - Programming Essentials in Python (Julio 2023).",
        "CertiProf International: DevOps Foundation Professional Certificate (DFPC) - ID: TLZZKDZKTHL-XPXRMHPSH-RLKFTJJHSS.",
        "CertiProf International: DevOps Essentials Professional Certificate (DEPC) - ID: TLZZLLDVDKK-XPWTMQXHS-RLKRJKLLTT.",
        "Distincion MakeX Robotics: 1.er Lugar Regional - Medalla de Oro en algoritmos de navegacion autonoma en tiempo real."
    ]
    ps.append("FBody 0.15 setgray")
    for c in certs:
        ps.append(f"56 {y+4} bullet")
        ps.append(f"64 {y} moveto ({esc(c)}) show")
        y -= 14

    # Page 2 Footer
    ps.append(f"FSmall 0.5 setgray 50 35 moveto ({esc('Nicolas Alexsander Munoz Mendez - Pagina 2 de 2')}) show")
    ps.append(f"FSmall 0.5 setgray 420 35 moveto ({esc('Descargado desde catstudio.cl')}) show")
    ps.append("showpage")
    
    return "\n".join(ps)

def main():
    repo_dir = "/home/alexsander/Escritorio/proyectos/deralexsander"
    assets_pdf = os.path.join(repo_dir, "assets", "cv-nicolas-munoz.pdf")
    root_pdf = os.path.join(repo_dir, "cv profecional.pdf")
    temp_ps = "/tmp/cv_nicolas.ps"
    
    print("⚡ Generando PostScript con datos actualizados...")
    ps_content = generate_postscript()
    with open(temp_ps, "w", encoding="utf-8") as f:
        f.write(ps_content)
        
    print(f"📦 Compilando PDF con ps2pdf hacia {assets_pdf}...")
    res = subprocess.run(["ps2pdf", "-sPAPERSIZE=a4", temp_ps, assets_pdf], capture_output=True, text=True)
    if res.returncode != 0:
        print("Error en ps2pdf:", res.stderr)
        return
        
    # Copiar a la raíz también para compatibilidad
    subprocess.run(["cp", assets_pdf, root_pdf])
    print(f"✅ PDF generado exitosamente en:\n  - {assets_pdf}\n  - {root_pdf}")

if __name__ == "__main__":
    main()
