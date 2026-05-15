import sqlite3

conn = sqlite3.connect(r'C:\Users\PC_LION\Desktop\bfi_app\database.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id TEXT,
    age INTEGER,
    gender TEXT,
    marital_status TEXT,
    education TEXT,
    employment TEXT,
    q1 INTEGER,
    q2 INTEGER,
    q3 INTEGER,
    q4 INTEGER,
    q5 INTEGER,
    q6 INTEGER,
    q7 INTEGER,
    q8 INTEGER,
    q9 INTEGER,
    q10 INTEGER,
    q11 INTEGER,
    q12 INTEGER,
    q13 INTEGER,
    q14 INTEGER,
    q15 INTEGER,
    q16 INTEGER,
    q17 INTEGER,
    q18 INTEGER,
    q19 INTEGER,
    q20 INTEGER,
    q21 INTEGER,
    q22 INTEGER,
    q23 INTEGER,
    q24 INTEGER,
    q25 INTEGER,
    q26 INTEGER,
    q27 INTEGER,
    q28 INTEGER,
    q29 INTEGER,
    q30 INTEGER,
    q31 INTEGER,
    q32 INTEGER,
    q33 INTEGER,
    q34 INTEGER,
    q35 INTEGER,
    q36 INTEGER,
    q37 INTEGER,
    q38 INTEGER,
    q39 INTEGER,
    q40 INTEGER,
    q41 INTEGER,
    q42 INTEGER,
    q43 INTEGER,
    q44 INTEGER,
    extraversion REAL,
    agreeableness REAL,
    conscientiousness REAL,
    neuroticism REAL,
    openness REAL,
    highest_task_total_rt REAL,
    lowest_task_total_rt REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS task_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id TEXT,
    task_trait TEXT,
    task_order INTEGER,
    shown_word TEXT,
    stem TEXT,
    participant_response TEXT,
    accuracy INTEGER,
    reaction_time REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print('Database initialized successfully.')
