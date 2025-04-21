import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Fetch name and photo_path from students table
c.execute('SELECT name, photo_path FROM students')
refs = {row[0]: row[1] for row in c.fetchall()}
print(refs)

# Create the attendance table
c.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date DATE DEFAULT CURRENT_DATE,
    status TEXT CHECK(status IN ('present', 'absent')),
    FOREIGN KEY(student_id) REFERENCES students(id)
)
''')

# Create the attendance_logs table
c.execute('''
CREATE TABLE IF NOT EXISTS attendance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    recognized INT,
    unknown INT
)
''')

# Commit changes and close connection
conn.commit()
conn.close()
