import psycopg
from dotenv import load_dotenv
import os
load_dotenv()


class DataBase:

    def __init__(self):
        self.cursor = None
        self.conn = None

    def doConnection(self):

        self.conn = psycopg.connect(dbname = os.getenv('DATABASE_NAME') ,user = os.getenv('DATABASE_USER') ,password = os.getenv('DATABASE_PASSWORD') ,host = os.getenv('DATABASE_HOST') ,port = os.getenv('DATABASE_PORT'))
        self.cursor = self.conn.cursor()
        return self.cursor

    def stopConnection(self):
        self.cursor.close()
        self.conn.close()
