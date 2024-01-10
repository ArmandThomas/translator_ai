import streamlit as st
from streamlit_mic_recorder import speech_to_text
from transformers import pipeline
from io import BytesIO
from gtts import gTTS

@st.cache_data
def get_model(type, model):
    return pipeline(type, model=model)


st.title("Home")
st.write("Welcome to the home page!")

list_nat = ["fr", "en", "es", "it", "de", "pt", "ru", "zh"]

source_lang = st.selectbox(
    "Source Language",
    list_nat,
)

text = speech_to_text(
    language=source_lang,
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=True,
)

if text is not None and source_lang != "":
    st.write(text)
    target_lang = st.selectbox(
        "Target Language",
        [x for x in list_nat if x != source_lang],
    )
    translate = st.button("Translate")

    if translate:
        with st.status("Translating your text..."):
            st.write("Getting the model to translate the text to the language...")
            translator = get_model("translation", "Helsinki-NLP/opus-mt-%s-%s" % (source_lang, target_lang))
            st.write("Translating the text...")
            st.write("You said : %s" % translator(text)[0]["translation_text"])

        # TTS
        with st.status("Making your voice sound like a native speaker..."):
            audio = gTTS(translator(text)[0]["translation_text"], lang=target_lang)
            mp3_fp = BytesIO()
            audio.write_to_fp(mp3_fp)

            st.audio(mp3_fp, format='audio/mp3', start_time=0)






