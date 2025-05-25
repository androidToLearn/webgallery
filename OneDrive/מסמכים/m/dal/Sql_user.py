from objects.User import User
from dal.DataBase import DataBase


class SqlUser:
    TABLE_NAME = 'users11'
    COLUMN_NAME = 'name'
    COLUMN_PASSWORD = 'password'

    CREATE_TABLE = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {COLUMN_NAME} TEXT,
        {COLUMN_PASSWORD} TEXT NOT NULL
    )
    """

    def __init__(self):
        database = DataBase()
        cursor = database.doConnection()
        cursor.execute(SqlUser.CREATE_TABLE)
        database.conn.commit()
        database.stopConnection()

    def insertOne(self, user: User):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            INSERT INTO {SqlUser.TABLE_NAME} ({SqlUser.COLUMN_NAME}, {SqlUser.COLUMN_PASSWORD})
            VALUES (%s, %s)
        """
        cursor.execute(query, (user.name, user.password))
        database.conn.commit()
        database.stopConnection()

    def getUserByName(self, name: str):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            SELECT {SqlUser.COLUMN_NAME}, {SqlUser.COLUMN_PASSWORD}
            FROM {SqlUser.TABLE_NAME} WHERE {SqlUser.COLUMN_NAME} = %s
        """
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        database.stopConnection()
        if row:
            return User(name=row[0], password=row[1])
        return None

    def getAllUsers(self):
        users = []
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            SELECT {SqlUser.COLUMN_NAME}, {SqlUser.COLUMN_PASSWORD}
            FROM {SqlUser.TABLE_NAME}
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        database.stopConnection()
        for row in rows:
            users.append(User(name=row[0], password=row[1]))

        return users

    def updateUser(self, user: User):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            UPDATE {SqlUser.TABLE_NAME}
            SET {SqlUser.COLUMN_PASSWORD} = %s
            WHERE {SqlUser.COLUMN_NAME} = %s
        """
        cursor.execute(query, (user.password, user.name))
        database.conn.commit()
        database.stopConnection()

    def deleteUserByName(self, name: str):
        database = DataBase()
        cursor = database.doConnection()
        query = f"""
            DELETE FROM {SqlUser.TABLE_NAME} WHERE {SqlUser.COLUMN_NAME} = %s
        """
        cursor.execute(query, (name,))
        database.conn.commit()
        database.stopConnection()
