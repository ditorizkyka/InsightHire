import spacy

def parse_jd(jd_text):
    jd_text = jd_text.replace("\n", " ")  # ganti newline dengan spasi
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(jd_text)

    filtered_jdText = []
    for token in doc:
        if token.is_stop or token.is_punct or not token.is_alpha:
            continue
        filtered_jdText.append(token.lemma_.lower())  # lowercase untuk konsistensi

    return " ".join(filtered_jdText)