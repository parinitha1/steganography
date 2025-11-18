Image Steganography Using LSB (FlASK Web App with OTP Verification)

This project hides secret text inside images using the Least Significant Bit (LSB) steganography method.
To prevent unauthorized access to hidden messages, the system uses OTP verification, where the OTP is generated at runtime and printed in the terminal, not stored in any database.

📁 Project Structure
project/
│── app.py               # Main Flask application (run this)
│── view_db.py           # View user database (optional)
│── users.db             # SQLite database storing user accounts
│── requirements.txt     # Required libraries
│
│── templates/
│     ├── index.html     # Home page
│     ├── encode.html    # Message hiding page
│     ├── decode.html    # Message decoding request page
│     ├── login.html     # Login page
│     ├── signup.html    # Registration page
│     └── verify.html    # OTP input page
│
│── static/
│     └── style.css      # UI styling
│
└── uploads/             # Stores uploaded & encoded images

📜 File-by-File Explanation
✔ 1. app.py

The main backend application.

Handles:

Running the Flask server

Login + Signup

Image uploading

LSB encoding (hiding message)

LSB decoding (extracting message)

OTP generation (random 6-digit code)

Printing OTP in terminal (NOT stored in DB)

Verifying user-entered OTP

Routing all HTML pages

➡ This is the file you run.

✔ 2. users.db

SQLite database

Stores user credentials ONLY

Does not store OTP

OTP is temporary and stored only in memory during verification

✔ 3. view_db.py

A helper script used to view user table entries.

Run manually if needed:

python view_db.py

✔ 4. HTML Templates
index.html

Home page

Navigation to encode/decode/login

encode.html

Upload image

Enter secret message

Encoded image saved into /uploads

decode.html

Upload encoded image

System generates OTP

OTP is printed in terminal only

User is redirected to enter OTP

verify.html

User enters OTP

If OTP matches → hidden message is shown

If incorrect → decoding blocked

login.html + signup.html

Handles user authentication.

✔ 5. style.css

Styles the HTML pages.

✔ 6. uploads/

Stores uploaded original images and the encoded output images.

🔐 OTP Verification Flow (Terminal-Based)

User logs in

Navigates to Decode page

Uploads the encoded image

Backend generates a 6-digit OTP

OTP is printed in the terminal console

Backend temporarily remembers the OTP (not stored anywhere)

User enters OTP in the verify.html page

If correct → hidden message is extracted

If incorrect → decoding denied

📌 This ensures only the real logged-in user sitting at the machine sees the OTP.

🛠️ Setup Instructions
1. Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

2. Install dependencies
pip install -r requirements.txt

3. Run the app
python app.py


Open:

http://127.0.0.1:5000/

🖥️ Technologies Used

Python

Flask

PIL/Pillow

SQLite

HTML/CSS

LSB Steganography

OTP Security (Console-based)

GitHub for version control
