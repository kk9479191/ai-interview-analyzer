import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="interview_ai"
    )

# ✅ INSERT FUNCTION (IMPORTANT)
def insert_result(name, question, answer, score, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO results (name, question, answer, score, result)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, question, answer, score, result))

    conn.commit()
    conn.close()

# ✅ FETCH FUNCTION (DASHBOARD KE LIYE)
def fetch_results():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM results")
    data = cursor.fetchall()

    conn.close()
    return data