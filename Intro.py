import os
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(page_title="Bitácora de clase", page_icon="📒", layout="wide")

TAM_IMG = (600, 400)
SITIO = "https://sites.google.com/view/aplicacionesdeia/inicio"

# Color de texto y de fondo de la etiqueta de cada área
AREAS = {
    "Voz y audio": ("#0B7A6D", "#D5F2EE"),
    "Visión": ("#2A56C6", "#DCE6FB"),
    "Texto e IA": ("#6D3FD1", "#E8DFFA"),
    "Dibujo": ("#B93A16", "#FADED4"),
    "IoT": ("#8A5A00", "#FCEBC2"),
}

# ---------- Estilos ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=DM+Sans:wght@400;500;700&display=swap');

    .stApp { background: #E9F0F4; }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1100px; padding-top: 3rem; }
    html, body, p, span, div, label { font-family: 'DM Sans', sans-serif; color: #10263A; }

    .titulo {
        font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800;
        font-size: 3.4rem; line-height: 1.02; letter-spacing: -0.02em; margin: 0 0 12px 0;
    }
    .intro { font-size: 1.1rem; color: #4A6275 !important; margin: 0 0 8px 0; max-width: 34em; }
    .intro a { color: #10263A !important; font-weight: 700; }

    /* Tarjetas */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF; border: none; border-radius: 22px;
        box-shadow: 0 8px 24px rgba(16, 38, 58, .07);
    }
    div[data-testid="stImage"] img { border-radius: 14px; }

    .chip {
        display: inline-block; font-size: .8rem; font-weight: 700;
        padding: 3px 12px; border-radius: 999px; margin-top: 6px;
    }
    .card-title {
        font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
        font-size: 1.2rem; line-height: 1.2; margin: 10px 0 6px 0; height: 2.9rem; overflow: hidden;
    }
    .card-desc { font-size: .95rem; color: #4A6275 !important; height: 5.6rem; overflow: hidden; }
    .card-emoji {
        aspect-ratio: 3 / 2; display: flex; align-items: center; justify-content: center;
        font-size: 4rem; background: #E9F0F4; border-radius: 14px;
    }

    /* Botón de abrir */
    a[data-testid="stBaseLinkButton-secondary"], div[data-testid="stLinkButton"] a {
        border-radius: 12px; border: 2px solid #10263A; font-weight: 700;
    }

    .vacio { color: #4A6275 !important; font-size: 1.1rem; padding: 40px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

ACTIVIDADES = [
    {
        "titulo": "Primer trabajo", "emoji": "🔊", "area": "Voz y audio",
        "imagen": "vapoi.jpg",
        "desc": "Aplicación que convierte texto en audio.",
        "url": "https://miprimertrabajitojiijiji.streamlit.app/",
        "boton": "Texto a voz",
    },
    {
        "titulo": "Texto a código Morse (audio)", "emoji": "📡", "area": "Voz y audio",
        "imagen": "morse1.png",
        "desc": "Aplicación que usa la conversión de voz a texto.",
        "url": "https://textoaaudio-e8atvrosvirkgucq7yfhqu.streamlit.app/",
        "boton": "Voz a texto",
    },
    {
        "titulo": "Traductor", "emoji": "🌍", "area": "Voz y audio",
        "imagen": "trad.png",
        "desc": "Traduce tu voz o un audio a otro idioma.",
        "url": "https://traductor1-cud5mwbxqpnw9mfi4bmj2t.streamlit.app/",
        "boton": "Traductor",
    },
    {
        "titulo": "OCR", "emoji": "🔎", "area": "Visión",
        "imagen": "ocr.png",
        "desc": "Reconoce texto en imágenes y lo muestra en pantalla.",
        "url": "https://8a3mzxo4ahszf7kz2u9jwk.streamlit.app/",
        "boton": "OCR",
    },
    {
        "titulo": "OCR a Morse", "emoji": "📝", "area": "Visión",
        "imagen": "ocraudio.png",
        "desc": "Reconoce texto en imágenes y lo convierte a código Morse.",
        "url": "https://ocr-audio-fw4c98qxulwsqkkzzdsnau.streamlit.app/",
        "boton": "OCR a Morse",
    },
    {
        "titulo": "Entrenando modelos", "emoji": "🧠", "area": "Visión",
        "imagen": "reco.jpg",
        "desc": "Este modelo reconoce objetos en imagenes",
        "url": "https://l37bxo8txruhjusy2ug4sz.streamlit.app/",
        "boton": "YOLO entrenado",
    },
    {
        "titulo": "WordCloud", "emoji": "☁️", "area": "Texto e IA",
        "imagen": "nube.jpg",
        "desc": "Genera una nube de palabras.",
        "url": "https://wordcloud-hbdsnmemycyswji6j2cavb.streamlit.app/",
        "boton": "WordCloud",
    },
    {
        "titulo": "Detector de sentimientos", "emoji": "😊", "area": "Texto e IA",
        "imagen": "senti.jpg",
        "desc": "Ingresa un texto y te dice si es positivo, negativo o neutro.",
        "url": "https://sentiment-6fgn5um9ucappfxvluu3c3f.streamlit.app/",
        "boton": "Sentimientos",
    },
    {
        "titulo": "TDF", "emoji": "❓", "area": "Texto e IA",
        "imagen": "pregunta.jpg",
        "desc": "En este enlace podras subir un texto y aparaceren preguntas con base a el",
        "url": "https://52uipfxaqbfkuwqbixdcji.streamlit.app/",
        "boton": "TDF",
    },
    {
        "titulo": "Detector de Samuel", "emoji": "✨", "area": "Visión",
        "imagen": "samu.jpg",
        "desc": "En esta pagina puedes tomar una foto y detectara si esta el estudiante que realizo estas actividades en ella.",
        "url": "https://detector-de-paz-cnymgqrevh7u6rwmkrzpih.streamlit.app/",
        "boton": "Detector",
    },
    {
        "titulo": "Tablero Inteligente", "emoji": "🧑‍🏫", "area": "Dibujo",
        "imagen": "Tablero.png",
        "desc": "Dibuja el boceto en el panel y presiona el botón para analizarlo.",
        "url": "https://drawrecog-ctizhf5hergbd67xemxkvs.streamlit.app/",
        "boton": "Tablero Inteligente",
    },
    {
        "titulo": "Detección de Dígitos Escritos a Mano", "emoji": "✍️", "area": "Dibujo",
        "imagen": "numeros.jpg",
        "desc": "Dibuja un dígito y la página lo detectará y reconocerá.",
        "url": "https://mnistpred-8w5uuho8jcqfnbhkdultgo.streamlit.app/",
        "boton": "Dígitos",
    },
    {
        "titulo": "Tablero para dibujo", "emoji": "🎨", "area": "Dibujo",
        "imagen": "dibujo.jpg",
        "desc": "Dibuja libremente lo que quieras.",
        "url": "https://tablero-bm2vwtpxghzkj9nciqt4jh.streamlit.app/",
        "boton": "Tablero de dibujo",
    },
    {
        "titulo": "Tablero del Terror", "emoji": "🕯️", "area": "Dibujo",
        "imagen": "terror.jpg",
        "desc": "Dibuja algo en el tablero y presiona el botón para crear una historia de terror relacionada con el dibujo.",
        "url": "https://bitacora-ykmsmns2h4xoopavt7mni2.streamlit.app/",
        "boton": "Tablero del Terror",
    },
    {
        "titulo": "MQTT Control", "emoji": "🎛️", "area": "IoT",
        "imagen": "control.jpg",
        "desc": "Envía órdenes y valores analógicos a tu dispositivo por MQTT.",
        "url": "https://iswuxstfarrgyemaeda7bm.streamlit.app/",
        "boton": "MQTT Control",
    },
    {
        "titulo": "Lector de Sensor MQTT", "emoji": "📡", "area": "IoT",
        "imagen": "recep.jpg",
        "desc": "Consulta el último mensaje publicado por tu sensor en tiempo real.",
        "url": "https://receptor-bexlqe23gjmfpulm3pdqct.streamlit.app/",
        "boton": "Lector MQTT",
    },
    {
        "titulo": "Control por voz", "emoji": "🎙️", "area": "IoT",
        "imagen": "voz.png",
        "desc": "Controla tu dispositivo por voz.",
        "url": "https://ctrlvoice-gvks7v9n4cyergxxxfhybp.streamlit.app/",
        "boton": "Control por voz",
    },
    {
        "titulo": "Análisis de plantas", "emoji": "🌿", "area": "Visión",
        "imagen": "plantas.png",
        "desc": "Toma la foto de una planta, reconocerá el tipo y te dirá sus cuidados.",
        "url": "https://visionapp-hwnwwkumtaxpztwxcusezw.streamlit.app/",
        "boton": "Análisis de plantas",
    },
    {
        "titulo": "Generación Aumentada por Recuperación (RAG)", "emoji": "📚", "area": "Texto e IA",
        "imagen": "pdf.jpg",
        "desc": "Este agente te ayudará a realizar análisis sobre el PDF cargado.",
        "url": "https://chatpdf-r6sxcbg5bfciwgrtyehqcz.streamlit.app/",
        "boton": "RAG",
    },
]


def cargar_imagen(ruta):
    img = Image.open(ruta).convert("RGB")
    return ImageOps.fit(img, TAM_IMG, Image.LANCZOS)


def mostrar_tarjeta(act):
    color, fondo = AREAS[act["area"]]
    with st.container(border=True):
        if act["imagen"] and os.path.exists(act["imagen"]):
            st.image(cargar_imagen(act["imagen"]), use_container_width=True)
        else:
            st.markdown(f"<div class='card-emoji'>{act['emoji']}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<span class='chip' style='color:{color};background:{fondo}'>{act['area']}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='card-title'>{act['emoji']} {act['titulo']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='card-desc'>{act['desc']}</div>", unsafe_allow_html=True)
        if act["url"]:
            st.link_button(f"Abrir: {act['boton']}", act["url"], use_container_width=True)
        else:
            st.button("Próximamente", disabled=True, use_container_width=True, key=f"d_{act['titulo']}")


def mostrar_fila(lista, por_fila=3):
    for i in range(0, len(lista), por_fila):
        cols = st.columns(por_fila)
        for col, act in zip(cols, lista[i : i + por_fila]):
            with col:
                mostrar_tarjeta(act)


# ---------- Encabezado ----------
st.markdown('<div class="titulo">Bitácora de clase</div>', unsafe_allow_html=True)
st.markdown(
    f"""<div class="intro">{len(ACTIVIDADES)} aplicaciones de inteligencia artificial hechas durante el curso.
    Más ejercicios en el <a href="{SITIO}" target="_blank">sitio del curso</a>.</div>""",
    unsafe_allow_html=True,
)

# ---------- Filtro por área ----------
opciones = ["Todas"] + list(AREAS.keys())
area = st.radio("Área", opciones, horizontal=True, label_visibility="collapsed")

lista = ACTIVIDADES if area == "Todas" else [a for a in ACTIVIDADES if a["area"] == area]

st.write("")
if lista:
    mostrar_fila(lista)
else:
    st.markdown("<div class='vacio'>No hay actividades en esta área todavía.</div>", unsafe_allow_html=True)
