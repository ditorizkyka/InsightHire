from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

def match_resume(preprocessed_jd, preprocessed_resume, setSkill):
    similarity = similarity_score(preprocessed_jd, preprocessed_resume)
    resume_skills = extract_skills(preprocessed_resume, setSkill)
    jd_skills = extract_skills(preprocessed_jd,setSkill)
    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - matched
    
    return similarity, matched, missing

def similarity_score(preprocessed_jd,preprocessed_resume):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    resume_embedding = model.encode(preprocessed_resume)
    jd_embedding = model.encode(preprocessed_jd)
    similarity_score = cos_sim(resume_embedding, jd_embedding).item() 

    return similarity_score 

def extract_skills(text: str, setSkill) -> set:
     # 📚 Daftar skill yang ingin dideteksi

    text = text.lower()
    found_skills = set()
    for skill in setSkill:
        if skill.lower() in text:
            found_skills.add(skill)
    return found_skills