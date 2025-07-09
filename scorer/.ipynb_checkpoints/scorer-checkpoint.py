

def score_resume(similarity, matched, missing):
    score = 0
    score = round(similarity * 100 + len(matched) * 3 - len(missing) * 2, 2)
    feedback = ""
    if not matched and not missing:
        feedback = "Tidak ada feedback yang match"
    elif not matched:
        feedback = "Tidak ada feedback yang match"
    elif not missing:
        feedback = "Wow, tidak ada yang miss!"
    else:
        feedback = f"Bagus di {', '.join(matched)}. Tambahkan {', '.join(missing)} di resume."
    
    return {
        "score": score,
        "matched": list(matched),
        "missing": list(missing),
        "feedback": feedback
    }

