import streamlit as st
import openai
from dotenv import load_dotenv
import re
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.header("Sachvortrag vs Rechtsvortrag")
text = st.text_area("Vertragstext")
sanitize = st.checkbox("Sanitize text")

analyze = st.button("Analysieren")

results = []
res_box = st.empty()


def run_prompts_for_section(text):
    if sanitize:
        prompt = f"""Sanitize the following text that was scanned via OCR: 

Original text:
{text}

Sanitized text:
"""
        chat_completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            temperature=0,
        )
        text = chat_completion.choices[0].text

    separator = "\n\n"
    paragraphs = text.split(separator)

    for paragraph in paragraphs:
        prompt = f"""Ist der Text ein Sachvortrag oder ein Rechtsvortrag?

Mögliche Antworten:
#1. Sachvortrag
#2. Rechtsvortrag
#3. Beides
#4. Keines



Text: ```
{paragraph}
````

Antwort: #"""

        chat_completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=10,
            temperature=0,
        )
        result_str = chat_completion.choices[0].text
        match = re.search("[0-9]", result_str)
        if match is not None:
            selected_option = int(match.group())
        else:
            selected_option = 4

        colors = ["green", "red", "orange", "black"]
        color_for_option = colors[selected_option - 1]

        results.append((paragraph, color_for_option))
        result = separator.join([f":{color}[{txt}]" for txt, color in results])
        res_box.markdown(result)


if analyze:
    separator = "\n\n\n"
    parts = text.split(separator)
    for part in parts:
        run_prompts_for_section(part)
