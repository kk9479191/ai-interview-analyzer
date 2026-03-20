from textblob import TextBlob

def analyze_answer(answer, emotion):

    sentiment = TextBlob(answer).sentiment.polarity

    score = int((sentiment + 1) * 40)

    if emotion == "happy":
        score += 20

    if score >= 60:
        result = "Selected"
    else:
        result = "Rejected"

    return score, result