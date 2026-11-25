from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

PAGE_W, PAGE_H = 960, 540
LEFT_W = 302
RIGHT_X = 335
RIGHT_W = PAGE_W - RIGHT_X - 24

PURPLE = HexColor("#3b216f")
ACCENT = HexColor("#7042b4")
LIGHT_PURPLE = HexColor("#f8f5fc")
CARD_PURPLE = HexColor("#eee7fa")
TEXT = HexColor("#273043")
MUTED = HexColor("#667085")
WHITE = HexColor("#ffffff")


def wrap_text(text, font, size, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c, text, x, y, width, font="Helvetica", size=8, leading=10.2,
                 color=TEXT, max_lines=None):
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap_text(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
        if len(wrap_text(text, font, size, width)) > max_lines:
            last = lines[-1]
            while stringWidth(last + "...", font, size) > width and last:
                last = last[:-1]
            lines[-1] = last.rstrip() + "..."
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_left_section(c, y, title):
    c.setFillColor(HexColor("#d8cff6"))
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(32, y, title)
    return y - 18


def draw_contact_icon(c, kind, x, y):
    c.saveState()
    c.setStrokeColor(PURPLE)
    c.setFillColor(PURPLE)
    c.setLineWidth(1)
    if kind == "location":
        c.circle(x, y + 1, 3.4, stroke=1, fill=0)
        c.circle(x, y + 1, 1, stroke=0, fill=1)
        c.line(x - 2.4, y - 1, x, y - 5)
        c.line(x + 2.4, y - 1, x, y - 5)
    elif kind == "email":
        c.roundRect(x - 4.5, y - 3.2, 9, 6.4, 0.8, stroke=1, fill=0)
        c.line(x - 4, y + 2.6, x, y - 0.3)
        c.line(x + 4, y + 2.6, x, y - 0.3)
    elif kind == "phone":
        p = c.beginPath()
        p.moveTo(x - 3.3, y + 4)
        p.curveTo(x - 4.5, y + 2.8, x - 1.8, y - 1.8, x + 1.5, y - 4)
        p.curveTo(x + 2.2, y - 4.6, x + 4.2, y - 2.7, x + 3.4, y - 1.8)
        p.lineTo(x + 1.6, y - 0.6)
        p.curveTo(x + 0.4, y - 1.2, x - 0.7, y - 0.1, x - 0.2, y + 1)
        p.lineTo(x + 1, y + 2.6)
        p.curveTo(x + 0.1, y + 3.5, x - 2, y + 5.2, x - 3.3, y + 4)
        c.drawPath(p, stroke=1, fill=0)
    elif kind == "linkedin":
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(x, y - 2.3, "in")
    elif kind == "github":
        p = c.beginPath()
        p.moveTo(x - 3.6, y + 1.4)
        p.lineTo(x - 3.8, y + 4)
        p.lineTo(x - 1.3, y + 2.8)
        p.curveTo(x - 0.2, y + 3.2, x + 0.4, y + 3.2, x + 1.3, y + 2.8)
        p.lineTo(x + 3.8, y + 4)
        p.lineTo(x + 3.6, y + 1.2)
        p.curveTo(x + 4.7, y - 2.5, x + 2.2, y - 4, x, y - 4)
        p.curveTo(x - 2.4, y - 4, x - 4.7, y - 2.4, x - 3.6, y + 1.4)
        c.drawPath(p, stroke=1, fill=0)
    elif kind == "web":
        c.circle(x, y, 4.2, stroke=1, fill=0)
        c.ellipse(x - 2, y - 4.2, x + 2, y + 4.2, stroke=1, fill=0)
        c.line(x - 4, y, x + 4, y)
        c.arc(x - 4, y - 2.2, x + 4, y + 2.2, 0, 180)
        c.arc(x - 4, y - 2.2, x + 4, y + 2.2, 180, 180)
    c.restoreState()


def main():
    output = "/Users/alexsander/Desktop/proyectos/deralexsander/scripts/curriculums/CV V2/Copia 2 - CV adaptado actualizado.pdf"
    c = canvas.Canvas(output, pagesize=(PAGE_W, PAGE_H))
    c.setTitle("CV adaptado - Nicolas Alexsander Munoz Mendez")

    c.setFillColor(PURPLE)
    c.rect(0, 0, LEFT_W, PAGE_H, fill=1, stroke=0)

    icon_x, icon_y = 151, 458
    c.setFillColor(WHITE)
    c.circle(icon_x, icon_y + 29, 18, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.circle(icon_x, icon_y + 29, 13, fill=1, stroke=0)
    c.setStrokeColor(WHITE)
    c.setLineWidth(4)
    c.setLineCap(1)
    c.line(icon_x - 17, icon_y - 4, icon_x - 22, icon_y + 22)
    c.line(icon_x - 22, icon_y + 22, icon_x - 11, icon_y + 31)
    c.line(icon_x + 17, icon_y - 4, icon_x + 22, icon_y + 22)
    c.line(icon_x + 22, icon_y + 22, icon_x + 11, icon_y + 31)
    c.setFillColor(WHITE)
    c.roundRect(icon_x - 29, icon_y - 18, 58, 25, 4, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.rect(icon_x - 25, icon_y - 14, 50, 16, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(icon_x, icon_y - 10, "</>")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(icon_x, 388, "Nicolás Alexsander")
    c.drawCentredString(icon_x, 367, "Muñoz Méndez")
    c.setFont("Helvetica", 10.5)
    c.setFillColor(HexColor("#ddd7f2"))
    c.drawCentredString(icon_x, 344, "Desarrollador Full-Stack")
    c.drawCentredString(icon_x, 329, "Egresando de Ing. en Informática")

    y = 290
    y = draw_left_section(c, y, "CONTACTO")
    contact = [
        ("location", "Valparaíso, Chile"),
        ("email", "nico.alexander.m.m@gmail.com"),
        ("phone", "+56 9 6878 7862"),
        ("linkedin", "linkedin.com/in/nicolas-munoz-mendez"),
        ("github", "github.com/deralexsander"),
        ("web", "deralexsander.github.io/deralexsander"),
    ]
    for kind, text in contact:
        c.setFillColor(HexColor("#b8ade7"))
        c.circle(37, y + 2, 8, fill=1, stroke=0)
        draw_contact_icon(c, kind, 37, y + 2)
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 7.8)
        c.drawString(53, y - 1, text)
        y -= 19

    y -= 4
    y = draw_left_section(c, y, "HABILIDADES TÉCNICAS")
    skill_groups = [
        ("Backend & APIs:", "Python, Django, Django REST Framework, Node.js"),
        ("Web & Frontend:", "JavaScript, TypeScript, Angular, HTML5, CSS3, Bootstrap"),
        ("Mobile:", "Ionic, Capacitor, Android Studio, Java, Kotlin"),
        ("Machine Learning & Datos:", "Scikit-Learn, Pandas, PostgreSQL, Cloud Firestore, SQLite"),
        ("Cloud, DevOps & Tools:", "Firebase, Railway, Cloudflare, GCP, Git, GitHub, VS Code"),
    ]
    for label, value in skill_groups:
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 7.6)
        c.drawString(32, y, label)
        c.setFont("Helvetica", 7.3)
        y = draw_wrapped(c, value, 32, y - 11, LEFT_W - 48,
                         font="Helvetica", size=7.2, leading=7.8,
                         color=WHITE, max_lines=2)
        y -= 4

    c.setFillColor(HexColor("#edf0f5"))
    c.setFillColor(LIGHT_PURPLE)
    c.rect(LEFT_W, 0, PAGE_W - LEFT_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(RIGHT_X, 493, "PERFIL")
    profile = (
        "Desarrollador Full-Stack con base técnica en electrónica, enfocado en arquitectura de software, "
        "APIs RESTful e integración de Machine Learning. Experiencia en despliegue de SaaS en producción, "
        "PostgreSQL, HTMX, TypeScript y Angular. Metodología Scrum, certificaciones internacionales DevOps "
        "y Python, y primer lugar regional en robótica."
    )
    draw_wrapped(c, profile, RIGHT_X, 474, RIGHT_W,
                 font="Helvetica", size=8.5, leading=10.4,
                 color=TEXT, max_lines=4)

    card_y = 367
    card_h = 56
    card_gap = 14
    card_w = (RIGHT_W - 3 * card_gap) / 4
    metrics = [
        ("7", "proyectos destacados"),
        ("+60K", "registros en PostgreSQL"),
        ("−40%", "latencia tras migrar a Firestore"),
        ("1.er", "lugar regional en robótica"),
    ]
    for i, (value, label) in enumerate(metrics):
        x = RIGHT_X + i * (card_w + card_gap)
        c.setFillColor(ACCENT)
        c.roundRect(x, card_y, card_w, card_h, 6, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(x + 9, card_y + 34, value)
        c.setFont("Helvetica", 7)
        draw_wrapped(c, label, x + 9, card_y + 16, card_w - 18,
                     font="Helvetica", size=7, leading=8,
                     color=WHITE, max_lines=2)

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(RIGHT_X, 349, "PROYECTOS DESTACADOS")

    projects = [
        ("G&M Constructora – Plataforma corporativa", "Nov 2026",
         "Consultoría web freelance: levantamiento de requerimientos, UI/UX mobile-first y despliegue en producción para una PYME."),
        ("D & G Parfums – Catálogo para punto de venta", "Nov 2026",
         "Diseño frontend freelance: catálogo responsive, búsqueda predictiva, notas aromáticas y mapa olfativo."),
        ("SmartBids – SaaS de licitaciones públicas", "Ago – Nov 2026",
         "Interfaz con HTMX, autenticación 2FA/OTP y firmas HMAC; despliegue en Railway con DNS y SSL/TLS."),
        ("Notes & Sillage – E-commerce serverless", "Oct 2026 – Actual",
         "Fundador y Full-Stack: Cloud Firestore, Cloudflare, notificaciones push y dashboards de ventas."),
        ("FerreMas – E-commerce y logística", "Mar – Jul 2025",
         "Google OAuth 2.0, Firebase Auth con RBAC y Google Maps API para despachos logísticos."),
        ("Servicio CATTECH – Pasarela financiera", "Ago – Nov 2024",
         "SDK de Mercado Pago, Cloud Firestore y aplicación móvil con Angular/Ionic."),
        ("NekoBeansWeb – Sistema administrativo", "Jun – Jul 2024",
         "Cotizaciones y ventas con Django, PostgreSQL y control de roles."),
    ]

    y = 327
    for i, (title, date, desc) in enumerate(projects, 1):
        c.setFillColor(HexColor("#c8b5f0"))
        c.circle(RIGHT_X + 11, y - 1, 11, fill=1, stroke=0)
        c.setFillColor(PURPLE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(RIGHT_X + 11, y - 4, str(i))

        c.setFillColor(TEXT)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(RIGHT_X + 32, y + 1, title)

        date_w = stringWidth(date, "Helvetica-Bold", 7.5)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(RIGHT_X + RIGHT_W - date_w, y + 1, date)

        draw_wrapped(c, desc, RIGHT_X + 32, y - 11, RIGHT_W - 42,
                     font="Helvetica", size=7.2, leading=8,
                     color=MUTED, max_lines=1)
        y -= 28

    card_bottom = 24
    card_top = 112
    half_gap = 18
    half_w = (RIGHT_W - half_gap) / 2
    c.setFillColor(CARD_PURPLE)
    c.roundRect(RIGHT_X, card_bottom, half_w, card_top - card_bottom,
                8, fill=1, stroke=0)
    c.roundRect(RIGHT_X + half_w + half_gap, card_bottom, half_w,
                card_top - card_bottom, 8, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(RIGHT_X + 14, 97, "EDUCACIÓN")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(RIGHT_X + 14, 77, "Ingeniería en Informática")
    c.setFont("Helvetica", 7.5)
    c.drawString(RIGHT_X + 14, 64,
                 "Duoc UC, Viña del Mar · 2023 – 2026 (egresando)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(RIGHT_X + 14, 47, "Técnico de Nivel Medio en Electrónica")
    c.setFont("Helvetica", 7.5)
    c.drawString(RIGHT_X + 14, 34,
                 "Colegio Don Orione, Quintero · Titulado 2022")

    cert_x = RIGHT_X + half_w + half_gap + 14
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(cert_x, 97, "CERTIFICACIONES Y LOGROS")
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 7.2)
    c.drawString(cert_x, 78, "PCAP – Programming Essentials in Python (Cisco, 2023)")
    c.drawString(cert_x, 64, "DevOps Foundation DFPC y Essentials DEPC® (CertiProf)")
    c.drawString(cert_x, 50, "1.er Lugar Regional – MakeX Robotics, Medalla de Oro")
    c.drawString(cert_x, 36, "Metodologías: Scrum, Kanban, Code Reviews")

    c.showPage()
    c.save()
    print(output)


if __name__ == "__main__":
    main()
