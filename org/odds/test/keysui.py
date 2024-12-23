import hashlib
import os.path
import sqlite3
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from sqlite3 import Connection
from tkinter import ttk

DB_PATH = Path(os.path.expanduser('~'), '.databox', 'keysui', 'storage.db')


class DBSetup:
    def __init__(self, p: Path):
        self.db_path = p
        self.conn = sqlite3.connect(self.db_path, timeout=10.0)
        self.cursor = self.conn.cursor()

        self.process_db()

    def process_db(self):
        self.setup_key_table()

    def setup_key_table(self):
        req = self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sig TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL
            )
        """)
        self.conn.commit()

        self.verify_key_table()

    def verify_key_table(self):
        self.cursor.execute("""
            INSERT INTO keys (sig, content)
            VALUES (?, ?)
        """, [
            hashlib.sha256('gensis'.encode()).hexdigest(),
            'genesis'
        ])

        a = self.cursor.execute("""
            SELECT * FROM keys
        """)
        print(a.fetchone().__str__())

        self.cursor.execute("""
            DELETE FROM keys
        """)


class SqliteDB:
    def __init__(self, db_path: Path, num_threads=3):
        self.db_path = db_path
        self.conn: Connection = sqlite3.connect(self.db_path)
        self.exec = ThreadPoolExecutor(num_threads)

    def _query(self, q: str, params=()):
        curs = self.conn.cursor()

        res = curs.execute(q, params)

        curs.close()

        if res.rowcount > 1:
            return res.fetchall()
        elif res.rowcount == 1:
            return res.fetchone()
        else:
            return None

    def query(self, q: str, params=()):
        f = self.exec.submit(self._query(q, params=params))
        print(f.result())

    def close(self):
        self.exec.shutdown(wait=True)
        self.conn.close()


class KeyManager(ttk.Frame):
    COL_IDENT = {'name': 'ident', 'label': 'Name'}
    COL_EMAIL = {'name': 'email', 'label': 'Email'}
    COL_SIG = {'name': 'sig', 'label': 'Fingerprint'}
    COL_CREATED = {'name': 'made', 'label': 'Created'}
    COL_EXPIRES = {'name': 'exp', 'label': 'Expires'}

    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.db = kwargs['db']

        '''
        control_bar >
            btn_gen_key
            btn_encrypt
            btn_decrpyt
        tree_box >
            tree_keys
        '''

        self.control_bar = ttk.Frame(self)
        self.control_bar.grid(row=0, column=0, sticky='ew')

        self.btn_gen_key = ttk.Button(self.control_bar, text='generate key')
        self.btn_gen_key.grid(row=0, column=0)

        self.btn_encrypt = ttk.Button(self.control_bar, text='encrypt...')
        self.btn_encrypt.grid(row=0, column=1)

        self.tree_box = ttk.Frame(self)
        self.tree_box.grid(row=1, column=0, sticky='nesw', pady=5)

        self.tree_keys = ttk.Treeview(
            self.tree_box,
            show='headings',
            selectmode='browse',
            columns=('ident', 'sig', 'made', 'exp')
        )
        self.tree_keys.heading(self.COL_IDENT['name'], text=self.COL_IDENT['label'])
        self.tree_keys.heading(self.COL_SIG['name'], text=self.COL_SIG['label'])
        self.tree_keys.heading('made', text='Created')
        self.tree_keys.heading('exp', text='Expires')

        key_scroll = ttk.Scrollbar(self.tree_box, orient=tk.VERTICAL, command=self.tree_keys.yview)
        self.tree_keys.configure(yscrollcommand=key_scroll.set)
        self.tree_keys.grid(row=0, column=0, sticky='nesw')

        self.load_keys()

    def load_keys(self):
        pass


class Keysui(tk.Tk):
    def __init__(self, db: SqliteDB = None):
        super().__init__()
        self.title('keysui')
        self.w = 640
        self.h = 480
        self.x_pos = int((self.winfo_screenwidth() / 2) - (self.w / 2))
        self.y_pos = int((self.winfo_screenheight() / 2) - (self.h / 2))
        self.minsize(self.w, self.h)
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        self.geometry(f"{self.w}x{self.h}+{self.x_pos}+{self.y_pos}")

        self.db = db

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nesw')

        self.key_manager = KeyManager(self.main_frame, db=self.db)
        self.key_manager.grid(row=0, column=0, sticky='nesw')

    def on_close(self):
        self.destroy()

    def start(self):
        try:
            self.mainloop()
        except KeyboardInterrupt:
            self.destroy()


def main():
    DBSetup(DB_PATH)
    db = SqliteDB(DB_PATH)
    app = Keysui(db=db)
    app.start()
    db.close()


if __name__ == "__main__":
    main()
