from datetime import datetime
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://adrian:z9Pb5KsRkzFmlMaO@cluster0.xj8hrn6.mongodb.net/")

db = cluster["bakery"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def reply():
    """
    It takes the text of the message and the number of the sender, and then replies with a message
    :return: The response is being returned.
    """
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    response = MessagingResponse()

    user = users.find_one({"number": number})
    if bool(user) is False:
        response.message("Hi, thanks for contacting *The Red Velvet*. \n"
                         "You can choose from one of the following options below:\n\n"
                         "*Type*\n\n1️⃣. To *contact* us \n2️⃣. *Order* Snacks\n"
                         "3️⃣. To know our *working hours* \n4️⃣. To get our *address*")
        users.insert_one({"number": number, "status": "main", "messages": []})
    else:
        response.message("Sorry, I don't understand.")

    users.update_one({"number": number}, {
                     "$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(response)


if __name__ == "__main__":
    app.run(port=5000)
