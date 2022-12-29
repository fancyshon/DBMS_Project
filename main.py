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
    rows = cursor.fetchall()

    cursor.close()
    conn.commit()

    return rows

##################################


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.execute_query)
        self.ui.comboBox.addItems(
            ["QUERY", "SELECT-FROM-WHERE", "DELETE", "INSERT", "UPDATE", "IN", "NOT IN", "EXISTS", "NOT EXISTS", "COUNT", "SUM", "MAX", "MIN", "AVG", "HAVING"])
        # self.ui.comboBox.currentText()

    def execute_query(self):
        # print(self.ui.textEdit.toPlainText())
        query = ""

        if self.ui.comboBox.currentText() == "QUERY":
            query = self.ui.textEdit.toPlainText()
        elif self.ui.comboBox.currentText() == "SELECT-FROM-WHERE":
            query = """SELECT * FROM "Actor" WHERE "Award(s) in 2022" = "None";"""
        elif self.ui.comboBox.currentText() == "DELETE":
            query = """DELETE FROM "Movie" WHERE "id" = 14 ;"""
        elif self.ui.comboBox.currentText() == "INSERT":
            query = """INSERT INTO "Movie" ("id", "Name" ,"Date", "Box office (US$)", "Genre", "DirectorID", "Distributed by") VALUES (14, "雷神索爾4", "2022-07-06", 7600000000, "動作", 14, "索尼影業");"""
        elif self.ui.comboBox.currentText() == "UPDATE":
            query = """UPDATE "Movie" SET "Box office (US$)" = 7610000000 WHERE "id" = 14 ;"""
        if self.ui.comboBox.currentText() == "IN":
            query = """SELECT * FROM "Movie" WHERE "Distributed by" IN ("索尼影業", "環球影業");"""
        elif self.ui.comboBox.currentText() == "NOT IN":
            query = """
                    SELECT * FROM "Movie" WHERE "id" NOT IN(
                        SELECT "MovieID" FROM "MovieTheater" WHERE EXISTS
                            (SELECT * FROM "Theater" WHERE "Theater"."id" = "MovieTheater"."TheaterID" AND "Theater"."Name" = "新光影城"))
                    """
        elif self.ui.comboBox.currentText() == "EXISTS":
            query = """
                    SELECT * FROM "Actor" WHERE "id" IN
                        (SELECT "ActorID" FROM "ActorMovie" WHERE EXISTS
                            (SELECT * FROM "Movie" WHERE "Movie"."id" = "ActorMovie"."MovieID" AND "Movie"."Name" = "紅色通緝令"))
                    """
        elif self.ui.comboBox.currentText() == "NOT EXISTS":
            query = """SELECT * FROM "Actor" WHERE "id" IN
                        (SELECT "ActorID" FROM "ActorMovie" WHERE NOT EXISTS
                            (SELECT * FROM "Movie" WHERE "Movie"."id" = "ActorMovie"."MovieID" AND "Movie"."Date" > "2022-01-01" ));
                    """
        elif self.ui.comboBox.currentText() == "COUNT":
            query = """SELECT COUNT("id") FROM "Movie" WHERE "Genre" = "動作";"""
        elif self.ui.comboBox.currentText() == "SUM":
            query = """SELECT Genre, SUM("Box office (US$)") FROM "Movie" WHERE Genre = "喜劇";"""
        elif self.ui.comboBox.currentText() == "MAX":
            query = """SELECT "Name", MAX("Revenue (US$)") FROM "Studio" ;"""
        elif self.ui.comboBox.currentText() == "MIN":
            query = """SELECT "Name", MIN("Box office (US$)") FROM "Movie";"""
        elif self.ui.comboBox.currentText() == "AVG":
            query = """SELECT Genre, AVG("Box office (US$)")  FROM "Movie" GROUP BY "Genre";"""
        elif self.ui.comboBox.currentText() == "HAVING":
            query = """
                    SELECT * FROM "Studio" WHERE "Name" IN
                        (SELECT "Distributed by" FROM "Movie" GROUP BY "Distributed by" HAVING COUNT(id) > 2);
                    """

        result = SQL_query(query, "MovieManagement.db")
        result_str = ""

        result_str += "Exrcuted query : {}\n\n".format(query)

        for row in result:
            for x in row:
                result_str += "{:15}".format(str(x))
            result_str += '\n'

        self.ui.textBrowser.setText(result_str)
        self.ui.textEdit.clear()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

    # db = "MovieManagement.db"
    # Can't use space in the colume name.
    # Not found => length = 0
