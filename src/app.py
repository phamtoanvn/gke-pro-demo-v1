import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_NAME = os.environ.get("DB_NAME", "postgres")

DB_HOST = "127.0.0.1" 

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        # Nếu kết nối thành công, lấy phiên bản Database
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        
        status = "Thanh cong! Web da ket noi Cloud SQL."
        version = db_version[0]
    else:
        status = "Loi ket noi Database (Kiem tra lai Secret/Proxy)"
        version = "N/A"

    return jsonify({
        "status": status, 
        "project": "Do An GKE Pro - Nhom 21",
        "database_version": version
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)