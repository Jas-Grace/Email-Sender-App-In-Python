from PyQt5.QtWidgets import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import subprocess
import time as tm
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtCore import Qt
# from PyQt5.uic import loadUi
file_path = ''

CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

def notify(title, text):
  subprocess.call(['osascript', '-e', CMD, title, text])

style = '''
*{
    font-family: 'lobster two';
}
QWidget {
    background-color:  #000080; 
} 
QLabel{
    color: #FFFFFF;
    font-size: 20px;
}
QLineEdit{
    color: #FFFFFF;
    font-size: 19px;
}
QTextEdit{
    color: #FFFFFF;
    border: 1px solid white;
    font-size: 20px;
}
QPushButton {
    background-color: #006325;
    font-size: 20px;
    color: white;

    border-radius: 5px;        
    border-width: 1px;
    border-color: #ae32a0;
    border-style: solid;
}
QPushButton:hover {
    background-color: #328930;
    color: yellow;
}
QPushButton:pressed {
    background-color: #80c342;
    color: red;
}
QPlainTextEdit{
    border-color:  white;
}
'''

class Widgets(QWidget):
    def __init__(self, **kwargs):
        super(Widgets, self).__init__()
        
        self.vlayout = QVBoxLayout(self)
        
        self.hlayout_0 = QHBoxLayout(self)
        self.l0 = QLabel()
        self.l0.setText("To use this software, you will have to enable less safe apps  to access your email, through this link - https://www.google.com/settings/security/lesssecureapps")
        self.hlayout_0.addWidget(self.l0)
        
        # Horizontal Layout 1****************************
        self.hlayout_1 = QHBoxLayout(self)
        
        self.l1 = QLabel()
        self.l1.setText("Enter the your email address: ")
        self.hlayout_1.addWidget(self.l1)
        
        self.text1 = QLineEdit()
        self.text1.setFixedWidth(630)
        self.text1.setFixedHeight(30)
        self.hlayout_1.addWidget(self.text1)
        
        # Horizontal Layout 2****************************
        self.hlayout_2 = QHBoxLayout()
        
        self.l2 = QLabel()
        self.l2.setText("Enter the password: ")
        self.hlayout_2.addWidget(self.l2)
        
        self.text2 = QLineEdit()
        self.text2.setFixedWidth(630)
        self.text2.setFixedHeight(30)
        self.text2.setEchoMode(QLineEdit.Password)
        self.hlayout_2.addWidget(self.text2)
        
        # Horizontal Layout 3****************************
        self.hlayout_3 = QHBoxLayout()
        
        self.l3 = QLabel()
        self.l3.setText("Enter the reciever's email: ")
        self.hlayout_3.addWidget(self.l3)
        
        self.text3 = QLineEdit()
        self.text3.setFixedWidth(630)
        self.text3.setFixedHeight(30)
        self.hlayout_3.addWidget(self.text3)
        
        # Horizontal Layout 4****************************
        self.hlayout_4 = QHBoxLayout()
        
        self.l4 = QLabel()
        self.l4.setText("Enter the subject: ")
        self.hlayout_4.addWidget(self.l4)
        
        self.text4 = QLineEdit()
        self.text4.setFixedWidth(630)
        self.text4.setFixedHeight(30)
        self.hlayout_4.addWidget(self.text4)
        
        # Horizontal Layout 5****************************
        self.hlayout_5 = QHBoxLayout()
        
        self.l5 = QLabel()
        self.l5.setText("Enter the message: ")
        self.hlayout_5.addWidget(self.l5)
        
        self.text5 = QTextEdit()
        self.text5.setFixedWidth(630)
        self.text5.setFixedHeight(200)
        self.hlayout_5.addWidget(self.text5)
        
        # Horizontal Layout 6****************************
        self.hlayout_6 = QHBoxLayout()
        
        self.l6 = QLabel()
        self.l6.setText("Add a file")
        self.hlayout_6.addWidget(self.l6)
        
        self.add_btn = QPushButton("Choose...")
        self.add_btn.setFixedWidth(70)
        self.add_btn.setFixedHeight(50)
        self.add_btn.clicked.connect(self.browse_file)
        self.hlayout_6.addWidget(self.add_btn)
        
        # Button****************************************
        self.btn = QPushButton("Submit")
        self.btn.setFixedWidth(80)
        self.btn.setFixedHeight(70)
        self.btn.clicked.connect(self.onclick)
        
        # Add layouts***********************************
        self.vlayout.addLayout(self.hlayout_0)
        self.vlayout.addLayout(self.hlayout_1)
        self.vlayout.addLayout(self.hlayout_2)
        self.vlayout.addLayout(self.hlayout_3)
        self.vlayout.addLayout(self.hlayout_4)
        self.vlayout.addLayout(self.hlayout_5)
        self.vlayout.addLayout(self.hlayout_6)
        self.vlayout.addWidget(self.btn, alignment=QtCore.Qt.AlignRight)
        self.setLayout(self.vlayout)
        
    def browse_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Select') 
        self.l6.setText(fname[0])
        global file_path
        file_path = fname[0]
    
    def onclick(self):
          try:
            global file_path
            email = self.text1.text()
            password = self.text2.text()
            send_to_email = self.text3.text()
            subject = self.text4.text()
            message = self.text5.toPlainText()
            
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = send_to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            # Setup the attachment
            filename = os.path.basename(file_path)
            attachment = open(file_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, send_to_email, text)
            server.quit()
            
            self.text1.setText('')
            self.text2.setText('')
            self.text3.setText('')
            self.text4.setText('')
            self.text5.insertPlainText('')
            notify('Email Sender',  f'Email sent successfully to {send_to_email}' )
         except:
             notify('Email Sender', 'Unable to send email. Check your internet connection and detials entered.')
     

def window(): 
    app = QApplication([])

    wig = Widgets()
    wig.setStyleSheet(style)
    wig.show()

    app.exec_()
    
if __name__ == "__main__":
    window()
    
