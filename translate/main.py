from deep_translator import GoogleTranslator
from langdetect import detect


def translate(text, src, target):
    text_object = GoogleTranslator(source=src, target=target)
    translated_text = text_object.translate(text=text)
    source = detect(text)
    if translated_text:
        return {"text": translated_text, "src": source}
    return
