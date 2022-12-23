import sqlite3
import sys
from MainWindow import *

def initialization():
    conn = sqlite3.connect("MovieManagement.db")
    print('Connect to database')
    conn.close()

def SQL_query(query, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute(query)
    row = cursor.fetchall()

    cursor.close()
    conn.commit()

    return row

##################################

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
		# in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.execute_query)

    def execute_query(self):
        print(self.ui.textEdit.toPlainText())
        SQL_query(self.ui.textEdit.toPlainText(), "MovieManagement.db")



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
    # db = "MovieManagement.db"
    # SQL_query("""CREATE TABLE Movie (
    #                 ID INT PRIMARY KEY ,
    #                 Name TEXT,
    #                 Genre TEXT,
    #                 Box_office INT);""", db)
    
    # Can't use space in the colume name.
    # Not found => length = 0
    # print(SQL_query("""INSERT INTO Movie (ID, Name, Genre, Box_office) VALUES (3, "It", "Scary", 9099); """, db))