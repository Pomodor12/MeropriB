# database.py
import sqlite3
from datetime import datetime

conn = sqlite3.connect("events.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()

def add_event(title: str, date: str):
    cursor.execute("INSERT INTO events (title, date) VALUES (?, ?)", (title, date))
    conn.commit()

def get_events():
    cursor.execute("SELECT id, title, date FROM events WHERE date >= ?", (datetime.now().strftime("%Y-%m-%d"),))
    return cursor.fetchall()

def get_week_events():
    cursor.execute("""
        SELECT id, title, date FROM events 
        WHERE date BETWEEN ? AND ?
        ORDER BY date
    """, (datetime.now().strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")))
    return cursor.fetchall()

def delete_event(event_id: int):
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
