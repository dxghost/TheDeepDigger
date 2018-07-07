import sqlite3


class CreatSQL:
    def __init__(self):
        self.connect()
        self.make_coursor()
        self.make_tables()
        self.commit_changes()
        self.close_connection()

    def connect(self):
        self.connection = sqlite3.connect('films_info.db')

    def make_coursor(self):
        self.cursor = self.connection.cursor()

    def make_tables(self):
        # Create tables
        self.cursor.execute(
            '''CREATE  TABLE IF NOT EXISTS Casts(ID INTEGER UNIQUE PRIMARY KEY , Cast TEXT UNIQUE)''')
        self.cursor.execute(
            '''CREATE  TABLE IF NOT EXISTS Genres(ID INTEGER UNIQUE PRIMARY KEY , Genre TEXT UNIQUE)''')
        self.cursor.execute(
            '''CREATE  TABLE IF NOT EXISTS Countries(ID INTEGER UNIQUE PRIMARY KEY , Country TEXT UNIQUE)''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Films(ID INTEGER UNIQUE PRIMARY KEY,Film_Name TEXT,Casts_ID TEXT,Abstract TEXT,Genres_ID TEXT,Keywords TEXT,Countries_ID TEXT,Language TEXT,Realese_Date TEXT,Url TEXT,ImageURL TEXT,FOREIGN KEY (Casts_ID) REFERENCES Casts(ID),FOREIGN KEY (Genres_ID) REFERENCES Genres(ID),FOREIGN KEY (Countries_ID) REFERENCES Countries(ID))''')

    def commit_changes(self):
        # Save (commit) the changes
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    CreatSQL()