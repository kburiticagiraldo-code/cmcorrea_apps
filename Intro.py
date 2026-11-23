import base64
import html
import io
import os

import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(page_title="Bitácora de clase", page_icon="📒", layout="wide")

# =====================================================================
#  TUS ENLACES: reemplaza solo lo que está entre comillas
#  (si dejas una vacía "", la tarjeta muestra "Próximamente")
# =====================================================================
SITIO = "https://sites.google.com/view/aplicacionesdeia/inicio"

ENLACES = {
    "primer_trabajo": "https://clase-multimodal-nmc8dpstqyjvmxchmpyanz.streamlit.app/",
    "morse": "https://zumprnqskp89dqj6szidhu.streamlit.app/",
    "traductor": "https://jkjlkjkkjkj.streamlit.app/",
    "ocr": "https://8f2elmawezvrr67ejhmnou.streamlit.app/",
    "ocr_morse": "https://ocr-audio-gwbrpqz9tgwhk2j2n5ebre.streamlit.app/",
    "yolo": "https://hjhwe2zbbvpyevunzku8gn.streamlit.app/",
    "wordcloud": "https://wordcloud-e3w7v3751l5.streamlit.app/",
    "sentimientos": "https://sentiment-smvfguulr2bgrh5en2x3wr.streamlit.app/",
    "tdf": "https://wh63whnb5ed4tvvnkbkr7z.streamlit.app/",
    "samuel": "https://detector-de-paz-dzw2akjvwst5v2deshp2jj.streamlit.app/",
    "tablero_inteligente": "https://drawrecog-qi7xwyweqxihpzpmvt2vcf.streamlit.app/",
    "digitos": "https://mnistpred-asmegbwmjuguh5fzvqvy2z.streamlit.app/",
    "tablero_dibujo": "https://tablero-mcthchpcxxmck5f9lmstmd.streamlit.app/",
    "tablero_terror": "https://historiasinfant-m5slvr7emrgcz7nm9aqbpj.streamlit.app/",
    "mqtt_control": "https://sendcmqtt-sayuhu2g3mwdmschezjwke.streamlit.app/",
    "mqtt_lector": "https://recepmqtt-9ptyc3h2yp8jzeosrhjxpp.streamlit.app/",
    "control_voz": "https://ctrlvoice-jldxcxlr6drl4w3pvmgkdt.streamlit.app/",
    "plantas": "https://visionapp-hakceuepzuhn8sjudhn9lk.streamlit.app/",
    "rag": "https://chatpdf-gecudpt2viptlspgnc7ssi.streamlit.app/",
}
# =====================================================================

TAM_IMG = (600, 400)

# color principal, color suave, color de degradado, icono, descripción
AREAS = {
    "Voz y audio": ("#0B8F80", "#D5F2EE", "#7FDAD0", "🎧", "Convierte voz, texto y audio entre formatos e idiomas."),
    "Visión": ("#2F5FD6", "#DCE6FB", "#8EB0F5", "👁️", "Modelos que ven: texto, objetos, rostros y plantas."),
    "Texto e IA": ("#7440DB", "#E8DFFA", "#B99AF3", "💬", "Análisis y generación de lenguaje con inteligencia artificial."),
    "Dibujo": ("#D2461C", "#FADED4", "#F5A98E", "🖌️", "Tableros donde la IA interpreta lo que dibujas."),
    "IoT": ("#B87400", "#FCEBC2", "#F5C65C", "📟", "Controla y monitorea dispositivos conectados por MQTT."),
}

ACTIVIDADES = [
    ("primer_trabajo", "Primer trabajo", "🗣️", "Voz y audio", "vapoi.jpg", "Aplicación que convierte texto en audio.", "Texto a voz"),
    ("morse", "Texto a código Morse (audio)", "📻", "Voz y audio", "morse1.png", "Convierte la voz en texto y lo transforma en código Morse.", "Morse"),
    ("traductor", "Traductor", "🌐", "Voz y audio", "trad.png", "Traduce tu voz o un audio a otro idioma.", "Traductor"),
    ("ocr", "OCR", "🔍", "Visión", "ocr.png", "Reconoce texto en imágenes y lo muestra en pantalla.", "OCR"),
    ("ocr_morse", "OCR a Morse", "📠", "Visión", "ocraudio.png", "Reconoce texto en imágenes y lo convierte a código Morse.", "OCR a Morse"),
    ("yolo", "Entrenando modelos", "🎯", "Visión", "reco.jpg", "Este modelo reconoce objetos en imágenes.", "YOLO entrenado"),
    ("wordcloud", "WordCloud", "☁️", "Texto e IA", "nube.jpg", "Genera una nube de palabras.", "WordCloud"),
    ("sentimientos", "Detector de sentimientos", "🎭", "Texto e IA", "senti.jpg", "Ingresa un texto y te dice si es positivo, negativo o neutro.", "Sentimientos"),
    ("tdf", "TDF", "🧩", "Texto e IA", "pregunta.jpg", "Sube un texto y aparecerán preguntas con base en él.", "TDF"),
    ("samuel", "Detector de Samuel", "🕵️", "Visión", "samu.jpg", "Toma una foto y detecta si está el estudiante que realizó estas actividades.", "Detector"),
    ("tablero_inteligente", "Tablero Inteligente", "🧠", "Dibujo", "Tablero.png", "Dibuja el boceto en el panel y presiona el botón para analizarlo.", "Tablero Inteligente"),
    ("digitos", "Detección de Dígitos Escritos a Mano", "🔢", "Dibujo", "numeros.jpg", "Dibuja un dígito y la página lo detectará y reconocerá.", "Dígitos"),
    ("tablero_dibujo", "Tablero para dibujo", "🎨", "Dibujo", "dibujo.jpg", "Dibuja libremente lo que quieras.", "Tablero de dibujo"),
    ("tablero_terror", "Tablero del Terror", "👻", "Dibujo", "terror.jpg", "Dibuja algo en el tablero y crea una historia de terror relacionada con el dibujo.", "Tablero del Terror"),
    ("mqtt_control", "MQTT Control", "🕹️", "IoT", "control.jpg", "Envía órdenes y valores analógicos a tu dispositivo por MQTT.", "MQTT Control"),
    ("mqtt_lector", "Lector de Sensor MQTT", "📶", "IoT", "recep.jpg", "Consulta el último mensaje publicado por tu sensor en tiempo real.", "Lector MQTT"),
    ("control_voz", "Control por voz", "🎙️", "IoT", "voz.png", "Controla tu dispositivo por voz.", "Control por voz"),
    ("plantas", "Análisis de plantas", "🪴", "Visión", "plantas.png", "Toma la foto de una planta, reconocerá el tipo y te dirá sus cuidados.", "Análisis de plantas"),
    ("rag", "Generación Aumentada por Recuperación (RAG)", "🗂️", "Texto e IA", "pdf.jpg", "Este agente te ayudará a realizar análisis sobre el PDF cargado.", "RAG"),
]

# ---------- Estilos ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=DM+Sans:wght@400;500;700&display=swap');

    .stApp { background: #E9F0F4; }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1150px; padding-top: 2rem; }
    html, body, p, span, div, label, a { font-family: 'DM Sans', sans-serif; }

    /* Hero */
    .hero {
        position: relative; overflow: hidden; border-radius: 32px;
        padding: 56px 48px 48px 48px; margin-bottom: 28px;
        background: linear-gradient(135deg, #10263A 0%, #17405C 55%, #1D6A78 100%);
    }
    .hero::before, .hero::after { content: ""; position: absolute; border-radius: 50%; }
    .hero::before { width: 360px; height: 360px; right: -90px; top: -120px;
                    background: radial-gradient(circle, rgba(127,218,208,.45), transparent 70%); }
    .hero::after  { width: 300px; height: 300px; right: 160px; bottom: -170px;
                    background: radial-gradient(circle, rgba(245,198,92,.40), transparent 70%); }
    .hero h1 {
        position: relative; z-index: 1; margin: 0 0 14px 0; padding: 0;
        font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800;
        font-size: clamp(2.4rem, 6vw, 4.2rem); line-height: 1; letter-spacing: -0.025em;
        color: #FFFFFF;
    }
    .hero p { position: relative; z-index: 1; margin: 0 0 26px 0; max-width: 32em;
              font-size: 1.15rem; color: #C5DCE8; }
    .hero .fila { position: relative; z-index: 1; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
    .dato {
        background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.2);
        border-radius: 16px; padding: 10px 18px; color: #FFFFFF;
    }
    .dato b { font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.6rem; margin-right: 6px; }
    .btn-sitio {
        background: #F5C65C; color: #10263A !important; font-weight: 700; text-decoration: none;
        padding: 13px 22px; border-radius: 14px; transition: transform .15s;
    }
    .btn-sitio:hover { transform: translateY(-2px); }

    /* Filtro como botones */
    div[role="radiogroup"] { gap: 10px; flex-wrap: wrap; }
    div[role="radiogroup"] > label {
        background: #FFFFFF; border-radius: 999px; padding: 9px 20px;
        box-shadow: 0 2px 8px rgba(16,38,58,.08); cursor: pointer; margin: 0;
    }
    div[role="radiogroup"] > label > div:first-child { display: none; }
    div[role="radiogroup"] > label p { color: #10263A; font-weight: 700; font-size: .98rem; }
    div[role="radiogroup"] > label:has(input:checked) { background: #10263A; }
    div[role="radiogroup"] > label:has(input:checked) p { color: #FFFFFF; }

    /* Encabezado de categoría */
    .seccion { display: flex; align-items: center; gap: 16px; margin: 38px 0 6px 0; }
    .seccion-icono {
        width: 58px; height: 58px; flex: none; border-radius: 18px; font-size: 1.9rem;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 6px 16px rgba(16,38,58,.12);
    }
    .seccion h2 {
        font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 1.7rem;
        line-height: 1.1; margin: 0; padding: 0; color: #10263A;
    }
    .seccion span.sub { display: block; margin-top: 4px; font-size: .98rem; color: #4A6275; }
    .seccion .cuenta {
        margin-left: auto; flex: none; font-weight: 700; font-size: .85rem;
        padding: 6px 14px; border-radius: 999px; background: #FFFFFF;
    }

    /* Cuadrícula de tarjetas */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 22px; margin-top: 18px; }
    .card {
        display: flex; flex-direction: column; background: #FFFFFF; border-radius: 26px;
        overflow: hidden; box-shadow: 0 8px 26px rgba(16,38,58,.08);
        transition: transform .2s, box-shadow .2s;
    }
    .card:hover { transform: translateY(-6px); box-shadow: 0 18px 38px rgba(16,38,58,.16); }
    .portada { position: relative; aspect-ratio: 3 / 2; }
    .portada img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .portada.emoji { display: flex; align-items: center; justify-content: center; font-size: 4.5rem; }
    .chip {
        position: absolute; left: 14px; top: 14px; font-size: .8rem; font-weight: 700;
        padding: 5px 13px; border-radius: 999px; background: #FFFFFF;
        box-shadow: 0 2px 8px rgba(0,0,0,.15);
    }
    .insignia {
        position: absolute; right: 14px; bottom: -22px; width: 54px; height: 54px;
        border-radius: 16px; background: #FFFFFF; font-size: 1.7rem;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 6px 16px rgba(16,38,58,.18);
    }
    .cuerpo { display: flex; flex-direction: column; flex: 1; padding: 18px 20px 20px 20px; }
    .cuerpo h3 {
        font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.28rem;
        line-height: 1.18; margin: 0 0 8px 0; padding: 0; color: #10263A; min-height: 3em;
        padding-right: 52px;
    }
    .cuerpo p { font-size: .96rem; line-height: 1.5; color: #4A6275; margin: 0 0 18px 0; flex: 1; }
    .abrir {
        display: block; text-align: center; text-decoration: none; font-weight: 700;
        padding: 12px 16px; border-radius: 14px; color: #FFFFFF !important;
    }
    .abrir:hover { filter: brightness(1.08); }
    .abrir.off { background: #C5D3DD !important; color: #4A6275 !important; pointer-events: none; }

    .vacio { color: #4A6275; font-size: 1.1rem; padding: 40px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def imagen_base64(ruta):
    """Devuelve la imagen recortada a 3:2 como texto base64 (o None si no existe)."""
    if not ruta or not os.path.exists(ruta):
        return None
    img = ImageOps.fit(Image.open(ruta).convert("RGB"), TAM_IMG, Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=82)
    return base64.b64encode(buf.getvalue()).decode()


def tarjeta(clave, titulo, emoji, area, imagen, desc, boton):
    color, suave, degradado, _icono_area, _desc_area = AREAS[area]
    b64 = imagen_base64(imagen)
    if b64:
        portada = f'<div class="portada"><img src="data:image/jpeg;base64,{b64}" alt="">'
    else:
        portada = (
            f'<div class="portada emoji" style="background:linear-gradient(135deg,{suave},{degradado})">{emoji}'
        )
    portada += (
        f'<span class="chip" style="color:{color}">{html.escape(area)}</span>'
        f'<span class="insignia">{emoji}</span></div>'
    )

    url = ENLACES.get(clave, "").strip()
    if url:
        accion = (
            f'<a class="abrir" style="background:{color}" href="{html.escape(url)}" '
            f'target="_blank" rel="noopener">Abrir {html.escape(boton)} ↗</a>'
        )
    else:
        accion = '<span class="abrir off">Próximamente</span>'

    return (
        f'<div class="card">{portada}<div class="cuerpo">'
        f"<h3>{html.escape(titulo)}</h3><p>{html.escape(desc)}</p>{accion}</div></div>"
    )


def seccion(nombre, n):
    color, suave, _deg, icono, desc = AREAS[nombre]
    return (
        f'<div class="seccion">'
        f'<div class="seccion-icono" style="background:{suave}">{icono}</div>'
        f'<div><h2>{html.escape(nombre)}</h2><span class="sub">{html.escape(desc)}</span></div>'
        f'<span class="cuenta" style="color:{color}">{n} apps</span>'
        f"</div>"
    )


def grid(items):
    return '<div class="grid">' + "".join(tarjeta(*a) for a in items) + "</div>"


# ---------- Hero ----------
st.markdown(
    f"""<div class="hero">
<h1>Bitácora de clase</h1>
<p>Todo lo que construimos en el curso de Aplicaciones de Inteligencia Artificial, en un solo lugar.</p>
<div class="fila">
<div class="dato"><b>{len(ACTIVIDADES)}</b>aplicaciones</div>
<div class="dato"><b>{len(AREAS)}</b>categorías</div>
<a class="btn-sitio" href="{html.escape(SITIO)}" target="_blank" rel="noopener">Ver el sitio del curso ↗</a>
</div>
</div>""",
    unsafe_allow_html=True,
)

# ---------- Filtro ----------
conteo = {a: sum(1 for x in ACTIVIDADES if x[3] == a) for a in AREAS}
etiquetas = {f"✨ Todas ({len(ACTIVIDADES)})": None}
etiquetas.update({f"{AREAS[a][3]} {a} ({n})": a for a, n in conteo.items()})

elegida = st.radio("Categoría", list(etiquetas.keys()), horizontal=True, label_visibility="collapsed")
area = etiquetas[elegida]

# ---------- Contenido ----------
if area is None:
    # Todas: agrupadas por categoría, cada una con su encabezado
    bloques = []
    for nombre in AREAS:
        items = [a for a in ACTIVIDADES if a[3] == nombre]
        if items:
            bloques.append(seccion(nombre, len(items)) + grid(items))
    st.markdown("".join(bloques), unsafe_allow_html=True)
else:
    items = [a for a in ACTIVIDADES if a[3] == area]
    if items:
        st.markdown(seccion(area, len(items)) + grid(items), unsafe_allow_html=True)
    else:
        st.markdown("<div class='vacio'>No hay actividades en esta categoría todavía.</div>", unsafe_allow_html=True)
