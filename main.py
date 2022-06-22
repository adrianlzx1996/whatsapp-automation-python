from datetime import datetime

from flask import Flask, request
from pymongo import MongoClient
from twilio.twiml.messaging_response import MessagingResponse

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
                         "*Type*\n\n1️⃣ To *contact* us \n2️⃣ *Order* Snacks\n"
                         "3️⃣ To know our *working hours* \n4️⃣ To get our *address*")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid respone")
            return str(response)

        if option == 1:
            response.message(
                "You can contact us through phone or e-mail.\n\n*Phone*: +6 012 345 6789"
                "\n*E-mail*: leongadrian36@gmail.com"
            )
        elif option == 2:
            response.message("You've entered *ordering mode*")
            response.message("You can select one of the following cakes to order:\n\n"
                             "*Type*\n\n"
                             "1️⃣ Red Velvet\n"
                             "2️⃣ Dark Forest\n"
                             "3️⃣ Ice Cream Cake\n"
                             "4️⃣ Plum Cake\n"
                             "0️⃣ Go Back\n"
                             )
            users.update_one({"number": number}, {
                             "$set": {"status": "ordering"}})
        elif option == 3:
            response.message("We work everyday from *9 AM* to *9 PM*.")
        elif option == 4:
            response.message("We have multiple stores across the city. ")
        else:
            response.message("Sorry, I don't understand.")
    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid respone")
            return str(response)

        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            response.message("You can choose from one of the following options below:\n\n"
                             "*Type*\n\n1️⃣. To *contact* us \n2️⃣. *Order* Snacks\n"
                             "3️⃣. To know our *working hours* \n4️⃣. To get our *address*")
            return str(response)
        elif 1 <= option <= 9:
            cakes = ["Red Velvet", "Dark Forest",
                     "Ice Cream Cake", "Plum Cake"]
            selected = cakes[option - 1]
            users.update_one({"number": number}, {
                             "$set": {"status": "address"}})
            users.update_one({"number": number}, {
                             "$set": {"item": selected}})
            response.message("Excelled choice!")
            response.message("Please enter your address to confirm the order.")
        else:
            response.message("Please enter a valid respone")
    elif user["status"] == "address":
        selected = user["item"]

        response.message("Thanks for shopping with us")
        response.message(
            f"Your order for {selected} have received and will be delivered within an hour.")
    else:
        response.message("Sorry, I don't understand.")

    users.update_one({"number": number}, {
                     "$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(response)


if __name__ == "__main__":
    app.run(port=5000)
