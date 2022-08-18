from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Records(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    debtor = db.Column(db.String, nullable=False)
    lender = db.Column(db.String, nullable=False)
    money = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=False)  # True means done
    room = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, debtor, lender, money, room) -> None:
        self.debtor = debtor
        self.lender = lender
        self.money = money
        self.room = room
