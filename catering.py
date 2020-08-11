import sys, random, barcode, datetime, os, subprocess, keyboard, collections
from math import sqrt
from barcode.writer import ImageWriter 
from PyQt5.QtCore import Qt, QSize, QRegExp, QAbstractTableModel, QPoint, QCoreApplication
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie, QRegExpValidator, QColor,\
           QImage, QPainter
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QDialog, QLabel, QPushButton,\
        QMessageBox, QSpinBox, QComboBox, QTextEdit, QApplication, QWidget,\
        QVBoxLayout, QTableView, QStyledItemDelegate, QCheckBox, QPlainTextEdit
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, create_engine,\
                     Float, select, update,insert, delete, func, and_, ForeignKey

def refresh(self):
    self.close()
    seatsArrange(self)

def paySuccess():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Payment succeeded!')
    msg.setWindowTitle('Payments instances')
    msg.exec_() 
    
def noImports():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    msg.setText('No imports available!')
    msg.setWindowTitle('Import')
    msg.exec_()   
    
def importDone():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Import done!')
    msg.setWindowTitle('Import')
    msg.exec_() 

def noBarcode(mbarcode):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No barcode '+mbarcode+' found!')
    msg.setWindowTitle('Import list')
    msg.exec_() 
    
def barcodeExist(mbarcode):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Barcode '+mbarcode+' exists already!')
    msg.setWindowTitle('Import list')
    msg.exec_() 
 
def alertText(message):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message)
    msg.setWindowTitle('Transactions')
    msg.exec_() 
    
def insertOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert succeeded!')
    msg.setWindowTitle('Insert records')
    msg.exec_()
           
def windowClose(self):
    self.close()
    sys.exit()
    
def countTurnover(mindex):
    metadata = MetaData()
    sales = Table('sales', metadata,
        Column('salesID', Integer, primary_key=True),
        Column('receiptnumber', Integer),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('item_price', Float),
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
            self.setGeometry(600, 200, 150, 100)
                
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
            self.k0Edit.setFixedWidth(300)
            self.k0Edit.setFont(QFont("Arial",10))
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
            self.k0Edit.setFixedWidth(280)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('New employee')
            self.k0Edit.addItem('View / Change employees')
                                       
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
            self.k0Edit.setFixedWidth(300)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Insert new articles')
            self.k0Edit.addItem('View / Change articles')
            self.k0Edit.addItem('Imports new articles')
            self.k0Edit.addItem('Imports price-changes articles')
            self.k0Edit.addItem('Imports expired articles')
            self.k0Edit.addItem('View imports new articles')
            self.k0Edit.addItem('View imports price-changes articles')
            self.k0Edit.addItem('View imports expired articles')
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
                    articleRequest(mflag)
                elif mindex == 2:
                    newProducts()
                elif mindex == 3:
                    changePrices()
                elif mindex == 4:
                    expiredProducts() 
                elif mindex == 5:
                    path = "./forms/Imports/New/"
                    mtitle = "View import new products"
                    viewList(path, mtitle)
                elif mindex == 6:
                    path = "./forms/Imports/Prices/"
                    mtitle = "View imports prices"
                    viewList(path, mtitle)
                elif mindex == 7:
                    path = "./forms/Imports/Expired/"
                    mtitle = "View import expired"
                    viewList(path, mtitle)
                elif mindex == 8:
                    flag = 2
                    articleRequest(flag)
                elif mindex == 9:
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
    
def purchaseMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Purchase Submenu")
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
            self.k0Edit.setFixedWidth(230)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Collecting purchases')
            self.k0Edit.addItem('View purchases')
            self.k0Edit.addItem('Printing purchases')
            self.k0Edit.addItem('Processing deliveries')
            self.k0Edit.addItem('View deliveries')
            self.k0Edit.addItem('Printing deliveries')
                             
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    purchaseCollect()
                elif mindex == 1:
                    if sys.platform == 'win32':
                        path = '.\\forms\\Purchasing\\'
                    else:
                        path = './forms/Purchasing/'
                    mtitle = 'View purchasing lists'
                    viewList(path, mtitle)
                elif mindex == 2:
                    if sys.platform == 'win32':
                        path = '.\\forms\\Purchasing\\'
                    else:
                        path = './forms/Purchasing/'
                    pickList(path)
                elif mindex == 3:
                    deliveryImport()
                elif mindex == 4:
                    if sys.platform == 'win32':
                        path = '.\\forms\\Deliveries\\'
                    else:
                        path = './forms/Deliveries/'
                    mtitle = 'View delivery lists'
                    viewList(path, mtitle)
                elif mindex == 5:
                    if sys.platform == 'win32':
                        path = '.\\forms\\Deliveries\\'
                    else:
                        path = './forms/Deliveries/'
                    pickList(path)
                     
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
    
def buttonMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Define Buttons")
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
            self.k0Edit.setFixedWidth(220)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Button new barcode')
            self.k0Edit.addItem('Button existing barcode')
            self.k0Edit.addItem('Groupbutton')
                                           
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
 
                if mindex == 0:
                    newBarcode()
                elif mindex == 1:
                    existingBarcode()
                elif mindex == 2:
                    groupButtons()
                      
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
            self.setGeometry(800, 50, 400, 600)
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
             
    header = ['ButtonNumber', 'Buttongrouptext', 'Reference']
    
    metadata = MetaData()
    groupbuttons = Table('groupbuttons', metadata,
        Column('groupID', Integer(), primary_key=True),
        Column('buttongrouptext', String),
        Column('reference', String))
     
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
                    self.setWindowTitle("Parameters changing")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setStyleSheet("background-color: #D9E1DF")
                    self.setFont(QFont('Arial', 10))  
                    
                    #reference
                    self.q2Edit = QLineEdit(rpbtn[2])
                    self.q2Edit.setFixedWidth(40)
                    self.q2Edit.setFont(QFont("Arial",10))
                    self.q2Edit.setStyleSheet('color: black; background-color: gainsboro')
                    self.q2Edit.setDisabled(True)
                    
                    #buttongroup
                    self.q3Edit = QPlainTextEdit()
                    self.q3Edit.setFixedSize(170,110)
                    self.q3Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.q3Edit.setFont(QFont("Consolas", 12, 75))
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                         
                    def updGroupbutton(self):
                        mbuttontext = self.q3Edit.toPlainText()
                        mlist = mbuttontext.split('\n')
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
                            insertOK()
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
            self.setGeometry(300, 50, 400, 600)
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
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
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
                         insertOK()
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
                    self.setGeometry(500, 200, 150, 150)
            
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
            self.k0Edit.setFixedWidth(280)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE') 
            self.k0Edit.addItem('Employees Submenu')
            self.k0Edit.addItem('Articles Submenu')
            self.k0Edit.addItem('Sales - View')
            self.k0Edit.addItem('Payments - View / Pay')
            self.k0Edit.addItem('Purchases Submenu')
            self.k0Edit.addItem('Buttons Submenu')
            self.k0Edit.addItem('Parameters - View / Change')
            self.k0Edit.addItem('Turnover Submenu')
            
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
                    salesRequest()
                elif mindex == 3:
                    paymentsRequest()
                elif mindex == 4:
                    purchaseMenu()
                elif mindex == 5:
                    buttonMenu()
                elif mindex == 6:
                    paramChange()
                elif mindex == 7:
                    turnoverMenu()

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
        selempl = select([employees]).where(employees.c.barcodeID == emplnr)
        rpempl = con.execute(selempl).first()
        if idx.column() == 0:
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
                  
                    def updateAcc():
                        fname = q2Edit.text()
                        lname = q3Edit.text()
                        cname = q4Edit.text()
                        maccess = q5Edit.text()
                        updacc = update(employees).where(employees.c.barcodeID == emplnr).\
                        values(firstname = fname,lastname = lname, callname = cname,\
                               access = int(maccess))
                        con.execute(updacc)
                        insertOK()
                        self.close()
                                          
                    self.setLayout(grid)
                    self.setGeometry(600, 200, 150, 100)
                    
            window = Window()
            window.exec_()
           
    win = Widget(data_list, header)
    win.exec_()
    
def changePrices():
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('item_price', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    path = "./forms/Imports/Prices/"
    mcount = 0
    for filename in os.listdir(path):
        file = (open(path+filename, "r"))
        if filename[-4:] != '.txt':
            lists = file.readlines()
            item = len(lists)
            for line in range(0, item):
                mbarcode = lists[line][:13].strip()
                mprice =  float(lists[line][14:26].strip())
                sel = select([articles]).where(articles.c.barcode == mbarcode)
                if con.execute(sel).fetchone():                    
                    updart = update(articles).where(articles.c.barcode == mbarcode).\
                        values(item_price = mprice)
                    con.execute(updart)
                else:
                    noBarcode(mbarcode)
            importDone()
            file.close()
            os.rename(path+filename,path+filename+'.txt')
            mcount += 1
    if mcount == 0:
        noImports()
                             
def expiredProducts():
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True))
    loss = Table('loss', metadata,
        Column('barcode', None, ForeignKey('articles.barcode')))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    path = "./forms/Imports/Expired/"
    for filename in os.listdir(path):
        file = (open(path+filename, "r"))
        mcount = 0
        if filename[-4:] != '.txt':
            lists = file.readlines()
            item = len(lists)
            for line in range(0, item):
                mbarcode = lists[line][:13].strip()
                selloss = select([loss]).where(loss.c.barcode == mbarcode)
                if con.execute(selloss).fetchone():
                    delloss = delete(loss).where(loss.c.barcode == mbarcode)
                    con.execute(delloss)
                sel = select([articles]).where(articles.c.barcode == mbarcode)
                if con.execute(sel).fetchone():
                    delart = delete(articles).where(articles.c.barcode == mbarcode)
                    con.execute(delart)
                else:
                    noBarcode(mbarcode)
            importDone()
            file.close()
            os.rename(path+filename,path+filename+'.txt')
            mcount += 1
    if mcount == 0:
        noImports()
 
def newProducts():
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('item_price', Float),
        Column('item_unit', String),
        Column('article_group', String),
        Column('thumbnail', String),
        Column('category', Integer),
        Column('VAT', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    path = "./forms/Imports/New/"
    for filename in os.listdir(path):
        file = (open(path+filename, "r"))
        mcount = 0
        if filename[-4:] != '.txt':
            lists = file.readlines()
            item = len(lists)
            for line in range(0, item):
                mbarcode = lists[line][:13].strip()           #0-12  +13 , 
                mdescr = lists[line][14:64].strip()           #14-63 +64 ,
                mprice =  float(lists[line][66:78].strip())   #66-77 +78 ,
                munit = lists[line][79:85].strip()            #79-84 +85 ,
                mgroup = lists[line][86:126].strip()          #86-125 +126 ,
                thumb = lists[line][127:178].strip()          #127-177 +178 ,
                mcat = int(lists[line][179:180].strip())      #179- 179 +180 ,
                mvat = lists[line][181:185].strip()           #181 - 184 +185 ,
         
                sel = select([articles]).where(articles.c.barcode == mbarcode)
                if con.execute(sel).fetchone():
                    barcodeExist(mbarcode)
                else:
                    insart = insert(articles).values(barcode = mbarcode,description=mdescr,\
                     item_price=mprice,item_unit=munit,article_group=mgroup,thumbnail=thumb,\
                     category=mcat,VAT=mvat)
                    con.execute(insart)
                    ean = barcode.get('ean13',mbarcode, writer=ImageWriter())
                    if sys.platform == 'win32':
                        ean.save('.\\Barcodes\\Articles\\'+str(mbarcode))
                    else:
                        ean.save('./Barcodes/Articles/'+str(mbarcode))
       
            importDone()
            file.close()
            os.rename(path+filename,path+filename+'.txt')
            mcount += 1
    if mcount == 0:
        noImports()
      
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
            self.setGeometry(250, 50, 1000, 900)
            
    window = Widget()
    window.exec_()
    
def printFile(filename, path):
    if sys.platform == 'win32':
        os.startfile(path+filename, "print")
    else:
        os.system("lpr "+path+filename)
    
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
              self.setGeometry(550, 200, 150, 150)
              
              def getfile(self):
                  filename = self.cb.currentText()
                  viewFile(path+filename, mtitle)
          
    win = combo()
    win.exec_()

def pickList(path):    
    filelist = []
    for file in os.listdir(path):
        if file[-4:] == '.txt':
            filelist.append(file)
    class combo(QDialog):
        def __init__(self, parent=None):
              super(combo, self).__init__(parent)
              self.setWindowTitle("Printing lists")
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
              
              numberEdit = QLineEdit('1')
              numberEdit.setStyleSheet("background: #F8F7EE")
              numberEdit.setFixedWidth(30)
              numberEdit.setFont(QFont("Arial",10))
              reg_ex = QRegExp("^[0-9]{1,2}$")
              input_validator = QRegExpValidator(reg_ex, numberEdit)
              numberEdit.setValidator(input_validator)
              
              def numberChanged():
                  numberEdit.setText(numberEdit.text())
              numberEdit.textChanged.connect(numberChanged)
                            
              nbrlbl = QLabel('Copies to print')
              nbrlbl.setFont(QFont("Arial", 10))
              grid.addWidget(nbrlbl, 3, 1, 1, 2)
              grid.addWidget(numberEdit, 3, 2, 1, 1, Qt.AlignRight)
              
              plbl = QLabel()
              pmap = QPixmap('./thumbs/MG3650.jpg')
              plbl.setPixmap(pmap)
              grid.addWidget(plbl , 3, 0, 2, 1, Qt.AlignCenter)
                    
              cancelBtn = QPushButton('Close')
              cancelBtn.clicked.connect(self.close) 
                
              grid.addWidget(cancelBtn, 4, 1, 1, 1, Qt.AlignRight)
              cancelBtn.setFont(QFont("Arial",10))
              cancelBtn.setFixedWidth(90)
              cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")    
              
              printBtn = QPushButton('Printing')
              printBtn.clicked.connect(lambda: getfile(self))  
                
              grid.addWidget(printBtn,  4, 2)
              printBtn.setFont(QFont("Arial",10))
              printBtn.setFixedWidth(90)
              printBtn.setStyleSheet("color: black;  background-color: gainsboro")    
               
              reslbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
              reslbl.setFont(QFont("Arial",10))
              grid.addWidget(reslbl, 5, 0, 1, 3, Qt.AlignCenter)
                
              self.setLayout(grid)
              self.setGeometry(550, 300, 150, 150)
              
              def getfile(self):
                  filename = self.cb.currentText()
                  mnumber = numberEdit.text()
                  for x in range(0, int(mnumber)):
                      printFile(filename,path)
                  printing()
          
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
           
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
    myear = int(str(datetime.date.today())[0:4])
    if myear%2 == 1 and int(rppar[3][2]) == 0:
        selarticles = select([articles]).order_by(articles.c.barcode)
        rparticles = con.execute(selarticles)
        updpar = update(params).where(params.c.paramID == 4).values(value = 1)
        con.execute(updpar)
                     
        for row in rparticles:
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
            mordersize = round(sqrt(2*row[5]*rppar[4][2])/(row[1]*rppar[5][2]),0)
            mjrverbr = row[5]
            if row[3] == 1:
                minstock = round(mjrverbr*1/17, 0) # < 3 weeks deliverytime
            elif row[3] == 2:
                minstock = round(mjrverbr*2/17, 0) # < 6 weeks deliverytime
            elif row[3] == 3:
                minstock = round(mjrverbr*4/17, 0) # < 12 weeks deliverytime
            elif row[3] == 4: 
                minstock = round(mjrverbr*8/17, 0) # < 26 weeks deliverytime
            elif row[3] == 5: 
                minstock = round(mjrverbr*16/17,0) # < 52 weeks deliverytime
                
            updart = update(articles).where(articles.c.barcode == row[0]).\
                values(annual_consumption_1 = 0, minimum_stock = minstock, order_size = mordersize)
            con.execute(updart)
  
def articleRequest(mflag):
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('item_price', Float),
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
        Column('VAT', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
     
    selarticles = select([articles]).order_by(articles.c.barcode)
    rparticles = con.execute(selarticles)
            
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
            table_view.setItemDelegateForColumn(9, showImage(self))
            table_view.setColumnWidth(9, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            if mflag == 1:
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
                                       
    header = ['Barcode','Description', 'Item-Price', 'Item-Stock', 'Item-Unit',\
          'Mininum-Stock', 'Order-Size', 'Location', 'Article_Group', 'Thumbnail',\
          'Category', 'Order-Balance', 'Order-Status' ,'Mutation-Date', \
          'Annual-Consumption_1','Annual-Consumption_2', 'VAT']    
        
    data_list=[]
    for row in rparticles:
        data_list += [(row)] 
    
    def defineButton(idx):
        mbarcode = idx.data()
        if idx.column() == 0:
            metadata = MetaData()
            buttons = Table('buttons', metadata,
                Column('buttonID', Integer, primary_key=True),
                Column('barcode', String),
                Column('buttontext', String),
                Column('accent', Integer))
            
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
                    self.q2Edit = QLineEdit()
                    self.q2Edit.setFixedWidth(40)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Consolas",10, 75))
                    reg_ex = QRegExp("^[0-9]{0,3}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    #button-text
                    self.q3Edit = QPlainTextEdit()
                    self.q3Edit.setFixedSize(170,100)
                    self.q3Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.q3Edit.setFont(QFont("Consolas",12,75))
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    
                    self.cBox = QCheckBox('Accentutation')
                    self.cBox.setFont(QFont("Arial",10))
                          
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    def cboxChanged():
                        self.cBox.setCheckState(self.cBox.checkState())
                    self.cBox.stateChanged.connect(cboxChanged)  
                    
                    lbl1 = QLabel('Barcodenummer')
                    lbl1.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl1, 1, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q1Edit, 1, 1)
                     
                    lbl2 = QLabel('Button-Number')
                    lbl2.setFont(QFont("Consolas", 10, 75))
                    grid.addWidget(lbl2, 2, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q2Edit, 2, 1)
                    
                    lbl3 = QLabel('Button-Text')
                    lbl3.setFont(QFont("Consolas", 12, 75))
                    grid.addWidget(lbl3, 3, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q3Edit, 3, 1)
                    
                    grid.addWidget(self.cBox, 4, 1, 1, 1, Qt.AlignRight)
                                 
                    applyBtn = QPushButton('Insert')
                    applyBtn.clicked.connect(lambda: insBtnText())
                       
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                    grid.addWidget(applyBtn, 5, 1 , 1, 1, Qt.AlignRight)
                        
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close) 
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
                    grid.addWidget(cancelBtn, 5, 0, 1, 2, Qt.AlignCenter)
                    
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 6, 0, 1, 3, Qt.AlignCenter)
                   
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
                             values(barcode=str(mbarcode), buttontext=mbtntext, accent=maccent)
                            con.execute(updbtn)
                            insertOK()
                            self.close()
                                            
                    self.setLayout(grid)
                    self.setGeometry(900, 200, 150, 100)
    
            window = Widget()
            window.exec_()
            
    def changeArticle(idx):
        mbarcode = idx.data() 
        selarticle = select([articles]).where(articles.c.barcode == mbarcode)
        rparticle = con.execute(selarticle).first()
        if idx.column() == 0:
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
        
                    #description
                    self.q2Edit = QLineEdit(rparticle[1])    
                    self.q2Edit.setFixedWidth(400)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{1,50}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    #item_price
                    self.q3Edit = QLineEdit(str(round(rparticle[2],2)))
                    self.q3Edit.setAlignment(Qt.AlignRight)
                    self.q3Edit.setFixedWidth(100)
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q3Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q3Edit)
                    self.q3Edit.setValidator(input_validator)
                    
                    #item_stock
                    self.q4Edit = QLineEdit(str(round(rparticle[3],2)))
                    self.q4Edit.setAlignment(Qt.AlignRight)
                    self.q4Edit.setFixedWidth(100)
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q4Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
                    
                    #item_unit
                    self.q5Edit = QComboBox()
                    self.q5Edit.setFixedWidth(170)
                    self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q5Edit.setFont(QFont("Arial",10))
                    self.q5Edit.addItem('stuk')
                    self.q5Edit.addItem('100')
                    self.q5Edit.addItem('meter')
                    self.q5Edit.addItem('kg')
                    self.q5Edit.addItem('liter')
                    self.q5Edit.addItem('m²')
                    self.q5Edit.addItem('m³')
                    self.q5Edit.setCurrentIndex(self.q5Edit.findText(rparticle[4]))
                    
                    #minimum stock
                    self.q6Edit = QLineEdit(str(round(rparticle[5],2)))
                    self.q6Edit.setAlignment(Qt.AlignRight)
                    self.q6Edit.setFixedWidth(100)
                    self.q6Edit.setFont(QFont("Arial",10))
                    self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q6Edit)
                    self.q6Edit.setValidator(input_validator)
        
                    #order_size
                    self.q7Edit = QLineEdit(str(round(rparticle[6],2)))
                    self.q7Edit.setAlignment(Qt.AlignRight)
                    self.q7Edit.setFixedWidth(100)
                    self.q7Edit.setFont(QFont("Arial",10))
                    self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q7Edit)
                    self.q7Edit.setValidator(input_validator)
                                 
                    #location
                    self.q8Edit = QLineEdit(rparticle[7])
                    self.q8Edit.setFixedWidth(100)
                    self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q8Edit.setFont(QFont("Arial",10))
                                
                    # article_group
                    self.q9Edit = QLineEdit(rparticle[8])
                    self.q9Edit.setFixedWidth(200)
                    self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q9Edit.setFont(QFont("Arial",10))
                        
                    #thumbnail
                    self.q10Edit = QLineEdit(rparticle[9])
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
                    self.q11Edit.setCurrentIndex(rparticle[10]-1)
         
                    #vat
                    self.q12Edit = QComboBox()
                    self.q12Edit.setFixedWidth(100)
                    self.q12Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q12Edit.setFont(QFont("Arial",10))
                    self.q12Edit.addItem('high')
                    self.q12Edit.addItem('low')
                    self.q12Edit.addItem('zero')
                    self.q12Edit.setCurrentIndex(self.q12Edit.findText(rparticle[16]))
                    
                    #order-balance
                    self.q13Edit = QLineEdit(str(round(rparticle[11],2)))
                    self.q13Edit.setFixedWidth(100)
                    self.q13Edit.setAlignment(Qt.AlignRight)
                    self.q13Edit.setStyleSheet('color: black')
                    self.q13Edit.setFont(QFont("Arial",10))
                    self.q13Edit.setDisabled(True)
                    
                    #order_status
                    self.q14Edit = QLineEdit(str(bool(rparticle[12])))
                    self.q14Edit.setFixedWidth(100)
                    self.q14Edit.setStyleSheet('color: black')
                    self.q14Edit.setFont(QFont("Arial",10))
                    self.q14Edit.setDisabled(True)
                   
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    def q3Changed():
                        self.q3Edit.setText(self.q3Edit.text())
                    self.q3Edit.textChanged.connect(q3Changed)
                    
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
                    
                    def q8Changed():
                        self.q8Edit.setText(self.q8Edit.text())
                    self.q8Edit.textChanged.connect(q8Changed)
                    
                    def q9Changed():
                        self.q9Edit.setText(self.q9Edit.text())
                    self.q9Edit.textChanged.connect(q9Changed)
                    
                    def q10Changed():
                        self.q10Edit.setText(self.q10Edit.text())
                    self.q10Edit.textChanged.connect(q10Changed)
                    
                    def q11Changed():
                        self.q11Edit.setCurrentIndex(self.q11Edit.currentIndex())
                    self.q11Edit.currentIndexChanged.connect(q11Changed)
                    
                    def q12Changed():
                        self.q5Edit.setCurrentText(self.q12Edit.currentText()) 
                    self.q12Edit.currentIndexChanged.connect(q12Changed)
                   
                    grid.addWidget(QLabel('Barcodenumber'), 1, 0)
                    grid.addWidget(self.q1Edit, 1, 1)
                    
                    grid.addWidget(QLabel('Description'), 2, 0)
                    grid.addWidget(self.q2Edit, 2, 1 ,1 ,2)
                    
                    grid.addWidget(QLabel('Item_Price'), 3, 0)
                    grid.addWidget(self.q3Edit, 3, 1)
                    
                    grid.addWidget(QLabel('Item-Unit'), 3, 2)
                    grid.addWidget(self.q5Edit, 3, 3)
                    
                    grid.addWidget(QLabel('Minimum_Stock'), 4, 0)
                    grid.addWidget(self.q6Edit, 4, 1)
                    
                    grid.addWidget(QLabel('Item-Stock'), 4, 2)
                    grid.addWidget(self.q4Edit, 4, 3)
                    
                    grid.addWidget(QLabel('Order-Size'), 5, 2)
                    grid.addWidget(self.q7Edit, 5, 3)
                      
                    grid.addWidget(QLabel('Location'), 5, 0)
                    grid.addWidget(self.q8Edit, 5, 1)
                    
                    grid.addWidget(QLabel('Articlegroup'), 6, 2)
                    grid.addWidget(self.q9Edit, 6, 3)
                    
                    grid.addWidget(QLabel('Thumbnail'), 6, 0)
                    grid.addWidget(self.q10Edit, 6, 1)
                    
                    grid.addWidget(QLabel('Category'), 7, 2 )
                    grid.addWidget(self.q11Edit, 7, 3)
                    
                    grid.addWidget(QLabel('VAT'), 7, 0 )
                    grid.addWidget(self.q12Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Order_Balance'), 8, 0 )
                    grid.addWidget(self.q13Edit, 8, 1)
                    
                    grid.addWidget(QLabel('Order-Status'), 8, 2 )
                    grid.addWidget(self.q14Edit, 8, 3)     
          
                    def updArticle(self):
                        mdescr = self.q2Edit.text()
                        mprice = float(self.q3Edit.text())
                        mstock = float(self.q4Edit.text())
                        munit = self.q5Edit.currentText()
                        mminstock = float(self.q6Edit.text())
                        morder_size = float(self.q7Edit.text())
                        mlocation = self.q8Edit.text()
                        martgroup = self.q9Edit.text()
                        mthumb = self.q10Edit.text()
                        mcategory = self.q11Edit.currentIndex()+1
                        mvat = self.q12Edit.currentText()
                        updarticle = update(articles).where(articles.c.barcode==mbarcode)\
                          .values(barcode=mbarcode,description=mdescr,\
                            item_price=mprice,item_stock=mstock,item_unit=munit,\
                            minimum_stock=mminstock,order_size=morder_size, \
                            location_warehouse=mlocation,article_group=martgroup,\
                            thumbnail=mthumb,category=mcategory,VAT=mvat)
                        con.execute(updarticle)
                        insertOK()
                        self.close()
                                 
                    applyBtn = QPushButton('Update')
                    applyBtn.clicked.connect(lambda: updArticle(self))
            
                    grid.addWidget(applyBtn, 9, 3, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                    
                    grid.addWidget(cancelBtn, 9, 3)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 10, 0, 1, 4, Qt.AlignCenter)
             
                    self.setLayout(grid)
                    self.setGeometry(500, 200, 150, 100)
         
            window = Widget()
            window.exec_()
            
    def bookingLoss(idx):
        mbarcode = idx.data()
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
                qnumber = QLineEdit('0')
                qnumber.setFixedWidth(150)
                qnumber.setFont(QFont("Arial",10))
                qnumber.setStyleSheet("color: black;  background-color: #F8F7EE")
                reg_ex = QRegExp("^[+]?[0-9]*\.?[0-9]+$")
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
                       Column('barcode', None, ForeignKey('articles.barcode')),
                       Column('number', Float),
                       Column('bookdate', String),
                       Column('category', String))
                    
                    mdescr = qloss.currentText()
                    mnumber = qnumber.text()
                    try:
                        lossnr = con.execute(select([func.max(loss.c.lossID, type_=Integer)])).scalar()
                        lossnr += 1
                    except:
                        lossnr = 1
                    mbookdate= str(datetime.datetime.now())[0:10]
                    
                    if float(mnumber) > 0:                 
                        ins = insert(loss).values(lossID = lossnr, barcode = mbarcode,\
                            number = mnumber, category = mdescr, bookdate = mbookdate)
                        con.execute(ins)
                        upd = update(articles).where(articles.c.barcode == mbarcode).\
                          values(item_stock = articles.c.item_stock - mnumber)
                        con.execute(upd)
                        insertOK()
                        self.close()
                    else:
                        message = 'Not all fields are filled in!'
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
        Column('item_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
     
    selsales = select([sales]).order_by(sales.c.receiptnumber)
    rpsales = con.execute(selsales)
    
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
              'Item-Price','Sub-Total','Sub-Vat','Callname','Mutation-date']      
        
    data_list=[]
    for row in rpsales:
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
     
    selpay = select([payments]).order_by(payments.c.paydate, payments.c.ovorderID)
    rppay = con.execute(selpay)
    
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
                        paySuccess()  
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
        inlogstr = random.randint(1000000, 9999999)
        ean = barcode.get('ean8', str(inlogstr), writer=ImageWriter()) # for barcode as png
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
            
            q1Edit = QLineEdit(str(mbarcode))
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
                    insacc = insert(employees).values(barcodeID = str(mbarcode),\
                       firstname = fname, lastname = lname,\
                       callname = cname, access = int(maccess))
                    con.execute(insacc)
                    insertOK()
                    self.close()
                else:
                    message = 'Not all fields are filled in!'
                    alertText(message)
                    self.close() 
           
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)
            
    window = Widget()
    window.exec_()
    
def newBarcode():
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('item_price', Float),
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
        Column('VAT', String))
    buttons = Table('buttons', metadata,
        Column('buttonID', Integer, primary_key=True),
        Column('buttontext', String),
        Column('barcode', String),
        Column('reference', String),
        Column('accent', Integer))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    mbarcode=(con.execute(select([func.max(articles.c.barcode, type_=String)])).scalar())
    # generate new barcode
    marticlenr = mbarcode[3:11]
    marticlenr = str((int(marticlenr[0:8]))+int(1))
    total = 0
    for i in range(int(8)):
        total += int(marticlenr[i])*(int(9)-i)
    checkdigit = total % 11 % 10
    marticlenr = marticlenr+str(checkdigit)
    ean = barcode.get('ean13','800'+str(marticlenr), writer=ImageWriter()) # for barcode as png
    mbarcode = ean.get_fullcode()
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
            grid.addWidget(pyqt, 0 ,0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
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
            
            #item_price
            self.q3Edit = QLineEdit('0')
            self.q3Edit.setFixedWidth(100)
            self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q3Edit)
            self.q3Edit.setValidator(input_validator)
 
            #item_unit
            self.q5Edit = QComboBox()
            self.q5Edit.setFixedWidth(170)
            self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q5Edit.setFont(QFont("Arial",10))
            self.q5Edit.addItem('stuk')
            self.q5Edit.addItem('100')
            self.q5Edit.addItem('meter')
            self.q5Edit.addItem('kg')
            self.q5Edit.addItem('liter')
            self.q5Edit.addItem('m²')
            self.q5Edit.addItem('m³')

            #order_size
            self.q7Edit = QLineEdit('0')
            self.q7Edit.setFixedWidth(100)
            self.q7Edit.setFont(QFont("Arial",10))
            self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q7Edit)
            self.q7Edit.setValidator(input_validator)
                         
            #location
            self.q8Edit = QLineEdit()
            self.q8Edit.setFixedWidth(100)
            self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q8Edit.setFont(QFont("Arial",10))
                        
            # article_group
            self.q9Edit = QLineEdit()
            self.q9Edit.setFixedWidth(200)
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
                        
            #button-number
            self.q13Edit = QLineEdit()
            self.q13Edit.setFixedWidth(40)
            self.q13Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q13Edit.setFont(QFont("Consolas",10, 75))
            reg_ex = QRegExp("^[0-9]{0,3}$")
            input_validator = QRegExpValidator(reg_ex, self.q13Edit)
            self.q13Edit.setValidator(input_validator)
            
            #button-text
            self.q14Edit = QPlainTextEdit()
            self.q14Edit.setFixedSize(170,100)
            self.q14Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.q14Edit.setFont(QFont("Consolas",12, 75))
            self.q14Edit.setStyleSheet('color: black; background-color: #F8F7EE')
             
            #accent
            self.cBox = QCheckBox('Accentutation')
            self.cBox.setFont(QFont("Arial",10))
                 
            def q2Changed():
                self.q2Edit.setText(self.q2Edit.text())
            self.q2Edit.textChanged.connect(q2Changed)
            
            def q3Changed():
                self.q3Edit.setText(self.q3Edit.text())
            self.q3Edit.textChanged.connect(q3Changed)
            
            def q5Changed():
                self.q5Edit.setCurrentText(self.q5Edit.currentText())
            self.q5Edit.currentIndexChanged.connect(q5Changed)
            
            def q7Changed():
                self.q7Edit.setText(self.q7Edit.text())
            self.q7Edit.textChanged.connect(q7Changed)
            
            def q8Changed():
                self.q8Edit.setText(self.q8Edit.text())
            self.q8Edit.textChanged.connect(q8Changed)
            
            def q9Changed():
                self.q9Edit.setText(self.q9Edit.text())
            self.q9Edit.textChanged.connect(q9Changed)
            
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
            
            def cboxChanged():
                self.cBox.setCheckState(self.cBox.checkState())
            self.cBox.stateChanged.connect(cboxChanged)
                         
            lbl1 = QLabel('Barcode')
            lbl1.setFont(QFont("Arial", 10))
            grid.addWidget(lbl1, 3, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q1Edit, 3, 1)
                      
            lbl2 = QLabel('Description')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 4, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q2Edit, 4, 1, 1, 3)
            
            lbl3 = QLabel('Item-price')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 5, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q3Edit, 5, 1)
            
            lbl10 = QLabel('Thumbnail')
            lbl10.setFont(QFont("Arial", 10))
            grid.addWidget(lbl10, 5, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q10Edit, 5, 2, 1, 1, Qt.AlignRight)
               
            lbl5 = QLabel('Item-unit')
            lbl5.setFont(QFont("Arial", 10))
            grid.addWidget(lbl5, 6, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q5Edit, 6, 1)
               
            lbl7 = QLabel('Order-size')
            lbl7.setFont(QFont("Arial", 10))
            grid.addWidget(lbl7, 7, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q7Edit, 7, 1)
            
            lbl8 = QLabel('Location')
            lbl8.setFont(QFont("Arial", 10))
            grid.addWidget(lbl8, 7, 0, 1, 2, Qt.AlignRight)
            grid.addWidget(self.q8Edit, 7, 2, 1, 1, Qt.AlignRight)
            
            lbl9 = QLabel('Article-Group')
            lbl9.setFont(QFont("Arial", 10))
            grid.addWidget(lbl9, 8, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q9Edit, 8, 1)   
     
            lbl11 = QLabel('Category')
            lbl11.setFont(QFont("Arial", 10))
            grid.addWidget(lbl11, 9, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q11Edit, 9, 1, 1, 1, Qt.AlignRight)
         
            lbl12 = QLabel('VAT')
            lbl12.setFont(QFont("Arial", 10))
            grid.addWidget(lbl12, 9, 2)
            grid.addWidget(self.q12Edit, 9, 2, 1, 1, Qt.AlignRight)
            
            lbl13 = QLabel('Button-Number')
            lbl13.setFont(QFont("Arial", 10))
            grid.addWidget(lbl13, 10, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q13Edit, 10, 1)
            
            lbl14 = QLabel('Button-Text')
            lbl14.setFont(QFont("Arial", 10))
            grid.addWidget(lbl14, 10, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q14Edit, 10, 2, 1, 1, Qt.AlignRight)
            
            grid.addWidget(self.cBox, 11, 2 , 1, 1, Qt.AlignRight)
                        
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insertart())
               
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(applyBtn, 12, 2, 1, 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close) 
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
    
            grid.addWidget(cancelBtn, 12, 1, 1, 3, Qt.AlignCenter)
            
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 13, 0, 1, 3, Qt.AlignCenter)
          
            def insertart():
                mdescr = self.q2Edit.text()
                mprice = float(self.q3Edit.text())
                munit = self.q5Edit.currentText()
                msize = float(self.q7Edit.text())
                mloc = self.q8Edit.text()
                mgroup = self.q9Edit.text()
                mthumb = self.q10Edit.text()
                mcat = int(self.q11Edit.currentIndex())+1
                mvat = self.q12Edit.currentText()
                mbtnnr =self.q13Edit.text()
                if self.cBox.checkState():
                    maccent = 1
                else:
                    maccent = 0
                if not self.q13Edit.text():
                    message = 'No buttonnumber filled in!'
                    alertText(message)
                    return
                else:
                    mbtnnr = int(self.q13Edit.text())
                    mbtntext = self.q14Edit.toPlainText()
                    mlist = mbtntext.split('\n')
                    for line in mlist:
                         if len(line) > 14:
                             message = 'No more then 14 characters per line allowed'
                             alertText(message)
                             break
                         elif len(mlist) > 4:
                             message = 'No more then 4 lines allowed!'
                             alertText(message)
                             break
                         elif not (mdescr and mprice and mcat):
                             message = 'Not all neccessary fields filled in!'
                             alertText(message)
                             break
                    else:
                        insart = insert(articles).values(barcode=str(mbarcode),\
                           description = mdescr,item_price=mprice, item_unit=munit,\
                           order_size=msize,location_warehouse=mloc, article_group=mgroup,\
                           thumbnail=mthumb,category=mcat,VAT=mvat)
                        con.execute(insart)
                        updbtn = update(buttons).where(buttons.c.buttonID==mbtnnr).\
                         values(barcode=str(mbarcode), buttontext=mbtntext, accent = maccent)
                        con.execute(updbtn)
                        if sys.platform == 'win32':
                            ean.save('.\\Barcodes\\Articles\\'+str(mbarcode))
                        else:
                            ean.save('./Barcodes/Articles/'+str(mbarcode))
                        insertOK()
                        self.close()
                
            self.setLayout(grid)
            self.setGeometry(800, 200, 150, 100)

    win = Widget()
    win.exec_()
    
def existingBarcode():
    mflag = 1
    articleRequest(mflag)
    
def insertArticles():
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('item_price', Float),
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
        Column('VAT', String))
 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    mbarcode=(con.execute(select([func.max(articles.c.barcode, type_=String)])).scalar())
    # generate new barcode
    marticlenr = mbarcode[3:11]
    marticlenr = str((int(marticlenr[0:8]))+int(1))
    total = 0
    for i in range(int(8)):
        total += int(marticlenr[i])*(int(9)-i)
    checkdigit = total % 11 % 10
    marticlenr = marticlenr+str(checkdigit)
    ean = barcode.get('ean13','800'+str(marticlenr), writer=ImageWriter()) # for barcode as png
    mbarcode = ean.get_fullcode()
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
            
            #item_price
            self.q3Edit = QLineEdit('0')
            self.q3Edit.setFixedWidth(100)
            self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q3Edit)
            self.q3Edit.setValidator(input_validator)
            
            #item_unit
            self.q5Edit = QComboBox()
            self.q5Edit.setFixedWidth(170)
            self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q5Edit.setFont(QFont("Arial",10))
            self.q5Edit.addItem('stuk')
            self.q5Edit.addItem('100')
            self.q5Edit.addItem('meter')
            self.q5Edit.addItem('kg')
            self.q5Edit.addItem('liter')
            self.q5Edit.addItem('m²')
            self.q5Edit.addItem('m³')
            
            #minimum stock
            self.q6Edit = QLineEdit('0')
            self.q6Edit.setFixedWidth(100)
            self.q6Edit.setFont(QFont("Arial",10))
            self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q6Edit)
            self.q6Edit.setValidator(input_validator)

            #order_size
            self.q7Edit = QLineEdit('0')
            self.q7Edit.setFixedWidth(100)
            self.q7Edit.setFont(QFont("Arial",10))
            self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q7Edit)
            self.q7Edit.setValidator(input_validator)
                         
            #location
            self.q8Edit = QLineEdit()
            self.q8Edit.setFixedWidth(100)
            self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q8Edit.setFont(QFont("Arial",10))
                        
            # article_group
            self.q9Edit = QLineEdit()
            self.q9Edit.setFixedWidth(200)
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
            
            def q2Changed():
                self.q2Edit.setText(self.q2Edit.text())
            self.q2Edit.textChanged.connect(q2Changed)
            
            def q3Changed():
                self.q3Edit.setText(self.q3Edit.text())
            self.q3Edit.textChanged.connect(q3Changed)
            
            def q5Changed():
                self.q5Edit.setCurrentText(self.q5Edit.currentText()) #+1
            self.q5Edit.currentIndexChanged.connect(q5Changed)
            
            def q6Changed():
                self.q6Edit.setText(self.q6Edit.text())
            self.q6Edit.textChanged.connect(q6Changed)
            
            def q7Changed():
                self.q7Edit.setText(self.q7Edit.text())
            self.q7Edit.textChanged.connect(q7Changed)
            
            def q8Changed():
                self.q8Edit.setText(self.q8Edit.text())
            self.q8Edit.textChanged.connect(q8Changed)
            
            def q9Changed():
                self.q9Edit.setText(self.q9Edit.text())
            self.q9Edit.textChanged.connect(q9Changed)
            
            def q10Changed():
                self.q10Edit.setText(self.q10Edit.text())
            self.q10Edit.textChanged.connect(q10Changed)
            
            def q11Changed():
                self.q11Edit.setCurrentIndex(self.q11Edit.currentIndex())
            self.q11Edit.currentIndexChanged.connect(q11Changed)
            
            def q12Changed():
                self.q5Edit.setCurrentText(self.q12Edit.currentText()) 
            self.q12Edit.currentIndexChanged.connect(q12Changed)
           
            grid.addWidget(QLabel('Barcodenumber'), 1, 0)
            grid.addWidget(self.q1Edit, 1, 1)
            
            grid.addWidget(QLabel('Description'), 2, 0)
            grid.addWidget(self.q2Edit, 2, 1 ,1 ,2)
            
            grid.addWidget(QLabel('Item_Price'), 3, 0)
            grid.addWidget(self.q3Edit, 3, 1)
            
            grid.addWidget(QLabel('Item-Unit'), 3, 2)
            grid.addWidget(self.q5Edit, 3, 3)
            
            grid.addWidget(QLabel('Minimum_Stock'), 4, 0)
            grid.addWidget(self.q6Edit, 4, 1)
            
            grid.addWidget(QLabel('Order-Size'), 4, 2)
            grid.addWidget(self.q7Edit, 4, 3)
              
            grid.addWidget(QLabel('Location'), 5, 0)
            grid.addWidget(self.q8Edit, 5, 1)
            
            grid.addWidget(QLabel('Articlegroup'), 5, 2)
            grid.addWidget(self.q9Edit, 5, 3)
            
            grid.addWidget(QLabel('Thumbnail'), 6, 0)
            grid.addWidget(self.q10Edit, 6, 1)
            
            grid.addWidget(QLabel('Category'), 6, 2 )
            grid.addWidget(self.q11Edit, 6, 3)
            
            grid.addWidget(QLabel('VAT'), 7, 0 )
            grid.addWidget(self.q12Edit, 7, 1)
  
            def insArticle(self):
                mdescr = self.q2Edit.text()
                mprice = float(self.q3Edit.text())
                munit = self.q5Edit.currentText()
                mminstock = float(self.q6Edit.text())
                morder_size = float(self.q7Edit.text())
                mlocation = self.q8Edit.text()
                martgroup = self.q9Edit.text()
                mthumb = self.q10Edit.text()
                mcategory = self.q11Edit.currentIndex()+1
                mvat = self.q12Edit.currentText()
                if mdescr and mprice and morder_size and mlocation and mcategory:
                    insart = insert(articles).values(barcode=mbarcode,description=mdescr,\
                        item_price=mprice,item_unit=munit, minimum_stock = mminstock,\
                        order_size=morder_size, location_warehouse=mlocation,\
                        article_group=martgroup,thumbnail=mthumb,\
                        category=mcategory,VAT=mvat)
                    con.execute(insart)
                    if sys.platform == 'win32':
                        ean.save('.\\Barcodes\\Articles\\'+str(mbarcode))
                    else:
                        ean.save('./Barcodes/Articles/'+str(mbarcode))
                    insertOK()
                    self.close()
                else:
                    message = 'Not all fields are filled in!'
                    alertText(message)
                    self.close()
 
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insArticle(self))
    
            grid.addWidget(applyBtn, 8, 3, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)
            
            grid.addWidget(cancelBtn, 8, 3)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 9, 0, 1, 4, Qt.AlignCenter)
            
    
            self.setLayout(grid)
            self.setGeometry(800, 200, 150, 100)
 
    window = Widget()
    window.exec_()
     
def requestLoss():
    metadata = MetaData()
    loss = Table('loss', metadata,
       Column('lossID', Integer, primary_key=True),
       Column('barcode', None, ForeignKey('articles.barcode')),
       Column('number', Float),
       Column('bookdate', String),
       Column('category', String))
    articles = Table('articles', metadata,
       Column('barcode', String, primary_key=True),
       Column('description', String),
       Column('item_price', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    selloss = select([loss, articles]).where(articles.c.barcode==loss.c.barcode).\
        order_by(loss.c.category, loss.c.bookdate)
    rploss = con.execute(selloss)
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
            table_view.setColumnHidden(5,True)
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

    header = ['ID','Barcode','Amount','Bookdate','Category','','Description','Item-Price']                                       
    
    data_list=[]
    for row in rploss:
        data_list += [(row)] 

    win = Widget(data_list, header)
    win.exec_()
    
def bookingLoss():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Booking loss articles")
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
            self.k0Edit.setFixedWidth(230)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Booking loss')
            self.k0Edit.addItem('Request loss items')
                           
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    flag = 2
                    articleRequest(flag)
                elif mindex == 1:
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
             
            grid.addWidget(closeBtn, 2, 1)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
    
def purchaseCollect():
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
        Column('order_status', Boolean))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
     
    selarticles = select([articles]).order_by(articles.c.barcode).\
      where(and_(articles.c.item_stock + articles.c.order_balance \
             < articles.c.minimum_stock, articles.c.order_status == True))
    rparticles = con.execute(selarticles)
    mbookdate = str(datetime.datetime.now())[0:10]
    if sys.platform == 'win32':
        orderlist = '.\\forms\\Purchasing\\Purchaselist_'+mbookdate+'.txt'
    else:
        orderlist = './forms//Purchasing/Purchacelist_'+mbookdate+'.txt'
    open(orderlist, 'w').write('')
    mline = 0
    pagenumber = 0
    def head():
        head =\
        ('Sales - Purchaselist: '+ mbookdate+' Pagenumber '+str(pagenumber)+' \n'+
        '==================================================================================================\n'+
        'Barcode       Description                                     Item-Price   Item-Unit   Ordersize  \n'
        '==================================================================================================\n')

        return(head)
    
    for row in rparticles:
        if mline%58 == 0:
           pagenumber += 1
           open(orderlist, "a").write(head())
           mline += 4
           
        mbarcode = row[0]
        mdescr = row[1][:45]
        mprice = row[2]
        munit = row[4]
        mordersize = row[6]
        #mordersize add to order_balance and order_status locked
        updart = update(articles).where(articles.c.barcode == row[0]).values\
         (order_balance=articles.c.order_balance+mordersize, order_status=False)
        con.execute(updart)
       
        open(orderlist,'a').write('{:<14s}'.format(mbarcode)+'{:<46s}'.format(mdescr)+\
         '{:>12.2f}'.format(mprice)+'{:>12s}'.format(munit)+'{:>12.2f}'.format(mordersize)+'\n')
        mline += 1
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    if mline > 0:
        msg.setText('The orderlist has been compiled\norder the listed items!')
    else:
        msg.setText('No items matching the search criteria were found!')
    msg.setWindowTitle('Payments instances')
    msg.exec_() 

def deliveryImport():
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('item_stock', Float),
        Column('order_balance', Float),
        Column('order_status', Boolean))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
    con = engine.connect()
    
    path = "./forms/Deliveries/"
    for filename in os.listdir(path):
        file = (open(path+filename, "r"))
        mcount = 0
        if filename[-4:] != '.txt':
            lists = file.readlines()
            item = len(lists)
            for line in range(0, item):
                mbarcode = lists[line][:13].strip()
                mdeliver =  float(lists[line][14:26].strip())
                sel = select([articles]).where(articles.c.barcode == mbarcode)
                if con.execute(sel).fetchone():
                    updart = update(articles).where(articles.c.barcode == mbarcode).\
                        values(item_stock=articles.c.item_stock+mdeliver,\
                        order_balance=articles.c.order_balance-mdeliver,\
                        order_status = True)
                    con.execute(updart)
                else:
                    noBarcode(mbarcode)
            file.close()
            os.rename(path+filename,path+filename+'.txt')
            importDone()
            mcount += 1
    if mcount == 0:
        noImports()
        
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
        Column('short', String),
        Column('number', Float),
        Column('item_price', Float),
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
        mprice = row[5]
        mdescr = row[2]
        self.mtotal += row[6]
        self.mlist.append('{:>3d}'.format(int(mnumber))+' {:<15s}'\
             .format(mdescr[:15])+'{:\u2000>12.2f}'.format(mprice*int(mnumber)))
        self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
        self.qtailEdit.setText(self.qtailtext)
        self.qtotalEdit.setText('{:>12.2f}'.format(self.mtotal))
              
        self.view.append(self.mlist[-1])
    self.mkop.setText('Clientnumber: '+str(self.mclient))

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
    self.mbarcode = rpacc[0]
    self.mcallname = rpacc[1]
    self.maccess = rpacc[2]
    self.logon = self.q1Edit.text()
    self.q1Edit.setText('')
    self.pixmap = QPixmap('./logos/green.png')
    self.logonstate.setPixmap(self.pixmap.scaled(40,40))
    self.plusminBtn.setStyleSheet("color: black;  background-color: #FFD700")
    self.view.setText('')
    self.mtotal = 0.00
    self.mtotvat = 0.00
    self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
    self.qtailEdit.setText(self.qtailtext) 
    if self.maccess < 2:
        self.plusminBtn.setText('+')
        self.plusminBtn.setChecked(False)
        self.plusminBtn.setHidden(True)
        self.qspin.setRange(1, 99)
        self.adminBtn.setHidden(True)
    elif self.maccess == 2:
        self.plusminBtn.setHidden(False)
        self.adminBtn.setHidden(True)
    elif self.maccess == 3:
        self.plusminBtn.setHidden(False)
        self.adminBtn.setHidden(False)
             
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Information barcodescan")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Catering system')
            grid.addWidget(lblinfo, 0, 0, 1, 1, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgba(45, 83, 115, 255); font: 25pt Comic Sans MS")
            
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 0, 1, 1, Qt.AlignRight)
        
            lbl = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            
            infotext = QPlainTextEdit(\
        '''                                                  Instruction catering point of sale.
        
        Logging in takes place with a barcode card with 4 access levels.
        Level 1. Selling, scanning, printing.
        Level 2. Return bookings, a checkable ± button is shown, with which return bookings can be made.
        Level 3. Administration, a button Adminstration is shown, for assigning productbuttons,
                 creating employees, administration, perform stock management and imports.
        level 0. Employee is not allowed for operation.
        Employee first time scan barcode  = logon, second time = logout.
        Other employee scanning = switching employee (for return booking, or replacement).
                         
        Article scanning:
        By default, scanning is performed with a number of 1.
        With the spinbox the correct number can be chosen for scanning, this can be done by the arrows of 
        the spinbox or with the mouse wheel. After every scan, the number is reset to 1.
        Selecting can also been done with the productbuttons for unpackaged products.
        When scanning is started, the close button is blocked until the button 'TRANSFER PAYED' is pressed.
        The print button is blocked until the first transaction is posted.
        In the following cases, an error message appears in red in the Notification Area. An acoustic alarm 
        will also sound for the following 3 cases.  
        
        1. If a read error occurs when scanning the barcode.
        2. If there is insufficient stock to deliver the order, current stock will also been showed.
        3. If the product is not (yet) included in the range.
        All other errors of notification will appear in red in the Notification Area.
                    
        If the item cannot be scanned, it is possible to insert the barcode manually after inserting press 
        <Enter> on the keyboard.
                           
        The receipt can be printed after scanning is finished.
        Before exiting the program, first press the TRANSFER PAYED button, so the close button is released.
        This will make the necessary bookings and prepare the POS for the next customer.
        
        Table arrangements:
        The table arrangements are established by checking free seats and pushing the button
        Open/Change Tables/Seats.
        After selecting and applying a popup is showed, with the possibility of printing a
        barcode for the clientID. With this barcode scanning it's possible to switch fast between
        clients. It's also possible to use the select client button to choose the desired client.
        With this button or scan the current account is selected.
        On the screen a layout of 100 selectable buttons is showed. These buttons are arranged in
        20 groups of 2 table seats and 15 groups of 4 table seats.
        By selecting the seats, combining or splitting of tables and seats can be established.
        By selecting the choise "Open Table" and applying the seats are added to a client.
        By clicking the "Refresh" button the seats with clientnumber and callname of the employee
        is displayed on the seat-buttons.
        Seats occupied are displayed for all employees, so all available seats are showed.
        Only the employee, that selected the seats, can add or remove seats to the assembly,
        by checking or unchecking buttons and selecting "Change seat client <number>". This occurs,
        if visitors from a group are leaving or joining the group.
        If no orders are placed, it's possible to remove with "Change seat client <number>" 
        all the selected seats, also the client is removed.. 
        If orders are placed, it's possible to uncheck the seats except the last one, for this seat
        must remain linked with the client, untill the bill is payed. The last seat is freed and the
        client is removed when the TRANSFER PAYED button is pushed.
        Before pushing the TRANSFER PAYED the bill can be printed and payed by cash or by pin
        transaction. For paying by cash a modest calculator is present.
        The thirst row of the calcultor shows the total sum of the bill.
        The second row under the "TRANSFER PAYED" button must be filled in with the cash sum, 
        received from the customer. By pushing the "REFUND"button the change is calculated.
        In case of incorrect entry the "DEL" button can be applied.
        The change is rounded. The rounding is changeable by the program by a authorised person. 
        ''')
            grid.addWidget(infotext, 1, 0)
                           
            infotext.setStyleSheet("font: 20px Consolas bold; color: black ; background-color: #D9E1DF")   
            infotext.setFixedSize(1000, 700)
            grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 1, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(100, 50, 350, 350)
            
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
    
def heading(self, mpage):
    kop=\
    ('Sales - Ordernumber: '+ str(self.mclient)+' Date : '+str(datetime.datetime.now())[0:10]+' Pagenumber '+str(mpage)+' \n'+
    '==================================================================================================\n'+
    'Artikelnr  Description                                  Number  Item_price    Subtotal         VAT\n'+
    '==================================================================================================\n')
    return(kop)

def printReceipt(self):
    if not self.mcallname:
        self.albl.setText('Not Logged on!')
        return
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./logos/logo.jpg')) 
    msgBox.setWindowTitle("Printing receipt")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setFont(QFont("Arial", 10))
    msgBox.setText("Do you want to print the receipt?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        metadata = MetaData()
        order_lines = Table('order_lines', metadata,
            Column('ID', Integer(), primary_key=True),
            Column('clientID', Integer),
            Column('callname', String),
            Column('barcode', String),
            Column('description', String),
            Column('number', Float),
            Column('item_price', Float),
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
        mpage = 0
        rgl = 0
        if sys.platform == 'win32':
            fbarc = '.\\forms\\Orderlines\\'+str(self.mclient)+'.txt'
        else:
            fbarc = './forms//Orderlines/'+str(self.mclient)+'.txt'
        
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
            msubtotvat = row[8]
            open(fbarc,'a').write(str(martnr) +'  '+'{:<40s}'.format(mdescr)+' '+'{:>6d}'\
                     .format(int(mnumber))+'{:>12.2f}'.format(float(mprice))+'{:>12.2f}'\
                     .format(float(msubtotal))+'{:>12.2f}'\
                     .format(float(msubtotvat))+'\n')
             
        tail=\
        ('===================================================================================================\n'+
         'Total  amount to pay inclusive VAT and amount VAT                         '+'{:>12.2f}'.format(self.mtotal)+'{:>12.2f}'.format(self.mtotvat)+' \n'+
         '===================================================================================================\n'+\
         'Employee : '+self.mcallname+'\n') 
        if rgl > 0:
            open(fbarc,'a').write(tail) 
            if sys.platform == 'win32':
                from os import startfile
                startfile(fbarc, "print")
            else:
                from os import system
                system("lpr "+fbarc)
            printing()
        else:
            self.albl.setText('There are no transactions yet!')
            
def payed(self):
    mbookd = str(datetime.datetime.now())[0:10]
    metadata = MetaData()
    sales = Table('sales', metadata,
        Column('salesID', Integer(), primary_key=True),
        Column('receiptnumber', Integer),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('item_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String),
        Column('clientID', Integer))
    order_lines = Table('order_lines', metadata,
        Column('ID', Integer(), primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('item_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('mutation_date', String),
        Column('callname', String),
        Column('clientID', Integer))
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
              description = row[2], number = row[3], item_price = row[4], sub_total = row[5],\
              sub_vat = row[6], mutation_date = row[7], callname = row[8], clientID = row[9])
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
        
        self.mtotal = 0.00
        self.mtotvat = 0.00
        self.mlist = []
        self.view.setText('')
        self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
        self.qtailEdit.setText(self.qtailtext)
        self.qtotalEdit.setText('')
        self.qtotalEdit.setPlaceholderText('TOTAL')
        self.qcashEdit.setText('')
        self.qcashEdit.setPlaceholderText('CASH')
        self.qchangeEdit.setText('')
        self.qchangeEdit.setPlaceholderText('CHANGE') 
        self.albl.setText('Transactions succeeded!')
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
          
        message = 'There are no transactions yet!'
        alertText(message)
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color:  #B0C4DE")

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
        
def checkLogoncode(c):
    checksum = int(c[0])+int(c[2])+int(c[4])+int(c[6])+(int(c[1])+
                int(c[3])+int(c[5]))*3
    checkdigit = (10-(checksum%10))%10
    if checkdigit == int(c[7]):
        return True
    else:
        return False
        
def checkBarcode(c):
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
    if len(barcodenr) == 13 and checkBarcode(barcodenr) and self.mcallname and self.mclient:
        self.q1Edit.setStyleSheet("color:black;  background-color: #F8F7EE")
        metadata = MetaData()
        articles = Table('articles', metadata,
            Column('barcode', String, primary_key=True),
            Column('description', String),
            Column('item_price', Float),
            Column('item_stock', Float),
            Column('VAT', String),
            Column('annual_consumption_1', Float),
            Column('annual_consumption_2', Float))
        order_lines = Table('order_lines', metadata,
            Column('ID', Integer(), primary_key=True),
            Column('barcode', String),
            Column('description', String),
            Column('number', Float),
            Column('item_price', Float),
            Column('sub_total', Float),
            Column('sub_vat', Float),
            Column('callname', String),
            Column('mutation_date', String),
            Column('clientID', Integer),
            Column('callname', String))
        
        engine = create_engine('postgresql+psycopg2://postgres:@localhost/catering')
        con = engine.connect()
                 
        selart = select([articles]).where(articles.c.barcode == barcodenr)
        selbal = select([order_lines]).where(and_(order_lines.c.barcode == barcodenr,\
                order_lines.c.clientID == self.mclient))
        rpart = con.execute(selart).first()
        rpbal = con.execute(selbal).first()
        if rpart and rpart[3] < mnumber:
            self.albl.setText(str(int(rpart[3]))+' in stock!')
            giveAlarm()
        elif rpart and self.maccess:
            if rpart[4] == 'high':      
                self.mvat = self.mvath
            elif rpart[4] == 'low': 
                self.mvat = self.mvatl
            else:
                self.mvat = self.mvatz
            mdescr = rpart[1]
            mdescr = mdescr[:40] if len(mdescr) > 40 else mdescr
            mprice = rpart[2]
            mutdate = str(datetime.datetime.now())[0:10]
            if rpbal:
                updbal = update(order_lines).where(and_(order_lines.c.barcode == barcodenr,\
                  order_lines.c.clientID == self.mclient)).values(number = order_lines.c.number+mnumber,\
                  sub_total = (order_lines.c.number+mnumber)*mprice,\
                  sub_vat = (order_lines.c.number+mnumber)*mprice*self.mvat, callname = self.mcallname,\
                  mutation_date = mutdate)
                con.execute(updbal)
            else:
                try:
                    midnr = (con.execute(select([func.max(order_lines.c.ID, type_=Integer)])).scalar()) 
                    midnr += 1
                except:
                    midnr = 1
                insbal = insert(order_lines).values(ID = midnr, clientID = self.mclient,\
                  barcode = barcodenr, description = mdescr, number = mnumber, item_price = mprice,\
                  sub_total = mnumber*mprice, sub_vat = mnumber*mprice*self.mvat,\
                  callname = self.mcallname, mutation_date = mutdate)
                con.execute(insbal)
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
            
            self.mkop.setText('Clientnumber: '+str(self.mclient))
            self.mlist.append('{:>3d}'.format(int(mnumber))+' {:<15s}'.format(mdescr[:15])+'{:\u2000>12.2f}'.format(mprice*int(mnumber)))
            self.mtotal += float(mprice)*float(mnumber)
            self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
            self.qtailEdit.setText(self.qtailtext)
            self.qtotalEdit.setText('{:>12.2f}'.format(self.mtotal))
                      
            self.view.append(self.mlist[-1])
            self.albl.setText('')
        elif self.maccess == 0 and self.mcallname:
            self.albl.setText('No permission to execute!')
        elif self.maccess == 0:
            self.albl.setText('Please logon with your barcodecard!')
        else:
            self.albl.setText('Article not in assortment!')
            giveAlarm()
                  
        self.closeBtn.setDisabled(True)
        self.closeBtn.setStyleSheet("color: grey; background-color: #B0C4DE")
        self.printBtn.setEnabled(True)
        self.printBtn.setStyleSheet("color: black;  background-color: #00FFFF")
        self.nextBtn.setEnabled(True)
        self.nextBtn.setStyleSheet("font: 12pt Arial; color: black; background-color: #00BFFF")
    elif len(barcodenr) == 8  and barcodenr[0] != '0':
        self.q1Edit.setStyleSheet("color:#F8F7EE;  background-color: #F8F7EE")
        self.q1Edit.setText('')
        self.mclient = 0
        if barcodenr == self.checknr and self.maccess > 0:
            self.maccess = 0
            self.plusminBtn.setHidden(True)
            self.adminBtn.setHidden(True)
            self.pixmap = QPixmap('./logos/red.png')
            self.logonstate.setPixmap(self.pixmap.scaled(40,40))
            self.view.setText('')
            self.mtotal = 0.00
            self.mtotvat = 0.00
            self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
            self.qtailEdit.setText(self.qtailtext) 
        else:
            self.checknr = barcodenr
            logon(self, barcodenr)
            self.albl.setText('')
    elif len(barcodenr) == 8 and barcodenr and barcodenr[0] == '0' :
        self.q1Edit.setStyleSheet("color:#F8F7EE;  background-color: #F8F7EE")
        self.q1Edit.setText('')
        self.checknr = barcodenr
        checkClient(self)
    elif not self.mcallname:
        self.albl.setText('Please logon with your barcodecard!')
    elif self.mclient == 0:
            self.albl.setText('First compose or choose existing table-arrangement!')
    else:
        #alarm if barcode scan failed
        self.albl.setText('Scanning error barcode!')
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
            mkop.setFixedWidth(1110)  
            
            view = QTextEdit()
            view.setStyleSheet('color: black; background-color: #F8F7EE')  
            view.setText('')
            view.setFont(QFont("Consolas", 12, 75))
            view.setFocusPolicy(Qt.NoFocus)
            view.setFixedSize(1110, 800)  
            
            mtotal = 0.00
            mtotvat = 0.00
            qtailEdit = QLineEdit()
            qtailEdit.setFont(QFont("Consolas", 12, 75))
            qtailEdit.setStyleSheet('color: black; background-color: #F8F7EE') 
            qtailEdit.setReadOnly(True)
            qtailEdit.setFixedWidth(1110)
            qtailEdit.setFocusPolicy(Qt.NoFocus)
            qtailtext = 'Clientnumber: '+str(self.mclient)+'  Total  incl. VAT'+'\u2000'*57+'{:\u2000>12.2f}'.format(mtotal)+'{:\u2000>12.2f}'.format(mtotvat)
            qtailEdit.setText(qtailtext)
   
            metadata = MetaData()
            order_lines = Table('order_lines', metadata,
                Column('ID', Integer(), primary_key=True),
                Column('barcode', String),
                Column('description', String),
                Column('number', Float),
                Column('item_price', Float),
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
                mdescr = row[2]
                mnumber = row[3]
                mprice = row[4]
                msubtot = row[5]
                msubvat = row[6]
                view.append('{:<14s}'.format(martnr)+'{:<40s}'.format(mdescr)+' {:>6d}'\
                 .format(int(mnumber))+'{:>12.2f}'.format(mprice)+'{:>12.2f}'\
                 .format(msubtot)+'{:>12.2f}'.format(msubvat))
                mtotal += msubtot
                mtotvat += msubvat
                x += 1 
            qtailtext = 'Clientnumber: '+str(self.mclient)+'  Total  incl. VAT'+'\u2000'*40+'{:\u2000>12.2f}'.format(mtotal)+'{:\u2000>12.2f}'.format(mtotvat)
            qtailEdit.setText(qtailtext)
            mkop.setText('Articlenumber Description                              Number  Item_price    Subtotal         VAT')
               
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
            self.setGeometry(100, 60, 600, 300)
            
    window = widget()
    window.exec_()

def choseClient(self):
    metadata = MetaData()
    order_lines = Table('order_lines', metadata,
        Column('ID', Integer(), primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('short', String),
        Column('number', Float),
        Column('item_price', Float),
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
        if idx.column() == 0:
            selcl = select([order_lines]).where(order_lines.c.clientID == self.mclient)
            rpcl = con.execute(selcl)
            if not rpcl:
                self.albl.setText('No records!')
                return
            self.view.setText('')   
            self.mtotal = 0
            self.mvat = 0
            for row in rpcl:
                mnumber = row[4]
                mprice = row[5]
                mdescr = row[2]
                self.mtotal += row[6]
                self.mlist.append('{:>3d}'.format(int(mnumber))+' {:<15s}'\
                     .format(mdescr[:15])+'{:\u2000>12.2f}'.format(mprice*int(mnumber)))
                self.qtailtext = 'Total  incl. VAT'+'\u2000'*3+'{:\u2000>12.2f}'.format(self.mtotal)
                self.qtailEdit.setText(self.qtailtext)
                self.qtotalEdit.setText('{:>12.2f}'.format(self.mtotal))
                      
                self.view.append(self.mlist[-1])
            self.mkop.setText('Clientnumber: '+str(self.mclient))

            if sys.platform == 'win32':
                keyboard.press_and_release('esc')                          #Windows
            else:
               subprocess.call(["xdotool", "key", "Escape"]) #Linux
    win = Widget(data_list, header)
    win.exec_()
    
def printClient_barcode(self):
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./logos/logo.jpg')) 
    msgBox.setWindowTitle("Printing clientnumber barcodeID")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setFont(QFont("Arial", 10))
    msgBox.setText("Do you want to print the barcode for scanning?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        self.printer = QPrinter()
        self.pixmap = QPixmap('./Barcodes/clients/'+str(self.mbarcode)+'.png')
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
             painter = QPainter(self.printer)
             rect = painter.viewport()
             size = self.pixmap.size()
             size.scale(rect.size(), Qt.KeepAspectRatio)
             painter.setViewport(rect.x(), rect.y(), 300 , 205) #aspect and size for barcodes ean 8
             painter.setWindow(self.pixmap.rect())
             painter.drawPixmap(0, 0, self.pixmap)
            
def seatsArrange(self):
    if not self.mcallname:
        self.albl.setText('Please logon with your barcodecard!')
        return
    mcallname = self.mcallname
    maccess = self.maccess
    mclient = self.mclient
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
             
            grid = QGridLayout()
            grid.setSpacing(0)
             
            self.lblseats = QLabel(' ')
            self.lblseats.setFont(QFont("Arial", 12, 75))
            self.lblseats.setText("Notification Bar")
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
            for  row in rptables:
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
                    if row[4] != self.mcallname and self.maccess < 2:
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
                
            seatlist = []   
            def gettable_seat(tindex):
                seatlist.append(tindex) 
            
            # remove seats with even occurences
            seatlist = [seat for seat, count in collections.Counter(seatlist).items() if count%2 == 1]
            seatlist.sort(reverse=True)
                                
            qcbEdit = QComboBox()
            qcbEdit.addItem('Open new table')
            selclient = select([clients]).where(clients.c.employee ==\
            self.mcallname).order_by(clients.c.clientID)
            rpclient = con.execute(selclient)
            tablelist = []
            for row in rpclient:
                qcbEdit.addItem('Change seats client '+str(row[0]))
                tablelist.append(row[1])
                
            qcbEdit.setFixedSize(200, 40)
            qcbEdit.setStyleSheet('font: 18px bold; color:black; background-color: #F8F7EE')
            grid.addWidget(qcbEdit, 2, 10, 1, 4)
            
            def qclientChanged():
                qcbEdit.setCurrentText(qcbEdit.currentText())
            qcbEdit.currentTextChanged.connect(qclientChanged)
            def connectClient(self):
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
                if len(seatlist) == 0:
                    self.lblseats.setText('Choose seat arrangement first!')
                    return
                else:
                    mflag = 0
                    x = 0
                    for val in seatlist:
                        seltab = select([tables_layout]).where(tables_layout.c.ID == seatlist[x])
                        rptab = con.execute(seltab).fetchone()
                        occ=rptab[2]
                        if occ == 0:
                            if indextext == 'Open new table':
                                mflag = 1
                            upd = update(tables_layout).where(tables_layout.c.ID ==\
                             seatlist[x]).values(occupied=1,clientID=self.mclient,\
                             callname=self.mcallname)
                            con.execute(upd)
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
                                self.lblseats.setText('Tableseats have been processed!')
                                if s > 1:
                                    upd = update(tables_layout).where(tables_layout.c.ID ==\
                                     seatlist[x]).values(occupied=0,clientID=0,callname='')
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
                                        self.lblseats.setText('Last seat can only be removed by button "TRANSFER PAYED" in mainscreen!')
                                    else:
                                        upd = update(tables_layout).where(tables_layout.c.ID ==\
                                          seatlist[x]).values(occupied=0,clientID=0,callname='')
                                        con.execute(upd)  
                                        delol = delete(clients).where(and_(clients.c.clientID ==\
                                            self.mclient, clients.c.employee == self.mcallname))
                                        con.execute(delol)
                        x += 1
                    if mflag:
                        inlogstr = ('010'+('000'+str(mclientnr))[-4:])
                        ean = barcode.get('ean8', str(inlogstr), writer=ImageWriter()) # for barcode as png
                        mbarcode = ean.get_fullcode()
                        if sys.platform == 'win32':
                            ean.save('.\\Barcodes\\clients\\'+str(mbarcode))
                        else:
                            ean.save('./Barcodes/clients/'+str(mbarcode))
                        insidx=insert(clients).values(clientID=mclientnr, employee=self.mcallname,\
                             barcode = mbarcode)
                        con.execute(insidx)
                        self.mbarcode = mbarcode
                        printClient_barcode(self)
                        
            clientBtn = QPushButton('Apply\nSeats')
            clientBtn.clicked.connect(lambda: connectClient(self))
            clientBtn.setFixedSize(200, 80)
            clientBtn.setStyleSheet("font: 24px bold; color: black; background-color: #45b39d")

            grid.addWidget(clientBtn, 1, 10, 1, 4)

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)
            closeBtn.setStyleSheet('font: 24px bold; color: black; background-color:  #00FFFF')
            closeBtn.setFixedSize(200, 80)
            
            grid.addWidget(closeBtn, 4, 10, 1, 4)
            
            refreshBtn = QPushButton('Refresh')
            refreshBtn.clicked.connect(lambda: refresh(self))
            refreshBtn.setFixedSize(200, 80)
            refreshBtn.setStyleSheet("font: 24px bold; color: black; background-color: #FFD700")

            grid.addWidget(refreshBtn, 3, 10, 1, 4)
            
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
                Column('buttongrouptext', String))
                                          
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
                total = float(self.qtotalEdit.text())
                if self.qcashEdit.text():
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
                                                                         
            self.q1Edit = QLineEdit('')
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
                self.mkop.setText('Clientnumber: '+str(self.mclient))
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
                Column('accent', Integer))
            
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
                    getMaingrouppicture()
                    btngroupChange(self)
                        
                def indexDecrease(self):
                    self.index -= 90
                    self.index = self.index%900
                    getMaingrouppicture()
                    btngroupChange(self)
                                                                                                        
                if self.btngroup == 1:
                    if self.flag == 1:
                        self.index -= 72
                        self.flag = 0
                    self.index += 0
                    if self.maccess < 3:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][1].strip()+'\n'+str(rphbtn[int(self.index/18)][0]))
                    self.hBtn.setStyleSheet('color: white; background-color:  #16a085')
                    self.btngroup = 2
                elif self.btngroup == 2:
                    self.index += 18
                    if self.maccess < 3:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][1].strip()+'\n'+str(rphbtn[int(self.index/18)][0]))
                    self.hBtn.setStyleSheet('color: black; background-color:  #f39c12')
                    self.btngroup = 3
                elif self.btngroup == 3:
                    self.index += 18
                    if self.maccess < 3:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][1].strip()+'\n'+str(rphbtn[int(self.index/18)][0]))
                    self.hBtn.setStyleSheet('color: white; background-color:  #ca6f1e')
                    self.btngroup = 4
                elif self.btngroup == 4:
                    self.index += 18
                    if self.maccess < 3:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][1].strip()+'\n'+str(rphbtn[int(self.index/18)][0]))
                    self.hBtn.setStyleSheet('color: white; background-color:    #c0392b')
                    self.btngroup = 5
                elif self.btngroup == 5:
                    self.index += 18
                    self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    if self.maccess < 3:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][2].strip())
                    else:
                        self.hBtn = QPushButton(rphbtn[int(self.index/18)][1].strip()+'\n'+str(rphbtn[int(self.index/18)][0]))
                    self.hBtn.setStyleSheet('color: black; background-color:   #f1c40f')
                    self.btngroup = 1
                    self.flag = 1
                    
                self.hBtn.setFont(QFont("Consolas", 12, 75))
                self.hBtn.setFocusPolicy(Qt.NoFocus)
                self.hBtn.setFixedSize(200,150)
                grid.addWidget(self.hBtn, 0, 3) #position groupbutton on first position from thirst row
                
                nextgrpBtn = QPushButton('\u21c8')
                nextgrpBtn.setStyleSheet("color: black;  background-color: #e7e71c")
                nextgrpBtn.setFont(QFont("Arial", 40, 75))
                nextgrpBtn.clicked.connect(lambda: indexIncrease(self))  
                nextgrpBtn.setFocusPolicy(Qt.NoFocus)
                nextgrpBtn.setFixedSize(200, 150)
                grid.addWidget(nextgrpBtn, 2, 3)
                
                getMaingrouppicture()
                                            
                previousgrpBtn = QPushButton('\u21ca')
                previousgrpBtn.setStyleSheet("color: black;  background-color: #e7e71c")
                previousgrpBtn.setFont(QFont("Arial", 40, 75))
                previousgrpBtn.clicked.connect(lambda: indexDecrease(self))  
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
                    aBtn = QPushButton(row[1].strip()+accent) #choose buttontext
                    if self.maccess == 3: #showbuttonnumber reference and barcode for administrator
                        aBtn = QPushButton(str(row[0])+'\n'+row[2].strip()+'\n'+row[3])
                    aBtn.setFont(QFont("Consolas", 12, 75))
                    aBtn.setStyleSheet('color: black; background-color:  #FFFFF0')
                    aBtn.setFocusPolicy(Qt.NoFocus)
                    aBtn.setFixedSize(200, 150)
                    btnlist.append(row[2].strip()) #choose barcode
                                      
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
                                                                                    
                    aBtn.clicked.connect(lambda checked, btn = btnlist[a%6] : getbarcode(btn))
                    a += 1
                
            self.btngroup = 1 
            self.index = 0
            self.flag = 0
           
            btngroupChange(self)
                                                     
            def getbarcode(btn):
                self.q1Edit.setText(btn) 
                if sys.platform == 'win32':
                    import keyboard
                    keyboard.write('\n')                          #Windows
                else:
                    subprocess.call(["xdotool", "key", "Return"]) #Linux
            
            def clientLines(self):
                if self.maccess:
                    choseClient(self)
                else:
                    self.albl.setText('Please logon with your barcodecard!')
                                       
            self.plusminBtn = QPushButton('+')
            self.plusminBtn.setCheckable(True)
            self.plusminBtn.setFont(QFont("Arial",12,75))
            self.plusminBtn.setStyleSheet("color: black;  background-color: #FFD700")
            self.plusminBtn.setHidden(True)
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
      
            grid.addWidget(self.displayBtn, 2, 7, 1, 1, Qt.AlignRight)
            
            self.tablesBtn = QPushButton('Open/Change\nTables/Seats')
            self.tablesBtn.clicked.connect(lambda: seatsArrange(self))
            self.tablesBtn.setFont(QFont("Arial",12,75))
            self.tablesBtn.setFocusPolicy(Qt.NoFocus)
            self.tablesBtn.setFixedSize(200,150)
            self.tablesBtn.setStyleSheet("color: black;  background-color: #d5bb55")
      
            grid.addWidget(self.tablesBtn, 3, 7, 1, 1, Qt.AlignRight)
            
            self.printBtn = QPushButton('Printing')
            self.printBtn.clicked.connect(lambda: printReceipt(self))
            self.printBtn.setFont(QFont("Arial",12,75))
            self.printBtn.setFocusPolicy(Qt.NoFocus)
            self.printBtn.setFixedSize(200,150)
            self.printBtn.setStyleSheet("color: black;  background-color: #00FFFF")
      
            grid.addWidget(self.printBtn, 1, 7, 1, 1, Qt.AlignRight)
            
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
            self.closeBtn.setStyleSheet("color: black; background-color:   #45b39d")

            grid.addWidget(self.closeBtn, 5, 7, 1, 1, Qt.AlignRight)
                                  
            infoBtn = QPushButton('Information')
            infoBtn.clicked.connect(lambda: info())
            infoBtn.setFont(QFont("Arial",12,75))
            infoBtn.setFocusPolicy(Qt.NoFocus)
            infoBtn.setFixedSize(200,150)
            infoBtn.setStyleSheet("color: black;  background-color: #00BFFF")
    
            grid.addWidget(infoBtn, 0, 7, 1, 1, Qt.AlignRight )
           
            self.nextBtn = QPushButton('Select\nClient')
            self.nextBtn.clicked.connect(lambda: clientLines(self))
            self.nextBtn.setFont(QFont("Arial",12,75))
            self.nextBtn.setFocusPolicy(Qt.NoFocus)
            self.nextBtn.setFixedSize(200,150)            
            self.nextBtn.setStyleSheet("color:black; background-color: #3498db")
       
            grid.addWidget(self.nextBtn, 4, 7, 1, 1, Qt.AlignRight)   
            
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