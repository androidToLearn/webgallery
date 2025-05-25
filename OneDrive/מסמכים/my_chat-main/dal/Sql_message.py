from objects.Message import Message
from dal.DataBase import DataBase


class Sql_message:
    COLUMN_ID = 'id'
    COLUMN_MESSAGE = 'm'
    COLUMN_FROM = 'f'
    COLUMN_TO = 't'
    COLUMN_FILENAME = 'file'
    COLUMN_ISFROM_GET = 'isFrom_get'
    COLUMN_ISTO_GET = 'isTo_get'
    TABLE_NAME = 'messages1'

    CREATE_TABLE = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {COLUMN_ID} SERIAL PRIMARY KEY,
        {COLUMN_MESSAGE} TEXT,
        {COLUMN_FROM} TEXT,
        {COLUMN_TO} TEXT,
        {COLUMN_FILENAME} TEXT,
        {COLUMN_ISFROM_GET} BOOLEAN,
        {COLUMN_ISTO_GET} BOOLEAN
    )
    """

    def __init__(self):
        database = DataBase()
        cursor = database.doConnection()
        cursor.execute(Sql_message.CREATE_TABLE)
        database.conn.commit()
        database.stopConnection()

    def insertOne(self, message: Message):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            INSERT INTO {Sql_message.TABLE_NAME}
            ({Sql_message.COLUMN_MESSAGE}, {Sql_message.COLUMN_FROM}, {Sql_message.COLUMN_TO}, {
            Sql_message.COLUMN_FILENAME}, {Sql_message.COLUMN_ISFROM_GET}, {Sql_message.COLUMN_ISTO_GET})
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING {Sql_message.COLUMN_ID}
        """
        cursor.execute(query, (message.message, message.sendFrom, message.sendTo,
                       message.filename, message.isFrom_get, message.isTo_get))
        message.id = cursor.fetchone()[0]
        database.conn.commit()
        database.stopConnection()

    def getAllMessages(self):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            SELECT * FROM {Sql_message.TABLE_NAME}
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        database.stopConnection()
        messages = []
        for row in rows:
            msg = Message(
                message=row[1],
                sendTo=row[3],
                sendFrom=row[2],
                id=row[0],
                filename=row[4],
                isFrom_get=row[5],
                isTo_get=row[6]
            )
            messages.append(msg)
        return messages

    def getAllByNameChatWith(self, nameSendFrom: str, nameSendTo: str):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            SELECT * FROM {Sql_message.TABLE_NAME}
            WHERE ({Sql_message.COLUMN_FROM} = '{nameSendFrom}' AND {Sql_message.COLUMN_TO} = '{nameSendTo}') or ({Sql_message.COLUMN_FROM} = '{nameSendTo}' and {Sql_message.COLUMN_TO} = '{nameSendFrom}')
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        database.stopConnection()
        messages = []
        for row in rows:
            msg = Message(
                message=row[1],
                sendTo=row[3],
                sendFrom=row[2],
                id=row[0],
                filename=row[4],
                isFrom_get=row[5],
                isTo_get=row[6]
            )
            messages.append(msg)
        return messages

    def delete_message(self, id: int):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            DELETE FROM {Sql_message.TABLE_NAME} WHERE {Sql_message.COLUMN_ID} = %s
        """
        cursor.execute(query, (id,))
        database.conn.commit()
        database.stopConnection()

    def update_message(self, message: Message):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            UPDATE {Sql_message.TABLE_NAME}
            SET {Sql_message.COLUMN_MESSAGE} = %s,
                {Sql_message.COLUMN_FROM} = %s,
                {Sql_message.COLUMN_TO} = %s,
                {Sql_message.COLUMN_FILENAME} = %s,
                {Sql_message.COLUMN_ISFROM_GET} = %s,
                {Sql_message.COLUMN_ISTO_GET} = %s
            WHERE {Sql_message.COLUMN_ID} = %s
        """
        cursor.execute(query, (message.message, message.sendFrom, message.sendTo,
                       message.filename, message.isFrom_get, message.isTo_get, message.id))
        database.conn.commit()
        database.stopConnection()

    def deleteAll(self):
        database = DataBase()
        cursor = database.doConnection()
        cursor.execute(f'DROP TABLE IF EXISTS {Sql_message.TABLE_NAME}')
        cursor.execute(Sql_message.CREATE_TABLE)
        database.conn.commit()
        database.stopConnection()
