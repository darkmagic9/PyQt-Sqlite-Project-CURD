from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys,sqlite3,time,pymysql
import datetime
import os

class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Register")

        self.setWindowTitle("Add Operator")
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        self.QBtn.clicked.connect(self.addoperator)

        layout = QVBoxLayout()

        self.codeinput = QLineEdit()
        self.codeinput.setPlaceholderText("Code")
        self.codeinput.setInputMask('99999')
        layout.addWidget(self.codeinput)

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Name")
        layout.addWidget(self.nameinput)

        self.validatorinput = QComboBox()
        self.validatorinput.addItem("N")
        self.validatorinput.addItem("Y")
        layout.addWidget(self.validatorinput)

        # self.validatorinput = QComboBox()
        # self.validatorinput.addItem("Mechanical")
        # self.validatorinput.addItem("Civil")
        # self.validatorinput.addItem("Electrical")
        # self.validatorinput.addItem("Electronics and Communication")
        # self.validatorinput.addItem("Computer Science")
        # self.validatorinput.addItem("Information Technology")
        # layout.addWidget(self.validatorinput)

        # self.seminput = QComboBox()
        # self.seminput.addItem("1")
        # self.seminput.addItem("2")
        # self.seminput.addItem("3")
        # self.seminput.addItem("4")
        # self.seminput.addItem("5")
        # self.seminput.addItem("6")
        # self.seminput.addItem("7")
        # self.seminput.addItem("8")
        # layout.addWidget(self.seminput)

        # self.addressinput = QLineEdit()
        # self.addressinput.setPlaceholderText("Address")
        # layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addoperator(self):

        name = ""
        validator = ""
        date = str(datetime.datetime.now().strftime("%Y%m%d"))
        code = -1
        time = str(datetime.datetime.now().strftime("%H%M%S"))
        user = "pydemo"
        userid = "11"

        name = self.nameinput.text()
        validator = self.validatorinput.itemText(self.validatorinput.currentIndex())
        code = self.codeinput.text()
        try:
            self.conn = pymysql.connect(host='128.100.117.99', user='root', passwd='namiki', database='lvp-svp')
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO operator (create_date,create_time,create_userfullname,create_userid,update_date,update_time,update_userfullname,update_userid,emp_id,emp_name,is_validator) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(date,time,user,userid,date,time,user,userid,code,name,validator))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Operator is added successfully to the database.')
            self.close()
            
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add operator to the database.')

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Search")

        self.setWindowTitle("Search user")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchoperator)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("emp_id No.")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchoperator(self):

        searchrol = ""
        searchrol = self.searchinput.text()
        try:
            self.conn = pymysql.connect(host='128.100.117.99', user='root', passwd='namiki', database='lvp-svp')
            self.c = self.conn.cursor()
            self.c.execute("SELECT * from operator WHERE emp_id="+str(searchrol))
            row = self.c.fetchone()
            serachresult = "emp_id : "+str(row[9])+'\n'+"Name : "+str(row[10])+'\n'+"validator : "+str(row[11])
            QMessageBox.information(QMessageBox(), 'Successful', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not Find operator from the database.')

class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete Operator")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deleteoperator)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("emp_id No.")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteoperator(self):

        delrol = ""
        delrol = self.deleteinput.text()
        try:
            self.conn = pymysql.connect(host='128.100.117.99', user='root', passwd='namiki', database='lvp-svp')
            self.c = self.conn.cursor()
            self.c.execute("DELETE from operator WHERE emp_id="+str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Deleted From Table Successful')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not Delete operator from the database.')

class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(120)

        layout = QVBoxLayout()

        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Enter Password.")
        self.QBtn = QPushButton()
        self.QBtn.setText("Login")
        self.setWindowTitle('Login')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Login")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        if(self.passinput.text() == "123456"):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Wrong Password')





class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("STDMGMT")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap('icon/logo.png')
        pixmap = pixmap.scaledToWidth(275)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(150)

        layout.addWidget(title)

        layout.addWidget(QLabel("Version 5.3.2"))
        layout.addWidget(QLabel("Copyright 2018 CYB Inc."))
        layout.addWidget(labelpic)


        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # self.conn = pymysql.connect(host='128.100.117.99', user='root', passwd='namiki', database='lvp-svp')
        # self.c = self.conn.cursor()
        # self.c.execute("CREATE TABLE IF NOT EXISTS operator(emp_id INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,validator TEXT,sem INTEGER,code INTEGER,address TEXT)")
        # self.c.close()

        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")
        self.setWindowTitle("Operator Management CRUD")

        self.setMinimumSize(800, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("id", 
                                                    "create_date", 
                                                    "create_time", 
                                                    "create_userfullname", 
                                                    "create_userid",
                                                    "update_date",
                                                    "update_time",
                                                    "update_userfullname",
                                                    "update_userid",
                                                    "emp_id",
                                                    "emp_name",
                                                    "is_validator",
                                                    "remark"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Add Operator", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Operator")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"),"Refresh",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Search", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        adduser_action = QAction(QIcon("icon/add.png"),"Insert Operator", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Search Operator", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Delete", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)


        about_action = QAction(QIcon("icon/info.png"),"Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def loaddata(self):
        self.connection = pymysql.connect(host='128.100.117.99', user='root', passwd='namiki', database='lvp-svp')
        self.cur = self.connection.cursor()
        query = "SELECT * FROM operator"
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.cur.close()
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()


app = QApplication(sys.argv)
passdlg = LoginDialog()
if(passdlg.exec_() == QDialog.Accepted):
    window = MainWindow()
    window.show()
    window.loaddata()
sys.exit(app.exec_())