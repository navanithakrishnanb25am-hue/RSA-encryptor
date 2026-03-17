from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, os
from email.message import EmailMessage
from dotenv import load_dotenv

# LOAD ENV
load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# DEBUG (optional - remove later)
print("Loaded EMAIL:", EMAIL)
print("Loaded PASSWORD:", "YES" if PASSWORD else "NO")

# ---------- EMAIL FUNCTION ----------
def send_email(receiver, message):

    try:
        msg = EmailMessage()
        msg["Subject"] = "🔐 RSA Encrypted Message"
        msg["From"] = EMAIL
        msg["To"] = receiver
        msg.set_content(f"""
Encrypted Message:

{message}

Use your RSA system to decrypt this message.
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(str(EMAIL), str(PASSWORD))
            smtp.send_message(msg)

        return True

    except Exception as e:
        print("EMAIL ERROR:", e)
        return False


# ---------- API ROUTE ----------
@app.route("/send", methods=["POST"])
def send():

    data = request.json

    receiver = data.get("receiver")
    message = data.get("message")

    if not receiver or not message:
        return jsonify({"status": "error", "msg": "Missing data"})

    success = send_email(receiver, message)

    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "msg": "Email failed"})


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
print("EMAIL:", EMAIL)
print("PASSWORD:", PASSWORD)