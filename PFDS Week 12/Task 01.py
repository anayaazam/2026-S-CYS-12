from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(488, 640)
        Form.setStyleSheet("background-color: rgb(145, 190, 210);")
        # University logo label
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(150, 10, 180, 140))
        self.label_6.setMinimumSize(QtCore.QSize(130, 130))
        self.label_6.setMaximumSize(QtCore.QSize(250, 250))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("../Pictures/Screenshots/University_of_Engineering_and_Technology_Lahore_logo.svg.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        # Empty label (placeholder)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(140, 10, 111, 51))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        # University name label
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 140, 471, 51))
        self.label.setStyleSheet('font: 57 italic 23pt "Z003";')
        self.label.setObjectName("label")
        # White card frame
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(90, 220, 303, 281))
        self.frame.setStyleSheet("background-color: white;\n border-radius: 10px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        # Vertical layout inside frame
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(18, 9, 21, 26)
        self.verticalLayout.setObjectName("verticalLayout")
        # Registration Form title
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setStyleSheet('font: 75 24pt "Yrsa";')
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        # User Name label
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        # User Name input
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setPlaceholderText("User Name")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        # Password label
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        # Password input
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setPlaceholderText("Password")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        # Login button
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setStyleSheet(
            "background-color: #2196F3;\n"
            "color: white;\n"
            "border-radius: 5px;\n"
            "padding: 8px;")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "University of Engineering and Technology"))
        self.label_2.setText(_translate("Form", "   Registration Form"))
        self.label_3.setText(_translate("Form", "User Name:"))
        self.label_4.setText(_translate("Form", "Password:"))
        self.pushButton.setText(_translate("Form", "Login"))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())