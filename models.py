import sqlite3

class DoorData:
    def __init__(self, customer, job_no, door_no, qty, revision):
        self.customer = customer
        self.job_no = job_no
        self.door_no = door_no
        # self.phase = phase 
        self.qty = qty
        self.revision = revision
        self.door_details = {}
        self.order_details = {}

    @classmethod
    def from_dict(cls, data):
        door_instance = cls(
            data.get('customer', ''),
            data.get('job_no', ''),
            data.get('door_no', ''),
            data.get('qty', ''),
            data.get('revision', '')
        )

        door_instance.add_door_details(
            data.get('Door Type', ''),
            data.get('Door Infill', ''),
            data.get('Fire Rating', ''),
            data.get('Certifire Compliant', ''),
            data.get('CE Compliant', ''),
            data.get('Finish', ''),
            data.get('Frame', ''),
            str(data.get('Leaf', '')),
            data.get('T', '')
        )

        door_instance.add_order_details(
            data.get('so', ''),
            data.get('oa_frame', ''),
            data.get('leaf', [])
        )

        return door_instance

    def add_door_details(self, door_type, door_infill, fire_rating, certifire_compliant, ce_compliant, finish, frame, leaf, t):
        self.door_details = {
            'Door Type': door_type,
            'Door Infill': door_infill,
            'Fire Rating': fire_rating,
            'Certifire Compliant': certifire_compliant,
            'CE Compliant': ce_compliant,
            'Finish': finish,
            'Frame': frame,
            'Leaf': leaf,
            'T': t
        }

    def add_order_details(self, so, oa_frame, leaf):
        self.order_details = {
            'so': so,
            'oa_frame': oa_frame,
            'leaf': leaf
        }

    def save_to_database(self, database_name='doors.db'):
        # Connect to the SQLite database
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT,
                job_no TEXT,
                door_no TEXT,
                qty TEXT,
                revision TEXT,
                door_type TEXT,
                door_infill TEXT,
                fire_rating TEXT,
                certifire_compliant TEXT,
                ce_compliant TEXT,
                finish TEXT,
                frame TEXT,
                leaf TEXT,
                t TEXT,
                so TEXT,
                oa_frame TEXT,
                leaf_detail TEXT
            )
        ''')

        # Insert data into the 'doors' table
        cursor.execute('''
            INSERT INTO doors (
                customer, job_no, door_no, qty, revision,
                door_type, door_infill, fire_rating, certifire_compliant,
                ce_compliant, finish, frame, leaf, t, so, oa_frame, leaf_detail
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.customer, self.job_no, self.door_no, self.qty, self.revision,
            self.door_details.get('Door Type', ''),
            self.door_details.get('Door Infill', ''),
            self.door_details.get('Fire Rating', ''),
            self.door_details.get('Certifire Compliant', ''),
            self.door_details.get('CE Compliant', ''),
            self.door_details.get('Finish', ''),
            self.door_details.get('Frame', ''),
            str(self.door_details.get('Leaf', '')),
            self.door_details.get('T', ''),
            self.order_details.get('so', ''),
            self.order_details.get('oa_frame', ''),
            str(self.order_details.get('leaf', '')[0])
        ))

        # Commit changes and close the connection
        conn.commit()
        conn.close()