import sqlite3
from pathlib import Path

def create_db():
    db_path = Path("..", "..", "resources", "store.db")
    if not db_path.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        db_path.touch()

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS markers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mile_num INTEGER NOT NULL,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                install_time BIGINT NOT NULL,
                last_maint_time BIGINT
            );
        """)

        conn.close()

def main():
    create_db()



if __name__ == "__main__":
    main()