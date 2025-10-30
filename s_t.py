import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator


st.markdown("""
    <style>
        body {
            background-color: #87CEFA;  /* Fondo celeste */
            color: #ffffff;  /* Texto blanco */
        }
        .stTitle {
            color: #f5a623;  /* Título en color dorado (como una estrella) */
            font-size: 2em;
            font-family: 'Arial', sans-serif;
        }
        .stHeader {
            color: #ff6347;  /* Cabecera en color tomate */
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #4caf50;  /* Fondo verde para los campos de texto */
            color: white;  /* Texto en blanco */
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #ffb6c1;  /* Botones de color suave (rosa) */
            color: #2a3d66;  /* Texto en color oscuro */
            border-radius: 10px;
            font-size: 1em;
        }
        .stRadio>div>label {
            color: #f9c74f;  /* Color dorado para las opciones del radio */
        }
        .stSubheader {
            color: #f7a7ff;  /* Subtítulo con un tono morado */
        }
    </style>
""", unsafe_allow_html=True)


st.title(" Traductor Estelar ✨")
st.subheader("🎧 Escucho lo que deseas traducir desde las estrellas")


image = Image.open('estrella.png')  
st.image(image, width=300)

with st.sidebar:
    st.subheader("🚀 Traductor Estelar")
    st.write("🌙 Presiona el botón, cuando escuches la señal, habla lo que quieres traducir, luego selecciona el idioma de entrada y salida.")


st.write("Toca el botón y habla lo que quieres traducir. Las estrellas te guiarán")


stt_button = Button(label="🎤 Escuchar", width=300, height=50)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))


result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
    

    try:
        os.mkdir("temp")
    except:
        pass
    
    st.title("🌟 Texto a Audio Estelar 🎶")
    translator = Translator()
    

    text = str(result.get("GET_TEXT"))
    

    in_lang = st.selectbox(
        "🌍 Selecciona el lenguaje de entrada",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    
    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"
    
    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    
    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"
    

    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )
    
    # Asignación de TLD para el acento
    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"
    

    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    display_output_text = st.checkbox("Mostrar el texto")
    
    if st.button("🌟 Convertir a Audio"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"🎶 **Tu audio:**")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        if display_output_text:
            st.markdown(f"🌟 **Texto de salida:**")
            st.write(f" {output_text}")
    
    # Función para eliminar ar

        
    


