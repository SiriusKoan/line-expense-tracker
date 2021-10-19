from database import db, Records


def parse_msg(msg):
    i = msg.index(" ")
    command = msg[:i]
    text = msg[i:]
    if command.startswith("/"):
        return command[1:], text
    return None


def add_record(debtor, lender, money):
    try:
        record = Records(debtor, lender, money)
        db.session.add(record)
        db.session.commit()
        return True
    except:
        return False


def remove_record(id):
    try:
        record = Records.query.filter_by(id=id).first()
        db.session.delete(record)
        db.session.commit()
        return True
    except:
        return False


def done_record(id):
    try:
        record = Records.query.filter_by(id=id)
        record.update({"status": True})
        db.session.commit()
        return True
    except:
        return False


def list_records():
    records = Records.query.all()
    records = [
        {
            "id": record.id,
            "debtor": record.debtor,
            "lender": record.lender,
            "money": record.money,
            "status": "Done" if record.status else "Not done yet",
        }
        for record in records
    ]
    return records
