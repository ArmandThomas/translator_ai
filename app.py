import streamlit as st
from streamlit_mic_recorder import speech_to_text
from transformers import pipeline
from io import BytesIO
from gtts import gTTS

# Met en cache les modèles pour éviter de les recharger à chaque fois

@st.cache_data
def get_model(type, model):
    return pipeline(type, model=model)

st.title("Home")
st.write("Welcome to the Translator !")

# Voici une liste de langues supportées par le modèle de traduction merci de supprimer si vous rencontrez des problèmes

list_nat = ["fr", "en", "es", "it", "de", "pt", "ru", "zh"]

# Un select qui permet de choisir la langue source

source_lang = st.selectbox(
    "Source Language",
    list_nat,
)

# Ici j'utilise le micro de l'utilisateur pour enregistrer sa voix et la convertir en texte grace à une librairie pour streamlit

text = speech_to_text(
    language=source_lang,
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=True,
)

# Si l'utilisateur a parlé et que le texte n'est pas vide alors on affiche le texte et on lui demande de choisir la langue cible

if text is not None and source_lang != "":

    # Affiche le texte que l'utilisateur a dit
    st.write(text)

    # Un select qui permet de choisir la langue cible

    target_lang = st.selectbox(
        "Target Language",
        [x for x in list_nat if x != source_lang],
    )

    translate = st.button("Translate")

    # si l'utilisateur clique sur le bouton "Translate" alors on traduit le texte et on le convertit en audio

    if translate:

        # Traduction
        with st.status("Translating your text..."):
            st.write("Getting the model to translate the text to the language...")

            # Récupère le modèle de traduction et le stocke dans une variable ce modèle est chargé dynamiquement et mis en cache, il dépends de la langue source et cible

            translator = get_model("translation", "Helsinki-NLP/opus-mt-%s-%s" % (source_lang, target_lang))
            st.write("Translating the text...")

            # Affiche le texte traduit
            st.write("You said : %s" % translator(text)[0]["translation_text"])

        # TTS
        with st.status("Making your voice sound like a native speaker..."):

            # Utilise la librairie gTTS pour convertir le texte en audio et le stocke dans une variable

            audio = gTTS(translator(text)[0]["translation_text"], lang=target_lang)

            # Crée un fichier audio et le stocke dans une variable
            mp3_fp = BytesIO()
            audio.write_to_fp(mp3_fp)

            # Affiche le fichier audio
            st.audio(mp3_fp, format='audio/mp3', start_time=0)






