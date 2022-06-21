from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    response = MessagingResponse()
    msg = response.message(
        f"Thanks for contacting me. You have sent '{text}' from {number}.")
    msg1 = response.message("hey 2")
    msg.media("https://hatrabbits.com/wp-content/uploads/2017/01/random.jpg")
    return str(response)


if __name__ == "__main__":
    app.run(port=5000)
