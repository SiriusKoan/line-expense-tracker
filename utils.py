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


def remove_all_records():
    try:
        db.session.query(Records).delete()
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

def done_all_records(**filters):
    try:
        record = Records.query.filter_by(status=False, **filters)
        record.update({"status": True})
        db.session.commit()
        return True
    except:
        return False

def list_records(**filters):
    records = Records.query
    records = records.filter_by(**filters).all()
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


def calculate_summary(username):
    record_debtor = (
        Records.query.filter_by(debtor=username).filter_by(status=False).all()
    )
    record_lender = (
        Records.query.filter_by(lender=username).filter_by(status=False).all()
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
