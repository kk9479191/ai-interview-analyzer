from flask import Flask, render_template, request
from analyzer import analyze_answer
from database import insert_result
from database import get_connection
from emotion import detect_emotion
import mysql.connector

app = Flask(__name__)
app.secret_key = "mysecretkey123"

QUESTION = "Explain Python programming language"

def calculate_score(answer, emotion):
    score = 0

    # 🔹 Good keywords
    good_words = ["experience", "skills", "project", "team", "learn", "develop"]

    for word in good_words:
        if word in answer.lower():
            score += 10

    # 🔹 Length check
    if len(answer.split()) > 20:
        score += 20

    # 🔹 Emotion bonus
    if emotion == "happy":
        score += 10
    elif emotion == "neutral":
        score += 5

    return score


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/interview", methods=["POST"])
def interview():

    name = request.form.get("name")

    return render_template(
        "interview.html",
        name=name,
        question=QUESTION
    )


from flask import Flask, render_template, request, jsonify, session, redirect

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    answer = data.get("answer")
    emotion = data.get("emotion") or "neutral"

    print("Emotion received:", emotion)

    score = calculate_score(answer, emotion)
    result = "Selected" if score >= 40 else "Rejected"

    insert_result("User", "Tell me about yourself", answer, score, result)

    session['score'] = score
    session['result'] = result
    session['emotion'] = emotion  

    return jsonify({"status": "success"})

@app.route("/result")
def result():
    score = session.get('score')
    result = session.get('result')
    emotion = session.get('emotion')

    return render_template("result.html", score=score, result=result)

from database import insert_result, fetch_results
@app.route("/dashboard")
def dashboard():
    data = fetch_results() 

    return render_template("dashboard.html", data=data)

@app.route("/clear")
def clear():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE results")

    conn.commit()
    conn.close()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
