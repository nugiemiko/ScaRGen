
import sys
from pathlib import Path
from pdf import splitPdf
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout,
    QFileDialog,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,    
)

class StreamRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.moveCursor(QTextCursor.MoveOperation.End)
        self.text_widget.insertPlainText(text)
        self.text_widget.moveCursor(QTextCursor.MoveOperation.End)

    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder = QFileDialog(self)

        self.setWindowTitle("Scarlet Report Generator")
        self.setFixedWidth(600)

        MainLayout = QVBoxLayout()
        pdfRows = QHBoxLayout()
        txtRows = QHBoxLayout()
        
        Label1 = QLabel("Pdf Splitter")
        self.LineInput1 = QLineEdit()
        self.LineInput1.setEnabled(False)
        self.LineInput1.setStyleSheet("border: 0px solid white; background-color: white")
        btn1 = QPushButton("Folder")
        btn1.pressed.connect(lambda: self.selectFolder(self.LineInput1))

        self.SplitTable1 = QTableWidget()
        self.SplitTable1.setColumnCount(2)
        self.SplitTable1.setHorizontalHeaderLabels(['Quotes', 'FileName'])
        self.add_table_row(self.SplitTable1, 'SITE QUALITY ACCEPTANCE CERTIFICATE,KPI Trend –,Productivity –', 'KPI stat QC and Certificate')
        self.add_table_row(self.SplitTable1, 'SITE QUALITY ACCEPTANCE CERTIFICATE,DRIVETEST', 'Plot DT')
        self.SplitTable1.setColumnWidth(0,367)
        self.SplitTable1.setFixedHeight(120)

        self.insertRowButton1 =QPushButton('Insert Row')
        self.deleteRowButton1 =QPushButton('Delete Row')
        self.insertRowButton1.pressed.connect(lambda: self.insert_empty_row(self.SplitTable1))
        self.deleteRowButton1.pressed.connect(lambda: self.delete_empty_row(self.SplitTable1))

        btnLayout1 = QVBoxLayout()
        btnLayout1.addWidget(self.insertRowButton1)
        btnLayout1.addWidget(self.deleteRowButton1)
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.SplitTable1)
        topLayout.addLayout(btnLayout1)

        pdfRows.addWidget(Label1)
        pdfRows.addWidget(self.LineInput1)
        pdfRows.addWidget(btn1)
        
        Label2 = QLabel("Text Splitter")
        self.LineInput2 = QLineEdit()
        self.LineInput2.setEnabled(False)
        self.LineInput2.setStyleSheet("border: 0px solid white; background-color: white")
        btn2 = QPushButton("Folder")
        btn2.pressed.connect(lambda: self.selectFolder(self.LineInput2))

        self.SplitTable2 = QTableWidget()
        self.SplitTable2.setColumnCount(2)
        self.SplitTable2.setHorizontalHeaderLabels(['Quotes', 'FileName'])
        self.add_table_row(self.SplitTable2, 'ALMAF', 'Alarm report')
        self.add_table_row(self.SplitTable2, 'EUTRANCELLFREQ', 'Neighbor report')
        self.SplitTable2.setColumnWidth(0,367)
        self.SplitTable2.setFixedHeight(120)

        self.insertRowButton2 = QPushButton('Insert Row')
        self.deleteRowButton2 = QPushButton('Delete Row')
        self.insertRowButton2.pressed.connect(lambda: self.insert_empty_row(self.SplitTable2))
        self.deleteRowButton2.pressed.connect(lambda: self.delete_empty_row(self.SplitTable2))

        btnLayout2 = QVBoxLayout()
        btnLayout2.addWidget(self.insertRowButton2)
        btnLayout2.addWidget(self.deleteRowButton2)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.SplitTable2)
        bottomLayout.addLayout(btnLayout2)

        txtRows.addWidget(Label2)
        txtRows.addWidget(self.LineInput2)
        txtRows.addWidget(btn2)

        lineLimiter = QLineEdit()
        lineLimiter.setEnabled(False)
        lineLimiter.setStyleSheet("border: 0px transparent; background-color: transparent")

        self.ExecBtn = QPushButton('Execute')
        self.ExecBtn.pressed.connect(lambda: self.execute_program())

        self.logText = QTextEdit()
        self.logText.setReadOnly(True)
        self.logText.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.logText.verticalScrollBar().setValue(self.logText.verticalScrollBar().maximum())
        #sb.setValue(sb.maximum())

        MainLayout.addWidget(lineLimiter)
        MainLayout.addLayout(pdfRows)
        MainLayout.addLayout(topLayout)
        MainLayout.addWidget(lineLimiter)
        MainLayout.addLayout(txtRows)
        MainLayout.addLayout(bottomLayout)
        MainLayout.addWidget(lineLimiter)
        MainLayout.addWidget(self.ExecBtn)
        MainLayout.addWidget(self.logText)

        widget = QWidget()
        widget.setLayout(MainLayout)
        self.setCentralWidget(widget)

        sys.stdout = StreamRedirector(self.logText)
        sys.stderr = StreamRedirector(self.logText)

    def selectFolder(self, widget_arg):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        widget_arg.setText(folder)
        teks = 'Add folder: ' + folder
        print(teks)

    def add_table_row(self, widget_arg, value1, value2):
        row_count = widget_arg.rowCount()
        widget_arg.insertRow(row_count)
        teks = 'Insert new row at ' + str(row_count) + '\n'
        widget_arg.setItem(row_count, 0, QTableWidgetItem(value1))
        teks = teks + 'Quotes: ' + value1 + '\n'
        widget_arg.setItem(row_count, 1, QTableWidgetItem(value2))
        teks = teks + 'Quotes: ' + value2
        print(teks)

    def insert_empty_row(self, widget_arg):
        row_count = widget_arg.rowCount()
        widget_arg.insertRow(row_count)
        teks = 'Insert new row at ' + str(row_count)
        print(teks)
        QTimer.singleShot(0, widget_arg.scrollToBottom)

    def delete_empty_row(self, widget_arg):
        indices = widget_arg.selectionModel().selectedRows()
        for index in sorted(indices):
            widget_arg.removeRow(index.row())
            teks = 'Delete row at ' + str(index.row())
            print(teks)
    
    def execute_program(self):
        dataPdf = {}

        if self.LineInput1.text != '':
            path = self.LineInput1.text()
            teks = 'Pdf Split on folder: ' + path
            print(teks)
            for row in range(self.SplitTable1.rowCount()):
                _key = self.SplitTable1.item(row, 1)
                _item = self.SplitTable1.item(row, 0)
                if _key and _item:
                    key = self.SplitTable1.item(row,1).text()
                    item = [x.strip() for x in self.SplitTable1.item(row,0).text().split(',')]
                    dataPdf[key] = item
            splitPdf(Path(path), dataPdf)
            self.LineInput1.setText('')
        if self.LineInput2.text != '':
            self.LineInput2.setText('')
        print(dataPdf)
    
app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()
