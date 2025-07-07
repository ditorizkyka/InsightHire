def from sentence_transformers import SentenceTransformer

def model_compute(preprocessed_resume, preprocessed_jd):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    resume_embedding = model.encode(preprocessed_resume)
    jd_embedding = model.encode(preprocessed_jd)
    return resume_embedding, jd_embedding

def compute_similarity():
    print("hw")