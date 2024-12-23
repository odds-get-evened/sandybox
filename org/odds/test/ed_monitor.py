import hashlib
import inspect
import json
import os.path
import re
import sqlite3
from pathlib import Path

DB_PATH = Path(os.path.expanduser('~'), '.databox', '')


class EDDBTables:
    TBL_SCANS = 'scans'
    TBL_SYSTEMS = 'systems'
    TBL_MATERIALS = 'materials'
    TBL_SCANS_MATERIALS = 'scans_materials'

    def __init__(self, p: Path):
        self.db_path = p
        self.conn = None
        self.cursor = None

        self.create_db()

    def create_db(self):
        if not self.table_exists('scans'):
            pass

    def table_exists(self, tbl_name: str):
        return False

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

    def query(self, sql: str, params=None):
        """
        execute an SQL query with optional parameters
        Parameters
        ----------
        sql
        params

        Returns
        -------
        query results or None
        """
        if self.conn is None:
            raise Exception('database connection failed')
        params = params or ()
        self.cursor.execute(sql.strip(), params)

        return self.cursor.fetchall()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def __enter__(self):
        self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class EventTypes:
    SAA_SIGNALS_FOUND = 'SAASignalsFound'
    SCAN = 'Scan'
    SCAN_ORGANIC = 'ScanOrganic'


class ScanFields:
    SYS_ADDR = 'SystemAddress'
    STAR_SYS = 'StarSystem'
    BODY_ID = 'BodyID'
    DIST_FROM_ARRIVAL = 'DistanceFromArrivalLS'
    TIDAL_LOCK = 'TidalLock'
    TERRAFORM_STATE = 'TerraformState'
    PLANET_CLASS = 'PlanetClass'


# loops thru all of the EventTypes class constants, and adds them to required fields
REQ_EVENT_TYPES = [v for k, v in inspect.getmembers(EventTypes) if k.isupper() and not callable(v)]


class PersistentStorage:
    def __init__(self, p: Path):
        self.path = p


class StellarEx:
    def __init__(self):
        self.previous_event = None
        self.current_events = None
        self.home_dir = None
        self.events = []

    def boot(self):
        self.home_dir = os.path.expanduser('~')
        if os.name == 'nt':
            self.boot_win()

    def get_youngest_journal(self):
        saved_path = [
            os.path.join(self.home_dir, i)
            for i in os.listdir(self.home_dir)
            if i == 'Saved Games'
        ][0]
        journal_path = Path(saved_path, 'Frontier Developments', 'Elite Dangerous')

        logs_pattern = re.compile(r"Journal\..*\.log$")
        youngest_journal = max([x for x in journal_path.iterdir() if logs_pattern.search(x.name)])

        return youngest_journal

    def boot_win(self):
        self.handler()
        youngest_journal = self.get_youngest_journal()

        print(f"using the journal {youngest_journal.name}")
        with open(youngest_journal, 'r') as f:
            for x in f.readlines():
                j = json.loads(x.strip())
                if j['event'] in REQ_EVENT_TYPES:
                    self.events.append(j)

    def handler(self):
        saved_path = [
            os.path.join(self.home_dir, i)
            for i in os.listdir(self.home_dir)
            if i == 'Saved Games'
        ][0]
        journals_path = Path(saved_path, 'Frontier Developments', 'Elite Dangerous')

        logs_pattern = re.compile(r"Journal\..*\.log$")
        logs = [log for log in journals_path.iterdir() if logs_pattern.search(log.name)]

        for log in logs:
            with open(log, 'r', encoding='utf8') as f:
                events = [json.loads(x) for x in f.readlines()]
                scans_events = [x for x in events if x['event'] == EventTypes.SCAN and x['ScanType'] == 'Detailed']
            [self.store_scan(x) for x in scans_events]

    def store_scan(self, scan):
        scan_str = json.dumps(scan)
        scan_hash = hashlib.sha256(scan_str.encode())
        print(json.dumps(scan, indent=4))


    def start(self):
        self.boot()


def main():
    app = StellarEx()
    app.start()


if __name__ == "__main__":
    main()
