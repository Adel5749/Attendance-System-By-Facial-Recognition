from datetime import datetime
import database



checkStatus=False
def WriteAttendees(name):
    global checkStatus

    database.cur.execute(f"Select * From Attendees Where Name='{name}'")
    result=database.cur.fetchall()

    msg=''

    if len(result)!=0:
        if checkStatus==False:
            msg='you attended already'
            print(checkStatus)

    else:
        database.cur.execute(f"Insert into Attendees values('{name}','{datetime.now().strftime('%H:%M:%S')}','{datetime.today().date()}')")
        database.db.commit()

        if checkStatus==False:
            msg=f"Thank you {name} " \
            f"Welcome to the class"
            print(checkStatus)

    checkStatus=True
    return msg


