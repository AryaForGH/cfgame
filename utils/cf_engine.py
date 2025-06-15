import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.split()

def evaluate_answer(jawaban, soal):
    tokens = preprocess(jawaban)
    matched = sum(1 for keyword in soal["kata_kunci"] if keyword in tokens)
    total = len(soal["kata_kunci"])

    if jawaban.strip().lower() == soal["jawaban"]:
        return 1.0, "🎉 Jawaban kamu benar sekali! Hebat! ⭐"
    elif matched > 0:
        score = matched / total
        if score >= 0.7:
            feedback = "💡 Hampir benar! Jawaban kamu mendekati."
        elif score >= 0.4:
            feedback = "📖 Kamu sudah cukup paham. Yuk coba lagi!"
        else:
            feedback = "🤔 Masih kurang tepat. Baca lagi deskripsinya ya!"
        return score, feedback
    else:
        return 0.0, "❌ Belum tepat, ayo coba lagi dengan teliti."
