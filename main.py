from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    response = MessagingResponse()
    if "hi" in text.lower():
        response.message("Hello")
    else:
        response.message("Sorry, I don't understand")
    return str(response)


if __name__ == "__main__":
    app.run(port=5000)
