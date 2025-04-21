import streamlit as st

import os
import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime

# === Ensure folders exist ===
if not os.path.exists("student_images"):
    os.makedirs("student_images")
if not os.path.exists("logs"):
    os.makedirs("logs")

# === Add Student ===
def addastudent():
    st.subheader("➕ Add a New Student")
    name = st.text_input("Enter the name of the student")
    file = st.file_uploader("Upload student image", type=["jpg", "jpeg", "png"])

    if st.button("Add Student"):
        if name and file:
            with open(f"student_images/{name}.jpg", "wb") as f:
                f.write(file.read())

            conn = sqlite3.connect("attendance.db")
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS students (name TEXT)''')
            c.execute('''INSERT INTO students VALUES (?)''', (name,))
            conn.commit()
            conn.close()

            st.success(f"Student {name} added successfully!")
        else:
            st.warning("Please provide both name and image.")

# === Delete Student ===
def deleteastudent():
    st.subheader("🗑️ Delete a Student")
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("SELECT name FROM students")
    data = c.fetchall()
    conn.close()

    student_list = [i[0] for i in data]
    selected_student = st.selectbox("Select a student to delete", student_list)

    if st.button("Delete Student"):
        os.remove(f"student_images/{selected_student}.jpg")

        conn = sqlite3.connect("attendance.db")
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE name=?", (selected_student,))
        conn.commit()
        conn.close()

        st.success(f"Student {selected_student} deleted successfully!")

# === Show Attendance ===
def showattendance():
    st.subheader("📋 Attendance Logs")
    logs = os.listdir("logs")
    logs.sort(reverse=True)

    selected_log = st.selectbox("Select a log file to view", logs)

    if selected_log:
        df = pd.read_csv(f"logs/{selected_log}")
        st.dataframe(df)

    present_students=[]

    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("SELECT name FROM students")
    data = c.fetchall()
    conn.close()

    all_students = [i[0] for i in data]
    attendance_data = []

    for student in all_students:
        status = "Present" if student in present_students else "Absent"
        attendance_data.append({"Name": student, "Status": status})

    df = pd.DataFrame(attendance_data)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(f"logs/attendance_{now}.csv", index=False)

    st.dataframe(df)
    st.success("Attendance marked and saved!")

# === UI Setup ===
st.set_page_config(page_title="AI Attendance System", layout="centered")
st.title("📸 AI Attendance System")
st.markdown("Manage students and mark attendance using face recognition.")

# === Navigation Tabs ===
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 View Attendance",
    "➕ Add Student",
    "🗑️ Delete Student",
    "📸 Mark Attendance"
])

with tab1:
    showattendance()

with tab2:
    addastudent()

with tab3:
    deleteastudent()

with tab4:
    st.subheader("📸 Upload Class Photo to Mark Attendance")
    upimage = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

    if upimage:
        st.image(upimage, caption="Uploaded Image", use_column_width=True)

    if st.button("🔍 Mark Attendance"):
        if upimage:
            st.toast("Running face recognition...", icon="🧠")
            markattendance(upimage)
        else:
            st.warning("Please upload an image first.")

# Footer
st.markdown("---")
st.caption("Made with ❤️ by you and your AI sidekick 🤖")
