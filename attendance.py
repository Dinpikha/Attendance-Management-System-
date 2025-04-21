# import sqlite3

# conn = sqlite3.connect('attendance.db')
# cursor = conn.cursor()
# try:
#     cursor.execute(
#         "INSERT INTO students (name, photo_path) VALUES (?, ?)",
#         ('Siddhi', 'static/student_photos/Image4.jpg')
#     )
#     conn.commit()
#     print("Student added successfully!")
# except sqlite3.IntegrityError as e:
#     print(f"Error: {e}") 
# finally:
#     conn.close()
