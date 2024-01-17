import sqlite3

def addData(data, cursor):
    cursor.executemany('INSERT INTO data (name, age) VALUES (?, ?)', data)

def getTableInfo(conn,cursor, tableName):
    cursor.execute("PRAGMA table_info(" + tableName + ")")
    columns = cursor.fetchall()
    conn.commit()

    return columns

def getData(conn,cursor, tableName):
    cursor.execute('''SELECT * FROM ''' + tableName)
    data = cursor.fetchall()
    conn.commit()

    return data

def deleteData(conn,cursor,id,tableName):
    cursor.execute('''DELETE FROM '''+tableName+''' WHERE id=?''', (id,))
    conn.commit()

def updateData(conn, cursor,id, data):
    cursor.execute('''UPDATE data SET name=?, age=? WHERE id=?''', (data, id))
    conn.commit()

def createTable(conn, cursor,tableName, keys):
    command = '''CREATE TABLE if not exists "''' + tableName + '''" (''' + keys + ''')'''
    cursor.execute(command)
    conn.commit()

def main():
    path = "Data/EsportData/data.db"
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    createTable(conn, cursor, "data", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER")
    addData([("John", 25), ("Jane", 30)], cursor)
    print(getTableInfo(conn, cursor, "data"))
    print(getData(conn, cursor, "data"))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()