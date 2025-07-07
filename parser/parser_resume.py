import fitz  # PyMuPDF
import spacy
import pandas as pd
import os

def parse_resume(text):
    text = text.replace("\n", "")         # Hilangkan newline
    text = text.replace("●", "")
    text = text.replace("|", "")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    filtered_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct or not token.is_alpha:
            continue
        filtered_tokens.append(token.lemma_)

    return " ".join(filtered_tokens)


