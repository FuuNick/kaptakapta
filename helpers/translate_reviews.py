from googletrans import Translator
from functools import lru_cache

@lru_cache(maxsize=10000)
def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, src='id', dest='en')
    return translation.text
