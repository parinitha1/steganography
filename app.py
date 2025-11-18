from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
from PIL import Image
import os
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "secret123"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========== DATABASE SETUP ==========
DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- ENCODE FUNCTION ----------
def encode_image(image_path, message):
    image = Image.open(image_path)
    encoded_image = image.copy()
    width, height = image.size
    message += "%%"  # delimiter
    binary_message = ''.join(format(ord(i), '08b') for i in message)
    data_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for n in range(3):
                if data_index < len(binary_message):
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
            encoded_image.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    return encoded_image

# ---------- DECODE FUNCTION ----------
def decode_image(image_path):
    image = Image.open(image_path)
    binary_data = ""
    for y in range(image.height):
        for x in range(image.width):
            pixel = list(image.getpixel((x, y)))
            for n in range(3):
                binary_data += str(pixel[n] & 1)

    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    decoded_message = ""
    for byte in all_bytes:
        decoded_message += chr(int(byte, 2))
        if decoded_message[-2:] == "%%":
            break

    return decoded_message[:-2]

# ========== AUTH FUNCTIONS ==========
def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# ---------- SIGNUP ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("All fields are required!")
            return redirect(url_for('signup'))

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash("Signup successful! You can now log in.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!")
            return redirect(url_for('signup'))

    return render_template('signup.html')

# ---------- LOGIN + MFA OTP ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if not user:
            flash("User not found! Please sign up.")
            return redirect(url_for('signup'))

        # Direct comparison (no encryption)
        if user[0] == password:
            # Step 1 passed — generate OTP
            otp = str(random.randint(100000, 999999))
            session['pending_user'] = username
            session['otp'] = otp
            print(f"🔐 OTP for {username}: {otp}")  # Shown in console for now
            flash("OTP sent! (Check console for now)")
            return redirect(url_for('verify'))
        else:
            flash("Incorrect password!")
            return redirect(url_for('login'))

    return render_template('login.html')

# ---------- VERIFY OTP ----------
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'pending_user' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        actual_otp = session.get('otp')

        if entered_otp == actual_otp:
            session['username'] = session.pop('pending_user')
            session.pop('otp', None)
            flash("✅ MFA Verified! You are logged in.")
            return redirect(url_for('decode_page'))
        else:
            flash("❌ Invalid OTP! Try again.")
            return redirect(url_for('verify'))

    return render_template('verify.html')

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

# ---------- HOME ----------
@app.route('/')
def home():
    return render_template('index.html')

# ---------- ENCODE ----------
@app.route('/encode', methods=['GET', 'POST'])
def encode_page():
    if request.method == 'POST':
        file = request.files['image']
        message = request.form['message']

        if not file or file.filename == '':
            flash("Please select an image!")
            return redirect(url_for('encode_page'))

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        encoded_image = encode_image(path, message)
        encoded_path = os.path.join(UPLOAD_FOLDER, "encoded_" + file.filename)
        encoded_image.save(encoded_path)

        flash("Message encoded successfully!")
        return render_template('encode.html', encoded_image=encoded_path)

    return render_template('encode.html', encoded_image=None)

# ---------- DECODE ----------
@app.route('/decode', methods=['GET', 'POST'])
def decode_page():
    message = None

    if 'username' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['image']

        if not file or file.filename == '':
            flash("Please upload an image.")
            return redirect(url_for('decode_page'))

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        message = decode_image(path)
        flash("Message decoded successfully!")

    return render_template('decode.html', message=message, username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)
