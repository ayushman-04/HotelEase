from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# --- PostgreSQL connection ---
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="hotel_db",
        user="postgres",
        password="admin123"
    )

@app.route('/')
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rooms WHERE available = TRUE;")
    rooms = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", rooms=rooms)

@app.route('/book/<int:room_id>')
def book(room_id):
    return render_template("booking.html", room_id=room_id)

@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form['name']
    email = request.form['email']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    room_id = request.form['room_id']

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO bookings (name, email, checkin, checkout, room_id) VALUES (%s, %s, %s, %s, %s)",
                (name, email, checkin, checkout, room_id))
    cur.execute("UPDATE rooms SET available = FALSE WHERE id = %s", (room_id,))
    conn.commit()
    cur.close()
    conn.close()

    return render_template("success.html", name=name, checkin=checkin, checkout=checkout)

if __name__ == "__main__":
    app.run(debug=True)
