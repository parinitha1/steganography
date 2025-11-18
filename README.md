🖼️ Image Steganography Using LSB (Flask Web App)

A simple and secure web application that hides and extracts secret messages inside images using the Least Significant Bit (LSB) technique.
The app includes user authentication and OTP verification, where the OTP is generated at runtime and shown in the terminal to ensure that only the authenticated user can decode the hidden message.

⭐ Features

🔐 Signup & Login authentication (SQLite)

🖼️ Hide text inside images using LSB

🔍 Decode hidden messages

🔑 OTP verification (printed in terminal, not stored in DB)

🗂️ Uploaded & encoded images saved automatically

🌐 Clean Flask-based web interface

📁 Project Structure
.
│── app.py                # Main Flask application
│── view_db.py            # View users stored in SQLite DB
│── users.db              # Database storing user accounts
│── requirements.txt      # Dependencies
│
│── templates/            # Frontend HTML pages
│   ├── index.html
│   ├── encode.html
│   ├── decode.html
│   ├── verify.html
│   ├── login.html
│   └── signup.html
│
│── static/               # CSS styling
│   └── style.css
│
└── uploads/              # Uploaded & encoded images

▶️ How to Run the Project
1. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

2. Install dependencies
pip install -r requirements.txt

3. Start the server
python app.py


Open the browser and go to:

http://127.0.0.1:5000/

🔐 OTP Verification

When a user attempts to decode an image:

User uploads the encoded image

System generates a 6-digit OTP

OTP is printed in the terminal only

User enters that OTP in verify.html

If OTP matches → message is revealed

If not → access is denied

✔ OTP is not stored in the database
✔ OTP lives only in memory until verification

🧠 How LSB Steganography Works

The system modifies the least significant bit of each image pixel to store message bits.
This makes the change visually undetectable.

Example:

Original pixel (binary):  11001100
Message bit:                    1
Modified pixel:          11001101


The human eye cannot notice this tiny change.

🛠️ Technologies Used

Python

Flask

SQLite

PIL / Pillow

HTML, CSS

LSB Steganography

OTP Verification
