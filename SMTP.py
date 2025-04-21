from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
import os
import sqlite3
load_dotenv()

api_key=os.getenv("API_KEY")
# print(f"API KEY : {api_key}")
def send_attendance_alert(student_name="Unknown"):
    Sender="dipikadipika1306@gmail.com"

    conn=sqlite3.connect('attendance.db')
    cursor=conn.cursor()

    Receiver="dipikac1306@gmail.com"



    i="Student _ name"
    msg=MIMEText(f"Hey {i} Your attendance is not marked . Kindly Contact to your subject teacher")
    msg["from"]=Sender
    msg["Subject"]="Student Attendance"
    msg["To"]=Receiver

    with smtplib.SMTP("smtp.gmail.com",587) as server :
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(Sender,api_key)
        server.sendmail(Sender,Receiver,msg.as_string())

    print("Email sent successfully with STARTTLS!")