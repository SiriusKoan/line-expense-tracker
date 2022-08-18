from os import getenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
from config import Config
from database import db
from utils import (
    add_record,
    calculate_summary,
    done_all_records,
    done_record,
    list_records,
    parse_msg,
    remove_all_records,
    remove_record,
)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

bot = LineBotApi(getenv("TOKEN"))
handler = WebhookHandler(getenv("WEBHOOK"))


@app.before_first_request
def init():
    db.create_all()


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if parse_msg(event.message.text):
        command, message = parse_msg(event.message.text)
    else:
        return False
    room = event.source.group_id if event.source.type == "group" else event.source.user_id
    if command == "help":
        bot.reply_message(
            event.reply_token,
            TextSendMessage(
                text="""
                /add <debtor> <lender> <money> - Add one record.
                /remove <record_id> - Remove specified record.
                /remove_all [filter] - Remove all records.
                /done <record_id> - Done specified record. The record will not be shown in summary when it is marked done.
                /done_all [filter] - Done all records.
                /summary <username> - Show specified user's summary.
                /list [filter] - Show all records.
                /list_done [filter] - Show all done records.
                /list_undone [filter] - Show all undone records.
                """
            ),
        )
    if command == "add":
        try:
            debtor, lender, money = message.split()
        except ValueError:
            bot.reply_message(event.reply_token, TextSendMessage(text="Invalid input."))
        else:
            print(event.source)
            if add_record(room, debtor, lender, money):
                bot.reply_message(event.reply_token, TextSendMessage(text="OK."))
            else:
                bot.reply_message(
                    event.reply_token, TextSendMessage(text="Error when storing.")
                )
    if command == "remove":
        try:
            id = int(message)
        except ValueError:
            bot.reply_message(
                event.reply_token, TextSendMessage(text="An integer is required.")
            )
        else:
            if remove_record(room, id):
                bot.reply_message(event.reply_token, TextSendMessage(text="OK."))
            else:
                bot.reply_message(
                    event.reply_token, TextSendMessage(text="Error when removing.")
                )
    if command == "remove_all":
        if message:
            removal = remove_all_records(room, debtor=message) and remove_all_records(room, lender=message)
        else:
            removal = remove_all_records(room)
        if removal:
            bot.reply_message(event.reply_token, TextSendMessage(text="OK."))
        else:
            bot.reply_message(
                event.reply_token, TextSendMessage(text="Error when removing.")
            )
    if command == "done":
        try:
            id = int(message)
        except ValueError:
            bot.reply_message(
                event.reply_token, TextSendMessage(text="An integer is required.")
            )
        else:
            if done_record(room, id):
                bot.reply_message(event.reply_token, TextSendMessage(text="OK."))
            else:
                bot.reply_message(
                    event.reply_token, TextSendMessage(text="Error when processing.")
                )
    if command == "done_all":
        if message:
            done = done_all_records(room, debtor=message) and done_all_records(room, lender=message)
        else:
            done = done_all_records(room)
        if done:
            bot.reply_message(event.reply_token, TextSendMessage(text="OK."))
        else:
            bot.reply_message(
                event.reply_token, TextSendMessage(text="Error when processing.")
            )
    if command == "list":
        msg = ""
        if message:
            records = list_records(room, debtor=message) + list_records(room, lender=message)
        else:
            records = list_records(room)
        for record in records:
            msg += f"id: {record['id']}, {record['status']}, {record['debtor']}: {record['money']} -> {record['lender']}, {record['timestamp']}\n"
        if msg == "":
            msg = "No record."
        bot.reply_message(event.reply_token, TextSendMessage(text=msg))
    if command == "list_done":
        msg = ""
        if message:
            records = list_records(room, status=True, debtor=message) + list_records(room, status=True, lender=message)
        else:
            records = list_records(room, status=True)
        for record in records:
            msg += f"id: {record['id']}, {record['status']}, {record['debtor']}: {record['money']} -> {record['lender']}, {record['timestamp']}\n"
        if msg == "":
            msg = "No record."
        bot.reply_message(event.reply_token, TextSendMessage(text=msg))
    if command == "list_undone":
        msg = ""
        if message:
            records = list_records(room, status=False, debtor=message) + list_records(room, status=False, lender=message)
        else:
            records = list_records(room, status=False)
        for record in records:
            msg += f"id: {record['id']}, {record['status']}, {record['debtor']}: {record['money']} -> {record['lender']}, {record['timestamp']}\n"
        if msg == "":
            msg = "No record."
        bot.reply_message(event.reply_token, TextSendMessage(text=msg))
    if command == "summary":
        summary = calculate_summary(room, message)
        msg = ""
        for username, money in summary.items():
            if money > 0:
                msg += f"{message}: {money} -> {username}\n"
            elif money < 0:
                msg += f"{username}: {-1 * money} -> {message}\n"
        print(msg)
        if msg == "":
            msg = "No record."
        bot.reply_message(event.reply_token, TextSendMessage(text=msg))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
