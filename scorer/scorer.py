

def score_resume(similarity, matched, missing, job):
    score = 0
    score = round(similarity * 100 + len(matched) * 3 - len(missing) * 2, 2)
    feedback = ""
    if not matched and not missing:
        feedback = "Deskripsi pekerjaan yang kamu masukan sepertinya tidak sesuai nih dengan target pekerjaan mu🫤"
    elif not matched:
        feedback = f"Wahh, sepertinya belum ada skill yang match nih dengan posisi yang mau kamu lamar😥, Coba beralih ke posisi lain atau perdalam skill dalam posisi tersebut yaa seperti {', '.join(missing)}, Goodluck😎👋."
    elif not missing:
        feedback = "WOW! Semua skill yang ada di CV mu dengan deskripsi job yang mau kamu lamar sesuai! Gassss lamar, kamulah yang terbaik dari seluruh kandidat🥶"
    else:
        feedback = f"Kamu sudah mencantumkan keyword {', '.join(matched)}. Untuk memperkuat CV-mu sebagai {job}, pertimbangkan untuk menambahkan skill {', '.join(missing)} sesuai dengan Job Description yang kamu lamar, Goodluck😎👋."

        
    return {
        "score": score,
        "matched": list(matched),
        "missing": list(missing),
        "feedback": feedback
    }

