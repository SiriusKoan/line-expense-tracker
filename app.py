from os import getenv
from re import L
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
from utils import add_record, done_record, list_records, parse_msg, remove_record

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

line_bot_api = LineBotApi(getenv("TOKEN"))
handler = WebhookHandler(getenv("WEBHOOK"))


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
    if command == "add":
        try:
            debtor, lender, money = message.split()
        except ValueError:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Invalid input.")
            )
        else:
            if add_record(debtor, lender, money):
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="OK.")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Error when storing.")
                )
    if command == "remove":
        try:
            id = int(message)
        except ValueError:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="An integer is required.")
            )
        else:
            if remove_record(id):
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="OK.")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Error when removing.")
                )
    if command == "done":
        try:
            id = int(message)
        except ValueError:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="An integer is required.")
            )
        else:
            if done_record(id):
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="OK.")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Error when processing.")
                )
    if command == "list":
        msg = ""
        records = list_records()
        for record in records:
            msg += f"id: {record.id}, status: {record.status}, {record.debtor}: {record.money} -> {record.lender}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
