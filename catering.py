import sys, re, random, barcode, datetime, os, shutil, subprocess, keyboard
from collections import Counter
from math import sqrt
from barcode.writer import ImageWriter 
from PyQt5.QtCore import Qt, QSize, QRegExp, QAbstractTableModel
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie, QRegExpValidator, QColor,\
           QImage, QPainter
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QDialog, QLabel, QPushButton,\
        QMessageBox, QSpinBox, QComboBox, QTextEdit, QApplication, QWidget,\
        QVBoxLayout, QTableView, QStyledItemDelegate, QCheckBox, QPlainTextEdit
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, create_engine,\
                     Float, select, update,insert, delete, func, and_, ForeignKey

def refresh(self, seatText):
    self.close()
    routeSeats = 0
    seatsArrange(self, routeSeats, seatText)

def alertText(message):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message)
    msg.setWindowTitle('Warning message')
    msg.exec_() 
    
def actionOK(message):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle('Information message')
    msg.exec_()
           
def windowClose(self):
    self.close()
    sys.exit()
    
def reprintForms(path):
    filelist = []
    for file in os.listdir(path):
        if file[-4:] == '.txt':
            filelist.append(file)
    class combo(QDialog):
        def __init__(self, parent=None):
              super(combo, self).__init__(parent)
              self.setWindowTitle("Reprinting forms")
              self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
              self.setFont(QFont("Arial", 10))
              self.setStyleSheet("background-color: #D9E1DF") 
                  
              grid = QGridLayout()
              grid.setSpacing(20)
              
              pyqt = QLabel()
              movie = QMovie('./logos/pyqt.gif')
              pyqt.setMovie(movie)
              movie.setScaledSize(QSize(240,80))
              movie.start()
              grid.addWidget(pyqt, 0 ,0, 1, 2)
            
              logo = QLabel()
              pixmap = QPixmap('./logos/logo.jpg')
              logo.setPixmap(pixmap)
              grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
              
              self.cb = QComboBox()
              self.cb.setFixedWidth(400)
              self.cb.setFont(QFont("Arial",12))
              self.cb.setStyleSheet("color: black;  background-color: #F8F7EE")
              for item in range(len(filelist)):
                  self.cb.addItem(filelist[item])
                  self.cb.model().sort(0)
              grid.addWidget(self.cb, 1, 0, 1, 3, Qt.AlignRight)
                         
              def cbChanged():
                  self.cb.setCurrentText(self.cb.currentText())
              self.cb.currentTextChanged.connect(cbChanged)
               
              self.q2Edit = QLineEdit('1')
              self.q2Edit.setStyleSheet("background: #F8F7EE")
              self.q2Edit.setFixedWidth(40)
              self.q2Edit.setFont(QFont("Arial",12))
              reg_ex = QRegExp("^[0-9]{1,2}$")
              input_validator = QRegExpValidator(reg_ex, self.q2Edit)
              self.q2Edit.setValidator(input_validator)
              
              def q2Changed():
                  self.q2Edit.setText(self.q2Edit.text())
              self.q2Edit.textChanged.connect(q2Changed) 
              
              def printForm():
                  filename = self.cb.currentText()
                  copies = int(self.q2Edit.text())
                  for x in range(0, copies):
                      if sys.platform == 'win32':
                          os.startfile(path+filename, "print")
                      else:
                          os.system("lpr "+path+filename)
                  message = 'Printing'
                  actionOK(message)
                  
              grid.addWidget(QLabel('Copies'), 2, 2, 1, 1, Qt.AlignTop | Qt.AlignRight)
              grid.addWidget(self.q2Edit, 2, 2, 1, 1, Qt.AlignBottom | Qt.AlignRight)
              
              plbl = QLabel()
              pmap = QPixmap('./logos/printer.png')
              plbl.setPixmap(pmap)
              grid.addWidget(plbl , 2, 0, 2, 2)
                    
              cancelBtn = QPushButton('Close')
              cancelBtn.clicked.connect(self.close)  
                
              grid.addWidget(cancelBtn, 3, 1, 1, 1, Qt.AlignRight)
              cancelBtn.setFont(QFont("Arial",10))
              cancelBtn.setFixedWidth(90)
              cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")    
              
              printBtn = QPushButton('Printen')
              printBtn.clicked.connect(lambda: printForm())  
                
              grid.addWidget(printBtn,  3, 2)
              printBtn.setFont(QFont("Arial",10))
              printBtn.setFixedWidth(90)
              printBtn.setStyleSheet("color: black;  background-color: gainsboro")    
                  
              grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
                
              self.setLayout(grid)
              self.setGeometry(900, 200, 150, 150)
              
    win = combo()
    win.exec_()
                     
def groupLines():
    metadata = MetaData()
    article_grouplines = Table('article_grouplines', metadata,
        Column('lineID', Integer, primary_key=True),
        Column('grouplinetext', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    sellines = select([article_grouplines]).order_by(article_grouplines.c.lineID)
    rplines = con.execute(sellines)
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setWindowTitle('Article-group lines')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(changeGroupline)
            grid.addWidget(table_view, 0, 0)
                       
            reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            reglbl.setFont(QFont("Arial", 10))
            grid.addWidget(reglbl, 1, 0)
            
            self.setLayout(grid)
            self.setGeometry(900, 100, 300, 600)
            self.setLayout(grid)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['Artlicle-grouplineID', 'Grouplinetext']
    
    data_list=[]
    for row in rplines:
        data_list += [(row)]
            
    def changeGroupline(idx):
        linenr = idx.data()
        if idx.column() == 0:
            selline = select([article_grouplines]).where(article_grouplines.c.lineID == linenr)
            rpline = con.execute(selline).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Changing Article-groupline items")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setStyleSheet("background-color: #D9E1DF")
                    self.setFont(QFont('Arial', 10))  
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)      
                
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                    
                    #ID
                    self.q1Edit = QLineEdit(str(rpline[0]))
                    self.q1Edit.setFixedWidth(40)
                    self.q1Edit.setFont(QFont("Arial",10))
                    self.q1Edit.setStyleSheet('color: black; background-color: gainsboro')
                    self.q1Edit.setDisabled(True)
                    
                    #QCombotextline
                    self.q2Edit = QLineEdit(rpline[1])
                    self.q2Edit.setFixedWidth(260)
                    self.q2Edit.setFont(QFont("Arial",10))
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    
                    lblq1 = QLabel('Linenumber')
                    lblq1.setFont(QFont("Arial", 10))
                    grid.addWidget(lblq1, 1, 0)
                    grid.addWidget(self.q1Edit, 1, 1)
                    lblq2 = QLabel('Combobox textline')
                    lblq2.setFont(QFont("Arial", 10))
                    grid.addWidget(lblq2, 2, 0)
                    grid.addWidget(self.q2Edit, 2, 1)
                        
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed) 
                    
                    def changeLine(self):
                        linetext = self.q2Edit.text()
                        updline = update(article_grouplines).where(article_grouplines.\
                         c.lineID == linenr).values(grouplinetext = linetext)
                        con.execute(updline)
                        self.close()
                        
                    applyBtn = QPushButton('Change')
                    applyBtn.clicked.connect(lambda: changeLine(self))  
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(applyBtn, 3, 1, 1, 1, Qt.AlignRight)
        
                    closeBtn = QPushButton('Close')
                    closeBtn.clicked.connect(self.close)  
                    closeBtn.setFont(QFont("Arial",10))
                    closeBtn.setFixedWidth(100)
                    closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(closeBtn, 3, 1)                 
        
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 4, 0, 1, 2, Qt.AlignCenter)
                   
                    self.setLayout(grid)
                    self.setGeometry(900, 150, 150, 100)      
        
            window = MainWindow()
            window.exec_()
        
    win = Widget(data_list, header)
    win.exec_()
    
def countTurnover(mindex):
    metadata = MetaData()
    sales = Table('sales', metadata,
        Column('salesID', Integer, primary_key=True),
        Column('receiptnumber', Integer),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('selling_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
 
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Countings gross turnover")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            q1Edit = QLineEdit('20')
            q1Edit.setFixedWidth(100)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            
            lbl4 = QLabel('')
            grid.addWidget(lbl4, 2, 0)

            def q1Changed():
                q1Edit.setText(q1Edit.text())
            q1Edit.textChanged.connect(q1Changed)
            
            if mindex == 0:
                reg_ex = QRegExp("^[2]{1}[0]{1}[0-9]{2}-[01]{1}[0-9]{1}-[0123]{1}[0-9]{1}$")
                input_validator = QRegExpValidator(reg_ex, q1Edit)
                q1Edit.setValidator(input_validator)
                lbl1 = QLabel('Daily <yyyy-mm-dd>')
                grid.addWidget(lbl1, 1, 0)
                grid.addWidget(q1Edit, 1, 1)
            elif mindex == 1:
                reg_ex = QRegExp("^[2]{1}[0]{1}[0-9]{2}-[01]{1}[0-9]{1}$")
                input_validator = QRegExpValidator(reg_ex, q1Edit)
                q1Edit.setValidator(input_validator)
                lbl1 = QLabel('Monthly <yyyy-mm>')
                grid.addWidget(lbl1, 1, 0)
                grid.addWidget(q1Edit, 1, 1)
            elif mindex == 2:
                reg_ex = QRegExp("^[2]{1}[0]{1}[0-9]{2}$")
                input_validator = QRegExpValidator(reg_ex, q1Edit)
                q1Edit.setValidator(input_validator)
                lbl1 = QLabel('Yearly <yyyy>')
                grid.addWidget(lbl1, 1, 0)
                grid.addWidget(q1Edit, 1, 1)
                          
            def counting(mindex):
                mdate = str(q1Edit.text())
                if mindex == 0 and len(mdate) == 10:
                    selsales = select([sales]).where(sales.c.mutation_date == mdate)
                elif mindex == 1 and len(mdate) == 7:
                    selsales = select([sales]).where(sales.c.mutation_date.like(mdate+'%'))
                elif mindex == 2 and len(mdate) == 4:
                    selsales = select([sales]).where(sales.c.mutation_date.like(mdate+'%'))
                else:
                    return
                
                rpsales = con.execute(selsales)
                
                total = 0
                totalvat = 0
                for row in rpsales:
                    total += row[6]
                    totalvat += row[7]               
                 
                lbl2 = QLabel('Totals: '+'{:12.2f}'.format(total)+'           Totals-VAT: '+'{:12.2f}'.format(totalvat)) 
                lbl2.setFont(QFont("Arial", 10))
                grid.addWidget(lbl2, 2, 0, 1, 3) 
                     
            applyBtn = QPushButton('Count')
            applyBtn.clicked.connect(lambda: counting(mindex))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 4, 2)

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 4, 1, 1, 1, Qt.AlignRight)                 

            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 5, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
             
def turnoverMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Turnover Menu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Daily gross turnover')
            self.k0Edit.addItem('Monthly gross turnover')
            self.k0Edit.addItem('Yearly gross turnover')
            
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
            
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                countTurnover(mindex)
                     
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
                                                   
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
    
def switchEmployee(self):
    mcallname = self.mcallname
    lblseats = self.lblseats
    self.view.setText('')  
    self.qtailEdit.setText('Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(0.00)) 
    self.qtotalEdit.setText('')
    self.qcashEdit.setText('')
    self.qchangeEdit.setText('')
  
    metadata = MetaData()
    clients = Table('clients', metadata,
        Column('clientID', Integer, primary_key=True),
        Column('employee', String))
    employees = Table('employees', metadata,
        Column('callname', String))
    tables_layout = Table('tables_layout', metadata,
        Column('clientID', Integer),
        Column('callname', String))
    order_lines = Table('order_lines', metadata,
        Column('callname', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    selempl = select([employees]).order_by(employees.c.callname)
    rpempl = con.execute(selempl)
    
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Switch Employee")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
        
            self.mcallname = mcallname
            self.lblseats = lblseats
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
                  
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            
            for row in rpempl:
                if row[0] != self.mcallname: 
                    self.k0Edit.addItem('Employee takes over: '+row[0])
                
            def switchServing(self):
                emplname = self.k0Edit.currentText()[21:]
                updcl = update(clients).where(clients.c.employee == self.mcallname)\
                    .values(employee = emplname)
                con.execute(updcl)
                updtables = update(tables_layout).where(tables_layout.c.callname==self.mcallname).\
                  values(callname = emplname) 
                con.execute(updtables)
                updorderlines = update(order_lines).where(order_lines.c.callname == self.mcallname).\
                    values(callname = emplname)
                con.execute(updorderlines)
                self.lblseats.setText('Employee '+emplname+' takes over the services from '+self.mcallname+'!')
                self.close()
                                              
            def k0Changed():
                self.k0Edit.setCurrentText(self.k0Edit.currentText())
            self.k0Edit.currentTextChanged.connect(k0Changed)
            
            lblcalln = QLabel('Active employee: '+self.mcallname)
            lblcalln.setFont(QFont("Arial", 10))
            grid.addWidget(lblcalln, 1, 1, 1, 2)
            
            lblk = QLabel('Employees')
            lblk.setFont(QFont("Arial", 10))
            grid.addWidget(lblk, 2, 0)
            grid.addWidget(self.k0Edit, 2, 1, 1, 2, Qt.AlignRight)
            
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: switchServing(self))
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 3, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 3, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 4, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
 
def employeeMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("employeeMenu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('New employee')
            self.k0Edit.addItem('View / change employees')
                                       
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    emplAccess()
                elif mindex == 1:
                    emplRequest()
            
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
    
def importMenu():
    import csv
    metadata=MetaData()
    params = Table('params', metadata,
       Column('paramID', Integer,primary_key=True),
       Column('value', Float))
    articles = Table('articles', metadata,
       Column('barcode', String, primary_key=True),
       Column('description', String),
       Column('short_descr', String),
       Column('item_price', Float),
       Column('item_unit', String),
       Column('article_group', String),
       Column('thumbnail', String),
       Column('category', Integer),
       Column('VAT', String),
       Column('order_status', Boolean),
       Column('supplierID', Integer),
       Column('item_stock', Float),
       Column('order_balance', Float))
    purchase_orderlines = Table('purchase_orderlines', metadata,
       Column('orderlineID', Integer,primary_key=True),
       Column('barcode', String),
       Column('supplierID', Integer),
       Column('delivery', Float),
       Column('delivery_date', String))
    invoices = Table('invoices', metadata,
       Column('invoiceID', Integer, primary_key=True),
       Column('barcode', String),
       Column('description', String),
       Column('delivery', Float),
       Column('item_price', Float),
       Column('supplierID', Integer),
       Column('orderlineID', Integer),
       Column('paydate', String),
       Column('bookdate', String),
       Column('item_unit', String))
    loss = Table('loss', metadata,
       Column('lossID', Integer, primary_key=True),
       Column('barcode', String),
       Column('number', Float),
       Column('bookdate', String),
       Column('category', String),
       Column('item_price', Float),
       Column('description', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    selpar = select([params]).where(params.c.paramID==3)
    rppar = con.execute(selpar).first()
    msep = chr(int(rppar[1]))   
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Importmenu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Import new articles')
            self.k0Edit.addItem('Import price changes')
            self.k0Edit.addItem('Import expired articles')
            self.k0Edit.addItem('Import deliveries articles')
                                         
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mtoday = str(datetime.datetime.now())[0:10]
                home = os.path.expanduser("~")
                log = open(str(home)+'/catering_import.log', 'a+')
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    path = "./forms/Imports/New/"
                    newpath = "./forms/ImportsDone/New/"
                    x = 0
                    for file in os.listdir(path):
                        filename = open(path+file,'r')
                        with filename:
                            reader = csv.reader(filename, delimiter=msep)
                            for line in reader:
                                if line[0].isnumeric():
                                    mbarcode = line[0] 
                                    mdescr = line[1] 
                                    mshort = line[2]
                                    mprice =  float(line[3])
                                    munit = line[4]          
                                    mgroup = line[5]         
                                    mthumb = line[6]       
                                    mcat = line[7]    
                                    mvat = line[8]
                                    msupplier = int(line[9])
                                    sel = select([articles]).where(articles.c.barcode == mbarcode)
                                    if con.execute(sel).fetchone():
                                        message = mtoday+' new items Barcode '+mbarcode+' exists!\n'
                                        log = open(str(home)+'/catering_import.log', 'a')
                                        log.write(message)
                                        continue
                                    elif not checkEan13(mbarcode):
                                        message = mtoday+' new items Barcode '+mbarcode+' is invalid!\n'
                                        log = open(str(home)+'/catering_import.log', 'a')
                                        log.write(message)
                                        continue
                                    else:
                                        insart = insert(articles).values(barcode=mbarcode,\
                                         description=mdescr,short_descr=mshort,\
                                         item_price=mprice,item_unit=munit,\
                                         article_group=mgroup,thumbnail=mthumb,\
                                         category=mcat,VAT=mvat,supplierID=msupplier)
                                        con.execute(insart)
                                        ean = barcode.get('ean13',mbarcode, writer=ImageWriter())
                                        if sys.platform == 'win32':
                                            ean.save('.\\Barcodes\\Articles\\'+str(mbarcode))
                                        else:
                                            ean.save('./Barcodes/Articles/'+str(mbarcode))
                            message = 'Import done!'                
                            actionOK(message)
                            filename.close()
                            shutil.move(path+file,newpath+file)
                        x += 1
                    if x == 0:
                        message = 'No imports available!'
                        actionOK(message)   
                elif mindex == 1:
                    path = "./forms/Imports/Prices/"
                    newpath = "./forms/ImportsDone/Prices/"
                    x = 0
                    for file in os.listdir(path):
                        filename = open(path+file,'r')
                        with filename:
                            reader = csv.reader(filename, delimiter=msep)
                            for line in reader:
                                if line[0].isnumeric():
                                    mbarcode = line[0] 
                                    mprice =  float(line[1])
                                    sel = select([articles]).where(articles.c.barcode == mbarcode)
                                    if con.execute(sel).fetchone():                    
                                        updart = update(articles).where(articles.c.barcode == mbarcode)\
                                          .values(item_price=mprice)
                                        con.execute(updart)
                                    else:
                                        message = mtoday+' Article price changes Barcode '+mbarcode+' not found!\n'
                                        log = open(str(home)+'/catering_import.log', 'a')
                                        log.write(message)
                                        continue
                            message = 'Import done!'
                            actionOK(message)
                            filename.close()
                            shutil.move(path+file,newpath+file)
                        x += 1
                    if x == 0:
                        message = 'No imports available!'
                        actionOK(message)     
                elif mindex == 2:
                    path = "./forms/Imports/Expired/"
                    newpath = "./forms/ImportsDone/Expired/"
                    x = 0
                    for file in os.listdir(path):
                        filename = open(path+file,'r')
                        with filename:
                            reader = csv.reader(filename, delimiter=msep)
                            for line in reader:
                                if line[0].isnumeric():
                                    mbarcode = line[0] 
                                    sel = select([articles]).where(articles.c.barcode == mbarcode)
                                    rp = con.execute(sel).first()
                                    if rp:
                                        try:
                                            lossnr = con.execute(select([func.max(loss.c.lossID, type_=Integer)])).scalar()
                                            lossnr += 1
                                        except:
                                            lossnr = 1
                                        insloss = insert(loss).values(lossID=lossnr,barcode=rp[0],number=-rp[11],\
                                          item_price=rp[3],category='Obsolete',bookdate=mtoday,description=rp[1])
                                        con.execute(insloss)
                                        delart = delete(articles).where(articles.c.barcode == mbarcode)
                                        con.execute(delart)
                                    else:
                                        message = mtoday+' Article expired items Barcode '+mbarcode+' not found!\n'
                                        log = open(str(home)+'/catering_import.log', 'a')
                                        log.write(message)
                                        continue
                            message = 'Import done!'
                            actionOK(message)
                            filename.close()
                            shutil.move(path+file,newpath+file)
                        x += 1
                    if x == 0:
                        message = 'No imports available!'
                        actionOK(message)   
                elif mindex == 3:
                    path = "./forms/Imports/Deliveries/"
                    newpath = "./forms/ImportsDone/Deliveries/"
                    x = 0
                    for file in os.listdir(path):
                        filename = open(path+file,'r')
                        with filename:
                            reader = csv.reader(filename, delimiter=msep)
                            for line in reader:
                                if line[0].isnumeric():
                                    mbarcode = line[0]
                                    selart = select([articles]).where(articles.c.barcode==mbarcode)
                                    rpart = con.execute(selart).first()
                                    if not rpart:
                                        message = mtoday+' Delivery items: Barcode '+mbarcode+' not found!\n'
                                        log = open(str(home)+'/catering_import.log', 'a')
                                        log.write(message)
                                        continue
                                    mdescription = rpart[1]
                                    mprice = rpart[3]
                                    msupplier = rpart[10]
                                    mdelivery = float(line[1])
                                    sel = select([articles]).where(articles.c.barcode == mbarcode)
                                    if con.execute(sel).fetchone():
                                        selord = select([purchase_orderlines]).where(purchase_orderlines\
                                          .c.barcode==mbarcode)
                                        if not con.execute(selord).fetchone():
                                            message = 'Collect purchases in menu "Purchasing" first!'
                                            alertText(message)
                                            return
                                        updart = update(articles).where(articles.c.barcode == mbarcode)\
                                         .values(item_stock=articles.c.item_stock+float(line[1]),order_status=True,\
                                           order_balance = articles.c.order_balance-float(line[1]))
                                        con.execute(updart)
                                        updord = update(purchase_orderlines).where(purchase_orderlines\
                                          .c.barcode==mbarcode).values(delivery=mdelivery,delivery_date=mtoday)
                                        con.execute(updord)
                                        try:
                                            paynr = (con.execute(select([func.max(invoices.c.invoiceID, type_=Integer)])).scalar())
                                            paynr += 1
                                        except:
                                            paynr = 1
                                        inspay = insert(invoices).values(invoiceID=paynr,\
                                           barcode=mbarcode,supplierID=msupplier,\
                                           description=mdescription,item_price=mprice,\
                                           delivery=mdelivery,bookdate=mtoday,\
                                           orderlineID=int(line[2]))
                                        con.execute(inspay)
                            message = 'Import done!'
                            actionOK(message)
                            filename.close()
                            log.close()
                            shutil.move(path+file,newpath+file)
                        x += 1
                    if x == 0:
                        message = 'No imports available!'
                        actionOK(message) 
                        
            lbllog = QLabel('View catering_import.log in your home folder!')  
            lbllog.setFont(QFont("Arial", 10))
            grid.addWidget(lbllog, 2, 0, 1, 3, Qt.AlignCenter)
                        
            applyBtn = QPushButton('Import')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 3, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 3, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 4, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_()
    
def articleMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("ArticleMenu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Insert new articles')
            self.k0Edit.addItem('View / change articles')
            self.k0Edit.addItem('Booking loss articles')
            self.k0Edit.addItem('View loss articles')
                                         
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    insertArticles()
                elif mindex == 1:
                    mflag = 0
                    btn = 0
                    articleRequest(mflag, btn)
                elif mindex == 2:
                    mflag = 2
                    btn = 0
                    articleRequest(mflag, btn)
                elif mindex == 3:
                    requestLoss()

            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_()
    
def requestSupplier():
    metadata = MetaData()
    suppliers = Table('suppliers', metadata,
        Column('supplierID', Integer, primary_key=True),
        Column('company_name', String),
        Column('street', String),
        Column('housenumber', String),
        Column('zipcode', String),
        Column('residence', String),
        Column('telephone', String),
        Column('email', String),
        Column('addition', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
     
    sel = select([suppliers]).order_by(suppliers.c.supplierID)
    if con.execute(sel).fetchone():
        selsup = select([suppliers]).order_by(suppliers.c.supplierID)
        rpsup = con.execute(selsup)
    else:
        message = "No records found!"
        alertText(message)
        return
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setWindowTitle('Suppliers request / change')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(changeSupplier)
            grid.addWidget(table_view, 0, 0)
                       
            reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            reglbl.setFont(QFont("Arial", 10))
            grid.addWidget(reglbl, 1, 0)
            
            self.setLayout(grid)
            self.setGeometry(800, 50, 1000, 600)
            self.setLayout(grid)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['Suppliernr', 'Company name', 'Street', 'Housenumber','Zip-code',\
              'Residence','Telephone', 'E-mail','Addional']
    
    data_list=[]
    for row in rpsup:
        data_list += [(row)]
         
    def changeSupplier(idx):
        suppliernr = idx.data()
        if idx.column()== 0:
            selsupl = select([suppliers]).where(suppliers.c.supplierID == suppliernr)
            rpsupl = con.execute(selsupl).first()
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    
                    self.setWindowTitle("Change supplier")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF") 
          
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                    
                    #supplierID
                    self.q1Edit = QLineEdit(str(rpsupl[0]))
                    self.q1Edit.setFixedWidth(100)
                    self.q1Edit.setDisabled(True)
                    self.q1Edit.setStyleSheet('color: black')
                    self.q1Edit.setFont(QFont("Arial", 10))
                    
                    #Company-name
                    self.q2Edit = QLineEdit(rpsupl[1])
                    self.q2Edit.setFixedWidth(300)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^.{1,40}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
         
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    #Street
                    self.q3Edit = QLineEdit(rpsupl[2])
                    self.q3Edit.setFixedWidth(300)
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q3Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^.{1,40}$")
                    input_validator = QRegExpValidator(reg_ex, self.q3Edit)
                    self.q3Edit.setValidator(input_validator)
                    
                    def q3Changed():
                        self.q3Edit.setText(self.q3Edit.text())
                    self.q3Edit.textChanged.connect(q3Changed)
                    
                    #housenumber
                    self.q4Edit = QLineEdit(rpsupl[3])
                    self.q4Edit.setFixedWidth(100)
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q4Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^.{1,13}$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
        
                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)
                    
                    #Zip-code
                    self.q5Edit = QLineEdit(rpsupl[4])
                    self.q5Edit.setFixedWidth(100)
                    self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q5Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^[0-9]{4}[0-9A-Za-z]{0,3}$")
                    input_validator = QRegExpValidator(reg_ex, self.q5Edit)
                    self.q5Edit.setValidator(input_validator)
                    
                    def q5Changed():
                        self.q5Edit.setText(self.q5Edit.text())
                    self.q5Edit.textChanged.connect(q5Changed)
                    
                    #residence
                    self.q6Edit = QLineEdit(rpsupl[5])
                    self.q6Edit.setFixedWidth(300)
                    self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q6Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^.{1,40}$")
                    input_validator = QRegExpValidator(reg_ex, self.q6Edit)
                    self.q6Edit.setValidator(input_validator)
                    
                    def q6Changed():
                        self.q6Edit.setText(self.q6Edit.text())
                    self.q6Edit.textChanged.connect(q6Changed)
                    
                    #telephone
                    self.q7Edit = QLineEdit(rpsupl[6])
                    self.q7Edit.setFixedWidth(150)
                    self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q7Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^[+0-9]{0,15}$")
                    input_validator = QRegExpValidator(reg_ex, self.q7Edit)
                    self.q7Edit.setValidator(input_validator)
                    
                    def q7Changed():
                        self.q7Edit.setText(self.q7Edit.text())
                    self.q7Edit.textChanged.connect(q7Changed)
                    
                    #email
                    self.q8Edit = QLineEdit(rpsupl[7])
                    self.q8Edit.setFixedWidth(300)
                    self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q8Edit.setFont(QFont("Arial", 10))
                                
                    def q8Changed():
                        self.q8Edit.setText(self.q8Edit.text())
                    self.q8Edit.textChanged.connect(q8Changed)
                    
                    #additions-country-bound
                    self.q9Edit = QPlainTextEdit(rpsupl[8])
                    self.q9Edit.setFixedSize(300,100)
                    self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q9Edit.setFont(QFont("Arial", 10))

                    def updateSupplier():
                        mcompany = self.q2Edit.text()
                        mstreet = self.q3Edit.text()
                        mhousenr = self.q4Edit.text()
                        mzipcode = self.q5Edit.text().upper()
                        mresid = self.q6Edit.text()
                        mtel = self.q7Edit.text()
                        def memailContr(memail):
                            ab = re.compile("[^@]+@[^@]+\\.[^@]+$")
                            if ab.match(memail):
                                return(True)
                            else:
                                return(False)
                        if memailContr(self.q8Edit.text()) and len(self.q8Edit.text()) < 201:
                            memail = self.q8Edit.text() 
                        else:
                            message = 'No valid e-mail adress!'
                            alertText(message)
                            return
                        if len(self.q9Edit.toPlainText()) > 1000:
                            message = 'No more then 1000 characters allowed!'
                            alertText(message)
                            return
                        else:
                            maddition = self.q9Edit.toPlainText()
                        
                        updsup = update(suppliers).where(suppliers.c.supplierID ==\
                          suppliernr).values(company_name=mcompany,\
                          street=mstreet,housenumber=mhousenr, zipcode=mzipcode,\
                          residence = mresid, telephone=mtel,email=memail,addition=maddition)
                        con.execute(updsup)
                        self.close()
                    
                    lblq1 = QLabel('Supplier id')
                    grid.addWidget(lblq1, 1, 0)
                    grid.addWidget(self.q1Edit, 1, 1)
                    
                    lblq2 = QLabel('Company name')
                    grid.addWidget(lblq2, 2, 0)
                    grid.addWidget(self.q2Edit, 2, 1)
                    
                    lblq3 = QLabel('Street')
                    grid.addWidget(lblq3, 3, 0)
                    grid.addWidget(self.q3Edit, 3, 1)
                    
                    lblq4 = QLabel('Housenumber')
                    grid.addWidget(lblq4, 4, 0)
                    grid.addWidget(self.q4Edit, 4, 1)
                    
                    lblq5 = QLabel('Zip-code')
                    grid.addWidget(lblq5, 5, 0)
                    grid.addWidget(self.q5Edit, 5, 1)
                    
                    lblq6 = QLabel('Residence')
                    grid.addWidget(lblq6, 6, 0)
                    grid.addWidget(self.q6Edit, 6, 1)
                    
                    lblq7 = QLabel('Telephone')
                    grid.addWidget(lblq7, 7, 0)
                    grid.addWidget(self.q7Edit, 7, 1)
                    
                    lblq8 = QLabel('E-Mail')
                    grid.addWidget(lblq8, 8, 0)
                    grid.addWidget(self.q8Edit, 8, 1)
                    
                    lblq9= QLabel('Addional country\nbound data')
                    grid.addWidget(lblq9, 9, 0)
                    grid.addWidget(self.q9Edit, 9, 1)
                  
                    applyBtn = QPushButton('Update')
                    applyBtn.clicked.connect(lambda: updateSupplier())  
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(90)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(applyBtn, 10, 1, 1, 1, Qt.AlignRight)
                    
                    closeBtn = QPushButton('Close')
                    closeBtn.clicked.connect(self.close)  
                    closeBtn.setFont(QFont("Arial",10))
                    closeBtn.setFixedWidth(90)
                    closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(closeBtn, 10, 1, 1, 1, Qt.AlignCenter)
                         
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 11, 0, 1, 2, Qt.AlignCenter)
                   
                    self.setLayout(grid)
                    self.setGeometry(900, 200, 350, 100)
                        
            window = Widget()
            window.exec_()
    
    win = Widget(data_list, header)
    win.exec_()
    
def newSupplier():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            
            self.setWindowTitle("Insert new supplier")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
    
            grid = QGridLayout()
            grid.setSpacing(20)
            
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
  
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
            
            metadata = MetaData()
            suppliers = Table('suppliers', metadata,
                Column('supplierID', Integer, primary_key=True),
                Column('company_name', String),
                Column('street', String),
                Column('housenumber', String),
                Column('zipcode', String),
                Column('residence', String),
                Column('telephone', String),
                Column('email', String),
                Column('addition', String))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
            con = engine.connect()
  
            try:
               supplnr = (con.execute(select([func.max(suppliers.c.supplierID, type_=Integer)])).scalar())
               supplnr += 1
            except:
               supplnr = 1
             
            #supplierID
            self.q1Edit = QLineEdit(str(supplnr))
            self.q1Edit.setFixedWidth(100)
            self.q1Edit.setDisabled(True)
            self.q1Edit.setStyleSheet('color: black')
            self.q1Edit.setFont(QFont("Arial", 10))
            
            #Company-name
            self.q2Edit = QLineEdit()
            self.q2Edit.setFixedWidth(300)
            self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q2Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^.{1,40}$")
            input_validator = QRegExpValidator(reg_ex, self.q2Edit)
            self.q2Edit.setValidator(input_validator)
 
            def q2Changed():
                self.q2Edit.setText(self.q2Edit.text())
            self.q2Edit.textChanged.connect(q2Changed)
            
            #Street
            self.q3Edit = QLineEdit()
            self.q3Edit.setFixedWidth(300)
            self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^.{1,40}$")
            input_validator = QRegExpValidator(reg_ex, self.q3Edit)
            self.q3Edit.setValidator(input_validator)
            
            def q3Changed():
                self.q3Edit.setText(self.q3Edit.text())
            self.q3Edit.textChanged.connect(q3Changed)
            
            #housenumber
            self.q4Edit = QLineEdit()
            self.q4Edit.setFixedWidth(100)
            self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q4Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^.{1,13}$")
            input_validator = QRegExpValidator(reg_ex, self.q4Edit)
            self.q4Edit.setValidator(input_validator)

            def q4Changed():
                self.q4Edit.setText(self.q4Edit.text())
            self.q4Edit.textChanged.connect(q4Changed)
            
            #Zip-code
            self.q5Edit = QLineEdit()
            self.q5Edit.setFixedWidth(100)
            self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q5Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^[0-9]{4}[0-9A-Za-z]{0,3}$")
            input_validator = QRegExpValidator(reg_ex, self.q5Edit)
            self.q5Edit.setValidator(input_validator)
            
            def q5Changed():
                self.q5Edit.setText(self.q5Edit.text())
            self.q5Edit.textChanged.connect(q5Changed)
            
            #residence
            self.q6Edit = QLineEdit()
            self.q6Edit.setFixedWidth(300)
            self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q6Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^.{1,40}$")
            input_validator = QRegExpValidator(reg_ex, self.q6Edit)
            self.q6Edit.setValidator(input_validator)
            
            def q6Changed():
                self.q6Edit.setText(self.q6Edit.text())
            self.q6Edit.textChanged.connect(q6Changed)
            
            #telephone
            self.q7Edit = QLineEdit()
            self.q7Edit.setFixedWidth(150)
            self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q7Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^[+0-9]{0,15}$")
            input_validator = QRegExpValidator(reg_ex, self.q7Edit)
            self.q7Edit.setValidator(input_validator)
            
            def q7Changed():
                self.q7Edit.setText(self.q7Edit.text())
            self.q7Edit.textChanged.connect(q7Changed)
            
            #email
            self.q8Edit = QLineEdit()
            self.q8Edit.setFixedWidth(300)
            self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q8Edit.setFont(QFont("Arial", 10))
             
            def q8Changed():
                self.q8Edit.setText(self.q8Edit.text())
            self.q8Edit.textChanged.connect(q8Changed)
            
            #additions-country-bound
            self.q9Edit = QPlainTextEdit()
            self.q9Edit.setFixedSize(300,100)
            self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q9Edit.setFont(QFont("Arial", 10))
                                        
            def insertSupplier():
                mcompany = self.q2Edit.text()
                mstreet = self.q3Edit.text()
                mhousenr = self.q4Edit.text()
                mzipcode = self.q5Edit.text().upper()
                mresid = self.q6Edit.text()
                mtel = self.q7Edit.text()
                def memailContr(memail):
                    ab = re.compile("[^@]+@[^@]+\\.[^@]+$")
                    if ab.match(memail):
                        return(True)
                    else:
                        return(False)
                if memailContr(self.q8Edit.text()) and len(self.q8Edit.text()) < 201:
                    memail = self.q8Edit.text()
                else:
                    message = 'No valid e-mail adress!'
                    alertText(message)
                    return
                if len(self.q9Edit.toPlainText()) > 1000:
                    message = 'No more then 1000 characters allowed!'
                    alertText(message)
                    return
                else:
                    maddition = self.q9Edit.toPlainText()
                
                inssup = insert(suppliers).values(supplierID=supplnr,company_name=mcompany,\
                  street=mstreet,housenumber=mhousenr, zipcode = mzipcode, residence = mresid,
                  telephone=mtel,email=memail,addition=maddition)
                con.execute(inssup)
                self.close()
            
            lblq1 = QLabel('Supplier id')
            grid.addWidget(lblq1, 1, 0)
            grid.addWidget(self.q1Edit, 1, 1)
            
            lblq2 = QLabel('Company name')
            grid.addWidget(lblq2, 2, 0)
            grid.addWidget(self.q2Edit, 2, 1)
            
            lblq3 = QLabel('Street')
            grid.addWidget(lblq3, 3, 0)
            grid.addWidget(self.q3Edit, 3, 1)
            
            lblq4 = QLabel('Housenumber')
            grid.addWidget(lblq4, 4, 0)
            grid.addWidget(self.q4Edit, 4, 1)
            
            lblq5 = QLabel('Zip-code')
            grid.addWidget(lblq5, 5, 0)
            grid.addWidget(self.q5Edit, 5, 1)
             
            lblq6 = QLabel('Residence')
            grid.addWidget(lblq6, 6, 0)
            grid.addWidget(self.q6Edit, 6, 1)
            
            lblq7 = QLabel('Telephone')
            grid.addWidget(lblq7, 7, 0)
            grid.addWidget(self.q7Edit, 7, 1)
            
            lblq8 = QLabel('E-Mail')
            grid.addWidget(lblq8, 8, 0)
            grid.addWidget(self.q8Edit, 8, 1)
            
            lblq9= QLabel('myear = int(str(datetime.date.today())[0:4]) country\nbound data\nVAT-number\nChamber of commerce')
            grid.addWidget(lblq9, 9, 0)
            grid.addWidget(self.q9Edit, 9, 1)
          
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insertSupplier())  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 10, 1, 1, 1, Qt.AlignRight)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 10, 0, 1, 2, Qt.AlignCenter)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 11, 0, 1, 2, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_()
    
def handleInvoices():
    metadata = MetaData()
    invoices = Table('invoices', metadata,
       Column('invoiceID', Integer, primary_key=True),
       Column('barcode', String),
       Column('description', String),
       Column('delivery', Float),
       Column('item_price', Float),
       Column('supplierID', Integer),
       Column('orderlineID', Integer),
       Column('paydate', String),
       Column('bookdate', String),
       Column('item_unit', String))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    sel = select([invoices]).order_by(invoices.c.supplierID, invoices.c.paydate)
    if con.execute(sel).fetchone():
        selinv = select([invoices]).order_by(invoices.c.supplierID, invoices.c.paydate)
        rpinv = con.execute(selinv)
    else:
        message = "no records found!"
        alertText(message)
        return
    class tableView(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(300, 50, 900, 900)
            self.setWindowTitle('Paying invoices suppliers')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(invoicePaying)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['InvoiceID', 'Barcode', 'Description', 'Deliveries', 'Itemprice',\
              'SupplierID', 'OrderlineID','Paydate','Bookdate','Item-unit']
    
    data_list=[]
    for row in rpinv:
        data_list += [(row)]
    
    def invoicePaying(idx):
        paynr=idx.data()
        if idx.column()==0:
            selinv = select([invoices]).where(invoices.c.invoiceID==paynr)
            rpinv = con.execute(selinv).first()
            class Window(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Paying invoice supplier")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setFont(QFont('Arial', 10))   
                    self.setStyleSheet("background-color: #D9E1DF")
                    
                    #invoiceID
                    q1Edit = QLineEdit(str(rpinv[0]))
                    q1Edit.setCursorPosition(0)
                    q1Edit.setFixedWidth(100)
                    q1Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                                    
                    #barcode
                    q2Edit = QLineEdit(rpinv[1])
                    q2Edit.setFixedWidth(130)
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                     
                    #description
                    q3Edit = QLineEdit(rpinv[2])
                    q3Edit.setFixedWidth(300)
                    q3Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                                               
                    #deliveries
                    q4Edit = QLineEdit('{:12.2f}'.format(rpinv[3]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                    
                    #item-price
                    q5Edit = QLineEdit('{:12.2f}'.format(rpinv[4]))
                    q5Edit.setFixedWidth(100)
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                    
                    #supplierID
                    q6Edit = QLineEdit(str(rpinv[5]))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
                    
                    #orderlineID
                    q7Edit = QLineEdit(str(rpinv[6]))
                    q7Edit.setFixedWidth(100)
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)
                    
                    #paydate
                    q8Edit = QLineEdit(str(rpinv[7]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    #item_unit
                    q9Edit = QLineEdit(rpinv[9])
                    q9Edit.setFixedWidth(160)
                    q9Edit.setAlignment(Qt.AlignRight)
                    q9Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                    
                    #bookdate
                    q10Edit = QLineEdit(str(rpinv[8]))
                    q10Edit.setFixedWidth(100)
                    q10Edit.setAlignment(Qt.AlignRight)
                    q10Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q10Edit.setDisabled(True)
                    
                    self.cBoxpay = QCheckBox()
                    self.cBoxpay.setText('Paying')
                    self.cBoxpay.setFont(QFont("Arial", 10))
                    if rpinv[7]:
                        self.cBoxpay.setChecked(True)
                        self.cBoxpay.setText('Payment done')
                        self.cBoxpay.setDisabled(True)
                      
                    def cboxChanged():
                        self.cBoxpay.setCheckState(self.cBoxpay.checkState())
                    self.cBoxpay.stateChanged.connect(cboxChanged) 
                    
                    def invPay(self):
                        mtoday = str(datetime.datetime.now())[0:10]
                        if self.cBoxpay.checkState():
                            upd = update(invoices).where(invoices.c.invoiceID==paynr)\
                              .values(paydate = mtoday)
                            con.execute(upd)
                            message = 'Payment done!'
                            actionOK(message)
                            self.close()
                        else:
                            self.close()
          
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
       
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 3, 1 ,1, Qt.AlignRight)
                    
                    lbl1 = QLabel('Invoicenr')
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(q1Edit, 1, 1)
                    
                    lbl2 = QLabel('Barcode')
                    grid.addWidget(lbl2, 1, 2)
                    grid.addWidget(q2Edit, 1, 3)
                           
                    lbl3 = QLabel('Description')  
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(q3Edit, 2, 1, 1, 3) 
                                                         
                    lbl4 = QLabel('Deliveries')  
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(q4Edit, 3, 1)
                    
                    lbl11 = QLabel('Bookdate')
                    grid.addWidget(lbl11, 3, 2)
                    grid.addWidget(q10Edit, 3, 3)
 
                    lbl5 = QLabel('Item-price')  
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(q5Edit, 4, 1)
                     
                    lbl10 = QLabel('Item-unit')
                    grid.addWidget(lbl10, 4, 2)
                    grid.addWidget(q9Edit, 4, 3)
                    
                    lbl7 = QLabel('supplierID')  
                    grid.addWidget(lbl7, 5, 0)
                    grid.addWidget(q6Edit, 5, 1)
                                   
                    lbl8 = QLabel('Orderlinenr')  
                    grid.addWidget(lbl8, 5, 2)
                    grid.addWidget(q7Edit, 5, 3)
                    
                    lbl9 = QLabel('Paydate')
                    grid.addWidget(lbl9, 6, 0)
                    grid.addWidget(q8Edit, 6, 1)
                                     
                    lbl6 = QLabel('Orderline total    =  '+'{:12.2f}'.format(rpinv[3]*rpinv[4]))
                    grid.addWidget(lbl6, 7, 0, 1, 2)
                    
                    grid.addWidget(self.cBoxpay, 7, 2, 1, 2)
                      
                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)
            
                    applyBtn = QPushButton('Pay / Close')
                    applyBtn.clicked.connect(lambda: invPay(self))
            
                    grid.addWidget(applyBtn, 8, 3, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(120)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 9, 0, 1, 4, Qt.AlignCenter)
                    
            mainWin = Window()
            mainWin.exec_() 
              
    win = tableView(data_list, header)
    win.exec_()
    
def supplierMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Supplier Submenu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
 
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Suppliers new')
            self.k0Edit.addItem('Suppliers view / change')
            self.k0Edit.addItem('Invoices suppliers / paying')
            
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    newSupplier()
                elif mindex == 1:
                    requestSupplier()
                elif mindex == 2:
                    handleInvoices()
                    
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 

def purchaseMenu():
    mtoday = str(datetime.datetime.now())[0:10]
    metadata = MetaData()
    purchase_orderlines = Table('purchase_orderlines', metadata,
        Column('orderlineID', Integer,primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('item_price', Float),
        Column('item_unit', String),
        Column('order_size', Float),
        Column('ordering_manual', Integer),
        Column('supplierID', Integer),
        Column('bookdate', String),
        Column('ordered', Float),
        Column('order_date', String),
        Column('delivery', Float),
        Column('delivery_date', String))
    suppliers = Table('suppliers', metadata,
        Column('supplierID', Integer, primary_key=True),
        Column('company_name', String))
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('item_stock', Float),
        Column('order_balance', Float),
        Column('order_status', Boolean),
        Column('supplierID', Integer))
    invoices = Table('invoices', metadata,
       Column('invoiceID', Integer, primary_key=True),
       Column('barcode', String),
       Column('description', String),
       Column('delivery', Float),
       Column('item_price', Float),
       Column('supplierID', Integer),
       Column('orderlineID', Integer),
       Column('paydate', String),
       Column('bookdate', String),
       Column('item_unit', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    selsup = select([purchase_orderlines,suppliers]).where(suppliers.c.supplierID==\
       purchase_orderlines.c.supplierID).distinct(purchase_orderlines.c.supplierID)\
      .order_by(purchase_orderlines.c.supplierID)
    rpsup = con.execute(selsup)
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Orders / deliveries")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            self.msuppliernr = 0
            self.msupplier = ''
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
 
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Collecting purchases')
            self.k0Edit.addItem('Manual - ordering')
            self.k0Edit.addItem('Unknown supplier - ordering')
            self.k0Edit.addItem('Receiving / processing deliveries')
            for row in rpsup:
                if not row[10] and not row[6]:
                    self.k0Edit.addItem('Ordering suppliernr '+str(row[13])+'\u2003'+row[14])
            self.k0Edit.addItem('To order yet - view')
            self.k0Edit.addItem('Ordered - view')
            self.k0Edit.addItem('All orders - view')
            self.k0Edit.addItem('Delivered orders - view')
            
            def k0Changed():
                self.k0Edit.setCurrentText(self.k0Edit.currentText())
            self.k0Edit.currentTextChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
             
            def menuChoice():
                mconnect = 0
                if self.k0Edit.currentText().startswith('Collecting'):
                    purchaseCollect(self)
                elif self.k0Edit.currentText().startswith('Manual'):
                    sel = selord = select([purchase_orderlines,suppliers]).where(and_\
                      (purchase_orderlines.c.ordering_manual==1, purchase_orderlines.c.\
                       order_date=='', purchase_orderlines.c.supplierID==\
                       suppliers.c.supplierID))
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines,suppliers]).where(and_\
                           (purchase_orderlines.c.ordering_manual==1, purchase_orderlines.c.\
                            order_date=='', purchase_orderlines.c.supplierID==\
                            suppliers.c.supplierID)).order_by(suppliers.c.company_name)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return
                    mconnect = 1
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Unknown'): 
                    sel = select([purchase_orderlines])\
                       .where(purchase_orderlines.c.supplierID==0)
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines])\
                            .where(purchase_orderlines.c.supplierID==0)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return
                    mconnect = 2
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Receiving'):
                    sel = select([purchase_orderlines,suppliers])\
                      .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                      purchase_orderlines.c.order_date != ''))
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines,suppliers])\
                          .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                          purchase_orderlines.c.order_date != '')).order_by(suppliers.c.company_name)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return 
                    mconnect = 3
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Ordering'):
                    mpos = self.k0Edit.currentText().find('\u2003')
                    self.msuppliernr = int(self.k0Edit.currentText()[20:mpos])
                    self.msupplier = self.k0Edit.currentText()[mpos+1:]
                    sel = select([purchase_orderlines,suppliers])\
                        .where(and_(purchase_orderlines.c.supplierID==self.msuppliernr,\
                        purchase_orderlines.c.order_date=='',suppliers.c.supplierID==\
                        purchase_orderlines.c.supplierID, purchase_orderlines.c.ordering_manual==0))
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines,suppliers])\
                          .where(and_(purchase_orderlines.c.supplierID==self.msuppliernr,\
                           purchase_orderlines.c.order_date=='',suppliers.c.supplierID==\
                           purchase_orderlines.c.supplierID, purchase_orderlines.c.ordering_manual==0))
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return                         
                    mconnect = 4
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('To'):
                    sel = select([purchase_orderlines])\
                     .where(purchase_orderlines.c.order_date == '')
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines])\
                          .where(purchase_orderlines.c.order_date == '').order_by(purchase_orderlines.c.supplierID)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return    
                    mconnect = 5
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Ordered'):
                    sel = select([purchase_orderlines,suppliers])\
                     .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                      purchase_orderlines.c.order_date != '')) 
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines,suppliers])\
                         .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                          purchase_orderlines.c.order_date != '')).order_by(suppliers.c.company_name)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return                        
                    mconnect = 6
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('All'):
                    sel = select([purchase_orderlines])
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines]).order_by(purchase_orderlines.c.supplierID)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return                         
                    mconnect = 7
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Delivered'):
                    sel = select([purchase_orderlines,suppliers])\
                     .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                      purchase_orderlines.c.delivery_date != ''))
                    if con.execute(sel).fetchone():
                         selord = select([purchase_orderlines,suppliers])\
                             .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                             purchase_orderlines.c.delivery_date != '')).order_by(suppliers.c.company_name)
                         rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return                         
                    mconnect = 8
                    orderViews(self,rpord, mconnect)
                
            def orderViews(self,rpord, mconnect):
                msuppliernr = self.msuppliernr
                msupplier = self.msupplier
                class Widget(QDialog):
                    def __init__(self, data_list, header, *args):
                        QWidget.__init__(self, *args)
                        self.setWindowTitle('Ordering / deliveries')
                        self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                        self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
                        self.setFont(QFont('Arial', 10))
                        
                        grid = QGridLayout()
                        grid.setSpacing(20)
                                                
                        table_model = MyTableModel(self, data_list, header)
                        table_view = QTableView()
                        table_view.setModel(table_model)
                        font = QFont("Arial", 10)
                        table_view.setFont(font)
                        table_view.resizeColumnsToContents()
                        table_view.setSelectionBehavior(QTableView.SelectRows)
                        table_view.resizeColumnsToContents()
                        table_view.clicked.connect(orderHandle)
                                      
                        grid.addWidget(table_view, 0, 0, 1, 6)
                        
                        def processOrders(self,rpord):
                            mtotal = 0
                            mpage = 0
                            rgl = 0
                            if sys.platform == 'win32':
                                fpurchase_order = '.\\forms\\Purchasing\\Purchase_Order_Supplier_'+str(msuppliernr)+'_'+msupplier+'_'+mtoday+'.txt'
                            else:
                                fpurchase_order = './forms//Purchasing/Purchase_Order_Supplier_'+str(msuppliernr)+'_'+msupplier+'_'+mtoday+'.txt'
                            def heading(self, mpage):
                                head=\
                            ('Purchase Order Supplier '+str(msuppliernr)+'  '+str(msupplier)+' Date : '+str(mtoday)+' Pagenumber '+str(mpage)+' \n'+
                            '==================================================================================================\n'+
                            'Order  Barcode       Description                      Number Unit               Price    Subtotal \n'+
                            '==================================================================================================\n')
                                return(head)
                            for row in rpord:
                                updline = update(purchase_orderlines)\
                                 .where(purchase_orderlines.c.orderlineID==row[0])\
                                 .values(ordered=row[5],order_date=mtoday)
                                con.execute(updline) 
                                morderline = row[0]
                                mbarcode = row[1]
                                mdescr = str(row[2])[0:30]
                                mprice = float(row[3])
                                munit = str(row[4])
                                mnumber = float(row[5])
                                mtotal += mprice*mnumber
                                rgl += 1
                                if rgl == 1:
                                    mpage += 1
                                    open(fpurchase_order, 'w').write(heading(self, mpage))
                                    rgl += 4
                                elif rgl%58 == 1:
                                    mpage += 1
                                    open(fpurchase_order, 'a').write(heading(self, mpage))
                                    rgl += 4
                                                                
                                open(fpurchase_order,'a').write('{:>6s}'.format(str(morderline))+' '+str(mbarcode)\
                                     +' '+'{:<30s}'.format(mdescr)+' '+'{:>8.2f}'.format(mnumber)\
                                     +' '+'{:<16s}'.format(munit)+'{:>8.2f}'.format(mprice)+'    '\
                                     +'{:>8.2f}'.format(mprice*mnumber)+'\n')
                                                                                                             
                            tail=\
                            ('===================================================================================================\n'+
                             'Total price orders                                                                   '+'{:>12.2f}'.format(mtotal)+'\n'+
                             '===================================================================================================\n')
                            if rgl > 0:
                                open(fpurchase_order,'a').write(tail) 
                                if sys.platform == 'win32':
                                    from os import startfile
                                    startfile(fpurchase_order, "print")
                                else:
                                    from os import system
                                    system("lpr "+fpurchase_order)
                                message ='Printing of purchase orders'
                                actionOK(message)
                            else:
                                message = 'No transactions for printing!'
                                alertText(message)
                    
                        if mconnect == 4:
                            printBtn = QPushButton('Process / Printing')
                            printBtn.clicked.connect(lambda: processOrders(self,rpord))
                            printBtn.setFont(QFont("Arial",10))
                            printBtn.setFixedWidth(180)
                            printBtn.setStyleSheet("color: black;  background-color: gainsboro")
                            
                            grid.addWidget(printBtn, 1, 5, 1, 1, Qt.AlignRight)
                        
                        closeBtn = QPushButton('Close')
                        closeBtn.clicked.connect(self.close)  
                        closeBtn.setFont(QFont("Arial",10))
                        closeBtn.setFixedWidth(100)
                        closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                        
                        if mconnect == 4:
                           grid.addWidget(closeBtn, 1, 4, 1, 1, Qt.AlignRight)
                        else:
                           grid.addWidget(closeBtn, 1, 5, 1, 1, Qt.AlignRight)
                                                           
                        reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                        reglbl.setFont(QFont("Arial", 10))
                        grid.addWidget(reglbl, 2, 0, 1, 6, Qt.AlignCenter)
                        
                        self.setLayout(grid)
                        self.setGeometry(300, 100, 1500, 700)
                        self.setLayout(grid)
                
                class MyTableModel(QAbstractTableModel):
                    def __init__(self, parent, mylist, header, *args):
                        QAbstractTableModel.__init__(self, parent, *args)
                        self.mylist = mylist
                        self.header = header
                    def rowCount(self, parent):
                        return len(self.mylist)
                    def columnCount(self, parent):
                        return len(self.mylist[0])
                    def data(self, index, role):
                        veld = self.mylist[index.row()][index.column()]
                        if not index.isValid():
                            return None
                        elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                            return Qt.AlignRight | Qt.AlignVCenter
                        elif role != Qt.DisplayRole:
                            return None
                        if type(veld) == float:
                            return '{:12.2f}'.format(veld)
                        else:
                            return veld
                    def headerData(self, col, orientation, role):
                        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                            return self.header[col]
                        return None
                         
                header = ['Orderlinenr','Barcode','Description','Item-price','Item-unit',\
                          'Order-size','Ordering-manual','SupplierID','Bookdate','Ordered amounts',\
                          'Order-date','Deliveries','Delivery-date','Suppliernr',\
                          'Company_name']
                
                if mconnect == 2 or mconnect==5 or mconnect==7:
                    del header[-2:]

                data_list=[]
                for row in rpord:
                    data_list += [(row)]
                     
                if mconnect == 4:
                    mpos = self.k0Edit.currentText().find('\u2003')
                    msuppliernr = int(self.k0Edit.currentText()[20:mpos])
                    selord = select([purchase_orderlines,suppliers])\
                        .where(and_(purchase_orderlines.c.supplierID==msuppliernr,\
                        purchase_orderlines.c.order_date=='',suppliers.c.supplierID==\
                        purchase_orderlines.c.supplierID))
                    rpord = con.execute(selord)
                                 
                def orderHandle(idx):
                    orderlinenr = idx.data()
                    if idx.column()==0:
                        if mconnect == 1:  #ordering manual
                            selorderline = select([purchase_orderlines, suppliers])\
                             .where(and_(purchase_orderlines.c.orderlineID==orderlinenr,\
                                purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                                purchase_orderlines.c.ordering_manual==1))\
                                .order_by(suppliers.c.company_name)
                            rporderline = con.execute(selorderline).first()
                        elif mconnect == 2:  #supplier unknown make order
                            selorderline = select([purchase_orderlines])\
                             .where(and_(purchase_orderlines.c.orderlineID==orderlinenr,\
                              purchase_orderlines.c.supplierID==0))
                            rporderline = con.execute(selorderline).first()
                        elif mconnect == 3: #process deliveries
                            selorderline = select([purchase_orderlines, suppliers])\
                             .where(and_(purchase_orderlines.c.orderlineID==orderlinenr,\
                                purchase_orderlines.c.supplierID==suppliers.c.supplierID))\
                                .order_by(suppliers.c.company_name)
                            rporderline = con.execute(selorderline).first()
                        elif mconnect == 4 or mconnect == 8: #orders generated all suppliers per supplier
                            selorderline = select([purchase_orderlines, suppliers])\
                             .where(and_(purchase_orderlines.c.orderlineID==orderlinenr,\
                                purchase_orderlines.c.supplierID==suppliers.c.supplierID)).order_by(suppliers.c.company_name)
                            rporderline = con.execute(selorderline).first()
                        elif mconnect==6:
                            selorderline = select([purchase_orderlines,suppliers])\
                             .where(and_(purchase_orderlines.c.orderlineID==orderlinenr,\
                                suppliers.c.supplierID==purchase_orderlines.c.supplierID)).\
                                 order_by(suppliers.c.company_name)
                            rporderline = con.execute(selorderline).first()
                        elif mconnect==5 or mconnect==7:
                            selorderline = select([purchase_orderlines])\
                             .where(purchase_orderlines.c.orderlineID==orderlinenr)\
                             .order_by(purchase_orderlines.c.supplierID)
                            rporderline = con.execute(selorderline).first()
    
                        class MainWindow(QDialog):
                            def __init__(self):
                                QDialog.__init__(self)
                                self.setWindowTitle("Ordering / Deliveries")
                                self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                
                                self.setStyleSheet("background-color: #D9E1DF")
                                self.setFont(QFont('Arial', 10)) 
                                
                                grid = QGridLayout()
                                grid.setSpacing(20)
                                
                                pyqt = QLabel()
                                movie = QMovie('./logos/pyqt.gif')
                                pyqt.setMovie(movie)
                                movie.setScaledSize(QSize(240,80))
                                movie.start()
                                grid.addWidget(pyqt, 0, 0, 1, 2)
                           
                                logo = QLabel()
                                pixmap = QPixmap('./logos/logo.jpg')
                                logo.setPixmap(pixmap.scaled(70,70))
                                grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)
                                
                                #orderline
                                self.q1Edit = QLineEdit(str(rporderline[0]))
                                self.q1Edit.setFixedWidth(40)
                                self.q1Edit.setFont(QFont("Arial",10))
                                self.q1Edit.setStyleSheet('color: black; background-color: gainsboro')
                                self.q1Edit.setDisabled(True)
                                
                                #barcode
                                self.q2Edit = QLineEdit(rporderline[1])
                                self.q2Edit.setFixedWidth(130)
                                self.q2Edit.setFont(QFont("Arial", 10))
                                self.q2Edit.setStyleSheet('color: black')
                                self.q2Edit.setDisabled(True)    
                                
                                #description
                                self.q3Edit = QLineEdit(rporderline[2])
                                self.q3Edit.setFixedWidth(300)
                                self.q3Edit.setFont(QFont("Arial", 10))
                                self.q3Edit.setDisabled(True)
                                self.q3Edit.setStyleSheet('color: black')
                                
                                #item-price
                                self.q4Edit = QLineEdit(str(rporderline[3]))
                                self.q4Edit.setFixedWidth(100)
                                self.q4Edit.setFont(QFont("Arial", 10))
                                self.q4Edit.setDisabled(True)
                                self.q4Edit.setStyleSheet('color: black')
                                
                                #item-unit
                                self.q4aEdit = QLineEdit(rporderline[4])
                                self.q4aEdit.setFixedWidth(100)
                                self.q4aEdit.setFont(QFont("Arial", 10))
                                self.q4aEdit.setDisabled(True)
                                self.q4aEdit.setStyleSheet('color: black')
                                
                                #Order-size
                                self.q5Edit = QLineEdit(str(rporderline[5]))
                                self.q5Edit.setFixedWidth(100)
                                self.q5Edit.setFont(QFont("Arial", 10))
                                self.q5Edit.setDisabled(True)
                                self.q5Edit.setStyleSheet('color: black')
                                   
                                #Ordering-manual
                                self.q7Edit = QLineEdit(str(rporderline[6]))
                                self.q7Edit.setFixedWidth(20)
                                self.q7Edit.setFont(QFont("Arial", 10))
                                self.q7Edit.setDisabled(True)
                                self.q7Edit.setStyleSheet('color: black')
                                
                                #Bookdate
                                self.q8Edit = QLineEdit(str(rporderline[8]))
                                self.q8Edit.setFixedWidth(100)
                                self.q8Edit.setFont(QFont("Arial", 10))
                                self.q8Edit.setDisabled(True)
                                self.q8Edit.setStyleSheet('color: black')
                                
                                #Ordered amount
                                if mconnect < 2:
                                    self.q9Edit = QLineEdit('0')
                                    self.q9Edit.setStyleSheet('color: black ; background-color: #F8F7EE')
                                    def q9Changed():
                                        self.q9Edit.setText(self.q9Edit.text())
                                    self.q9Edit.textChanged.connect(q9Changed)    
                                else:
                                    self.q9Edit = QLineEdit(str(rporderline[9]))
                                    self.q9Edit.setDisabled(True)
                                    self.q9Edit.setStyleSheet('color: black')
                                self.q9Edit.setFixedWidth(50)
                                self.q9Edit.setFont(QFont("Arial", 10))
                                                                  
                                #Order_date
                                self.q10Edit = QLineEdit(rporderline[10])
                                self.q10Edit.setFixedWidth(100)
                                self.q10Edit.setFont(QFont("Arial", 10))
                                self.q10Edit.setDisabled(True)
                                self.q10Edit.setStyleSheet('color: black')
                                
                                #Deliveries
                                self.q11Edit = QLineEdit(str(rporderline[11]))
                                self.q11Edit.setFixedWidth(100)
                                self.q11Edit.setFont(QFont("Arial", 10))
                                self.q11Edit.setDisabled(True)
                                self.q11Edit.setStyleSheet('color: black')
                                if mconnect == 3:
                                    self.q11Edit.setEnabled(True)
                                    self.q11Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                                    def q11Changed():
                                        self.q11Edit.setText(self.q11Edit.text())
                                    self.q11Edit.textChanged.connect(q11Changed)
                                
                                #Delivery_date
                                self.q12Edit = QLineEdit(rporderline[12])
                                self.q12Edit.setFixedWidth(100)
                                self.q12Edit.setFont(QFont("Arial", 10))
                                self.q12Edit.setDisabled(True)
                                self.q12Edit.setStyleSheet('color: black')
                             
                                #Suppliernr
                                if mconnect == 2:
                                    self.q13Edit = QLineEdit('')
                                    def q13Changed():
                                       self.q13Edit.setText(self.q13Edit.text())
                                    self.q13Edit.textChanged.connect(q13Changed)
                                    self.q13Edit.setFixedWidth(100)
                                    self.q13Edit.setFont(QFont("Arial", 10))
                                    self.q13Edit.setStyleSheet('color: black ; background-color: #F8F7EE')
                                    reg_ex = QRegExp("^[0-9]{1,10}$")
                                    input_validator = QRegExpValidator(reg_ex, self.q13Edit)
                                    self.q13Edit.setValidator(input_validator)
                                else:
                                    self.q13Edit = QLineEdit(str(rporderline[6]))
                                    self.q13Edit.setDisabled(True)
                                    self.q13Edit.setFixedWidth(100)
                                    self.q13Edit.setFont(QFont("Arial", 10))
                                    self.q13Edit.setStyleSheet('color: black')
                                if not(mconnect == 2 or mconnect == 5 or mconnect == 7):
                                    #Company-name
                                    self.q14Edit = QLineEdit(rporderline[14])
                                    self.q14Edit.setFixedWidth(300)
                                    self.q14Edit.setFont(QFont("Arial", 10))
                                    self.q14Edit.setDisabled(True)
                                    self.q14Edit.setStyleSheet('color: black') 
                                    
                                    lbl14 = QLabel('Company name')
                                    lbl14.setFont(QFont("Arial",10))
                                    grid.addWidget(lbl14, 8, 0)
                                    grid.addWidget(self.q14Edit, 8, 1, 1, 3)
 
                                lbl1 = QLabel('Orderlinenr')
                                lbl1.setFont(QFont("Arial",10))
                                grid.addWidget(lbl1, 1, 0)
                                grid.addWidget(self.q1Edit, 1, 1)
                                
                                lbl2 = QLabel('Barcode')
                                lbl2.setFont(QFont("Arial",10))
                                grid.addWidget(lbl2, 1, 2)
                                grid.addWidget(self.q2Edit, 1, 3)
                                
                                lbl3 = QLabel('Description')
                                lbl3.setFont(QFont("Arial",10))
                                grid.addWidget(lbl3, 2, 0)
                                grid.addWidget(self.q3Edit, 2, 1, 1, 3)
                                    
                                lbl4 = QLabel('Item-price') 
                                lbl4.setFont(QFont("Arial",10))
                                grid.addWidget(lbl4, 3, 0)
                                grid.addWidget(self.q4Edit, 3, 1)
                                
                                lbl4a = QLabel('Item-unit') 
                                lbl4a.setFont(QFont("Arial",10))
                                grid.addWidget(lbl4a, 3, 2)
                                grid.addWidget(self.q4aEdit, 3, 3)
                                                                                            
                                lbl5 = QLabel('Order-size') 
                                lbl5.setFont(QFont("Arial",10))
                                grid.addWidget(lbl5, 4, 0)
                                grid.addWidget(self.q5Edit, 4, 1)
                                                                                                                
                                lbl7 = QLabel('Manual ordering')
                                lbl7.setFont(QFont("Arial",10))
                                grid.addWidget(lbl7, 4, 2)
                                grid.addWidget(self.q7Edit, 4,3)
                                
                                lbl8 = QLabel('Booking date')
                                lbl8.setFont(QFont("Arial",10))
                                grid.addWidget(lbl8, 5, 0)
                                grid.addWidget(self.q8Edit, 5, 1)
                                
                                lbl9 = QLabel('Ordering amount')
                                lbl9.setFont(QFont("Arial",10))
                                grid.addWidget(lbl9, 5, 2)
                                grid.addWidget(self.q9Edit, 5, 3)
                                
                                lbl10 = QLabel('Order date')
                                lbl10.setFont(QFont("Arial",10))
                                grid.addWidget(lbl10, 6, 0)
                                grid.addWidget(self.q10Edit, 6, 1)
                                
                                lbl11 = QLabel('Delivered amount')
                                lbl11.setFont(QFont("Arial",10))
                                grid.addWidget(lbl11, 6, 2)
                                grid.addWidget(self.q11Edit, 6, 3)
                                
                                lbl12 = QLabel('Delivery date')
                                lbl12.setFont(QFont("Arial",10))
                                grid.addWidget(lbl12, 7, 0)
                                grid.addWidget(self.q12Edit, 7, 1)
                                
                                lbl13 = QLabel('Suppliernumber')
                                lbl13.setFont(QFont("Arial",10))
                                grid.addWidget(lbl13, 7, 2)
                                grid.addWidget(self.q13Edit, 7, 3)
                                
                                self.setLayout(grid)
                                self.setGeometry(900, 200, 150, 150)
 
                                def saveHandled(self):
                                    mnumber=float(self.q9Edit.text())
                                    mtoday = str(datetime.datetime.now())[0:10]
                                    if mconnect == 1:
                                        selline = select([purchase_orderlines,suppliers])\
                                         .where(and_(purchase_orderlines.c.orderlineID==rporderline[0],\
                                          purchase_orderlines.c.ordering_manual==1,\
                                          purchase_orderlines.c.supplierID==suppliers.c.supplierID))
                                        rpline=con.execute(selline).first()
                                        if not rpline:
                                            message = 'No matching records found!'
                                            alertText(message)
                                            return
                                        msuppliernr = rporderline[13]
                                        msupplier = rporderline[14]
                                        mordered=float(self.q9Edit.text())
                                        upd = update(purchase_orderlines)\
                                          .where(purchase_orderlines.c.orderlineID==rporderline[0])\
                                          .values(ordered=mordered,order_date=mtoday)
                                        con.execute(upd)
                                        mpage = 0
                                        rgl = 0
                                        if sys.platform == 'win32':
                                            fpurchase_order = '.\\forms\\Purchasing\\Purchase_Order_Manual_Supplier_'+str(msuppliernr)+'_'+msupplier+'_'+mtoday+'.txt'
                                        else:
                                            fpurchase_order = './forms//Purchasing/Purchase_Order_Manual_Supplier_'+str(msuppliernr)+'_'+msupplier+'_'+mtoday+'.txt'
                                        def heading(self, mpage):
                                            head=\
                                        ('Purchase Order Supplier '+str(msuppliernr)+'  '+str(msupplier)+' Date : '+str(mtoday)+' Pagenumber '+str(mpage)+' \n'+
                                        '==================================================================================================\n'+
                                        'Order  Barcode       Description                      Number Unit               Price    Subtotal \n'+
                                        '==================================================================================================\n')
                                            return(head)
                                        updline = update(purchase_orderlines)\
                                            .where(purchase_orderlines.c.orderlineID==rporderline[0])\
                                             .values(ordered=row[5],order_date=mtoday)
                                        con.execute(updline) 
                                        morderline = rporderline[0]
                                        mbarcode = rporderline[1]
                                        mdescr = str(rporderline[2])[0:30]
                                        mprice = float(rporderline[3])
                                        munit = str(rporderline[4])
                                        mtotal = mprice*mnumber
                                        rgl += 1
                                        if rgl == 1:
                                            mpage += 1
                                            open(fpurchase_order, 'w').write(heading(self, mpage))
                                            rgl += 4
                                                                                          
                                        open(fpurchase_order,'a').write('{:>6s}'.format(str(morderline))+' '+str(mbarcode)\
                                             +' '+'{:<30s}'.format(mdescr)+' '+'{:>8.2f}'.format(mnumber)\
                                             +' '+'{:<16s}'.format(munit)+'{:>8.2f}'.format(mprice)+'    '\
                                             +'{:>8.2f}'.format(mprice*mnumber)+'\n')
                                                                                                                     
                                        tail=\
                                        ('===================================================================================================\n'+
                                         'Total price orders                                                                   '+'{:>12.2f}'.format(mtotal)+'\n'+
                                         '===================================================================================================\n')
                                        open(fpurchase_order,'a').write(tail) 
                                        if sys.platform == 'win32':
                                            from os import startfile
                                            startfile(fpurchase_order, "print")
                                        else:
                                            from os import system
                                            system("lpr "+fpurchase_order)
                                        message ='Update Ok - Printing of purchase order!'
                                        actionOK(message)
                                        self.close()
                                    elif mconnect == 2:
                                        msuppliernr=int(self.q13Edit.text())
                                        sel = select([suppliers]).where(suppliers.c.supplierID ==msuppliernr)
                                        rp = con.execute(sel).first()
                                        if not rp:
                                            message = 'SupplierID does not exist!'
                                            alertText(message)
                                            return
                                        mtoday = str(datetime.datetime.now())[0:10]
                                        msupplier = rp[1]
                                        upd = update(purchase_orderlines)\
                                          .where(purchase_orderlines.c.orderlineID==rporderline[0])\
                                          .values(supplierID=msuppliernr,order_date=mtoday)
                                        con.execute(upd)
                                        updart = update(articles).where(articles.c.barcode==rporderline[1])\
                                           .values(supplierID=msuppliernr)
                                        con.execute(updart)
                                        mpage = 0
                                        rgl = 0
                                        if sys.platform == 'win32':
                                            fpurchase_order = '.\\forms\\Purchasing\\Purchase_Order_No_Supplier_Supplier_'+str(msuppliernr)+'_'+msupplier+'_'+mtoday+'.txt'
                                        else:
                                            fpurchase_order = './forms//Purchasing/Purchase_Order_No_Supplier_Supplier_'+str(msuppliernr)+'_'+msupplier+'_'+mtoday+'.txt'
                                        def heading(self, mpage):
                                            head=\
                                        ('Purchase Order Supplier '+str(msuppliernr)+'  '+str(msupplier)+' Date : '+str(mtoday)+' Pagenumber '+str(mpage)+' \n'+
                                        '==================================================================================================\n'+
                                        'Order  Barcode       Description                      Number Unit               Price    Subtotal \n'+
                                        '==================================================================================================\n')
                                            return(head)
                                        updline = update(purchase_orderlines)\
                                            .where(purchase_orderlines.c.orderlineID==rporderline[0])\
                                             .values(ordered=row[5],order_date=mtoday)
                                        con.execute(updline) 
                                        morderline = rporderline[0]
                                        mbarcode = rporderline[1]
                                        mdescr = str(rporderline[2])[0:30]
                                        mprice = float(rporderline[3])
                                        munit = str(rporderline[4])
                                        mnumber = float(rporderline[5])
                                        mtotal = mprice*mnumber
                                        rgl += 1
                                        if rgl == 1:
                                            mpage += 1
                                            open(fpurchase_order, 'w').write(heading(self, mpage))
                                            rgl += 4
                                                                                          
                                        open(fpurchase_order,'a').write('{:>6s}'.format(str(morderline))+' '+str(mbarcode)\
                                             +' '+'{:<30s}'.format(mdescr)+' '+'{:>8.2f}'.format(mnumber)\
                                             +' '+'{:<16s}'.format(munit)+'{:>8.2f}'.format(mprice)+'    '\
                                             +'{:>8.2f}'.format(mprice*mnumber)+'\n')
                                                                                                                     
                                        tail=\
                                        ('===================================================================================================\n'+
                                         'Total price orders                                                                   '+'{:>12.2f}'.format(mtotal)+'\n'+
                                         '===================================================================================================\n')
                                        open(fpurchase_order,'a').write(tail) 
                                        if sys.platform == 'win32':
                                            from os import startfile
                                            startfile(fpurchase_order, "print")
                                        else:
                                            from os import system
                                            system("lpr "+fpurchase_order)
                                        message ='Update Ok - Printing of purchase order!'
                                        actionOK(message)
                                        self.close()
                                    elif mconnect == 3:
                                        mdelivered = float(self.q11Edit.text())
                                        upd = update(purchase_orderlines)\
                                          .where(purchase_orderlines.c.orderlineID==rporderline[0])\
                                          .values(delivery=mdelivered,delivery_date=mtoday)
                                        con.execute(upd)
                                        updart = update(articles).where(articles.c.barcode == rporderline[1])\
                                          .values(item_stock = articles.c.item_stock+mdelivered,\
                                          order_balance=articles.c.order_balance-mdelivered,\
                                          order_status=True)
                                        con.execute(updart)
                                        try:
                                            paynr = (con.execute(select([func.max(invoices.c.invoiceID, type_=Integer)])).scalar())
                                            paynr += 1
                                        except:
                                            paynr = 1
                                        inspay = insert(invoices).values(invoiceID=paynr,\
                                           barcode=rporderline[1],supplierID=rporderline[7],\
                                           description=rporderline[2],item_price=rporderline[3],\
                                           delivery=rporderline[11],bookdate=rporderline[12],\
                                           orderlineID=rporderline[0],item_unit=rporderline[4])
                                        con.execute(inspay)
                                        message = 'Updates and invoice booking succeeded!'
                                        actionOK(message)
                                        self.close()
              
                                if mconnect == 3:
                                    applyBtn = QPushButton('Processing')
                                    applyBtn.clicked.connect(lambda: saveHandled(self))
                                    applyBtn.setFont(QFont("Arial",10))
                                    applyBtn.setFixedWidth(180)
                                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                    grid.addWidget(applyBtn, 10, 3, 1, 1, Qt.AlignRight)
                                elif mconnect < 3:
                                    applyBtn = QPushButton('Process - Printing')
                                    applyBtn.clicked.connect(lambda: saveHandled(self))
                                    applyBtn.setFont(QFont("Arial",10))
                                    applyBtn.setFixedWidth(180)
                                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                    grid.addWidget(applyBtn, 10, 3, 1, 1, Qt.AlignRight)
                                    
                                cancelBtn = QPushButton('Close')
                                cancelBtn.clicked.connect(self.close)
                                cancelBtn.setFont(QFont("Arial",10))
                                cancelBtn.setFixedWidth(100)
                                cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                if mconnect < 4:
                                    grid.addWidget(cancelBtn, 10, 2, 1, 1, Qt.AlignRight)
                                else:
                                    grid.addWidget(cancelBtn, 10, 3, 1, 1, Qt.AlignRight)  
  
                                reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                                reglbl.setFont(QFont("Arial",10))                               
                                grid.addWidget(reglbl, 11, 0, 1, 4, Qt.AlignCenter)   
                                                    
                        window = MainWindow()
                        window.exec_()
 
                win = Widget(data_list, header)
                win.exec_()  
             
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice())
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 

def groupButtons():
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setWindowTitle('Groupbuttons buttontext')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showGroupbutton)
            grid.addWidget(table_view, 0, 0)
                       
            reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            reglbl.setFont(QFont("Arial", 10))
            grid.addWidget(reglbl, 1, 0)
            
            self.setLayout(grid)
            self.setGeometry(800, 50, 500, 600)
            self.setLayout(grid)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['ButtonNumber', 'Buttongrouptext', 'Reference', 'Button-color']
    
    metadata = MetaData()
    groupbuttons = Table('groupbuttons', metadata,
        Column('groupID', Integer(), primary_key=True),
        Column('buttongrouptext', String),
        Column('reference', String),
        Column('bg_color', String))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
        
    sel = select([groupbuttons]).order_by(groupbuttons.c.groupID)
    rp = con.execute(sel)
    
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showGroupbutton(idx):
        groupbuttonnr = idx.data()
        if idx.column() == 0: 
            selbtn = select([groupbuttons]).where(groupbuttons.c.groupID == groupbuttonnr)
            rpbtn = con.execute(selbtn).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Groupbuttons changing")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setStyleSheet("background-color: #D9E1DF")
                    self.setFont(QFont('Arial', 10))  
                    
                    #reference
                    self.q2Edit = QLineEdit(rpbtn[2])
                    self.q2Edit.setFixedWidth(40)
                    self.q2Edit.setFont(QFont("Arial",10))
                    self.q2Edit.setStyleSheet('color: black; background-color: gainsboro')
                    self.q2Edit.setDisabled(True)
                    
                    #buttongrouptext
                    self.q3Edit = QPlainTextEdit(rpbtn[1])
                    self.q3Edit.setFixedSize(170,110)
                    self.q3Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.q3Edit.setFont(QFont("Consolas", 12, 75))
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    
                    #button background-color
                    self.q4Edit = QLineEdit(rpbtn[3])
                    self.q4Edit.setFixedWidth(80)
                    self.q4Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^[#]{1}[a-fA-F0-9]{6}$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                                                       
                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)
                         
                    def updGroupbutton(self):
                        mbuttontext = self.q3Edit.toPlainText()
                        mlist = mbuttontext.split('\n')
                        mbtncolor = self.q4Edit.text()
                        if len(mbtncolor) < 7:
                            mbtncolor = '#FFFFF0'
                        for line in mlist:
                            if len(line) > 14:
                                 message = 'No more then 14 characters per line allowed'
                                 alertText(message)
                                 break
                            elif len(mlist) > 5:
                                 message= 'No more then 5 lines allowed'
                                 alertText(message)
                                 break
                        else:
                            updbtn = update(groupbuttons).where(groupbuttons.c.groupID == groupbuttonnr).\
                                   values(buttongrouptext = mbuttontext)
                            con.execute(updbtn)
                            message = 'Groupbutton text /color change succeeded!'
                            actionOK(message)
                            self.close()
                                                                  
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl1 = QLabel('Groupbuttonnumber')
                    lbl1.setFont(QFont("Arial",10))
                    grid.addWidget(lbl1, 1, 0)
                    
                    lbl2 = QLabel(str(groupbuttonnr))
                    lbl2.setFont(QFont("Arial",10))
                    grid.addWidget(lbl2, 1, 1)
                        
                    lbl3 = QLabel('Reference') 
                    lbl3.setFont(QFont("Arial",10))
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(self.q2Edit, 2, 1)
                                                                                
                    lbl4 = QLabel('Buttongrouptext') 
                    lbl4.setFont(QFont("Arial",10))
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(self.q3Edit, 3, 1)
                                      
                    lbl5 = QLabel('Button Color') 
                    lbl5.setFont(QFont("Arial",10))
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(self.q4Edit, 4, 1)
                     
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 , 0 , 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
                    
                    reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    reglbl.setFont(QFont("Arial",10))                               
                    grid.addWidget(reglbl, 8, 0, 1, 3, Qt.AlignCenter)                  
                    self.setLayout(grid)
                    self.setGeometry(900, 200, 150, 150)
            
                    applyBtn = QPushButton('Change')
                    applyBtn.clicked.connect(lambda: updGroupbutton(self))
            
                    grid.addWidget(applyBtn, 7, 2, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
         
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
            
                    grid.addWidget(cancelBtn, 7, 1, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                          
            window = MainWindow()
            window.exec_()
            
    win = Widget(data_list, header)
    win.exec_()
    
def paramChange():
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setWindowTitle('Parameters requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showSelection)
            grid.addWidget(table_view, 0, 0)
                       
            reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            reglbl.setFont(QFont("Arial", 10))
            grid.addWidget(reglbl, 1, 0)
            
            self.setLayout(grid)
            self.setGeometry(900, 150, 450, 400)
            self.setLayout(grid)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['ParamID', 'Item', 'Value']
    
    metadata = MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('item', String),
        Column('value', Float))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
        
    sel = select([params]).order_by(params.c.paramID)
    
    rp = con.execute(sel)
    
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showSelection(idx):
        paramnr = idx.data()
        if idx.column() == 0: 
            selpar = select([params]).where(params.c.paramID == paramnr)
            rppar = con.execute(selpar).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Parameters changing")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setStyleSheet("background-color: #D9E1DF")
                    self.setFont(QFont('Arial', 10))  
                    
                    #item
                    self.q1Edit = QLineEdit(rppar[1])
                    self.q1Edit.setCursorPosition(0)
                    self.q1Edit.setFixedWidth(220)
                    self.q1Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q1Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{0,20}$")
                    input_validator = QRegExpValidator(reg_ex, self.q1Edit)
                    self.q1Edit.setValidator(input_validator)
                                    
                    #value
                    self.q2Edit = QLineEdit(str(round(float(rppar[2]),2)))
                    self.q2Edit.setFixedWidth(100)
                    self.q2Edit.setAlignment(Qt.AlignRight)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    def q1Changed():
                        self.q1Edit.setText(self.q1Edit.text())
                    self.q1Edit.textChanged.connect(q1Changed)
                    
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                                     
                    def updparams(self):
                         mitem = self.q1Edit.text()   
                         mvalue = self.q2Edit.text()

                         updpar = update(params).where(params.c.paramID == paramnr).\
                               values(item = mitem, value = float(mvalue))
                         con.execute(updpar)
                         message = 'Parameter change succeeded!'
                         actionOK(message)
                         self.close()
                                                      
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl1 = QLabel('Parameter')
                    lbl1.setFont(QFont("Arial",10))
                    grid.addWidget(lbl1, 1, 0)
                    lbl2 = QLabel(str(paramnr))
                    lbl2.setFont(QFont("Arial",10))
                    grid.addWidget(lbl2, 1, 1)
                           
                    lbl3 = QLabel('Item') 
                    lbl3.setFont(QFont("Arial",10))
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(self.q1Edit, 2, 1, 1, 2) 
                                                         
                    lbl4 = QLabel('Value') 
                    lbl4.setFont(QFont("Arial",10))
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(self.q2Edit, 3, 1)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 , 0 , 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
                    
                    reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    reglbl.setFont(QFont("Arial",10))                               
                    grid.addWidget(reglbl, 8, 0, 1, 3, Qt.AlignCenter)                  
                    self.setLayout(grid)
                    self.setGeometry(900, 200, 150, 150)
            
                    applyBtn = QPushButton('Change')
                    applyBtn.clicked.connect(lambda: updparams(self))
            
                    grid.addWidget(applyBtn, 7, 2, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
 
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
            
                    grid.addWidget(cancelBtn, 7, 1, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                      
            window = MainWindow()
            window.exec_()
            
    win = Widget(data_list, header)
    win.exec_()
    
def adminMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Administrator Menu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
  
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE') 
            self.k0Edit.setMaxVisibleItems(14)
            self.k0Edit.addItem('Employees submenu')
            self.k0Edit.addItem('Articles submenu')
            self.k0Edit.addItem('Article-groups lines - view / change')
            self.k0Edit.addItem('Purchase submenu')
            self.k0Edit.addItem('Suppliers submenu')
            self.k0Edit.addItem('Imports submenu')
            self.k0Edit.addItem('Groupbuttons grouptext / color')
            self.k0Edit.addItem('Payments - view / pay')
            self.k0Edit.addItem('Parameters - view / change')
            self.k0Edit.addItem('Sales - view')
            self.k0Edit.addItem('Additionals - view')
            self.k0Edit.addItem('Turnover Submenu - view')
            self.k0Edit.addItem('Reprint purchase orders')
            self.k0Edit.addItem('Reprint sales receipts')
             
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
            
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                
                if mindex == 0:
                    employeeMenu()
                elif mindex == 1:
                    articleMenu()
                elif mindex == 2:
                    groupLines()
                elif mindex == 3:
                    purchaseMenu()
                elif mindex == 4:
                    supplierMenu()
                elif mindex == 5:
                    importMenu()
                elif mindex == 6:
                    groupButtons()
                elif mindex == 7:
                    paymentsRequest()
                elif mindex == 8:
                    paramChange()
                elif mindex == 9:
                    salesRequest()
                elif mindex == 10:
                    additionRequest()
                elif mindex == 11:
                    turnoverMenu()
                elif mindex == 12:
                    if sys.platform == 'win32':
                        path = '.\\forms\\Purchasing\\'
                    else:
                        path = './forms/Purchasing/'
                    reprintForms(path)
                elif mindex == 13:
                    if sys.platform == 'win32':
                        path = '.\\forms\\Sales\\'
                    else:
                        path = './forms/Sales/'
                    reprintForms(path)

            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_()  
    
def emplRequest():
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(500, 50, 600, 800)
            self.setWindowTitle('employees requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
            table_view.clicked.connect(changeemployees)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
        
    metadata = MetaData()
    employees = Table('employees', metadata,
         Column('barcodeID', String, primary_key=True),
         Column('firstname', String),
         Column('lastname', String),
         Column('access', Integer),
         Column('callname', String))
        
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
    con = engine.connect()
        
    selacc = select([employees]).order_by(employees.c.lastname)
    rpacc = con.execute(selacc)
        
    header = ['AccountID','Firstname','Lastname','Acceslevel','Callname']                                       
        
    data_list=[]
    for row in rpacc:
        data_list += [(row)] 
        
    def changeemployees(idx):
        emplnr = idx.data()
        if idx.column() == 0:
            selempl = select([employees]).where(employees.c.barcodeID == emplnr)
            rpempl = con.execute(selempl).first()
            class Window(QDialog):
                 def __init__(self, parent=None):
                    super(Window, self).__init__(parent)
                    
                    self.setWindowTitle("Employee changing")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                           
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF")  
                     
                    self.path = './Barcodes/employees/'
                    self.mbarcode = emplnr
            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
                    
                    q1Edit = QLineEdit(rpempl[0])
                    q1Edit.setFixedWidth(100)
                    q1Edit.setFont(QFont("Arial",10))
                    q1Edit.setStyleSheet("color: black")
                    q1Edit.setDisabled(True)
                                    
                    q2Edit = QLineEdit(rpempl[1])     #firstname
                    q2Edit.setFixedWidth(200)
                    q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{1,20}$")
                    input_validator = QRegExpValidator(reg_ex, q2Edit)
                    q2Edit.setValidator(input_validator)
                     
                    q3Edit = QLineEdit(rpempl[2])   #lastname
                    q3Edit.setFixedWidth(200)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^.{1,20}$")
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q3Edit.setValidator(input_validator)
                     
                    q4Edit = QLineEdit(rpempl[4])   #callname
                    q4Edit.setFixedWidth(200)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^.{1,20}$")
                    input_validator = QRegExpValidator(reg_ex, q4Edit)
                    q4Edit.setValidator(input_validator)
                    
                    q5Edit = QLineEdit(str(rpempl[3]))   #access
                    q5Edit.setFixedWidth(30)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0123]{1}$")
                    input_validator = QRegExpValidator(reg_ex, q5Edit)
                    q5Edit.setValidator(input_validator)
                    
                    def q2Changed():
                        q2Edit.setText(q2Edit.text())
                    q2Edit.textChanged.connect(q2Changed)
                     
                    def q3Changed():
                        q3Edit.setText(q3Edit.text())
                    q3Edit.textChanged.connect(q3Changed)  
                    
                    def q4Changed():
                        q4Edit.setText(q4Edit.text())
                    q4Edit.textChanged.connect(q4Changed)  
                    
                    def q5Changed():
                        q5Edit.setText(q5Edit.text())
                    q5Edit.textChanged.connect(q5Changed)
        
                    lbl1 = QLabel('Employee-barcode')
                    lbl1.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl1, 4, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q1Edit, 4, 1)
                              
                    lbl2 = QLabel('First name')
                    lbl2.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl2, 5, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q2Edit, 5, 1)
                    
                    lbl3 = QLabel('Last name')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 6, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q3Edit, 6, 1)
                    
                    lbl4 = QLabel('Call name')
                    lbl4.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl4, 7, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q4Edit, 7, 1)
                    
                    lbl5 = QLabel('Access level')
                    lbl5.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl5, 8, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q5Edit, 8, 1)
                    
                    applyBtn = QPushButton('Update')
                    applyBtn.clicked.connect(lambda: updateAcc())
                       
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                    grid.addWidget(applyBtn,9, 2, 1, 1, Qt.AlignRight)
                    
                    printBtn = QPushButton('Print Barcode')
                    printBtn.clicked.connect(lambda: prepareEan(self))
                       
                    printBtn.setFont(QFont("Arial",10))
                    printBtn.setFixedWidth(120)
                    printBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                    grid.addWidget(printBtn,9, 1, 1, 1, Qt.AlignRight)
                    
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close) 
            
                    grid.addWidget(cancelBtn, 9, 0, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
                    
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 10, 0, 1, 3, Qt.AlignCenter)
                    
                    def prepareEan(self):
                        ean = barcode.get('ean8', str(self.mbarcode[:8]), writer=ImageWriter()) # for barcode as png
                        emplnr = ean.get_fullcode()
                        if rpempl:
                            if sys.platform == 'win32':
                                ean.save('.\\Barcodes\\employees\\'+emplnr)
                            else:
                                ean.save('./Barcodes/employees/'+emplnr)
                        x1 = 267.3
                        y1 = 213.1
                        printEan(self, x1 , y1)
                  
                    def updateAcc():
                        fname = q2Edit.text()
                        lname = q3Edit.text()
                        cname = q4Edit.text()
                        maccess = q5Edit.text()
                        updacc = update(employees).where(employees.c.barcodeID == emplnr).\
                        values(firstname = fname,lastname = lname, callname = cname,\
                               access = int(maccess))
                        con.execute(updacc)
                        message = 'Employee change succeeded!'
                        actionOK(message)
                        self.close()
                                          
                    self.setLayout(grid)
                    self.setGeometry(600, 200, 150, 100)
                    
            window = Window()
            window.exec_()
           
    win = Widget(data_list, header)
    win.exec_()
     
def viewFile(pathfile, mtitle):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle(mtitle)
              
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
                        
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
        
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 1)
            
            lblh = QLabel(mtitle)
                     
            grid.addWidget(lblh, 0, 0, 1, 2, Qt.AlignCenter)
            lblh.setStyleSheet("color:rgba(45, 83, 115, 255); font: 25pt Comic Sans MS")
            
            text_edit = QPlainTextEdit()
            text_edit.setStyleSheet('color: black; background-color: #F8F7EE') 
            text_edit.setFont(QFont("Consolas",12,75))
            text = open(pathfile).read()
            text_edit.setPlainText(text)
           
            grid.addWidget(text_edit, 1, 0, 1, 2)
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 1, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            lblreg = (QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'))
            lblreg.setFont(QFont("Arial",10))
            grid.addWidget(lblreg, 3, 0, 1, 2, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(250, 50, 1200, 900)
            
    window = Widget()
    window.exec_()
    
def viewList(path, mtitle):
    filelist = []
    for file in os.listdir(path):
        if file[-4:] == '.txt':
            filelist.append(file)
    class combo(QDialog):
        def __init__(self, parent=None):
              super(combo, self).__init__(parent)
              self.setWindowTitle("Viewing List")
              self.setWindowIcon(QIcon('./logos/logo.jpg'))
              
              self.setStyleSheet("background-color: #D9E1DF")
              self.setFont(QFont('Arial', 10))
              
              grid = QGridLayout()
              grid.setSpacing(20)
            
              logo = QLabel()
              pixmap = QPixmap('./logos/logo.jpg')
              logo.setPixmap(pixmap)
              grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
                       
              pyqt = QLabel()
              movie = QMovie('./logos/pyqt.gif')
              pyqt.setMovie(movie)
              movie.setScaledSize(QSize(240,80))
              movie.start()
              grid.addWidget(pyqt, 0 ,0, 1, 1)
                
              self.cb = QComboBox()
              self.cb.setFixedWidth(420)
              self.cb.setFont(QFont("Arial",10))
              self.cb.setStyleSheet("color: black;  background-color: #F8F7EE")
              grid.addWidget(self.cb, 1, 0, 1, 3, Qt.AlignRight)
              
              for item in range(len(filelist)):
                  self.cb.addItem(filelist[item])
                  self.cb.model().sort(0)
                  grid.addWidget(self.cb, 1, 0, 1, 3, Qt.AlignRight)
                  
              def cbChanged():
                  self.cb.setCurrentText(self.cb.currentText())
              self.cb.currentIndexChanged.connect(cbChanged)
                     
              cancelBtn = QPushButton('Close')
              cancelBtn.clicked.connect(self.close) 
                
              grid.addWidget(cancelBtn, 4, 1, 1, 1, Qt.AlignRight)
              cancelBtn.setFont(QFont("Arial",10))
              cancelBtn.setFixedWidth(90)
              cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")    
              
              viewBtn = QPushButton('View')
              viewBtn.clicked.connect(lambda: getfile(self))  
                
              grid.addWidget(viewBtn,  4, 2)
              viewBtn.setFont(QFont("Arial",10))
              viewBtn.setFixedWidth(90)
              viewBtn.setStyleSheet("color: black;  background-color: gainsboro")    
               
              reslbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
              reslbl.setFont(QFont("Arial",10))
              grid.addWidget(reslbl, 5, 0, 1, 3, Qt.AlignCenter)
                
              self.setLayout(grid)
              self.setGeometry(900, 200, 150, 150)
              
              def getfile(self):
                  filename = self.cb.currentText()
                  viewFile(path+filename, mtitle)
          
    win = combo()
    win.exec_()

def calculationStock():
    metadata = MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('item', String),
        Column('value', Float))
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('category', Integer),
        Column('annual_consumption_1', Float),
        Column('annual_consumption_2', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    myear = int(str(datetime.date.today())[0:4])
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
    myear = int(str(datetime.date.today())[0:4])
    if myear%2 == 1 and int(rppar[3][2]) == 0:
        selarticles = select([articles]).order_by(articles.c.barcode)
        rparticles = con.execute(selarticles)
        updpar = update(params).where(params.c.paramID == 4).values(value = 1)
        con.execute(updpar)
                     
        for row in rparticles:
            if row[4]>0:
                mordersize = round(sqrt(2*row[5]*rppar[4][2])/(row[1]*rppar[5][2]),0)
                mjrverbr = row[4]
                if row[3] == 1:
                    minstock = round(mjrverbr*1/104, 0) # < 3 days deliverytime
                elif row[3] == 2:
                    minstock = round(mjrverbr*1/52, 0) # < 1 week deliverytime
                elif row[3] == 3:
                    minstock = round(mjrverbr*1/26, 0) # < 2 weeks deliverytime
                elif row[3] == 4:
                    minstock = round(mjrverbr*1/17, 0) # < 3 weeks deliverytime
                elif row[3] == 5:
                    minstock = round(mjrverbr*2/17, 0) # < 6 weeks deliverytime
                elif row[3] == 6:
                    minstock = round(mjrverbr*4/17, 0) # < 12 weeks deliverytime
                elif row[3] == 7:
                    minstock = round(mjrverbr*8/17, 0) # < 26 weeks deliverytime
                elif row[3] == 8:
                    minstock = round(mjrverbr*16/17,0) # < 52 weeks deliverytime

                updart = update(articles).where(articles.c.barcode == row[0]).\
                    values(annual_consumption_2 = 0, minimum_stock = minstock, order_size = mordersize)
                con.execute(updart)
    elif myear%2 == 0 and int(rppar[3][2]) == 1:
        selarticles = select([articles]).order_by(articles.c.barcode)
        rparticles = con.execute(selarticles)
        updpar = update(params).where(params.c.paramID == 4).values(value = 0)
        con.execute(updpar)
                   
        for row in rparticles:
            if row[5] > 0:
                mordersize = round(sqrt(2*row[5]*rppar[4][2])/(row[1]*rppar[5][2]),0)
                mjrverbr = row[5]
                if row[3] == 1:
                    minstock = round(mjrverbr*1/104, 0) # < 3 days deliverytime
                elif row[3] == 2:
                    minstock = round(mjrverbr*1/52, 0) # < 1 week deliverytime
                elif row[3] == 3:
                    minstock = round(mjrverbr*1/26, 0) # < 2 weeks deliverytime
                elif row[3] == 4:
                    minstock = round(mjrverbr*1/17, 0) # < 3 weeks deliverytime
                elif row[3] == 5:
                    minstock = round(mjrverbr*2/17, 0) # < 6 weeks deliverytime
                elif row[3] == 6:
                    minstock = round(mjrverbr*4/17, 0) # < 12 weeks deliverytime
                elif row[3] == 7:
                    minstock = round(mjrverbr*8/17, 0) # < 26 weeks deliverytime
                elif row[3] == 8:
                    minstock = round(mjrverbr*16/17,0) # < 52 weeks deliverytime

                updart = update(articles).where(articles.c.barcode == row[0]).\
                    values(annual_consumption_1 = 0, minimum_stock = minstock, order_size = mordersize)
                con.execute(updart)

def articleRequest(mflag, btn):
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('short_descr', String),
        Column('item_price', Float),
        Column('selling_price', Float),
        Column('selling_contents', Float),
        Column('item_stock', Float),
        Column('item_unit', String),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('location_warehouse', String),
        Column('article_group', String),
        Column('thumbnail', String),
        Column('category', Integer),
        Column('order_balance', Float),
        Column('order_status', Boolean),
        Column('mutation_date', String),
        Column('annual_consumption_1', Float),
        Column('annual_consumption_2', Float),
        Column('VAT', String),
        Column('additional', Integer),
        Column('ordering_manual', Integer),
        Column('supplierID', Integer))
    article_grouplines = Table('article_grouplines', metadata,
        Column('lineID', Integer, primary_key=True),
        Column('grouplinetext', String))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    sel = select([articles])
    if con.execute(sel).fetchone():
        selarticles = select([articles]).order_by(articles.c.barcode)
        rparticles = con.execute(selarticles)
    else:
        message = "no records found!"
        alertText(message)
        return
 
    class Mainwindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(100, 50, 1800, 900)
            self.setWindowTitle('Articles requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.setItemDelegateForColumn(12, showImage(self))
            table_view.setColumnWidth(12, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            if mflag == 1 or mflag == 4:
                table_view.clicked.connect(defineButton)
            elif mflag == 2:
                table_view.clicked.connect(bookingLoss)
            else:
                table_view.clicked.connect(changeArticle)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
       
    class showImage(QStyledItemDelegate):  
           def __init__(self, parent):
               QStyledItemDelegate.__init__(self, parent)
           def paint(self, painter, option, index):        
                painter.fillRect(option.rect,QColor(255,255,255))
                image = QImage(index.data())
                pixmap = QPixmap(image)
                pixmap.scaled(256,256) 
                return(painter.drawPixmap(option.rect, pixmap))
                                       
    header = ['Barcode','Description','Short Description','Item-Price','Selling-Price',\
              'Selling-contents','Item-Stock','Item-Unit','Mininum-Stock','Order-Size',\
              'Location', 'Article_Group','Thumbnail','Category','Order-Balance',\
              'Order-Status','Mutation-Date','Annual-Consumption_1',\
              'Annual-Consumption_2','VAT','Additional','Ordering manual','SupplierID']    
        
    data_list=[]
    for row in rparticles:
        data_list += [(row)] 
    
    def defineButton(idx):
        mbarcode = idx.data()
        if idx.column() == 0 and mflag == 4:
            metadata = MetaData()
            buttons = Table('buttons', metadata,
                Column('buttonID', Integer, primary_key=True),
                Column('barcode', String),
                Column('buttontext', String),
                Column('accent', Integer),
                Column('bg_color', String))
            
            selbtn = select([buttons]).where(buttons.c.buttonID==btn)
            rpbtn = con.execute(selbtn).first()
               
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    
                    self.setWindowTitle("Button Text")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                           
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF")  
            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 1)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                    
                    #barcode
                    self.q1Edit = QLineEdit(str(mbarcode)) 
                    self.q1Edit.setFixedWidth(130)
                    self.q1Edit.setFont(QFont("Arial",10))
                    self.q1Edit.setStyleSheet("color: black")
                    self.q1Edit.setDisabled(True)
                    
                    #button-number
                    self.q2Edit = QLineEdit(str(rpbtn[0]))
                    self.q2Edit.setFixedWidth(40)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Consolas",10, 75))
                    reg_ex = QRegExp("^[0-9]{0,3}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    #button-text
                    self.q3Edit = QPlainTextEdit(rpbtn[2])
                    self.q3Edit.setFixedSize(170,100)
                    self.q3Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.q3Edit.setFont(QFont("Consolas",12,75))
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                        
                    #button background-color
                    self.q4Edit = QLineEdit(rpbtn[4])
                    self.q4Edit.setFixedWidth(80)
                    self.q4Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[#]{1}[a-fA-F0-9]{6}$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    
                    self.cBox = QCheckBox('Accentuation')
                    self.cBox.setFont(QFont("Arial",10))
                    if rpbtn[3]:
                        self.cBox.setChecked(True)
                          
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    def cboxChanged():
                        self.cBox.setCheckState(self.cBox.checkState())
                    self.cBox.stateChanged.connect(cboxChanged) 
                    
                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)
                    
                    lbl1 = QLabel('Barcodenummer')
                    lbl1.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl1, 1, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q1Edit, 1, 1)
                     
                    lbl2 = QLabel('Button-Number')
                    lbl2.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl2, 2, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q2Edit, 2, 1)
                    
                    lbl3 = QLabel('Button-Text')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 3, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q3Edit, 3, 1)
                    
                    lbl4 = QLabel('Button-color')
                    lbl4.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl4, 4, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q4Edit, 4, 1)
                    
                    grid.addWidget(self.cBox, 5, 1, 1, 1, Qt.AlignRight)
                                 
                    applyBtn = QPushButton('Insert')
                    applyBtn.clicked.connect(lambda: insBtnText())
                       
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                    grid.addWidget(applyBtn, 6, 1 , 1, 1, Qt.AlignRight)
                        
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close) 
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
                    grid.addWidget(cancelBtn, 6, 0, 1, 2, Qt.AlignCenter)
                    
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 7, 0, 1, 3, Qt.AlignCenter)
                   
                    def insBtnText():
                        maccent = self.cBox.checkState()
                        if self.cBox.checkState():
                            maccent = 1
                        else:
                            maccent = 0
                        if not self.q2Edit.text():
                            message = 'No buttonnumber filled in!'
                            alertText(message)
                            return
                        else:
                            mbtnnr = int(self.q2Edit.text())
                        mbtntext = self.q3Edit.toPlainText()
                        if mbtntext.strip() == '':
                            updbtn = update(buttons).where(buttons.c.buttonID==mbtnnr).\
                             values(barcode='', buttontext='',accent=0,bg_color='#FFFFF0')
                            con.execute(updbtn)
                            message = 'Button released empty!'
                            actionOK(message)
                            self.close()
                        else:
                            mbtncolor = self.q4Edit.text()
                            if len(mbtncolor) < 7:
                                mbtncolor = '#FFFFF0'
                            mlist = mbtntext.split('\n')
                            for line in mlist:
                                 if len(line) > 14:
                                     message = 'No more then 14 characters per line allowed'
                                     alertText(message)
                                     break
                                 elif len(mlist) > 4:
                                     message= 'No more then 4 lines allowed!'
                                     alertText(message)
                                     break
                            else:
                                updbtn = update(buttons).where(buttons.c.buttonID==mbtnnr).\
                                 values(barcode=str(mbarcode),buttontext=mbtntext,\
                                  bg_color=mbtncolor,accent=maccent)
                                con.execute(updbtn)
                                message = 'Productbutton text / color changed!'
                                actionOK(message)
                                self.close()
                                            
                    self.setLayout(grid)
                    self.setGeometry(900, 200, 150, 100)
    
            window = Widget()
            window.exec_()
            
    def changeArticle(idx):
        mbarcode = idx.data() 
        if idx.column() == 0:
            selarticle = select([articles]).where(articles.c.barcode == mbarcode)
            rparticle = con.execute(selarticle).first()
            sellines = select([article_grouplines]).order_by(article_grouplines.c.lineID)
            rplines = con.execute(sellines)
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    
                    self.setWindowTitle("Article Change")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                           
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF")  
            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 3, 1 ,1, Qt.AlignRight)
                    
                    #barcode
                    self.q1Edit = QLineEdit(str(mbarcode)) 
                    self.q1Edit.setFixedWidth(130)
                    self.q1Edit.setFont(QFont("Arial",10))
                    self.q1Edit.setStyleSheet("color: black")
                    self.q1Edit.setDisabled(True)
                                   
                    #additional product
                    self.cBox = QCheckBox('Additional product')
                    self.cBox.setFont(QFont("Arial", 10))
                    if rparticle[20]:
                        self.cBox.setChecked(True)
        
                    #description
                    self.q2Edit = QLineEdit(rparticle[1])    
                    self.q2Edit.setFixedWidth(400)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{1,50}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    #short-description
                    self.q2aEdit = QLineEdit(rparticle[2])    
                    self.q2aEdit.setFixedWidth(150)
                    self.q2aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2aEdit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{1,15}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2aEdit)
                    self.q2aEdit.setValidator(input_validator)
                   
                    #item_price
                    self.q3Edit = QLineEdit(str(round(rparticle[3],2)))
                    self.q3Edit.setAlignment(Qt.AlignRight)
                    self.q3Edit.setFixedWidth(100)
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q3Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q3Edit)
                    self.q3Edit.setValidator(input_validator)
                    
                    #selling-price
                    self.q3aEdit = QLineEdit(str(round(rparticle[4],2)))
                    self.q3aEdit.setAlignment(Qt.AlignRight)
                    self.q3aEdit.setFixedWidth(100)
                    self.q3aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q3aEdit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q3aEdit)
                    self.q3aEdit.setValidator(input_validator)
                    
                    #selling-contents
                    self.q3bEdit = QLineEdit(str(round(rparticle[5],3)))
                    self.q3bEdit.setAlignment(Qt.AlignRight)
                    self.q3bEdit.setFixedWidth(100)
                    self.q3bEdit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q3bEdit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q3bEdit)
                    self.q3bEdit.setValidator(input_validator)
                    
                    #item_stock
                    self.q4Edit = QLineEdit(str(round(rparticle[6],2)))
                    self.q4Edit.setAlignment(Qt.AlignRight)
                    self.q4Edit.setFixedWidth(100)
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q4Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
                    
                    #item_unit
                    self.q5Edit = QComboBox()
                    self.q5Edit.setFixedWidth(170)
                    self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q5Edit.setFont(QFont("Arial",10))
                    self.q5Edit.addItem('piece')
                    self.q5Edit.addItem('100')
                    self.q5Edit.addItem('meter')
                    self.q5Edit.addItem('kg')
                    self.q5Edit.addItem('carton 1 ltr')
                    self.q5Edit.addItem('bottle 1 ltr')
                    self.q5Edit.addItem('bottle 0.75 ltr')
                    self.q5Edit.addItem('bottle 0.5 ltr')
                    self.q5Edit.addItem('bottle 0.33 ltr')
                    self.q5Edit.addItem('bottle 0.25 ltr')
                    self.q5Edit.addItem('m²')
                    self.q5Edit.addItem('m³')
                    self.q5Edit.setCurrentIndex(self.q5Edit.findText(rparticle[7]))
                    
                    #minimum stock
                    self.q6Edit = QLineEdit(str(round(rparticle[8],2)))
                    self.q6Edit.setAlignment(Qt.AlignRight)
                    self.q6Edit.setFixedWidth(100)
                    self.q6Edit.setFont(QFont("Arial",10))
                    self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q6Edit)
                    self.q6Edit.setValidator(input_validator)
        
                    #order_size
                    self.q7Edit = QLineEdit(str(round(rparticle[9],2)))
                    self.q7Edit.setAlignment(Qt.AlignRight)
                    self.q7Edit.setFixedWidth(100)
                    self.q7Edit.setFont(QFont("Arial",10))
                    self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q7Edit)
                    self.q7Edit.setValidator(input_validator)
                    
                    #ordering_manual
                    self.cBoxord = QCheckBox('Ordering - Generate (off) / Manual (on)')
                    self.cBoxord.setFont(QFont("Arial",10))
                    if rparticle[21]:
                        self.cBoxord.setChecked(True)
     
                    #supplier ID
                    self.q7aEdit = QLineEdit(str(rparticle[22]))
                    self.q7aEdit.setFixedWidth(100)
                    self.q7aEdit.setFont(QFont("Arial",10))
                    self.q7aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0-9]{0,8}$")
                    input_validator = QRegExpValidator(reg_ex, self.q7aEdit)
                    self.q7Edit.setValidator(input_validator)
                                
                    #location
                    self.q8Edit = QLineEdit(rparticle[10])
                    self.q8Edit.setFixedWidth(100)
                    self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q8Edit.setFont(QFont("Arial",10))
                                
                    # article_group
                    self.q9Edit = QComboBox()
                    self.q9Edit.setFixedWidth(260)
                    self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q9Edit.setFont(QFont("Arial",10))
                    for row in rplines:
                        if row[1]:
                            self.q9Edit.addItem(row[1])
                    self.q9Edit.setCurrentIndex(self.q9Edit.findText(rparticle[11]))
                        
                    #thumbnail
                    self.q10Edit = QLineEdit(rparticle[12])
                    self.q10Edit.setFixedWidth(200)
                    self.q10Edit.setFont(QFont("Arial",10))
                    self.q10Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                                
                    #category
                    self.q11Edit = QComboBox()
                    self.q11Edit.setFixedWidth(260)
                    self.q11Edit.setFont(QFont("Arial",10))
                    self.q11Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q11Edit.addItem('0. Daily fresh products.')
                    self.q11Edit.addItem('1. Stock-driven < 3 days.')
                    self.q11Edit.addItem('2. Stock-driven < 1 weeks.')
                    self.q11Edit.addItem('3. Stock-driven < 2 weeks.')
                    self.q11Edit.addItem('4. Stock-driven < 3 weeks.')
                    self.q11Edit.addItem('5. Stock-driven < 6 weken')
                    self.q11Edit.addItem('6. Stock-driven < 12 weeks')
                    self.q11Edit.addItem('7. Stock-driven < 26 weeks')
                    self.q11Edit.addItem('8. Stock-driven < 52 weeks')
                    self.q11Edit.setCurrentIndex(rparticle[13])
         
                    #vat
                    self.q12Edit = QComboBox()
                    self.q12Edit.setFixedWidth(100)
                    self.q12Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q12Edit.setFont(QFont("Arial",10))
                    self.q12Edit.addItem('high')
                    self.q12Edit.addItem('low')
                    self.q12Edit.addItem('zero')
                    self.q12Edit.setCurrentIndex(self.q12Edit.findText(rparticle[19]))
                    
                    #order-balance
                    self.q13Edit = QLineEdit(str(round(rparticle[14],2)))
                    self.q13Edit.setFixedWidth(100)
                    self.q13Edit.setAlignment(Qt.AlignRight)
                    self.q13Edit.setStyleSheet('color: black')
                    self.q13Edit.setFont(QFont("Arial",10))
                    self.q13Edit.setDisabled(True)
                    
                    #order_status
                    self.q14Edit = QLineEdit(str(bool(rparticle[15])))
                    self.q14Edit.setFixedWidth(100)
                    self.q14Edit.setStyleSheet('color: black')
                    self.q14Edit.setFont(QFont("Arial",10))
                    self.q14Edit.setDisabled(True)
                                      
                    def cboxChanged():
                        self.cBox.setCheckState(self.cBox.checkState())
                    self.cBox.stateChanged.connect(cboxChanged)
                   
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    def q2aChanged():
                        self.q2aEdit.setText(self.q2aEdit.text())
                    self.q2aEdit.textChanged.connect(q2aChanged)
                    
                    def q3Changed():
                        self.q3Edit.setText(self.q3Edit.text())
                    self.q3Edit.textChanged.connect(q3Changed)
                    
                    def q3aChanged():
                        self.q3aEdit.setText(self.q3aEdit.text())
                    self.q3Edit.textChanged.connect(q3aChanged)
                    
                    def q3bChanged():
                        self.q3bEdit.setText(self.q3bEdit.text())
                    self.q3bEdit.textChanged.connect(q3bChanged)
                    
                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)
                    
                    def q5Changed():
                        self.q5Edit.setCurrentText(self.q5Edit.currentText()) 
                    self.q5Edit.currentIndexChanged.connect(q5Changed)
                    
                    def q6Changed():
                        self.q6Edit.setText(self.q6Edit.text())
                    self.q6Edit.textChanged.connect(q6Changed)
                    
                    def q7Changed():
                        self.q7Edit.setText(self.q7Edit.text())
                    self.q7Edit.textChanged.connect(q7Changed)
                    
                    def cboxordChanged():
                        self.cBoxord.setCheckState(self.cBoxord.checkState())
                    self.cBoxord.stateChanged.connect(cboxordChanged)
                    
                    def q7aChanged():
                        self.q7aEdit.setText(self.q7aEdit.text())
                        self.q7aEdit.textChanged.connect(q7aChanged)
                    
                    def q8Changed():
                        self.q8Edit.setText(self.q8Edit.text())
                    self.q8Edit.textChanged.connect(q8Changed)
                    
                    def q9Changed():
                        self.q9Edit.setCurrentText(self.q9Edit.currentText()) 
                    self.q9Edit.currentIndexChanged.connect(q9Changed)
                    
                    def q10Changed():
                        self.q10Edit.setText(self.q10Edit.text())
                    self.q10Edit.textChanged.connect(q10Changed)
                    
                    def q11Changed():
                        self.q11Edit.setCurrentIndex(self.q11Edit.currentIndex())
                    self.q11Edit.currentIndexChanged.connect(q11Changed)
                    
                    def q12Changed():
                        self.q5Edit.setCurrentText(self.q12Edit.currentText()) 
                    self.q12Edit.currentIndexChanged.connect(q12Changed)
    
                    lblhead = QLabel('Changing articles')
                    lblhead.setFont(QFont("Arial", 12))
                    grid.addWidget(lblhead, 0, 1, 1, 3, Qt.AlignCenter)
                   
                    grid.addWidget(QLabel('Barcodenumber'), 1, 0)
                    grid.addWidget(self.q1Edit, 1, 1)
                    
                    grid.addWidget(self.cBox, 1, 2, 1, 2)
                    
                    grid.addWidget(QLabel('Description'), 2, 0)
                    grid.addWidget(self.q2Edit, 2, 1 ,1 ,2)
                    
                    grid.addWidget(QLabel('Short-Description'), 3, 0)
                    grid.addWidget(self.q2aEdit, 3, 1)
                     
                    grid.addWidget(QLabel('Item_Price'), 3, 2)
                    grid.addWidget(self.q3Edit, 3, 3)
                    
                    grid.addWidget(QLabel('Selling-Price'), 4, 0)
                    grid.addWidget(self.q3aEdit, 4, 1)
                    
                    grid.addWidget(QLabel('Selling-contents'), 4, 2)
                    grid.addWidget(self.q3bEdit, 4, 3)
                    
                    grid.addWidget(QLabel('Item-Unit'), 5, 0)
                    grid.addWidget(self.q5Edit, 5, 1)
                    
                    grid.addWidget(QLabel('Minimum_Stock'), 5, 2)
                    grid.addWidget(self.q6Edit, 5, 3)
                    
                    grid.addWidget(QLabel('Order-Size'), 6, 0)
                    grid.addWidget(self.q7Edit, 6, 1)
                    
                    grid.addWidget(self.cBoxord, 6, 2, 1 , 2)
                  
                    grid.addWidget(QLabel('Item-Stock'), 7, 0)
                    grid.addWidget(self.q4Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Location'), 7, 2)
                    grid.addWidget(self.q8Edit, 7, 3)
                    
                    grid.addWidget(QLabel('Articlegroup'), 8, 0)
                    grid.addWidget(self.q9Edit, 8, 1)
                    
                    grid.addWidget(QLabel('Thumbnail'), 8, 2)
                    grid.addWidget(self.q10Edit, 8, 3)
                    
                    grid.addWidget(QLabel('Category'), 9, 0)
                    grid.addWidget(self.q11Edit, 9, 1)
                    
                    grid.addWidget(QLabel('VAT'), 9, 2)
                    grid.addWidget(self.q12Edit, 9, 3)
                    
                    grid.addWidget(QLabel('Suppliernumber'), 10, 0)
                    grid.addWidget(self.q7aEdit, 10, 1)
                    
                    grid.addWidget(QLabel('Order-Balance'), 10, 2)
                    grid.addWidget(self.q13Edit, 10, 3)
                    
                    grid.addWidget(QLabel('Order-Status'), 11, 2 )
                    grid.addWidget(self.q14Edit, 11, 3)     
          
                    def updArticle(self):
                        mdescr = self.q2Edit.text()
                        mshort = self.q2aEdit.text()
                        mprice = float(self.q3Edit.text())
                        msellprice = float(self.q3aEdit.text())
                        msellcontents = float(self.q3bEdit.text())
                        mstock = float(self.q4Edit.text())
                        munit = self.q5Edit.currentText()
                        mminstock = float(self.q6Edit.text())
                        morder_size = float(self.q7Edit.text())
                        mlocation = self.q8Edit.text()
                        martgroup = self.q9Edit.currentText()
                        mthumb = self.q10Edit.text()
                        mcategory = self.q11Edit.currentIndex()
                        mvat = self.q12Edit.currentText()
                        msupplier = self.q7aEdit.text()
                        if self.cBox.checkState():
                            madd = 1
                        else:
                            madd = 0
                        if self.cBoxord.checkState():
                            morderstate = 1
                        else:
                            morderstate = 0
                        updarticle = update(articles).where(articles.c.barcode==mbarcode)\
                          .values(barcode=mbarcode,description=mdescr,short_descr=mshort,\
                            item_price=mprice,selling_price=msellprice,selling_contents=\
                            msellcontents,item_stock=mstock,item_unit=munit,\
                            minimum_stock=mminstock,order_size=morder_size, \
                            location_warehouse=mlocation,article_group=martgroup,\
                            thumbnail=mthumb,category=mcategory,VAT=mvat, additional = madd,\
                            ordering_manual = morderstate, supplierID=msupplier)
                        con.execute(updarticle)
                        message = 'Article changes succeeded!'
                        actionOK(message)
                        self.close()
                        
                    def prepareEan(self):
                        ean = barcode.get('ean13', str(mbarcode[:13]), writer=ImageWriter()) # for barcode as png
                        self.mbarcode = ean.get_fullcode()
                        self.path = '.\\Barcodes\\Articles\\'
                        if sys.platform == 'win32':
                            self.path = '.\\Barcodes\\Articles\\'
                            ean.save(self.path+self.mbarcode)
                        else:
                            self.path ='./Barcodes/Articles/'
                            ean.save(self.path+self.mbarcode)
                        x1 = 372.9
                        y1 = 228.5
                        printEan(self, x1 , y1)
                                 
                    applyBtn = QPushButton('Update')
                    applyBtn.clicked.connect(lambda: updArticle(self))
            
                    grid.addWidget(applyBtn, 12, 3, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(90)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                    
                    grid.addWidget(cancelBtn, 12, 3)
                    
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(90)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    printBtn = QPushButton('Print Barcode')
                    printBtn.clicked.connect(lambda: prepareEan(self))
                    
                    grid.addWidget(printBtn, 12, 2)
                    printBtn.setFont(QFont("Arial",10))
                    printBtn.setFixedWidth(120)
                    printBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 13, 0, 1, 4, Qt.AlignCenter)
             
                    self.setLayout(grid)
                    self.setGeometry(500, 200, 150, 100)
         
            window = Widget()
            window.exec_()
            
    def bookingLoss(idx):
        mbarcode = idx.data()
        if idx.column()==0:
            sel = select([articles]).where(articles.c.barcode == mbarcode)
            rp = con.execute(sel).first()
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Booking loss articles")
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                            Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                    self.setFont(QFont('Arial', 10))
                    
                    q1Edit = QLineEdit(mbarcode)
                    q1Edit.setFixedWidth(130)
                    q1Edit.setFont(QFont("Arial", 10))
                    q1Edit.setStyleSheet("color: black")
                    q1Edit.setDisabled(True)
                                    
                    #Loss description
                    qloss = QComboBox()
                    qloss.setFixedWidth(230)
                    qloss.setFont(QFont("Arial", 10))
                    qloss.setStyleSheet("color: black;  background-color: #F8F7EE")
                    qloss.addItem('Obsolete')
                    qloss.addItem('Warehouse differences.')
                    qloss.addItem('Damaged')
                    qloss.addItem('Shelf Life')
                           
                    #number
                    qnumber = QLineEdit('-')
                    qnumber.setFixedWidth(150)
                    qnumber.setFont(QFont("Arial",10))
                    qnumber.setStyleSheet("color: black;  background-color: #F8F7EE")
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, qnumber)
                    qnumber.setValidator(input_validator)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                                  
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                    
                    lbl1 = QLabel('Barcodenumber')  
                    lbl1.setFont(QFont("Arial",10))
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(q1Edit, 1, 1)
                    
                    lbl2 = QLabel('Loss description')  
                    lbl2.setFont(QFont("Arial",10))
                    grid.addWidget(lbl2, 2, 0)
                    grid.addWidget(qloss, 2, 1)
                            
                    lbl3 = QLabel('Number')  
                    lbl3.setFont(QFont("Arial",10))
                    grid.addWidget(lbl3, 3, 0)
                    grid.addWidget(qnumber, 3, 1)
                           
                    def qlossChanged():
                        qloss.setCurrentText(qloss.currentText())
                    qloss.currentIndexChanged.connect(qlossChanged)
                    
                    def qnumberChanged():
                        qnumber.setText(qnumber.text())
                    qnumber.textChanged.connect(qnumberChanged)
                    
                    def insertLoss():
                        metadata = MetaData()
                        loss = Table('loss', metadata,
                           Column('lossID', Integer, primary_key=True),
                           Column('barcode', String),
                           Column('number', Float),
                           Column('bookdate', String),
                           Column('category', String),
                           Column('item_price', Float),
                           Column('description', String))
                        
                        mcategory = qloss.currentText()
                        mnumber = qnumber.text()
                        mprice = rp[3]
                        mdescription = rp[1]
                        try:
                            lossnr = con.execute(select([func.max(loss.c.lossID, type_=Integer)])).scalar()
                            lossnr += 1
                        except:
                            lossnr = 1
                        mbookdate= str(datetime.datetime.now())[0:10]
                        
                        if not(mnumber == '-' or mnumber == '-0'):               
                            ins = insert(loss).values(lossID = lossnr, barcode = mbarcode,\
                                number = mnumber, category = mcategory, bookdate = mbookdate,
                                item_price = mprice, description = mdescription)
                            con.execute(ins)
                            upd = update(articles).where(articles.c.barcode == mbarcode).\
                              values(item_stock = articles.c.item_stock + mnumber)
                            con.execute(upd)
                            message = 'Booking loss succeeded!'
                            actionOK(message)
                            self.close()
                        else:
                            message = 'Not valid amount!'
                            alertText(message)
                            self.close()
                                                     
                    self.setLayout(grid)
                    self.setGeometry(600, 200, 150, 150)
            
                    applyBtn = QPushButton('Change')
                    applyBtn.clicked.connect(lambda: insertLoss())
            
                    grid.addWidget(applyBtn, 4, 1, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                   
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close) 
                    
                    grid.addWidget(cancelBtn, 4, 1)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    lbl4 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl4.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl4, 6, 0, 1, 2, Qt.AlignCenter)     
              
            win = Widget()
            win.exec_()
            
    win = Mainwindow(data_list, header)
    win.exec_()
    
def salesRequest():
    metadata = MetaData()
    sales = Table('sales', metadata,
        Column('salesID', Integer, primary_key=True),
        Column('receiptnumber', Integer),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('selling_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    sel = select([sales])
    if con.execute(sel).fetchone():
        selsales = select([sales]).order_by(sales.c.receiptnumber)
        rpsales = con.execute(selsales)
    else:
        message = "No records found!"
        alertText(message)
        return
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(100, 50, 1300, 900)
            
            self.setWindowTitle('Sales requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
                                       
    header = ['ID','Receiptnummber','Barcode','Description','Number',\
              'Selling-price','Sub-Total','Sub-Vat','Callname','Mutation-date']      
        
    data_list=[]
    for row in rpsales:
        data_list += [(row)]
                                    
    win = MyWindow(data_list, header)
    win.exec_()
    
def additionRequest():
    metadata = MetaData()
    addition = Table('addition', metadata,
        Column('addID', Integer, primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('item_price', Float),
        Column('number', Float),
        Column('item_unit', String),
        Column('article_group', String),
        Column('location_warehouse', String))
    
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
    con = engine.connect()
    sel = select([addition])
    if con.execute(sel).fetchone():
        seladd = select([addition]).order_by(addition.c.article_group, addition.c.barcode)
        rpadd = con.execute(seladd) 
    else:
        message = 'No records found!'
        alertText(message)
        return
     
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(500, 50, 900, 900)
            self.setWindowTitle('Sales requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
            
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
    
    header = ['addID','Barcode','Description','Item-price','Number',\
              'Item_unit','Article_Group','Location-Warehouse'] 
        
    data_list=[]
    for row in rpadd:
        data_list += [(row)] 
 
    win = MyWindow(data_list, header)
    win.exec_()
               
def paymentsRequest():
    metadata = MetaData()
    payments = Table('payments', metadata,
        Column('payID', Integer, primary_key=True),
        Column('kind', String),
        Column('amount', Float),
        Column('bookdate', String),
        Column('paydate', String),
        Column('instance', String),
        Column('accountnumber', String),
        Column('ovorderID', Integer))
 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    sel = select([payments])
    if con.execute(sel).fetchone():
        selpay = select([payments]).order_by(payments.c.paydate, payments.c.ovorderID)
        rppay = con.execute(selpay)
    else:
        message = 'No records found!'
        alertText(message)
        return
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(500, 50, 900, 900)
            self.setWindowTitle('Sales requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
            table_view.clicked.connect(showSelection)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
    
    header = ['payID','Kind','Amount','Bookdate','Paydate',\
              'Instance','Accountnumber','Receiptnumber']                                       
        
    data_list=[]
    for row in rppay:
        data_list += [(row)] 
        
    def showSelection(idx):
        mpaynr = idx.data()
        if idx.column()==0:
            selp = select([payments]).where(payments.c.payID == mpaynr)
            rpp = con.execute(selp).first()
                      
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    self.setWindowTitle("Payments instances")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                           
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF") 
                
                    grid = QGridLayout()
                    grid.setSpacing(20)
                                                        
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                    
                    #kind
                    q1Edit = QLineEdit(rpp[1])
                    q1Edit.setFixedWidth(250)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                                    
                    #amount
                    q2Edit = QLineEdit(str(round(float(rpp[2]),2)))
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setFixedWidth(150)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                     
                    #bookdate
                    q3Edit = QLineEdit(str(rpp[3]))
                    q3Edit.setFixedWidth(150)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                    
                    #paydate
                    q4Edit = QLineEdit(str(rpp[4]))
                    q4Edit.setFixedWidth(150)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                                 
                    #instance
                    q5Edit = QLineEdit(rpp[5])
                    q5Edit.setFixedWidth(250)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                      
                    #accountnumber
                    q9Edit = QLineEdit(str(rpp[6]))
                    q9Edit.setFixedWidth(250)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                                     
                    #receiptnumber)
                    q12Edit = QLineEdit(str(rpp[7]))
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setFixedWidth(150)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)    
                            
                    lbl3 = QLabel('Kind')  
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(q1Edit, 2, 1)
                                                         
                    lbl4 = QLabel('Amount')  
                    lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(q2Edit, 3, 1)
                    
                    lbl5 = QLabel('Bookdate')  
                    lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(q3Edit, 4, 1)
                    
                    lbl6 = QLabel('Paydate')  
                    lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl6, 5, 0)
                    grid.addWidget(q4Edit, 5, 1)
                    
                    lbl7 = QLabel('Pay')
                    lbl7.setFont(QFont("Arial",10))
                    grid.addWidget(lbl7, 6, 0, 1, 1, Qt.AlignRight)
                         
                    self.cBox = QCheckBox()
                    self.cBox.setStyleSheet('color: black; background-color: #F8F7EE')
                    grid.addWidget(self.cBox, 6, 1)
                    if len(rpp[4])==10:
                        lbl7 = QLabel('Payed')
                        lbl7.setFont(QFont("Arial",10))
                        grid.addWidget(lbl7, 6, 0, 1, 1, Qt.AlignRight)
                        self.cBox.setStyleSheet('color: black')
                        self.cBox.setEnabled(False)
                        
                    def cboxChanged():
                        self.cBox.setCheckState(self.cBox.checkState())
                    self.cBox.stateChanged.connect(cboxChanged)
                    
                    def updPayment(self):
                        mstatus = self.cBox.checkState()
                        if mstatus:
                            mpaydate = str(datetime.datetime.now())[0:10]
                            updpay = update(payments).where(payments.c.payID == mpaynr).\
                            values(paydate = mpaydate)
                            con.execute(updpay)
                            message = 'Payment succeeded!'
                            actionOK(message)
                            self.close()
                        else:
                            message = 'Not all fields are filled in!'
                            alertText(message)
                            self.close()
                                                                               
                    lbl7 = QLabel('Instance')  
                    lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl7, 7, 0)
                    grid.addWidget(q5Edit, 7, 1, 1, 2)
                     
                    lbl20 = QLabel('Accountnumber')  
                    lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl20, 10, 0)
                    grid.addWidget(q9Edit, 10, 1, 1, 2)
                          
                    lbl23 = QLabel('Receiptnumber')  
                    lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl23, 13, 0)
                    grid.addWidget(q12Edit, 13, 1)
                   
                    payBtn = QPushButton('Paying')
                    payBtn.clicked.connect(lambda: updPayment(self))
            
                    grid.addWidget(payBtn, 14, 1, 1 , 1, Qt.AlignRight)
                    payBtn.setFont(QFont("Arial",10))
                    payBtn.setFixedWidth(100)
                    payBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    closeBtn = QPushButton('Close')
                    closeBtn.clicked.connect(self.close)
            
                    grid.addWidget(closeBtn, 14, 1)
                    closeBtn.setFont(QFont("Arial",10))
                    closeBtn.setFixedWidth(100)
                    closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 15, 0, 1, 2, Qt.AlignCenter)
                    
                    self.setLayout(grid)
                    self.setGeometry(600, 200, 150, 150)
                    
            window = MainWindow()
            window.exec_()
                                     
    win = MyWindow(data_list, header)
    win.exec_()
    
def emplAccess():
    metadata = MetaData()
    employees = Table('employees', metadata,
         Column('barcodeID', String, primary_key=True),
         Column('firstname', String),
         Column('lastname', String),
         Column('access', Integer),
         Column('callname', String))
        
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
    con = engine.connect()
    while True:
        inlognr = random.randint(0, 99999)
        inlogstr = str(int(2400000+inlognr))
        ean = barcode.get('ean8', inlogstr, writer=ImageWriter()) # for barcode as png
        mbarcode = ean.get_fullcode()
        
        selbarc = select([employees]).where(employees.c.barcodeID==mbarcode)
        rpbarc = con.execute(selbarc).first()
        if not rpbarc:
            if sys.platform == 'win32':
               ean.save('.\\Barcodes\\employees\\'+str(mbarcode))
               break
            else:
               ean.save('./Barcodes/employees/'+str(mbarcode))
               break
           
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            
            self.setWindowTitle("Access employees")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")  
    
            grid = QGridLayout()
            grid.setSpacing(20)
            
            self.mbarcode = mbarcode
            
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            q1Edit = QLineEdit(str(self.mbarcode))
            q1Edit.setFixedWidth(100)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.setStyleSheet("color: black")
            q1Edit.setDisabled(True)
                            
            q2Edit = QLineEdit()     #firstname
            q2Edit.setFixedWidth(200)
            q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            q2Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^.{1,20}$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)
             
            q3Edit = QLineEdit()   #lastname
            q3Edit.setFixedWidth(200)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^.{1,20}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
             
            q4Edit = QLineEdit()   #callname
            q4Edit.setFixedWidth(200)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^.{1,20}$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
            
            q5Edit = QLineEdit('1')   #access
            q5Edit.setFixedWidth(30)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0123]{1}$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
            
            def q2Changed():
                q2Edit.setText(q2Edit.text())
            q2Edit.textChanged.connect(q2Changed)
             
            def q3Changed():
                q3Edit.setText(q3Edit.text())
            q3Edit.textChanged.connect(q3Changed)  
            
            def q4Changed():
                q4Edit.setText(q4Edit.text())
            q4Edit.textChanged.connect(q4Changed)  
            
            def q5Changed():
                q5Edit.setText(q5Edit.text())
            q5Edit.textChanged.connect(q5Changed)

            lbl1 = QLabel('Employee-barcode')
            lbl1.setFont(QFont("Arial", 10))
            grid.addWidget(lbl1, 4, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q1Edit, 4, 1)
                      
            lbl2 = QLabel('First name')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 5, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q2Edit, 5, 1)
            
            lbl3 = QLabel('Last name')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 6, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q3Edit, 6, 1)
            
            lbl4 = QLabel('Call name')
            lbl4.setFont(QFont("Arial", 10))
            grid.addWidget(lbl4, 7, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q4Edit, 7, 1)
            
            lbl5 = QLabel('Access level')
            lbl5.setFont(QFont("Arial", 10))
            grid.addWidget(lbl5, 8, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q5Edit, 8, 1)
            
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insertacc())
               
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(applyBtn,9, 2, 1 , 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close) 
    
            grid.addWidget(cancelBtn, 9, 1, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 10, 0, 1, 3, Qt.AlignCenter)
          
            def insertacc():
                fname = q2Edit.text()
                lname = q3Edit.text()
                cname = q4Edit.text()
                maccess = q5Edit.text()
                if fname and lname and cname:
                    insacc = insert(employees).values(barcodeID = str(self.mbarcode),\
                       firstname = fname, lastname = lname,\
                       callname = cname, access = int(maccess))
                    con.execute(insacc)
                  
                    self.path = './Barcodes/employees/'
                    x1 = 267.3
                    y1 = 213.1
                    printEan(self, x1, y1)
                    self.close()
                else:
                    message = 'Not all fields are filled in!'
                    alertText(message)
                    self.close() 
           
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)
            
    window = Widget()
    window.exec_()
    
def existingBarcode():
    mflag = 1
    btn = 0
    articleRequest(mflag, btn)
    
def insertArticles():
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('short_descr', String),
        Column('item_price', Float),
        Column('selling_price', Float),
        Column('selling_contents', Float),
        Column('item_stock', Float),
        Column('item_unit', String),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('location_warehouse', String),
        Column('article_group', String),
        Column('thumbnail', String),
        Column('category', Integer),
        Column('order_balance', Float),
        Column('order_status', Boolean),
        Column('mutation_date', String),
        Column('annual_consumption_1', Float),
        Column('annual_consumption_2', Float),
        Column('VAT', String),
        Column('additional', Integer),
        Column('supplierID', Integer),
        Column('ordering_manual', Integer))
    article_grouplines = Table('article_grouplines', metadata,
        Column('lineID', Integer, primary_key=True),
        Column('grouplinetext', String))
 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    try:
        mbarcode=(con.execute(select([func.max(articles.c.barcode, type_=String)])\
                        .where(articles.c.barcode.like('28'+'%'))).scalar())
        mbarcode = int(str(mbarcode[:12]))+1
        ean = barcode.get('ean13',str(mbarcode), writer=ImageWriter()) #for barcode as png
        mbarcode = ean.get_fullcode()
    except:
        mbarcode = 280000000001
        ean = barcode.get('ean13',str(mbarcode), writer=ImageWriter()) #for barcode as png
        mbarcode = ean.get_fullcode()
    sellines = select([article_grouplines]).order_by(article_grouplines.c.lineID)  
    rplines = con.execute(sellines)
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            
            self.setWindowTitle("Articles new insert")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")  
    
            grid = QGridLayout()
            grid.setSpacing(20)
            
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 3, 1 ,1, Qt.AlignRight)
            
            lblhead = QLabel('Insert new articles')
            lblhead.setFont(QFont("Arial", 12))
            grid.addWidget(lblhead, 0, 1, 1, 3, Qt.AlignCenter)
            
            #barcode
            self.q1Edit = QLineEdit(str(mbarcode)) 
            self.q1Edit.setFixedWidth(130)
            self.q1Edit.setFont(QFont("Arial",10))
            self.q1Edit.setStyleSheet("color: black")
            self.q1Edit.setDisabled(True)
 
            #description
            self.q2Edit = QLineEdit()    
            self.q2Edit.setFixedWidth(400)
            self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q2Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^.{1,50}$")
            input_validator = QRegExpValidator(reg_ex, self.q2Edit)
            self.q2Edit.setValidator(input_validator)
            
            #short
            self.q2aEdit = QLineEdit()    
            self.q2aEdit.setFixedWidth(150)
            self.q2aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q2aEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^.{1,15}$")
            input_validator = QRegExpValidator(reg_ex, self.q2aEdit)
            self.q2aEdit.setValidator(input_validator)
            
            #item_price
            self.q3Edit = QLineEdit('0')
            self.q3Edit.setFixedWidth(100)
            self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q3Edit)
            self.q3Edit.setValidator(input_validator)
            
            #selling_price
            self.q3aEdit = QLineEdit('0')
            self.q3aEdit.setFixedWidth(100)
            self.q3aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3aEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q3aEdit)
            self.q3aEdit.setValidator(input_validator)
            
            #selling_contents
            self.q3bEdit = QLineEdit('0')
            self.q3bEdit.setFixedWidth(100)
            self.q3bEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3bEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q3bEdit)
            self.q3bEdit.setValidator(input_validator)
            
            #item_unit
            self.q5Edit = QComboBox()
            self.q5Edit.setFixedWidth(170)
            self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q5Edit.setFont(QFont("Arial",10))
            self.q5Edit.addItem('piece')
            self.q5Edit.addItem('100')
            self.q5Edit.addItem('meter')
            self.q5Edit.addItem('kg')
            self.q5Edit.addItem('carton 1 ltr')
            self.q5Edit.addItem('bottle 1 ltr')
            self.q5Edit.addItem('bottle 0.75 ltr')
            self.q5Edit.addItem('bottle 0.5 ltr')
            self.q5Edit.addItem('bottle 0.33 ltr')
            self.q5Edit.addItem('bottle 0.25 ltr')
            self.q5Edit.addItem('m²')
            self.q5Edit.addItem('m³')
            
            #minimum stock
            self.q6Edit = QLineEdit('0')
            self.q6Edit.setFixedWidth(100)
            self.q6Edit.setFont(QFont("Arial",10))
            self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q6Edit)
            self.q6Edit.setValidator(input_validator)

            #order_size
            self.q7Edit = QLineEdit('0')
            self.q7Edit.setFixedWidth(100)
            self.q7Edit.setFont(QFont("Arial",10))
            self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q7Edit)
            self.q7Edit.setValidator(input_validator)
            
            #ordering_manual
            self.cBoxord = QCheckBox('Ordering - Generate (off) / Manual (on)')
            self.cBoxord.setFont(QFont("Arial",10))
            
            #supplier ID
            self.q7aEdit = QLineEdit('0')
            self.q7aEdit.setFixedWidth(100)
            self.q7aEdit.setFont(QFont("Arial",10))
            self.q7aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0-9]{0,8}$")
            input_validator = QRegExpValidator(reg_ex, self.q7aEdit)
            self.q7Edit.setValidator(input_validator)
                         
            #location
            self.q8Edit = QLineEdit()
            self.q8Edit.setFixedWidth(100)
            self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q8Edit.setFont(QFont("Arial",10))

            # article_group
            self.q9Edit = QComboBox()
            self.q9Edit.setFixedWidth(260)
            for row in rplines:
                if row[1]:
                    self.q9Edit.addItem(row[1])
            self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q9Edit.setFont(QFont("Arial",10))
                
            #thumbnail
            self.q10Edit = QLineEdit('./thumbs/')
            self.q10Edit.setFixedWidth(200)
            self.q10Edit.setFont(QFont("Arial",10))
            self.q10Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                        
            #category
            self.q11Edit = QComboBox()
            self.q11Edit.setFixedWidth(260)
            self.q11Edit.setFont(QFont("Arial",10))
            self.q11Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q11Edit.addItem('0. Daily fresh products.')
            self.q11Edit.addItem('1. Stock-driven < 3 days.')
            self.q11Edit.addItem('2. Stock-driven < 1 weeks.')
            self.q11Edit.addItem('3. Stock-driven < 2 weeks.')
            self.q11Edit.addItem('4. Stock-driven < 3 weeks.')
            self.q11Edit.addItem('5. Stock-driven < 6 weken')
            self.q11Edit.addItem('6. Stock-driven < 12 weeks')
            self.q11Edit.addItem('7. Stock-driven < 26 weeks')
            self.q11Edit.addItem('8. Stock-driven < 52 weeks') 
            
            #vat
            self.q12Edit = QComboBox()
            self.q12Edit.setFixedWidth(100)
            self.q12Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q12Edit.setFont(QFont("Arial",10))
            self.q12Edit.addItem('high')
            self.q12Edit.addItem('low')
            self.q12Edit.addItem('zero')
            
            #additional products
            self.cBox = QCheckBox('Additional product')
            self.cBox.setFont(QFont("Arial",10))
            
            #barcode overruled
            self.q13Edit = QLineEdit() 
            self.q13Edit.setFixedWidth(130)
            self.q13Edit.setFont(QFont("Arial",10))
            self.q13Edit.setStyleSheet("color: black; background-color: #F8F7EE")
            self.q13Edit.setSelection(0,13)
            
            def q1Changed():
                self.q1Edit.setText(self.q1Edit.text())
            self.q1Edit.textChanged.connect(q1Changed)
            
            def cboxChanged():
                self.cBox.setCheckState(self.cBox.checkState())
            self.cBox.stateChanged.connect(cboxChanged) 
           
            def q2Changed():
                self.q2Edit.setText(self.q2Edit.text())
            self.q2Edit.textChanged.connect(q2Changed)
            
            def q3Changed():
                self.q3Edit.setText(self.q3Edit.text())
            self.q3Edit.textChanged.connect(q3Changed)
            
            def q3aChanged():
                self.q3aEdit.setText(self.q3aEdit.text())
            self.q3aEdit.textChanged.connect(q3aChanged)
            
            def q3bChanged():
                self.q3bEdit.setText(self.q3bEdit.text())
            self.q3bEdit.textChanged.connect(q3bChanged)
            
            def q5Changed():
                self.q5Edit.setCurrentText(self.q5Edit.currentText()) #+1
            self.q5Edit.currentIndexChanged.connect(q5Changed)
            
            def q6Changed():
                self.q6Edit.setText(self.q6Edit.text())
            self.q6Edit.textChanged.connect(q6Changed)
            
            def q7Changed():
                self.q7Edit.setText(self.q7Edit.text())
            self.q7Edit.textChanged.connect(q7Changed)
            
            def q7aChanged():
                self.q7aEdit.setText(self.q7aEdit.text())
            self.q7aEdit.textChanged.connect(q7aChanged)
            
            def cboxordChanged():
                self.cBoxord.setCheckState(self.cBoxord.checkState())
            self.cBoxord.stateChanged.connect(cboxordChanged) 
            
            def q8Changed():
                self.q8Edit.setText(self.q8Edit.text())
            self.q8Edit.textChanged.connect(q8Changed)
            
            def q9Changed():
                self.q9Edit.setCurrentText(self.q9Edit.currentText()) #+1
            self.q9Edit.currentIndexChanged.connect(q9Changed)
            
            def q10Changed():
                self.q10Edit.setText(self.q10Edit.text())
            self.q10Edit.textChanged.connect(q10Changed)
            
            def q11Changed():
                self.q11Edit.setCurrentIndex(self.q11Edit.currentIndex())
            self.q11Edit.currentIndexChanged.connect(q11Changed)
            
            def q12Changed():
                self.q12Edit.setCurrentText(self.q12Edit.currentText()) 
            self.q12Edit.currentIndexChanged.connect(q12Changed)
            
            def q13Changed():
                self.q13Edit.setText(self.q13Edit.text()) 
            self.q13Edit.textChanged.connect(q13Changed)
            
            grid.addWidget(QLabel('Barcodenumber'), 1, 0)
            grid.addWidget(self.q1Edit, 1, 1)
            
            grid.addWidget(self.cBox, 1, 2, 1 , 2)
            
            grid.addWidget(QLabel('Description'), 2, 0)
            grid.addWidget(self.q2Edit, 2, 1 ,1 ,2)
            
            grid.addWidget(QLabel('Short Description'), 3, 0)
            grid.addWidget(self.q2aEdit, 3, 1)
            
            grid.addWidget(QLabel('Item_Price'), 3, 2)
            grid.addWidget(self.q3Edit, 3, 3)
            
            grid.addWidget(QLabel('Selling-Price'), 4, 0)
            grid.addWidget(self.q3aEdit, 4, 1)
            
            grid.addWidget(QLabel('Selling-Contents'), 4, 2)
            grid.addWidget(self.q3bEdit, 4, 3)
            
            grid.addWidget(QLabel('Item-Unit'), 5, 0)
            grid.addWidget(self.q5Edit, 5, 1)
            
            grid.addWidget(QLabel('Minimum_Stock'), 5, 2)
            grid.addWidget(self.q6Edit, 5, 3)
            
            grid.addWidget(QLabel('Order-Size'), 6, 0)
            grid.addWidget(self.q7Edit, 6, 1)
                       
            grid.addWidget(self.cBoxord, 6, 2, 1 , 2)
              
            grid.addWidget(QLabel('Location'), 7, 0)
            grid.addWidget(self.q8Edit, 7, 1)
            
            grid.addWidget(QLabel('Articlegroup'), 7, 2)
            grid.addWidget(self.q9Edit, 7, 3)
            
            grid.addWidget(QLabel('Thumbnail'), 8, 0)
            grid.addWidget(self.q10Edit, 8, 1)
            
            grid.addWidget(QLabel('Category'), 8, 2)
            grid.addWidget(self.q11Edit, 8, 3)
            
            grid.addWidget(QLabel('VAT'), 9, 0 )
            grid.addWidget(self.q12Edit, 9, 1)
            
            grid.addWidget(QLabel('Suppliernumber'), 9, 2)
            grid.addWidget(self.q7aEdit, 9, 3)
            
            grid.addWidget(QLabel('Barcode overruled by scanning'), 10, 0)
            grid.addWidget(self.q13Edit, 10, 1)
            grid.addWidget(QLabel('Fill all fields before scanning'), 10, 2)
            
            def insArticle(self):
                def writeArticle():
                    mdescr = self.q2Edit.text()
                    mshort = self.q2aEdit.text()
                    mprice = float(self.q3Edit.text())
                    msellprice = float(self.q3aEdit.text())
                    msellcontent = float(self.q3bEdit.text())
                    munit = self.q5Edit.currentText()
                    mminstock = float(self.q6Edit.text())
                    morder_size = float(self.q7Edit.text())
                    mlocation = self.q8Edit.text()
                    martgroup = self.q9Edit.currentText()
                    mthumb = self.q10Edit.text()
                    mcategory = self.q11Edit.currentIndex()+1
                    mvat = self.q12Edit.currentText()
                    msupplier = self.q7aEdit.text()
                    if self.cBox.checkState():
                        madd = 1
                    else:
                        madd = 0
                    if self.cBoxord.checkState():
                        morderstate = 1
                    else:
                        morderstate = 0
                    if mdescr and mshort and mprice and morder_size and mcategory:
                        insart = insert(articles).values(barcode=mbarcode,description=mdescr,\
                            short_descr=mshort,item_price=mprice,selling_price=msellprice,\
                            selling_contents=msellcontent,item_unit=munit, minimum_stock=mminstock,\
                            order_size=morder_size, location_warehouse=mlocation,\
                            article_group=martgroup,thumbnail=mthumb,\
                            category=mcategory,VAT=mvat, additional = madd,\
                            ordering_manual = morderstate, supplierID = msupplier)
                        con.execute(insart)
                        ean = barcode.get('ean13',str(mbarcode), writer=ImageWriter())
                        if sys.platform == 'win32':
                            ean.save('.\\Barcodes\\Articles\\'+str(mbarcode))
                        else:
                            ean.save('./Barcodes/Articles/'+str(mbarcode))
                        #x1 = 372.9
                        #y1 = 228.5
                        #printEan(self, x1, y1)
                        message =  "Insert succeeded"
                        actionOK(message)
                        self.close()
                    else:
                        message = 'Not all fields are filled in!'
                        alertText(message)
                        self.close()
                        
                if len(self.q13Edit.text())==13 and checkEan13(self.q13Edit.text()):
                    mbarcode = str(self.q13Edit.text())
                    writeArticle()
                elif len(self.q13Edit.text()) > 0:
                    message = 'Scan error occurred!'
                    alertText(message)
                else:
                    mbarcode = str(self.q1Edit.text())
                    writeArticle()
 
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insArticle(self))
    
            grid.addWidget(applyBtn, 11, 3, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(90)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)
            
            grid.addWidget(cancelBtn, 11, 3)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 12, 0, 1, 4, Qt.AlignCenter)
   
            self.setLayout(grid)
            self.setGeometry(800, 200, 150, 100)
 
    window = Widget()
    window.exec_()
     
def requestLoss():
    metadata = MetaData()
    loss = Table('loss', metadata,
       Column('lossID', Integer, primary_key=True),
       Column('barcode', String),
       Column('number', Float),
       Column('bookdate', String),
       Column('category', String),
       Column('item_price', Float),
       Column('description', String))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    sel = select([loss]).order_by(loss.c.category, loss.c.bookdate)
    if con.execute(sel).fetchone():
        selloss = select([loss]).order_by(loss.c.category, loss.c.bookdate)
        rploss = con.execute(selloss)
    else:
        message = "No records found!"
        alertText(message)
        return
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(600, 50, 1000, 800)
            self.setWindowTitle('Loss articles requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
                
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None

    header = ['ID','Barcode','Amount','Bookdate','Category','Item-Price','Description']                                       
    
    data_list=[]
    for row in rploss:
        data_list += [(row)]

    win = Widget(data_list, header)
    win.exec_()
     
def purchaseCollect(self):
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('item_price', Float),
        Column('item_stock', Float),
        Column('item_unit', String),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('order_balance', Float),
        Column('order_status', Boolean),
        Column('ordering_manual', Integer),
        Column('supplierID', Integer))
    purchase_orderlines = Table('purchase_orderlines', metadata,
        Column('orderlineID', Integer, primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('item_price', Float),
        Column('item_unit', String),
        Column('item_stock', Float),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('ordering_manual', Integer),
        Column('supplierID', Integer),
        Column('bookdate', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
     
    selarticles = select([articles]).order_by(articles.c.barcode).\
      where(and_(articles.c.item_stock + articles.c.order_balance \
             < articles.c.minimum_stock, articles.c.order_status == True))
    rparticles = con.execute(selarticles)
    mbookdate = str(datetime.datetime.now())[0:10]
    mflag = 0
    for row in rparticles:
        try:
            mordnr = (con.execute(select([func.max(purchase_orderlines.c.orderlineID,\
                            type_=Integer)])).scalar())
            mordnr += 1
        except:
            mflag = 1
            mordnr = 1
        mbarcode = row[0]
        mdescr= row[1]
        mprice = row[2]
        mstock = row[3]
        munit = row[4]
        minstock =row[5]
        mordersize = row[6]
        mmanual = row[9]
        msupplier = row[10]
        inssup = insert(purchase_orderlines).values(orderlineID=mordnr,barcode=mbarcode,\
            description=mdescr,item_price=mprice,item_unit=munit,item_stock=mstock,\
            minimum_stock=minstock,order_size=mordersize,ordering_manual=mmanual,\
            supplierID=msupplier,bookdate=mbookdate)
        con.execute(inssup)
        updart = update(articles).where(articles.c.barcode==row[0]).values(order_status=False,\
            order_balance=articles.c.order_balance+row[6])
        con.execute(updart)
    if mflag:
        message = 'Orderlines inserts processed successful!'
        actionOK(message)
    else:
        message = "No matching records found!"
        alertText(message) 
    self.close()
        
def checkClient(self):
    metadata = MetaData()
    clients = Table('clients', metadata,
        Column('clientID', Integer, primary_key=True),
        Column('barcode', String),
        Column('employee', String))
    order_lines = Table('order_lines', metadata,
        Column('ID', Integer(), primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('short_descr', String),
        Column('number', Float),
        Column('selling_price', Float),
        Column('selling_contents', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String),
        Column('clientID', Integer))
    
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
    con = engine.connect()
    selcl = select([clients]).where(and_(clients.c.barcode == self.checknr,\
                  clients.c.employee == self.mcallname))
    rpcl = con.execute(selcl).first() 
    if rpcl:
        self.mclient = rpcl[0]
        selord = select([order_lines]).where(order_lines.c.clientID == self.mclient)
        rpord = con.execute(selord)
        if not rpord:
            self.albl.setText('No records!')
            return
    else:
        self.mclient = ''
        self.albl.setText('No match clientnumber/barcodenumber/callname found!')
        return

    self.view.setText('')   
    self.mtotal = 0
    self.mvat = 0
    for row in rpord:
        mnumber = row[4]
        msellingprice = row[5]
        mshort = row[3]
        self.mtotal += row[7]
        self.mlist.append('{:>3d}'.format(int(mnumber))+' {:<15s}'\
             .format(mshort)+'{:\u2000>12.2f}'.format(msellingprice*int(mnumber)))
        self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
        self.qtailEdit.setText(self.qtailtext)
        self.qtotalEdit.setText('{:>12.2f}'.format(self.mtotal))
              
        self.view.append(self.mlist[-1])
    self.mkop.setText('Client: '+str(self.mclient)+' Empl. '+str(self.mcallname))

def logon(self, barcodenr):
    metadata = MetaData()
    employees = Table('employees', metadata,
        Column('barcodeID', String, primary_key=True),
        Column('callname', String),
        Column('access', Integer))
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
    con = engine.connect()
    selacc = select([employees]).where(employees.c.barcodeID == barcodenr)
    rpacc = con.execute(selacc).first()
    if not rpacc:
        return
    self.mbarcode = rpacc[0]
    self.mcallname = rpacc[1]
    self.maccess = rpacc[2]
    self.logon = self.q1Edit.text()
    self.q1Edit.setText('')
    self.pixmap = QPixmap('./logos/green.png')
    self.logonstate.setPixmap(self.pixmap.scaled(40,40))
    self.view.setText('')
    self.mtotal = 0.00
    self.mtotvat = 0.00
    self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
    self.qtailEdit.setText(self.qtailtext) 
    if self.maccess < 2:
         self.adminBtn.setHidden(True)
    elif self.maccess == 2:
        self.adminBtn.setHidden(False)
             
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Information barcodescan")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint,False)
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Catering Point of Sale')
            grid.addWidget(lblinfo, 0, 0, 1, 1, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgba(45, 83, 115, 255); font: 25pt Comic Sans MS")
            
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 0, 1, 1, Qt.AlignRight)
        
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0)
            
            infotext = QPlainTextEdit(\
        '''                                                                        User information.
        
        Logging in takes place with a barcode card with 3 access levels.
        Level 1. Selling, scanning, printing and tablemanagement.
        Level 2. Administration, a button Administration is shown, for assigning productbuttons,
                     creating employees, administration, perform stock management and imports.
        level 0. Employee is not allowed for operation.
        Employee first time scan barcode  = logon, second time = logout.
        Other employee scanning = switching employee (for replacement).
                         
        Article scanning:
        By default, scanning is performed with a number of 1.
        With the spinbox the number can be chosen, this can be done by the arrows
        of the spinbox or with the mouse wheel. After every scan, the number is reset to 1.
        Selecting can also been done with the productbuttons for unpackaged products.
        If scanning is started, the close button is blocked until 'TRANSFER PAYED' is pressed.
        The print button is blocked until the first transaction is posted.
        Errors or messages appears in red in the Notification Area. 
        A acoustic alarm  will also sound for the following 3 cases.  
        
        1. Read error occurs when scanning the barcode.
        2. Insufficient stock to deliver the order, current stock will also been showed.
        3. The product is not (yet) included in the range.
        
        All other messages will appear without acoustic alarm in red in the Notification Area.
                    
        If the item cannot be scanned, it is possible to insert the barcode manually after
        inserting press <Enter> on the keyboard.
                                          
        The receipt can be printed after scanning is finished.
        After paying, press "TRANSFER PAYED "button, so the "Exit" button is released.
        Also this will make the necessary bookings and prepare the POS for the next client.
        
        Table arrangements:
        The table arrangements are established by checking free seats and pushing the button
        Open/Change Tables/Seats.
        
        After selecting and applying a popup is showed, with the possibility of printing a
        barcode for the client. With this barcodescan it's possible to switch fast between clients.
        It's also possible to use the "Select Client" button to choose the desired client.
        With this button or scan the desired client is selected.
        
        A layout of 100 selectable buttons is showed. These buttons are arranged in 20 groups
        of 2 table seats and 15 groups of 4 table seats.
        By selecting the seats, combining or splitting of tables and seats can be established.
        By selecting the choise "Open Table" and checking the seats are added to a client,
        after pushing the "Apply Seats" button.
        By clicking the "Refresh" button the seats with clientnumbers and names of the employee
        are showed on the seats.
        All occupied and available seats are showed for all employees.
        Only the employee, that selected the seats, can add or remove seats to the assembly,
        by checking or unchecking buttons and selecting "Change seat client <number>". 
        This occurs, if visitors from a group are leaving or joining the group.
        If no orders are placed, it's possible to remove with "Change seat client <number>" 
        all the unchecked seats, also the client is removed. 
        If orders are placed, it's possible to uncheck the seats except the last seat, which
        must remain linked with the client, untill the bill is payed. The last seat is freed 
        and the client is removed when the TRANSFER PAYED button is pushed.
        
        With the button "Switch Employee" it is possible to transfer the clients 
        to another employee by end of shift or interim interruption.
        
        Before pushing the TRANSFER PAYED button the bill can be printed and payed by cash
        or by pin transaction.
        For paying by cash a modest calculator is present.
        The thirst row of the calculator shows the total sum of the bill.
        The second row under the "TRANSFER PAYED" button must be filled in with the cash, 
        supplied by the customer. By pushing the "REFUND" button the change is calculated.
        In case of incorrect entry the "DEL" button can be applied.
        
        The change is rounded. The rounding is adaptable by a authorised person. 
        ''')
            grid.addWidget(infotext, 1, 0)
                           
            infotext.setStyleSheet("font: 20px Arial; color: black ; background-color: #D9E1DF")   
            infotext.setFixedSize(1100, 700)
            infotext.setReadOnly(True)
            grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 1, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(300, 50, 350, 350)
            
    window = Widget()
    window.exec_()

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setFont(QFont("Arial", 10))
    msg.setText('Just a moment printing is starting!')
    msg.setWindowTitle('Printing')
    msg.exec_()

def printReceipt(self):
    if not self.maccess:
        self.albl.setText('Not Logged on!')
        return
    metadata = MetaData()
    order_lines = Table('order_lines', metadata,
        Column('ID', Integer(), primary_key=True),
        Column('clientID', Integer),
        Column('callname', String),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('selling_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
    con = engine.connect()
    delbal = delete(order_lines).where(and_(order_lines.c.number == 0,\
                   order_lines.c.clientID == self.mclient, order_lines.c.callname ==\
                   self.mcallname))
    con.execute(delbal)
    selb = select([order_lines]).where(and_(order_lines.c.clientID == self.mclient,\
                order_lines.c.callname== self.mcallname)).order_by(order_lines.c.barcode)
    rpb = con.execute(selb)
    
    mtotvat = 0
    mtotal = 0
    def heading(self, mpage):
        head=\
('Sales - Ordernumber: '+ str(self.mclient)+' Date : '+str(datetime.datetime.now())[0:10]+' Pagenumber '+str(mpage)+' \n'+
'==================================================================================================\n'+
'Artikelnr  Description                                  Number  Item_price    Subtotal         VAT\n'+
'==================================================================================================\n')
        return(head)

    mpage = 0
    rgl = 0
    if sys.platform == 'win32':
        fbarc = '.\\forms\\Sales\\'+str(self.mclient)+'.txt'
    else:
        fbarc = './forms//Sales/'+str(self.mclient)+'.txt'
    
    for row in rpb:
        rgl += 1
        if rgl == 1 :
            mpage += 1
            open(fbarc, 'w').write(heading(self, mpage))
            rgl += 4
        elif rgl%58 == 1:
            mpage += 1
            open(fbarc, 'a').write(heading(self, mpage))
            rgl += 4
            
        martnr = row[3]
        mdescr = row[4]
        mnumber = row[5]
        mprice = row[6]
        msubtotal = row[7]
        msubvat = row[8]
        mtotvat += msubvat
        mtotal += msubtotal
        open(fbarc,'a').write(str(martnr) +'  '+'{:<40s}'.format(mdescr)+' '+'{:>6d}'\
                 .format(int(mnumber))+'{:>12.2f}'.format(float(mprice))+'{:>12.2f}'\
                 .format(float(msubtotal))+'{:>12.2f}'\
                 .format(float(msubvat))+'\n')
         
    tail=\
    ('===================================================================================================\n'+
     'Total  amount to pay inclusive VAT and amount VAT                         '+'{:>12.2f}'.format(mtotal)+'{:>12.2f}'.format(mtotvat)+' \n'+
     '===================================================================================================\n'+\
     'Employee : '+self.mcallname+' **** Thank you for visiting us ***\n') 
    if rgl > 0:
        open(fbarc,'a').write(tail) 
        if sys.platform == 'win32':
            from os import startfile
            startfile(fbarc, "print")
        else:
            from os import system
            system("lpr "+fbarc)
        self.albl.setText('Printing of receipt')
    else:
        self.albl.setText('No transactions for printing!')
            
def payed(self):
    mbookd = str(datetime.datetime.now())[0:10]
    metadata = MetaData()
    sales = Table('sales', metadata,
        Column('salesID', Integer(), primary_key=True),
        Column('receiptnumber', Integer),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('selling_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String),
        Column('clientID', Integer),
        Column('short_descr', String))
    order_lines = Table('order_lines', metadata,
        Column('ID', Integer(), primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('selling_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('mutation_date', String),
        Column('callname', String),
        Column('clientID', Integer),
        Column('short_descr', String))
    clients = Table('clients', metadata,
        Column('clientID', Integer, primary_key=True),
        Column('employee', String))
    tables_layout = Table('tables_layout', metadata,
        Column('ID', Integer, primary_key=True),
        Column('clientID', Integer),
        Column('callname', String),
        Column('occupied', Integer))
    payments = Table('payments', metadata,
        Column('payID', Integer(), primary_key=True),
        Column('basis', Float),
        Column('kind', String),
        Column('amount', Float),
        Column('bookdate', String),
        Column('paydate', String),
        Column('instance', String),
        Column('accountnumber', String),
        Column('ovorderID', Integer))
              
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    delsal = delete(order_lines).where(and_(order_lines.c.number == 0,\
              order_lines.c.clientID == self.mclient, order_lines.c.callname == self.mcallname))
    con.execute(delsal)
    if self.mtotal != int(0):
        try:
            mrcptnr = (con.execute(select([func.max(sales.c.receiptnumber, type_=Integer)])).scalar())
            mrcptnr += 1
        except:
            mrcptnr = 1
        sellines = select([order_lines]).where(and_(order_lines.c.clientID == self.mclient,\
                         order_lines.c.callname == self.mcallname))
        rplines = con.execute(sellines)
        try:
            mpaynr = (con.execute(select([func.max(payments.c.payID, type_=Integer)])).scalar())
            mpaynr +=1
        except:
            mpaynr = 1
        mtotal = 0
        mtotal_vat = 0
        for row in rplines:
            try:
                midnr = (con.execute(select([func.max(sales.c.salesID, type_=Integer)])).scalar())
                midnr += 1
            except:
                midnr = 1
            ins = insert(sales).values(salesID=midnr, receiptnumber = mrcptnr, barcode = row[1],\
              description = row[2], number = row[3], selling_price = row[4], sub_total = row[5],\
              sub_vat = row[6], mutation_date = row[7], callname = row[8], clientID = row[9],\
              short_descr = row[10])
            con.execute(ins)
            mtotal += row[5]
            mtotal_vat += row[6]
           
        insdr = insert(payments).values(payID = mpaynr, bookdate = mbookd,\
              kind = 'VAT payment    ', basis = mtotal, amount = mtotal_vat, instance = 'Tax authorities',\
              ovorderID = mrcptnr, accountnumber = 'NL10 ABNA 9999999977')
        con.execute(insdr)
        dellines = delete(order_lines).where(and_(order_lines.c.callname == self.mcallname,\
                     order_lines.c.clientID == self.mclient))
        con.execute(dellines)
        updlayout = update(tables_layout).where(and_(tables_layout.c.clientID == self.mclient,\
          tables_layout.c.callname == self.mcallname)).values(occupied = 0, clientID = 0, callname = '')
        con.execute(updlayout)
        delclient = delete(clients).where(and_(clients.c.clientID == self.mclient,\
                      clients.c.employee == self.mcallname))
        con.execute(delclient)
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color:  #B0C4DE")
        self.printBtn.setDisabled(True)
        self.printBtn.setStyleSheet("color: grey; background-color: #00FFFF")
        self.albl.setText('Transactions successful!')
    else:
        try:
            updlayout = update(tables_layout).where(and_(tables_layout.c.clientID == self.mclient,\
              tables_layout.c.callname == self.mcallname)).values(occupied = 0, clientID = 0, callname = '')
            con.execute(updlayout)
            delclient = delete(clients).where(and_(clients.c.clientID == self.mclient,\
                          clients.c.employee == self.mcallname))
            con.execute(delclient)
        except Exception: 
            pass
        self.albl.setText('There are no transactions!')
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color:  #45b39d")
    self.mtotal = 0.00
    self.mtotvat = 0.00
    self.mlist = []
    self.view.setText('')
    self.mkop.setText('No client selected')
    self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
    self.qtailEdit.setText(self.qtailtext)
    self.qtotalEdit.setText('')
    self.qtotalEdit.setPlaceholderText('TOTAL')
    self.text = ''
    self.qcashEdit.setText(self.text)
    self.qcashEdit.setPlaceholderText('CASH')
    self.qchangeEdit.setText('')
    self.qchangeEdit.setPlaceholderText('CHANGE') 

def giveAlarm():
    if sys.platform == 'win32':
        import winsound
        winsound.Beep(2300,250)
        winsound.Beep(2300,250)
    else:
        #sudo apt install sox
        from os import system
        system('play -nq -t alsa synth {} sine {}'.format(0.25, 2300))
        system('play -nq -t alsa synth {} sine {}'.format(0.25, 2300))

def plusminChange(self):
    if self.plusminBtn.isChecked():
        self.plusminBtn.setText('-')
        self.qspin.setRange(-99, -1)
    else:
        self.plusminBtn.setText('+')
        self.qspin.setRange(1, 99)
        
def checkEan8(c):
    checksum = (int(c[0])+int(c[2])+int(c[4])+int(c[6]))*3+(int(c[1])+
                int(c[3])+int(c[5]))
    checkdigit = (10-(checksum%10))
    if checkdigit == int(c[7]):
        return True
    else:
        return False
        
def checkEan13(c):
    checksum = int(c[0])+int(c[2])+int(c[4])+int(c[6])+int(c[8])+int(c[10])+(int(c[1])+
                int(c[3])+int(c[5])+int(c[7])+int(c[9])+int(c[11]))*3
    checkdigit = (10-(checksum%10))%10
    if checkdigit == int(c[12]):
        return True
    else:
        return False
    
def set_barcodenr(self):
    barcodenr = str(self.q1Edit.text())
    mnumber = float(self.qspin.value())
    myear = int(str(datetime.datetime.now())[0:4])
    if len(barcodenr) == 13 and checkEan13(barcodenr) and self.mcallname and self.mclient:
        self.q1Edit.setStyleSheet("color:black;  background-color: #F8F7EE")
        metadata = MetaData()
        articles = Table('articles', metadata,
            Column('barcode', String, primary_key=True),
            Column('description', String),
            Column('item_price', Float),
            Column('item_stock', Float),
            Column('VAT', String),
            Column('annual_consumption_1', Float),
            Column('annual_consumption_2', Float),
            Column('short_descr', String),
            Column('selling_price', Float),
            Column('selling_contents', Float),
            Column('additional', Integer),
            Column('item_unit', String),
            Column('location_warehouse', String),
            Column('article_group', String))
        order_lines = Table('order_lines', metadata,
            Column('ID', Integer(), primary_key=True),
            Column('barcode', String),
            Column('description', String),
            Column('number', Float),
            Column('selling_price', Float),
            Column('sub_total', Float),
            Column('sub_vat', Float),
            Column('callname', String),
            Column('mutation_date', String),
            Column('clientID', Integer),
            Column('callname', String),
            Column('short_descr', String))
        addition = Table('addition', metadata,
            Column('addID', Integer, primary_key=True),
            Column('barcode', String),
            Column('description', String),
            Column('item_price', Float),
            Column('number', Float),
            Column('item_unit', String),
            Column('article_group', String),
            Column('location_warehouse', String))
        clients = Table('clients', metadata,
            Column('clientID', Integer, primary_key=True),
            Column('employee', String))
        
        engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
        con = engine.connect()
        
        selcl = select([clients]).where(and_(clients.c.clientID==self.mclient,clients.c.employee==self.mcallname))
        rpcl = con.execute(selcl).first()
        
        if not rpcl:
            self.q1Edit.setText('')
            self.albl.setText('First logon with switched employee!')
            return
         
        selart = select([articles]).where(articles.c.barcode == barcodenr)
        selordlines = select([order_lines]).where(and_(order_lines.c.barcode == barcodenr,\
                order_lines.c.clientID == self.mclient))
        rpart = con.execute(selart).first()
        if not rpart:
            self.albl.setText('Article not in assortment!')
            giveAlarm()
            self.q1Edit.setSelection(0,13)
            return
        mdescr = rpart[1]
        mprice = rpart[2]
        munit = rpart[11]
        mloc = rpart[12]
        mgroup = rpart[13]
        rpordlines = con.execute(selordlines).first()
        if rpart and rpart[3] < mnumber:
            self.albl.setText(str(int(rpart[3]))+' in stock!')
            giveAlarm()
            self.q1Edit.setSelection(0,13)
            return
        elif rpart and rpart[10]:
            if myear%2 == 1:     #odd year
                updart = update(articles).where(articles.c.barcode == rpart[0])\
                    .values(item_stock = articles.c.item_stock - mnumber,\
                     annual_consumption_2 = articles.c.annual_consumption_2 + mnumber)
                con.execute(updart)
            elif myear%2 == 0:   #even year
                updart = update(articles).where(articles.c.barcode == rpart[0])\
                    .values(item_stock = articles.c.item_stock - mnumber,\
                     annual_consumption_1 = articles.c.annual_consumption_1 + mnumber)
                con.execute(updart)
            try:
                idnr = (con.execute(select([func.max(addition.c.addID, type_=Integer)])).scalar()) 
                idnr += 1
            except:
                idnr = 1
            insadd = insert(addition).values(addID = idnr, barcode = barcodenr, description = mdescr,\
                item_price = mprice, number = mnumber, item_unit = munit, article_group =\
                mgroup, location_warehouse = mloc)
            con.execute(insadd)
            self.albl.setText(str(mnumber)+' x '+mdescr[:15]+' reduced from stock '+mgroup)
        elif rpart and self.maccess:
            if rpart[4] == 'high':      
                self.mvat = self.mvath
            elif rpart[4] == 'low': 
                self.mvat = self.mvatl
            else:
                self.mvat = self.mvatz
            mdescr = rpart[1]
            mshort = rpart[7]
            mdescr = mdescr[:40] if len(mdescr) > 40 else mdescr
            msellingprice = rpart[8]
            msellingcontents = rpart[9]
            mutdate = str(datetime.datetime.now())[0:10]
            if rpordlines:
                updordlines = update(order_lines).where(and_(order_lines.c.barcode == barcodenr,\
                  order_lines.c.clientID == self.mclient)).values(number = order_lines.c.number+mnumber,\
                  sub_total = (order_lines.c.number+mnumber)*msellingprice, short_descr = mshort,\
                  sub_vat = (order_lines.c.number+mnumber)*msellingprice*self.mvat, callname = self.mcallname,\
                  mutation_date = mutdate)
                con.execute(updordlines)
            else:
                try:
                    midnr = (con.execute(select([func.max(order_lines.c.ID, type_=Integer)])).scalar()) 
                    midnr += 1
                except:
                    midnr = 1
                insordlines = insert(order_lines).values(ID = midnr, clientID = self.mclient,\
                  barcode = barcodenr, description = mdescr, short_descr = mshort, number = mnumber, selling_price = msellingprice,\
                  sub_total = mnumber*msellingprice, sub_vat = mnumber*msellingprice*self.mvat,\
                  callname = self.mcallname, mutation_date = mutdate)
                con.execute(insordlines)
            if myear%2 == 1:     #odd year
                updart = update(articles).where(articles.c.barcode == rpart[0])\
                    .values(item_stock = articles.c.item_stock - mnumber*msellingcontents,\
                     annual_consumption_2 = articles.c.annual_consumption_2 + mnumber*msellingcontents)
                con.execute(updart)
            elif myear%2 == 0:   #even year
                updart = update(articles).where(articles.c.barcode == rpart[0])\
                    .values(item_stock = articles.c.item_stock - mnumber*msellingcontents,\
                     annual_consumption_1 = articles.c.annual_consumption_1 + mnumber*msellingcontents)
                con.execute(updart)
            
            self.mkop.setText('Client: '+str(self.mclient)+' Empl. '+str(self.mcallname))
            self.mlist.append('{:>3d}'.format(int(mnumber))+' {:<15s}'.format(mshort)+'{:\u2000>12.2f}'.format(msellingprice*int(mnumber)))
            self.mtotal += float(msellingprice)*float(mnumber)
            self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
            self.qtailEdit.setText(self.qtailtext)
            self.qtotalEdit.setText('{:>12.2f}'.format(self.mtotal))
                      
            self.view.append(self.mlist[-1])
            self.albl.setText('')
            self.plusminBtn.setChecked(False)
            self.plusminBtn.setText('+')
            self.qspin.setRange(1, 99)
        elif self.maccess == 0:
            self.albl.setText('Please logon with your barcodecard!')
        else:
            self.albl.setText('Article not in assortment!')
            self.q1Edit.setSelection(0,13)
            giveAlarm()
                  
        self.closeBtn.setDisabled(True)
        self.closeBtn.setStyleSheet("color: grey; background-color: #B0C4DE")
        self.printBtn.setEnabled(True)
        self.printBtn.setStyleSheet("color: black;  background-color: #00FFFF")
        self.clientBtn.setEnabled(True)
        self.clientBtn.setStyleSheet("font: 12pt Arial; color: black; background-color: #00BFFF")
    elif len(barcodenr) == 8 and barcodenr[0:2] == '24' and checkEan8(barcodenr):
        self.q1Edit.setStyleSheet("color:#F8F7EE;  background-color: #F8F7EE")
        self.q1Edit.setText('')
        self.mkop.setText('No client selected')
        self.mclient = 0
        if barcodenr == self.checknr and self.maccess > 0: #zelf al ingelogd dus uitloggen
            self.maccess = 0
            self.adminBtn.setHidden(True)
            self.pixmap = QPixmap('./logos/red.png')
            self.logonstate.setPixmap(self.pixmap.scaled(40,40))
            self.view.setText('')
            self.mtotal = 0.00
            self.mtotvat = 0.00
            self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
            self.qtailEdit.setText(self.qtailtext) 
        else:   #another person logged on, so switch logon
            self.checknr = barcodenr
            logon(self, barcodenr)
            self.albl.setText('')
    elif len(barcodenr) == 8 and barcodenr[0:2] == '26' and checkEan8(barcodenr):
        self.q1Edit.setStyleSheet("color:#F8F7EE;  background-color: #F8F7EE")
        self.q1Edit.setText('')
        self.checknr = barcodenr
        checkClient(self)
    elif not self.mcallname:
        self.albl.setText('Please logon with your barcodecard!')
    elif self.maccess == 0 and self.mcallname:
        self.albl.setText('No permission to execute!')
        self.pixmap = QPixmap('./logos/red.png')
        self.logonstate.setPixmap(self.pixmap.scaled(40,40))
        giveAlarm()
    elif self.mclient == 0:
        self.albl.setText('Compose or choose existing table-arrangement!')
    else:
        #alarm if barcode scan failed
        self.albl.setText('Scanning error barcode!')
        self.q1Edit.setSelection(0,13)
        giveAlarm()
    
    self.q1Edit.setSelection(0,13)
    self.qspin.setValue(1)

def bigDisplay(self):
    mcallname = self.mcallname
    mclient = self.mclient
    albl = self.albl
    if mclient == 0:
        self.albl.setText('First choose a clientnumber')
        return
    class widget(QDialog):
        def __init__(self):
            super(widget,self).__init__()
            
            self.setWindowTitle("Client Orderlines")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))
            
            grid = QGridLayout()
            grid.setSpacing(0)
            
            self.albl = albl
            self.mclient = mclient
            self.mcallname = mcallname
            
            mkop = QLineEdit()
            mkoptext = 'Articlenumber Description                              Number  Item_price    Subtotal         VAT'
            mkop.setText(mkoptext)
            mkop.setReadOnly(True)
            mkop.setFont(QFont("Consolas", 12, 75))
            mkop.setStyleSheet("color: black; background-color: #F8F7EE")  
            mkop.setFocusPolicy(Qt.NoFocus)
            mkop.setFixedWidth(850)  
            
            view = QTextEdit()
            view.setStyleSheet('color: black; background-color: #F8F7EE')  
            view.setText('')
            view.setFont(QFont("Consolas", 12, 75))
            view.setFocusPolicy(Qt.NoFocus)
            view.setFixedSize(850, 700)  
            
            mtotal = 0.00
            mtotvat = 0.00
            qtailEdit = QLineEdit()
            qtailEdit.setFont(QFont("Consolas", 12, 75))
            qtailEdit.setStyleSheet('color: black; background-color: #F8F7EE') 
            qtailEdit.setReadOnly(True)
            qtailEdit.setFixedWidth(850)
            qtailEdit.setFocusPolicy(Qt.NoFocus)
            qtailtext = 'Clientnumber: '+str(self.mclient)+'  Total  incl. VAT'+'\u2000'*57+'{:\u2000>12.2f}'.format(mtotal)+'{:\u2000>12.2f}'.format(mtotvat)
            qtailEdit.setText(qtailtext)
   
            metadata = MetaData()
            order_lines = Table('order_lines', metadata,
                Column('ID', Integer(), primary_key=True),
                Column('barcode', String),
                Column('short_descr', String),
                Column('number', Float),
                Column('selling_price', Float),
                Column('sub_total', Float),
                Column('sub_vat', Float),
                Column('callname', String),
                Column('mutation_date', String),
                Column('clientID', Integer),
                Column('callname', String))
            engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
            con = engine.connect()
                     
            sellines = select([order_lines]).where(and_(order_lines.c.callname == self.mcallname,\
                    order_lines.c.clientID == self.mclient))
            rplines = con.execute(sellines)           
            self.albl.setText('Client '+str(self.mclient))
            x = 0
            for row in rplines:
                martnr = row[1]
                mshort = row[2]
                mnumber = row[3]
                mprice = row[4]
                msubtot = row[5]
                msubvat = row[6]
                view.append('{:<14s}'.format(martnr)+'{:<15s}'.format(mshort)+' {:>6d}'\
                 .format(int(mnumber))+'{:>12.2f}'.format(mprice)+'{:>12.2f}'\
                 .format(msubtot)+'{:>12.2f}'.format(msubvat))
                mtotal += msubtot
                mtotvat += msubvat
                x += 1 
            qtailtext = 'Clientnumber: '+str(self.mclient)+'  Total  incl. VAT'+'\u2000'*15+'{:\u2000>12.2f}'.format(mtotal)+'{:\u2000>12.2f}'.format(mtotvat)
            qtailEdit.setText(qtailtext)
            mkop.setText('Articlenumber Description      Number  Item_price    Subtotal         VAT')
               
            grid.addWidget(mkop, 2, 0, 1, 12, Qt.AlignRight)           
            grid.addWidget(view, 3 ,0, 1, 12, Qt.AlignRight)
            grid.addWidget(qtailEdit, 4, 0, 1, 12, Qt.AlignRight)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)
            closeBtn.setFont(QFont("Arial",12))
            closeBtn.setFocusPolicy(Qt.NoFocus)
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black; background-color: gainsboro")

            grid.addWidget(closeBtn, 9, 11, 1, 1, Qt.AlignRight)
            
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            lbl3.setFixedHeight(40)
            grid.addWidget(lbl3, 10, 0, 1, 12, Qt.AlignCenter)
                                      
            self.setLayout(grid)
            self.setGeometry(400, 60, 600, 300)
            
    window = widget()
    window.exec_()

def choseClient(self):
    if not self.maccess:
        self.albl.setText('Please logon with your barcodecard!')
        return
    metadata = MetaData()
    order_lines = Table('order_lines', metadata,
        Column('ID', Integer(), primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('short_descr', String),
        Column('number', Float),
        Column('selling_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String),
        Column('clientID', Integer))
    clients = Table('clients', metadata,
        Column('clientID', Integer, primary_key=True),
        Column('employee', String))
         
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    selcl = select([clients]).where(clients.c.employee == self.mcallname).\
        order_by(clients.c.clientID)
    if con.execute(selcl).fetchone():
        rpcl = con.execute(selcl)
    else:
        self.albl.setText('No current orders found for this employee!') 
        return
    
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(700, 50, 350, 300)
            self.setWindowTitle('Clientnumber')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            table_view.setStyleSheet('font : 24px bold ; color:black ; background-color: #c2be7f')
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(getClientnr)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
        
    header = ['Clientnumber','Employee'] 
        
    data_list=[]
    for row in rpcl:
         data_list += [(row)]
     
    def getClientnr(idx):
        self.mclient = idx.data()
        self.q1Edit.setText('') 
        if idx.column() == 0:
            selord = select([order_lines]).where(order_lines.c.clientID == self.mclient)
            rpord = con.execute(selord)
            self.view.setText('')   
            self.mtotal = 0
            self.mvat = 0
            for row in rpord:
                mnumber = row[4]
                mprice = row[5]
                mdescr = row[3]
                self.mtotal += row[6]
                self.mlist.append('{:>3d}'.format(int(mnumber))+' {:<15s}'\
                     .format(mdescr)+'{:\u2000>12.2f}'.format(mprice*int(mnumber)))
                self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
                self.qtailEdit.setText(self.qtailtext)
                self.qtotalEdit.setText('{:>12.2f}'.format(self.mtotal))
                self.view.append(self.mlist[-1])
            self.mkop.setText('Client: '+str(self.mclient)+' Empl. '+str(self.mcallname))
            if sys.platform == 'win32':
                keyboard.press_and_release('esc')            #Windows
            else:
                subprocess.call(["xdotool", "key", "Escape"]) #Linux
    win = Widget(data_list, header)
    win.exec_()
    
def printEan(self, x1 ,y1):
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./logos/logo.jpg')) 
    msgBox.setWindowTitle("Printing barcodeID")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setFont(QFont("Arial", 10))
    msgBox.setText("Do you want to print the barcode for scanning?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        self.printer = QPrinter()
        self.pixmap = QPixmap(self.path+str(self.mbarcode)+'.png')
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
             painter = QPainter(self.printer)
             rect = painter.viewport()
             size = self.pixmap.size()
             size.scale(rect.size(), Qt.KeepAspectRatio)
             painter.setViewport(rect.x(), rect.y(), x1 , y1) #aspect and size for barcodes Ean 
             painter.setWindow(self.pixmap.rect())
             painter.drawPixmap(0, 0, self.pixmap)
            
def seatsArrange(self, routeSeats, seatText):
    if not self.maccess:
        self.albl.setText('Please logon with your barcodecard!')
        return
    if routeSeats:
        self.q1Edit.setText('')
    mcallname = self.mcallname
    maccess = self.maccess
    mclient = self.mclient
    mview = self.view
    mqtail = self.qtailEdit
    mqtotal = self.qtotalEdit
    self.text = ''
    mqcash = self.qcashEdit
    mqchange = self.qchangeEdit
    
    class widget(QDialog):
        def __init__(self):
            super(widget,self).__init__()
            
            self.setWindowTitle("Seats Arrangements")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))
            
            self.mcallname = mcallname
            self.maccess = maccess
            self.mclient = mclient
            self.view = mview
            self.qtailEdit = mqtail
            self.qtotalEdit = mqtotal
            self.qcashEdit = mqcash
            self.qchangeEdit = mqchange
            self.seatText = seatText
             
            grid = QGridLayout()
            grid.setSpacing(0)
             
            self.lblseats = QLabel(' ')
            self.lblseats.setFont(QFont("Arial", 12, 75))
            self.lblseats.setText(self.seatText)
            self.lblseats.setAlignment(Qt.AlignCenter)
            self.lblseats.setStyleSheet("color: red ; background-color : #39CCCC")
            self.lblseats.setFixedSize(1200, 40)
            grid.addWidget(self.lblseats, 12, 0, 1,  12, Qt.AlignTop)
             
            metadata = MetaData()
            tables_layout = Table('tables_layout', metadata,
                Column('ID', Integer, primary_key=True),
                Column('table_seat', String),
                Column('occupied', Integer),
                Column('clientID',Integer),
                Column('callname', String))
            clients = Table('clients', metadata,
                Column('clientID', primary_key=True),
                Column('employee', None, ForeignKey('tables_layout.callname')),
                Column('barcode', String))
                  
            engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
            con = engine.connect()
  
            seltables = select([tables_layout]).order_by(tables_layout.c.ID)
            rptables = con.execute(seltables)
            t = 0
            for row in rptables:
                if row[3]:
                    clientnr = '\nClientnr '+str(row[3])
                    client = clientnr
                else:
                    clientnr = 0
                    client = ''
                if row[4]:
                    empl = '\nServing:\n'+row[4]
                else:
                    empl = '' 
                tBtn = QPushButton()
                tBtn.setFixedSize(100,80)
                tBtn.setFont(QFont("Times", 9, 75))
                tBtn.setFocusPolicy(Qt.NoFocus)
                tBtn.setCheckable(True)
                if row[2]:
                    tBtn.setChecked(True)
                    if row[4] != self.mcallname:
                        tBtn.setDisabled(True)
                if t < 40:
                    tBtn.setStyleSheet("color: black;  background-color: #23cfb2")
                    tBtn.setText('Table '+str(row[1])+client+empl)
                    grid.addWidget(tBtn, int(t/10)+1, t%10)
                elif t > 39:
                    tBtn.setStyleSheet("color: black;  background-color: #f19314")
                    tBtn.setText('Table '+str(row[1])+client+empl)
                    if int((t-40)%12) > 7:
                       grid.addWidget(tBtn, int(t/12)+2, int((t-40)%12))
                    else:
                       grid.addWidget(tBtn, int(t/12)+3, int((t-40)%12))
                tBtn.clicked.connect(lambda checked, tindex = t : gettable_seat(tindex))
                t += 1
                
            self.seatlist = []   
            def gettable_seat(tindex):
                self.seatlist.append(tindex) 
                                
            qcbEdit = QComboBox()
            qcbEdit.addItem('Open new table')
            selclient = select([clients]).where(clients.c.employee ==\
                            self.mcallname).order_by(clients.c.clientID)
            rpclient = con.execute(selclient)

            for row in rpclient:
                qcbEdit.addItem('Change seats client '+str(row[0]))
                                        
            qcbEdit.setFixedSize(200, 40)
            qcbEdit.setStyleSheet('font: 18px bold; color:black; background-color: #F8F7EE')
            grid.addWidget(qcbEdit, 1, 10, 1, 2, Qt.AlignTop)
            
            def qclientChanged():
                qcbEdit.setCurrentText(qcbEdit.currentText())
            qcbEdit.currentTextChanged.connect(qclientChanged)
            
            def connectClient(self):
                #remove seats with even occurences
                self.seatlist = [seat for seat, count in Counter(self.seatlist).items() if count%2 == 1]
                self.seatlist.sort(reverse=True) #high numbers first 
                indextext = qcbEdit.currentText()
                if indextext == 'Open new table':
                    try:
                        mclientnr = con.execute(select([func.max(clients.c.clientID, type_=Integer)])).scalar()
                        mclientnr += 1
                    except:
                        mclientnr = 1
                    self.mclient=int(mclientnr)
                else:
                    self.mclient=int(indextext[20:])
                if len(self.seatlist) == 0:
                    self.seatText = 'Choose seat arrangement first!'
                    self.lblseats.setText(self.seatText)
                    return
                else:
                    mcheck = 0
                    x = 0
                    for val in self.seatlist:
                        seltab = select([tables_layout]).where(tables_layout.c.ID == self.seatlist[x])
                        rptab = con.execute(seltab).fetchone()
                        occ=rptab[2]
                        if occ == 0:
                            if indextext == 'Open new table':
                                mcheck = 1
                            upd = update(tables_layout).where(tables_layout.c.ID ==\
                             self.seatlist[x]).values(occupied=1,clientID=self.mclient,\
                             callname=self.mcallname)
                            con.execute(upd)
                            self.seatText = 'Tableseats have been processed!'
                            self.lblseats.setText(self.seatText)
                        else:
                            if indextext !=  'Open new table':
                                selseats = select([tables_layout]).where(and_\
                                    (tables_layout.c.occupied == 1,\
                                    tables_layout.c.clientID == self.mclient,\
                                    tables_layout.c.callname == self.mcallname))
                                rpseats = con.execute(selseats)
                                s = 0
                                for seat in rpseats:
                                    if seat[2]:
                                        s += 1
                                self.seatText = 'Tableseats have been processed!'
                                self.lblseats.setText(self.seatText)
                                if s > 1:
                                    upd = update(tables_layout).where(and_(tables_layout.c.ID ==\
                                     self.seatlist[x], tables_layout.c.clientID == self.mclient, \
                                     tables_layout.c.callname == self.mcallname))\
                                     .values(occupied=0,clientID=0,callname='')
                                    con.execute(upd)
                                else:
                                    metadata = MetaData()
                                    order_lines = Table('order_lines', metadata,
                                        Column('ID', Integer, primary_key=True),
                                        Column('clientID', Integer),
                                        Column('callname', String))
                                    selol = select([order_lines]).where(and_(order_lines.c.\
                                      clientID == self.mclient, order_lines.c.callname == self.mcallname))
                                    rpol = con.execute(selol).first()
                                    if rpol and s == 1:
                                        self.seatText = 'Last seat can only be removed by button "TRANSFER PAYED" in mainscreen!'
                                        self.lblseats.setText(self.seatText)
                                    elif s == 1:
                                        upd = update(tables_layout).where(and_(tables_layout.c.ID ==\
                                          self.seatlist[x], tables_layout.c.clientID == self.mclient,\
                                           tables_layout.c.callname == self.mcallname))\
                                           .values(occupied=0,clientID=0,callname='')
                                        con.execute(upd) 
                                        delol = delete(clients).where(and_(clients.c.clientID ==\
                                              self.mclient, clients.c.employee == self.mcallname))
                                        con.execute(delol)
                                    else:
                                        upd = update(tables_layout).where(and_(tables_layout.c.ID ==\
                                          self.seatlist[x], tables_layout.c.clientID == self.mclient,\
                                           tables_layout.c.callname == self.mcallname))\
                                           .values(occupied=0,clientID=0,callname='')
                                        con.execute(upd) 
                        x += 1
                    if mcheck:
                        inlogstr = str(int(2600000+mclientnr))
                        ean = barcode.get('ean8', inlogstr, writer=ImageWriter()) # for barcode as png
                        mbarcode = ean.get_fullcode()
                        if sys.platform == 'win32':
                            ean.save('.\\Barcodes\\clients\\'+str(mbarcode))
                        else:
                            ean.save('./Barcodes/clients/'+str(mbarcode))
                        insidx=insert(clients).values(clientID=mclientnr, employee=self.mcallname,\
                             barcode = mbarcode)
                        con.execute(insidx)
                        self.mbarcode = mbarcode
                        self.path = './Barcodes/clients/'
                        x1 = 267.3
                        y1 = 213.1
                        printEan(self, x1, y1)
                
                seatText = self.seatText
                refresh(self, seatText)
                
            clientBtn = QPushButton('Apply\nSeats')
            clientBtn.clicked.connect(lambda: connectClient(self))
            clientBtn.setFixedSize(200, 80)
            clientBtn.setStyleSheet("font: 24px bold; color: black; background-color: #39CCCC")

            grid.addWidget(clientBtn, 2, 10, 1, 2)
            
            emplBtn = QPushButton('Switch Employee')
            emplBtn.clicked.connect(lambda: switchEmployee(self))
            emplBtn.setFixedSize(200, 80)
            emplBtn.setStyleSheet("font: 24px bold; color: black; background-color: #00BFFF")
            
            grid.addWidget(emplBtn, 3, 10, 1, 2)

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)
            closeBtn.setStyleSheet('font: 24px bold; color: black; background-color:  #00FFFF')
            closeBtn.setFixedSize(200, 80)
            
            grid.addWidget(closeBtn, 4, 10, 1, 2)
           
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            lbl3.setFixedHeight(40)
            grid.addWidget(lbl3, 13, 0, 1, 11, Qt.AlignCenter)
                                      
            self.setLayout(grid)
            self.setGeometry(100, 60, 600, 300)
            
    window = widget()
    window.exec_()
      
def barcodeScan():
    #check order_sizes and minimum_stock
    calculationStock()
    class widget(QDialog):
        def __init__(self):
            super(widget,self).__init__()
            
            self.setWindowTitle("Catering sales")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))
            
            self.mvatz = 0
            self.mcallname = '' 
            self.maccess = 0
            self.mclient = 0
            self.checknr = ''
                        
            metadata = MetaData()
            params = Table('params', metadata,
                Column('paramID', Integer(), primary_key=True),
                Column('item', String),
                Column('value', Float))
            groupbuttons = Table('groupbuttons', metadata,
                Column('groupID',Integer(), primary_key=True),
                Column('reference', String),
                Column('buttongrouptext', String),
                Column('bg_color', String))
                                           
            engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
            con = engine.connect()
            selpar = select([params]).order_by(params.c.paramID)
            rppar = con.execute(selpar).fetchall()
            
            selhbtn = select([groupbuttons]).order_by(groupbuttons.c.groupID)
            rphbtn = con.execute(selhbtn).fetchall()
                
            self.mvatl = rppar[0][2]
            self.mvath = rppar[1][2]
            rounding = rppar[6][2]

            grid = QGridLayout()
            grid.setSpacing(0)
  
            self.qtotalEdit = QLineEdit('')
            self.qtotalEdit.setPlaceholderText("TOTAL")
            self.qtotalEdit.setFixedSize(200, 48)
            self.qtotalEdit.setDisabled(True)
            self.qtotalEdit.setAlignment(Qt.AlignRight)
            self.qtotalEdit.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
                           
            grid.addWidget(self.qtotalEdit, 4, 6, 1, 1, Qt.AlignTop)
              
            self.text = ''
            self.qcashEdit = QLineEdit(self.text)
            self.qcashEdit.setPlaceholderText("CASH")
            self.qcashEdit.setFixedSize(200, 49)
            self.qcashEdit.setAlignment(Qt.AlignRight)
            self.qcashEdit.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
            self.qcashEdit.setFocusPolicy(Qt.NoFocus)
            grid.addWidget(self.qcashEdit, 4, 6, 1, 1, Qt.AlignVCenter)
              
            self.qchangeEdit = QLineEdit('')
            self.qchangeEdit.setFixedSize(200, 52)
            self.qchangeEdit.setPlaceholderText("CHANGE")
            self.qchangeEdit.setDisabled(True)
            self.qchangeEdit.setAlignment(Qt.AlignRight)
            self.qchangeEdit.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
            grid.addWidget(self.qchangeEdit, 5, 6, 1, 1, Qt.AlignVCenter)
            
            self.qtextEdit = QLineEdit()
            self.qtextEdit.setFixedSize(600, 53)
            self.qtextEdit.setPlaceholderText("TRANSFER DATA - PAYING")
            self.qtextEdit.setDisabled(True)
            self.qtextEdit.setAlignment(Qt.AlignCenter)
            self.qtextEdit.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
            grid.addWidget(self.qtextEdit, 5, 4, 1, 3, Qt.AlignBottom)
            def calcChange(self):
                self.qcashEdit.setText(self.text)
                if self.qtotalEdit.text():
                    total = float(self.qtotalEdit.text())
                else:
                    total = 0
                if not (self.qcashEdit.text() == '.' or self.qcashEdit.text() == ''):
                    cash = float(self.qcashEdit.text())
                else:
                    cash = 0
                change = cash-total
                
                def round_nearest(change, rounding):
                    return round(change/rounding) * rounding
               
                self.qchangeEdit.setText('{:>12.2f}'.format(round_nearest(change, rounding)))

            calcBtn = QPushButton('REFUND')
            calcBtn.setFocusPolicy(Qt.NoFocus)
            calcBtn.setFixedSize(200, 100)
            calcBtn.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
            
            calcBtn.clicked.connect(lambda: calcChange(self))
            grid.addWidget(calcBtn, 4, 6, 2, 1, Qt.AlignRight | Qt.AlignVCenter)
            
            payBtn = QPushButton('TRANSFER\nPAYED')
            payBtn.setFocusPolicy(Qt.NoFocus)
            payBtn.setFixedSize(198, 152)
            payBtn.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
            
            payBtn.clicked.connect(lambda: payed(self))
            grid.addWidget(payBtn, 3, 6, 1, 1, Qt.AlignTop)
            rlist = ['1','2','3','4','5','6','7','8','9','0','.','DEL']
            for t in range(0,12):
                rBtn = QPushButton()
                rBtn.setFixedSize(132, 100)
                rBtn.setFont(QFont("Times", 14, 75))
                rBtn.setStyleSheet("color: white;  background-color: #7f8371")
                rBtn.setFocusPolicy(Qt.NoFocus)
                rBtn.setText(rlist[t])
                if t == 0:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignTop)
                elif t == 1:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignTop | Qt.AlignCenter)
                elif t == 2:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignTop | Qt.AlignRight)
                elif t == 3:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignVCenter)
                elif t == 4:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignVCenter | Qt.AlignCenter)
                elif t == 5:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignVCenter | Qt.AlignRight)
                elif t == 6:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignBottom)
                elif t == 7:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignBottom | Qt.AlignCenter)
                elif t == 8:
                   grid.addWidget(rBtn, 3, 4, 2, 2, Qt.AlignBottom | Qt.AlignRight)
                elif t == 9:
                   grid.addWidget(rBtn, 5, 4, 2, 2, Qt.AlignTop)
                elif t == 10:
                   grid.addWidget(rBtn, 5, 4, 2, 2, Qt.AlignTop | Qt.AlignCenter)
                elif t == 11:
                   grid.addWidget(rBtn, 5, 4, 2, 2, Qt.AlignTop | Qt.AlignRight)
 
                rBtn.clicked.connect(lambda checked, nr = rlist[t] : getnumber(nr))
                
            def getnumber(nr):
                if nr == '.' and '.' in self.text:
                    return
                elif nr == 'DEL':
                    nr = ''
                    self.text = nr
                self.text += nr
                self.qcashEdit.setText(self.text)
                                                                         
            self.q1Edit = QLineEdit()
            self.q1Edit.setText('')
            self.q1Edit.setStyleSheet("color: #F8F7EE;  background-color: #F8F7EE")
            self.q1Edit.setFont(QFont("Arial", 12, 75))
            self.q1Edit.setFixedSize(155, 40)
            self.q1Edit.setFocus(True)
            reg_ex = QRegExp("^[0-9]{8}|^[0-9]{13}$")
            input_validator = QRegExpValidator(reg_ex, self.q1Edit)
            self.q1Edit.setValidator(input_validator)
            self.q1Edit.returnPressed.connect(lambda: set_barcodenr(self))
                       
            self.qspin = QSpinBox()
            self.qspin.setRange(1, 99)
            self.qspin.setValue(1)
            self.qspin.setFocusPolicy(Qt.NoFocus)
            self.qspin.lineEdit().setReadOnly(True)
            self.qspin.setFrame(True)
            self.qspin.setFont(QFont('Arial', 12))
            self.qspin.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.qspin.setFixedSize(60, 40)
             
            def valuechange():
                self.qspin.setValue(self.qspin.value())
            self.qspin.valueChanged.connect(valuechange)
            
            self.logonstate = QLabel()
            self.pixmap = QPixmap('./logos/red.png')
            self.logonstate.setPixmap(self.pixmap.scaled(40,40))
            grid.addWidget(self.logonstate, 0, 6, 1, 1, Qt.AlignRight | Qt.AlignBottom)
                     
            self.mkop = QLineEdit()
            if self.mclient:
                self.mkop.setText('Client: '+str(self.mclient)+' Empl. '+str(self.mcallname))
            else:
                self.mkop.setText('No client selected')
            self.mkop.setReadOnly(True)
            self.mkop.setFont(QFont("Consolas", 20, 75))
            self.mkop.setStyleSheet("color: black; background-color: #F8F7EE")  
            self.mkop.setFocusPolicy(Qt.NoFocus)
            self.mkop.setFixedWidth(600)  
            
            self.view = QTextEdit()
            self.view.setStyleSheet('color: black; background-color: #F8F7EE')  
            self.mlist = []
            self.view.setText('')
            self.view.setFont(QFont("Consolas",20, 75))
            self.view.setFocusPolicy(Qt.NoFocus)
            self.view.setFixedSize(600, 190)  
            
            self.mtotal = 0.00
            self.mtotvat = 0.00
            self.qtailEdit = QLineEdit()
            self.qtailEdit.setFont(QFont("Consolas", 20, 75))
            self.qtailEdit.setStyleSheet('color: black; background-color: #F8F7EE') 
            self.qtailEdit.setReadOnly(True)
            self.qtailEdit.setFixedWidth(600)
            self.qtailEdit.setFocusPolicy(Qt.NoFocus)
            self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
            self.qtailEdit.setText(self.qtailtext)

            grid .addWidget(self.mkop, 1, 4, 2, 3, Qt.AlignRight | Qt.AlignTop)           
            grid.addWidget(self.view,  1, 4, 2, 3, Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(self.qtailEdit, 1, 4, 2, 3, Qt.AlignRight | Qt.AlignBottom)
            
            self.albl = QLabel()
            self.albl.setFont(QFont("Arial", 12, 75))
            self.albl.setStyleSheet("color: red ; background-color : #39CCCC")
            self.albl.setText("Notification Bar")
            self.albl.setAlignment(Qt.AlignCenter)
            self.albl.setFixedSize(560, 40)
            grid.addWidget(self.albl, 0, 4, 1, 3, Qt.AlignBottom)

            lbl1 = QLabel('Barcodescan')
            lbl1.setFont(QFont("Arial", 12))
            grid.addWidget(lbl1, 0, 5, 1, 1, Qt.AlignRight | Qt.AlignTop)
            grid.addWidget(self.q1Edit , 0, 6, 1, 1, Qt.AlignRight | Qt.AlignTop)
            
            lbl2 = QLabel('Number')
            lbl2.setFont(QFont("Arial", 12))
            grid.addWidget(lbl2, 0, 6, 1, 1, Qt.AlignVCenter)
            grid.addWidget(self.qspin, 0, 6, 1, 1, Qt.AlignRight | Qt.AlignVCenter)
                    
            metadata = MetaData()
            buttons = Table('buttons', metadata,
                Column('buttonID', Integer(), primary_key=True),
                Column('buttontext', String),
                Column('reference', String),
                Column('barcode',  String),
                Column('accent', Integer),
                Column('bg_color', String))
            
            def getMaingrouppicture():
                piclist = ['./logos/1.png','./logos/2.png','./logos/3.png',\
                     './logos/4.png','./logos/5.png','./logos/6.png','./logos/7.png',\
                     './logos/8.png', './logos/9.png','./logos/10.png']
                lblpic = QLabel()
                pixmap = QPixmap(piclist[int(self.index/90)])
                lblpic.setPixmap(pixmap.scaled(196,300))
                grid.addWidget(lblpic, 3, 3, 2, 1)
                
            def btngroupChange(self):
                def indexIncrease(self):
                    self.index += 90
                    self.index = self.index%900 
                    self.btngroup = 1
                    getMaingrouppicture()
                    btngroupChange(self)
                        
                def indexDecrease(self):
                    self.index -= 90
                    self.index = self.index%900
                    self.btngroup = 1
                    getMaingrouppicture()
                    btngroupChange(self)
                                                                                                        
                if self.btngroup == 1:
                    self.index -= self.index%90
                    if self.maccess < 2:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(str(rphbtn[int(self.index/18)][0])+'\n'+rphbtn[int(self.index/18)][1].strip())
                    self.hBtn.setStyleSheet('color: black; background-color:'+rphbtn[int(self.index/18)][3])
                    self.btngroup = 2
                elif self.btngroup == 2:
                    self.index += 18
                    if self.maccess < 2:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(str(rphbtn[int(self.index/18)][0])+'\n'+rphbtn[int(self.index/18)][1].strip())
                    self.hBtn.setStyleSheet('color: black; background-color:'+rphbtn[int(self.index/18)][3])
                    self.btngroup = 3
                elif self.btngroup == 3:
                    self.index += 18
                    if self.maccess < 2:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(str(rphbtn[int(self.index/18)][0])+'\n'+rphbtn[int(self.index/18)][1].strip())
                    self.hBtn.setStyleSheet('color: black; background-color:'+rphbtn[int(self.index/18)][3])
                    self.btngroup = 4
                elif self.btngroup == 4:
                    self.index += 18
                    if self.maccess < 2:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(str(rphbtn[int(self.index/18)][0])+'\n'+rphbtn[int(self.index/18)][1].strip())
                    self.hBtn.setStyleSheet('color: black; background-color:'+rphbtn[int(self.index/18)][3])
                    self.btngroup = 5
                elif self.btngroup == 5:
                    self.index += 18
                    if self.maccess < 2:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(str(rphbtn[int(self.index/18)][0])+'\n'+rphbtn[int(self.index/18)][1].strip())
                    self.hBtn.setStyleSheet('color: black; background-color:'+rphbtn[int(self.index/18)][3])
                    self.btngroup = 1
                             
                self.hBtn.setFont(QFont("Consolas", 12, 75))
                self.hBtn.setFocusPolicy(Qt.NoFocus)
                self.hBtn.setFixedSize(200,150)
                grid.addWidget(self.hBtn, 0, 3) 
                
                nextgrpBtn = QPushButton('\u21c8')
                nextgrpBtn.setStyleSheet("color: black;  background-color: #e7e71c")
                nextgrpBtn.setFont(QFont("Arial", 40, 75))
                nextgrpBtn.clicked.connect(lambda: indexDecrease(self))  
                nextgrpBtn.setFocusPolicy(Qt.NoFocus)
                nextgrpBtn.setFixedSize(200, 150)
                grid.addWidget(nextgrpBtn, 2, 3)
                
                getMaingrouppicture()
                                            
                previousgrpBtn = QPushButton('\u21ca')
                previousgrpBtn.setStyleSheet("color: black;  background-color: #e7e71c")
                previousgrpBtn.setFont(QFont("Arial", 40, 75))
                previousgrpBtn.clicked.connect(lambda: indexIncrease(self))  
                previousgrpBtn.setFocusPolicy(Qt.NoFocus)
                previousgrpBtn.setFixedSize(200, 150)    
                grid.addWidget(previousgrpBtn, 5, 3)
                 
                logo = QLabel()
                pixmap = QPixmap('./logos/logo.png')
                pixmap.scaled(196,146)
                logo.setPixmap(pixmap)
            
                grid.addWidget(logo, 1, 3)
                                                        
                self.hBtn.clicked.connect(lambda: btngroupChange(self)) 
                          
                a = self.index
                selbtn = select([buttons]).where(and_(buttons.c.buttonID>self.index,\
                     buttons.c.buttonID<self.index+19)).order_by(buttons.c.buttonID)
                rpbtn = con.execute(selbtn) 
                  
                btnlist = []
                for row in rpbtn:
                    accent = ''
                    if row[4]:
                        accent = '\n\u2B24'
                    if self.maccess < 2:               #choose buttontext
                        aBtn = QPushButton(row[1].strip()+accent) 
                        btnlist.append(row[3].strip()) #choose barcode
                        aBtn.clicked.connect(lambda checked, btnbarcode = btnlist[a%18] : getbarcode(btnbarcode))
                    else:    #showbuttonnumber reference and barcode for administrator
                        aBtn = QPushButton(str(row[0])+'\n'+row[2].strip()+'\n'+row[3])
                        btnlist.append(str(row[0]))    #choose buttonnumber
                        aBtn.clicked.connect(lambda checked, btnnumber = btnlist[a%18] : getbuttonnr(btnnumber)) 
                    aBtn.setFont(QFont("Consolas", 12, 75))
                    aBtn.setStyleSheet('color: black; background-color:'+row[5])
                    aBtn.setFocusPolicy(Qt.NoFocus)
                    aBtn.setFixedSize(200, 150)
                                
                    if a < self.index+3:
                        grid.addWidget(aBtn, 0, a%3)
                    elif a < self.index+6:
                        grid.addWidget(aBtn, 1, a%3) 
                    elif a < self.index+9:
                        grid.addWidget(aBtn, 2, a%3) 
                    elif a < self.index+12:
                        grid.addWidget(aBtn, 3, a%3)
                    elif a < self.index+15:
                        grid.addWidget(aBtn, 4, a%3) 
                    elif a < self.index+18:
                        grid.addWidget(aBtn, 5, a%3) 
    
                    a += 1
                                    
            self.btngroup = 1 
            self.index = 0
              
            btngroupChange(self)
                                                     
            def getbarcode(btnbarcode):
                self.q1Edit.setText(btnbarcode) 
                if sys.platform == 'win32':
                    import keyboard
                    keyboard.write('\n')                          #Windows
                else:
                    subprocess.call(["xdotool", "key", "Return"]) #Linux
                    
            def getbuttonnr(btnnumber):
                mflag = 4
                articleRequest(mflag, btnnumber)
                                       
            self.plusminBtn = QPushButton('+')
            self.plusminBtn.setCheckable(True)
            self.plusminBtn.setFont(QFont("Arial",12,75))
            self.plusminBtn.setStyleSheet("color: black;  background-color: #FFD700")
            self.plusminBtn.clicked.connect(lambda: plusminChange(self))
            self.plusminBtn.setFocusPolicy(Qt.NoFocus)
            self.plusminBtn.setFixedSize(40, 40)
                 
            grid.addWidget(self.plusminBtn, 0, 6, 1, 1, Qt.AlignCenter | Qt.AlignVCenter)
                    
            self.displayBtn = QPushButton('Big Display')
            self.displayBtn.clicked.connect(lambda: bigDisplay(self))
            self.displayBtn.setFont(QFont("Arial",12,75))
            self.displayBtn.setFocusPolicy(Qt.NoFocus)
            self.displayBtn.setFixedSize(200,150)
            self.displayBtn.setStyleSheet("color: black;  background-color: #A267A1")
      
            grid.addWidget(self.displayBtn, 3, 7, 1, 1, Qt.AlignRight)
            
            routeSeats = 1
            seatText = "Notification Bar"
            self.tablesBtn = QPushButton('Open/Change\nTables/Seats')
            self.tablesBtn.clicked.connect(lambda: seatsArrange(self, routeSeats, seatText))
            self.tablesBtn.setFont(QFont("Arial",12,75))
            self.tablesBtn.setFocusPolicy(Qt.NoFocus)
            self.tablesBtn.setFixedSize(200,150)
            self.tablesBtn.setStyleSheet("color: black;  background-color: #d5bb55")
      
            grid.addWidget(self.tablesBtn, 4, 7, 1, 1, Qt.AlignRight)
            
            self.printBtn = QPushButton('Printing')
            self.printBtn.clicked.connect(lambda: printReceipt(self))
            self.printBtn.setFont(QFont("Arial",12,75))
            self.printBtn.setFocusPolicy(Qt.NoFocus)
            self.printBtn.setFixedSize(200,150)
            self.printBtn.setStyleSheet("color: black;  background-color: #00FFFF")
      
            grid.addWidget(self.printBtn, 2, 7, 1, 1, Qt.AlignRight)
            
            self.adminBtn = QPushButton('Administration')
            self.adminBtn.setFocusPolicy(Qt.NoFocus)
            self.adminBtn.setHidden(True)
            self.adminBtn.setFont(QFont("Arial",12,75))
            self.adminBtn.setFixedSize(200, 40) 
            self.adminBtn.setStyleSheet("color: black; background-color: #FFD700")
            self.adminBtn.clicked.connect(lambda: adminMenu()) 
    
            grid.addWidget(self.adminBtn, 0, 4, 1, 1, Qt.AlignVCenter)
                                                   
            self.closeBtn = QPushButton('Exit')
            self.closeBtn.clicked.connect(lambda: windowClose(self))
            self.closeBtn.setFont(QFont("Arial",12,75))
            self.closeBtn.setFocusPolicy(Qt.NoFocus)
            self.closeBtn.setFixedSize(200,150)
            self.closeBtn.setStyleSheet("color: black; background-color:   #B0C4DE") 

            grid.addWidget(self.closeBtn, 0, 7, 1, 1, Qt.AlignRight)
                                  
            infoBtn = QPushButton('Information')
            infoBtn.clicked.connect(lambda: info())
            infoBtn.setFont(QFont("Arial",12,75))
            infoBtn.setFocusPolicy(Qt.NoFocus)
            infoBtn.setFixedSize(200,150)
            infoBtn.setStyleSheet("color: black;  background-color: #00BFFF")
    
            grid.addWidget(infoBtn, 1, 7, 1, 1, Qt.AlignRight )
           
            self.clientBtn = QPushButton('Select\nClient')
            self.clientBtn.clicked.connect(lambda: choseClient(self))
            self.clientBtn.setFont(QFont("Arial",12,75))
            self.clientBtn.setFocusPolicy(Qt.NoFocus)
            self.clientBtn.setFixedSize(200,150)            
            self.clientBtn.setStyleSheet("color:black; background-color: #3498db")
        
            grid.addWidget(self.clientBtn, 5, 7, 1, 1, Qt.AlignRight)   
            
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            lbl3.setFixedHeight(40)
            grid.addWidget(lbl3, 6, 0, 1, 7, Qt.AlignCenter)
                                      
            self.setLayout(grid)
            self.setGeometry(100, 40, 600, 300)
            
    window = widget()
    window.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    if sys.platform == "linux":
        os.system("../.usbkbd.sh")
    barcodeScan()
    app.exec_()  