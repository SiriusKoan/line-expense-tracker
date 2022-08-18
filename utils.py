from database import db, Records


def parse_msg(msg):
    try:
        i = msg.index(" ")
    except ValueError:
        command = msg
        text = ""
    else:
        command = msg[:i]
        text = msg[i:]
    if command.startswith("/"):
        return command[1:].strip(), text.strip()
    return None


def add_record(room, debtor, lender, money):
    try:
        record = Records(debtor, lender, money, room)
        db.session.add(record)
        db.session.commit()
        return True
    except:
        return False


def remove_record(room, id):
    try:
        record = Records.query.filter_by(id=id, room=room).first()
        db.session.delete(record)
        db.session.commit()
        return True
    except:
        return False


def remove_all_records(room):
    try:
        Records.query.filter_by(room=room).delete()
        db.session.commit()
        return True
    except:
        return False


def done_record(room, id):
    try:
        record = Records.query.filter_by(id=id, room=room)
        record.update({"status": True})
        db.session.commit()
        return True
    except:
        return False

def done_all_records(room, **filters):
    try:
        record = Records.query.filter_by(room=room, status=False, **filters)
        record.update({"status": True})
        db.session.commit()
        return True
    except:
        return False

def list_records(room, **filters):
    records = Records.query
    records = records.filter_by(room=room, **filters).all()
    records = [
        {
            "id": record.id,
            "debtor": record.debtor,
            "lender": record.lender,
            "money": record.money,
            "status": "Done" if record.status else "Not done yet",
            "timestamp": record.timestamp.strftime("%Y-%m-%d"),
        }
        for record in records
    ]
    return records


def calculate_summary(room, username):
    record_debtor = (
        Records.query.filter_by(room=room, debtor=username, status=False).all()
    )
    record_lender = (
        Records.query.filter_by(room=room, lender=username, status=False).all()
    )
    people = {}
    for record in record_debtor:
        if record.lender in people:
            people[record.lender] += record.money
        else:
            people[record.lender] = record.money
    for record in record_lender:
        if record.debtor in people:
            people[record.debtor] -= record.money
        else:
            people[record.debtor] = -1 * record.money
    return people
