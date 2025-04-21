import streamlit as st
import pandas as pd
import sqlite3
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;700&family=Lavishly+Yours&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [class*="css"]  {
    font-family: 'EB Garamond', serif;
    background-color: #fff5f8;
    color: #3e3e3e;
}

h3 {
    font-family: 'Lavishly Yours', cursive; !important
    font-size: 2.5em; 
    color: white;
    margin-bottom: 10px;
}
.pixel-font {
    font-family: 'Press Start 2P', cursive;
    font-size: 1.6em;
    color:#ffcce7;
    text-align: center;
}
button {
    background-color: #ffc0cb !important;
    color: #4a4a4a !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.6em 1em !important;
    transition: background-color 0.3s ease;
    font-weight: bold;
    font-size: 1.1em;
}

button:hover {
    background-color: #b76e79 !important;
    color: #fff !important;
    
}

div.stButton > button {
    width: 100%;
    margin-top: 10px;
}

.stFileUploader label {
    font-weight: bold;
    color: #e75480;
    font-size: 2.1em;
}

img {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
col1,col2=st.columns([5,1])
with col1:
    
    
    st.markdown("<div class='pixel-font'>Attendance Management System</div>", unsafe_allow_html=True)

with col2:
    st.image('HELLO.jpeg',caption=None,width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto",use_container_width=False)

from PIL import Image
upimage=st.file_uploader("📸 Upload Image here",type=["jpg","png","jpeg"])
if upimage is not None:
    image=Image.open(upimage)
    st.image(image,caption="Uploaded image",use_container_width=True)


if st.button("📍 Mark Attendance",use_container_width=True):
    if upimage is not None:
        st.toast("Attendance Marked ! ",icon="🎉")
    else:
        st.toast("Upload a Image first !")


from datetime import datetime
conn = sqlite3.connect('attendance.db')
cursor=conn.cursor()
cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS attendance(
    Rollno INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL ,
    Email TEXT NOT NULL,
    Total INTEGER NOT NULL 
    )


    """
    )

today = datetime.now().strftime("%d-%m-%Y")
cursor.execute("PRAGMA table_info(attendance)")
cols = [c[1] for c in cursor.fetchall()]
if today not in cols:
    cursor.execute(f'ALTER TABLE attendance ADD COLUMN "{today}" TEXT')
    conn.commit()
non_date = {"Rollno", "Name", "Email", "Total"}
date_cols = [c for c in cols if c not in non_date]
day_count = len(date_cols)
if day_count == 0:
    "Nothing to do yet"
cases = [f'CASE WHEN "{dc}"="Present" THEN 1 ELSE 0 END' for dc in date_cols]
sum_expr = " + ".join(cases)
cursor.execute("SELECT Rollno FROM attendance")
for (roll,) in cursor.fetchall():
    cursor.execute(
        f"SELECT ({sum_expr}) * 100.0 / {day_count} FROM attendance WHERE Rollno = ?",
        (roll,)
    )
    pct = cursor.fetchone()[0] or 0.0

    cursor.execute(
        "UPDATE attendance SET Total = ? WHERE Rollno = ?",
        (round(pct, 2), roll)
    )
    if cursor.rowcount == 0:
        st.warning(f"Could not update Rollno {roll}")  # sanity check

conn.commit()





# sql2 = "UPDATE attendance SET Total = ?, attendance_status = ? WHERE Rollno = ?"
# cursor.execute(sql2, (Total, attendance_status, roll))



def showattendance():
    conn = sqlite3.connect('attendance.db')
    cursor=conn.cursor()


   
    conn.commit()

    df = pd.read_sql_query("SELECT * FROM attendance", conn)


    st.markdown("### 📋 Attendance Table")
    
    st.dataframe(df, use_container_width=True,hide_index=True)




conn.close()

def addastudent():
    conn = sqlite3.connect('attendance.db')
    cursor=conn.cursor()
    Rollno=st.number_input("📎Enter Roll no of the Student", min_value=1, step=1, format="%i")
    name=st.text_input("📝Enter the Name of the Student")
    Email=st.text_input("Enter the Mail of the Student")

    if st.button("Add Student",use_container_width=True):
         if not Rollno or not name.strip():
            st.toast(" Please fill all the fields!", icon="⚠️")
         else:
            
            cursor.execute("SELECT * FROM attendance WHERE Rollno = ?", (Rollno,))
            existing_student = cursor.fetchone()

            if existing_student:
                st.toast("Student already added!", icon="⚠️")
            else:
                

                cursor.execute("INSERT INTO attendance(Rollno, Name, Total,Email) VALUES (?, ?,?,?)", (Rollno, name.strip(),0,Email.strip()))
                conn.commit()
                st.toast("Student Added ! ",icon="🎉")
            conn.close()
def deleteastudent():
    conn = sqlite3.connect('attendance.db')
    cursor=conn.cursor()
   
    cursor.execute("SELECT Rollno FROM attendance")
    rolls= [row[0] for row in cursor.fetchall()]

    Roll=st.number_input("📎Enter Roll no of the Student",min_value=1, step=1, format="%i")
    if  st.button("Delete ",use_container_width=True):
        if Roll not in rolls:
            st.toast('Enter a Valid Roll no !')
        else :
            
            cursor.execute("DELETE FROM attendance WHERE Rollno=?" , (Roll,))
            conn.commit()
            st.toast('Student Deleted ' , icon='🎉')
   

page=st.selectbox("Select Page",['📊 Go to Dashboard','➕ Add a new Student','🗑️Delete a Student'])
if page=='📊 Go to Dashboard':
    showattendance()
elif page =='➕ Add a new Student':
    addastudent()
elif page =='🗑️Delete a Student':
    deleteastudent()

