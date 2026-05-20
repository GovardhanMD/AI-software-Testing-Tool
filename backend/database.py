import sqlite3
import json
from datetime import datetime

DB_PATH = 'test_results.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS test_runs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  timestamp TEXT,
                  total_tests INTEGER,
                  passed INTEGER,
                  failed INTEGER,
                  test_cases TEXT)''')
    conn.commit()
    conn.close()

def save_test_run(filename, total, passed, failed, test_cases):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO test_runs (filename, timestamp, total_tests, passed, failed, test_cases)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (filename, datetime.now().isoformat(), total, passed, failed, json.dumps(test_cases)))
    conn.commit()
    run_id = c.lastrowid
    conn.close()
    return run_id

def get_all_runs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM test_runs ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [{'id': r[0], 'filename': r[1], 'timestamp': r[2], 
             'total_tests': r[3], 'passed': r[4], 'failed': r[5],
             'test_cases': json.loads(r[6])} for r in rows]

def get_run_by_id(run_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM test_runs WHERE id = ?', (run_id,))
    r = c.fetchone()
    conn.close()
    if r:
        return {'id': r[0], 'filename': r[1], 'timestamp': r[2],
                'total_tests': r[3], 'passed': r[4], 'failed': r[5],
                'test_cases': json.loads(r[6])}
    return None
