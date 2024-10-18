import textwrap
import streamlit as st
import openai
import langid
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import random
import requests


def detect_language(text):
    lang, _ = langid.classify(text)
    return lang


def translate_text(text, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Translate this to {target_language}: '{text}'"}]
    )
    return response.choices[0].message['content']


def generate_response(text, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{text}. Respond in {target_language}"}]
    )
    return response.choices[0].message['content']


def explain_writing(text, language):
    prompt = f"How do I write '{text}' in {language}?"
    return generate_response(prompt, language)


def generate_pronunciation(text, language):
    translated_text = translate_text(text, language)
    tts = gTTS(text=translated_text, lang=language)
    filename = f"pronunciation_{random.randint(1000, 9999)}.mp3"
    tts.save(filename)
    return filename

def generate_meme_caption(keywords):
    prompt = f"Generate a funny, creative meme caption based on these keywords: {', '.join(keywords)}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']


def generate_meme_image(keywords):
    prompt = f"A meme image based on these keywords: {', '.join(keywords)}"
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )

    image_url = response['data'][0]['url']
    img = Image.open(requests.get(image_url, stream=True).raw)

    caption = generate_meme_caption(keywords)

    draw = ImageDraw.Draw(img)
    image_width, image_height = img.size

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    max_width = image_width - 40
    wrapped_text = textwrap.fill(caption, width=30)
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (image_width - text_width) // 2
    y = image_height - text_height - 20

    shadow_color = "black"
    shadow_offset = 3
    draw.text((x - shadow_offset, y - shadow_offset), wrapped_text, font=font, fill=shadow_color)
    draw.text((x + shadow_offset, y - shadow_offset), wrapped_text, font=font, fill=shadow_color)
    draw.text((x - shadow_offset, y + shadow_offset), wrapped_text, font=font, fill=shadow_color)
    draw.text((x + shadow_offset, y + shadow_offset), wrapped_text, font=font, fill=shadow_color)

    text_color = "white"
    draw.text((x, y), wrapped_text, font=font, fill=text_color)

    filename = f"meme_{random.randint(1000, 9999)}.jpg"
    img.save(filename)
    return filename


def translate_document(file, target_language):
    lines = []
    for line in file:
        translated_line = translate_text(line.strip(), target_language)
        lines.append(translated_line)
    return lines


st.title("ProfessorX Chatbot")

languages = {"English": "en", "Spanish": "es", "French": "fr", "German": "de", "Chinese": "zh", "Romanian": "ro"}


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Chat with ProfessorX", "How to Write", "Pronunciation", "Meme Generator", "Let ProfessorX help you"])

with tab1:
    st.subheader("Talk to ProfessorX")
    user_input = st.text_input("Enter your message:", "")
    if st.button("Send"):
        if user_input:
            detected_language = detect_language(user_input)
            st.write(f"Detected Language: {detected_language}")
            response = generate_response(user_input, detected_language)
            st.write(f"ProfessorX: {response}")

with tab2:
    st.subheader("How to Write in a Language")
    text_to_write = st.text_input("Enter the text you want to write:")
    language_to_write = st.text_input("Enter the language you want to write in (e.g., Italian, Spanish):")
    if st.button("Explain Writing"):
        if text_to_write and language_to_write:
            explanation = explain_writing(text_to_write, language_to_write)
            st.write(f"ProfessorX: {explanation}")

with tab3:
    response_language = st.selectbox("Select response/pronunciation language:", list(languages.keys()))
    target_language_code = languages[response_language]
    st.subheader("Pronunciation")
    text_to_pronounce = st.text_input("Enter the text you want pronounced:")
    if st.button("Generate Pronunciation"):
        if text_to_pronounce:
            audio_file = generate_pronunciation(text_to_pronounce, target_language_code)
            st.audio(audio_file, format="audio/mp3")
            st.write(f"Pronunciation generated in {response_language}. You can hear it above!")

with tab4:
    st.subheader("Meme Generator")
    meme_description = st.text_input("Enter keywords for your meme (e.g., dog, animated, food, hungry):")
    if st.button("Generate Meme"):
        if meme_description:
            keywords = meme_description.split(", ")
            meme_file = generate_meme_image(keywords)
            st.image(meme_file)
            st.write(f"Meme generated! You can find it in the file: {meme_file}")

with tab5:
    st.subheader("Let ProfessorX Help You with Text")
    uploaded_file = st.file_uploader("Upload a text file with what you want to translate:", type=["txt"])
    if uploaded_file:
        target_language_for_text = st.selectbox("Select language for translation:", list(languages.keys()))
        if st.button("Translate "):
            translated_text = translate_document(uploaded_file, languages[target_language_for_text])
            st.write("Translated:")
            for line in translated_text:
                st.write(line)
