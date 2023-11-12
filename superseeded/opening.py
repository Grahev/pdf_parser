# your_main_class.py

import sqlite3
import os
import pandas as pd
from pdf_data_extractor import PDFDataExtractor, Door
from extractor import extract_data


class Opening:
    def __init__(self, file, phase, status):
        self.phase = phase
        self.status = status
        self.doors = self.extract_pdf_data(file)

    def extract_pdf_data(self, file):
        return extract_data(file)

    
    def save_to_db(self, db_path='database/your_database.db'):
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            # Create a table if it doesn't exist
            c.execute('''
                    CREATE TABLE IF NOT EXISTS doors (
                        job_no TEXT,
                        door_no TEXT,
                        qty INTEGER,
                        revision TEXT,
                        customer TEXT,
                        door_type TEXT,
                        door_infill TEXT,
                        fire_rating TEXT,
                        certfire_compilant TEXT,
                        ce_compilant TEXT,
                        finish TEXT,
                        frame TEXT,
                        leaf TEXT,
                        height_so INTEGER,
                        height_oa_frame INTEGER,
                        height_leaf INTEGER,
                        width_so INTEGER,
                        width_oa_frame INTEGER,
                        width_leaf INTEGER,
                        phase TEXT,
                        status TEXT
                    )
            ''')
            # Insert data for each door instance
            for door_data in self.doors:
                print(door_data)
                if isinstance(door_data, dict):
                    # If the item is a dictionary, use it directly
                    job_info = door_data.get('job_info', {})
                    general_info = door_data.get('general_info', {})
                    structural_opening = door_data.get('structural_opening', {})
                elif isinstance(door_data, Door):
                    # If the item is an instance of Door class, access attributes directly
                    job_info = door_data.job_info
                    general_info = door_data.general_info
                    structural_opening = door_data.structural_opening
                else:
                    print(f"Unsupported data type: {type(door_data)}")
                    continue
                h = structural_opening['height']
                w = structural_opening['width']

                c.execute('''
    INSERT INTO doors VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_info.get('job_no', None),
                job_info.get('door_no', None),
                job_info.get('qty', None),
                job_info.get('revision', None),
                job_info.get('customer', None),
                general_info.get('Door Type', None),
                general_info.get('Door Infill', None),
                general_info.get('Fire Rating', None),
                general_info.get('Certfire Compilant', None),
                general_info.get('CE Compliant', None),
                general_info.get('Finish', None),
                general_info.get('Frame', None),
                general_info.get('Leaf', None),
                h.get('so', None), #height so
                h.get('oa_frame', None),
                h.get('leaf', None),
                w.get('so', None),
                w.get('oa_frame', None),
                w.get('leaf', None)[0], #TODO parse only one leaf 
                self.phase,
                self.status
            ))

                
            # Commit and close the connection
            conn.commit()
            conn.close()

    def fetch_by_job_no(self, job_no, db_path='database/your_database.db'):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''
            SELECT * FROM doors
            WHERE job_no = ?
        ''', (job_no,))

        result = c.fetchall()

        # Close the connection
        conn.close()

        return result

    def fetch_by_customer(self, customer, db_path='database/your_database.db'):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''
            SELECT * FROM doors
            WHERE customer = ?
        ''', (customer,))

        result = c.fetchall()

        # Close the connection
        conn.close()

        return result

    def export_to_excel(self, job_no, excel_file='exports/exported_data.xlsx', db_path='database/your_database.db'):
        # Fetch data from the database
        if job_no:
            result = self.fetch_by_job_no(job_no, db_path)
        elif customer:
            result = self.fetch_by_customer(customer, db_path)
        else:
            print("Specify either job_no or customer for export.")
            return

        # Convert the data to a DataFrame
        columns = [
            'job_no', 'door_no', 'qty', 'revision', 'customer',
            'door_type', 'door_infill', 'fire_rating', 'certfire_compilant',
            'ce_compilant', 'finish', 'frame', 'leaf',
            'height_so', 'height_oa_frame', 'height_leaf',
            'width_so', 'width_oa_frame', 'width_leaf',
            'phase', 'status'
        ]

        df = pd.DataFrame(result, columns=columns)

        # Export to Excel
        df.to_excel(excel_file, index=False)
