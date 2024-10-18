import textwrap
# from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import pydub
import streamlit as st
import openai
import langid
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import random
# import os
import requests
import tempfile

# Set your OpenAI API key here
openai.api_key = 'sk-dxZ21bnDQC_qVx-G73MdfTfKQi5Sw9gMnYQJYIXu0JT3BlbkFJLXkpHdYw_9a7BnjxIJx99nO0eLtfehnqXt43zK3hQA'


# Function to detect language
def detect_language(text):
    lang, _ = langid.classify(text)
    return lang


# Function to translate text to a specified language using OpenAI
def translate_text(text, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Translate this to {target_language}: '{text}'"}]
    )
    return response.choices[0].message['content']


# Function to generate response from chatbot using OpenAI
def generate_response(text, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{text}. Respond in {target_language}"}]
    )
    return response.choices[0].message['content']


# Function to explain how to write in a specified language
def explain_writing(text, language):
    prompt = f"How do I write '{text}' in {language}?"
    return generate_response(prompt, language)


# Function to generate pronunciation audio in the selected language
def generate_pronunciation(text, language):
    # Translate text to the selected pronunciation language
    translated_text = translate_text(text, language)
    tts = gTTS(text=translated_text, lang=language)
    filename = f"pronunciation_{random.randint(1000, 9999)}.mp3"
    tts.save(filename)
    return filename


# Function to generate a meme using OpenAI's image generation
def generate_meme_caption(keywords):
    prompt = f"Generate a funny, creative meme caption based on these keywords: {', '.join(keywords)}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']


def generate_meme_image(keywords):
    # Generate image based on keywords using DALL·E
    prompt = f"A meme image based on these keywords: {', '.join(keywords)}"
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )

    image_url = response['data'][0]['url']
    img = Image.open(requests.get(image_url, stream=True).raw)

    # Generate creative meme caption
    caption = generate_meme_caption(keywords)

    # Prepare the drawing context
    draw = ImageDraw.Draw(img)
    image_width, image_height = img.size

    # Load font and adjust size
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Ensure the font file is available
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font

    # Wrap text to fit within the image width
    max_width = image_width - 40  # Padding on both sides
    wrapped_text = textwrap.fill(caption, width=30)  # Adjust width according to image size

    # Measure text size to calculate position
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (image_width - text_width) // 2  # Center horizontally
    y = image_height - text_height - 20  # Position near the bottom

    # Add shadow to the text for better readability
    shadow_color = "black"
    shadow_offset = 3
    draw.text((x - shadow_offset, y - shadow_offset), wrapped_text, font=font, fill=shadow_color)
    draw.text((x + shadow_offset, y - shadow_offset), wrapped_text, font=font, fill=shadow_color)
    draw.text((x - shadow_offset, y + shadow_offset), wrapped_text, font=font, fill=shadow_color)
    draw.text((x + shadow_offset, y + shadow_offset), wrapped_text, font=font, fill=shadow_color)

    # Draw main text
    text_color = "white"
    draw.text((x, y), wrapped_text, font=font, fill=text_color)

    # Save and return the filename
    filename = f"meme_{random.randint(1000, 9999)}.jpg"
    img.save(filename)
    return filename


def convert_audio_to_text(audio_file):
    # Convert the audio file to the correct format if necessary
    sound = pydub.AudioSegment.from_file(audio_file)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        sound.export(temp_audio.name, format="mp3")

        # Transcribe audio using OpenAI Whisper API
        with open(temp_audio.name, "rb") as audio:
            transcript = openai.Audio.transcribe("whisper-1", audio)

    return transcript['text']


# Streamlit App
st.title("ProfessorX Chatbot")

# Language Selection Dropdown (for responses and pronunciation)
languages = {"English": "en", "Spanish": "es", "French": "fr", "German": "de", "Chinese": "zh", "Romanian": "ro"}
response_language = st.selectbox("Select response/pronunciation language:", list(languages.keys()))
target_language_code = languages[response_language]

# Tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Chat with ProfessorX", "How to Write", "Pronunciation", "Meme Generator", "Talk with ProfessorX"])

with tab1:
    st.subheader("Talk to ProfessorX")
    user_input = st.text_input("Enter your message:", "")
    if st.button("Send"):
        if user_input:
            detected_language = detect_language(user_input)
            st.write(f"Detected Language: {detected_language}")
            response = generate_response(user_input, target_language_code)
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
    st.subheader("Voice Input")

    # Allow user to upload an audio file for processing
    uploaded_file = st.file_uploader("Upload your voice recording", type=["mp3", "wav", "ogg"])

    if uploaded_file is not None:
        # Convert uploaded audio to text
        user_voice_input = convert_audio_to_text(uploaded_file)
        st.write(f"You said: {user_voice_input}")

        # Generate response from ProfessorX based on the voice input
        detected_language = detect_language(user_voice_input)
        st.write(f"Detected Language: {detected_language}")
        response = generate_response(user_voice_input, target_language_code)
        st.write(f"ProfessorX: {response}")
