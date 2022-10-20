from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import setup
from oracle import ora_sms, ora_cash
from api import api_sms, api_stand, api_customer
from datetime import datetime
import sys

app = QtWidgets.QApplication([])
ui = uic.loadUi("mydesign.ui")
ui.setWindowTitle("Регистрация консов на стенде")

ui.lineEdit_2.setText('1')
ui.lineEdit.setText('1000')
ui.lineEdit_3.setText('1000')
ui.lineEdit_5.setText('1000')

mas = []
ui.comboBox.addItems(setup.api_dict)
ui.comboBox_2.addItems(setup.stand_dict)
ui.comboBox_3.addItems(setup.provider_dict)
ui.comboBox_4.addItems(setup.provider_dict)
ui.comboBox_5.addItems(setup.provider_dict)


def button():
    setusa = '-'
    cash, cash2 = '-', '-'
    iterations = int(ui.lineEdit_2.text())
    many = ui.lineEdit.text()
    pro = ui.comboBox_3.currentText()
    provider = setup.provider_dict[pro]
    many2 = ui.lineEdit_3.text()
    pro2 = ui.comboBox_4.currentText()
    provider2 = setup.provider_dict[pro2]
    stand = setup.stand_dict[ui.comboBox_2.currentText()]
    api = setup.api_dict[ui.comboBox.currentText()]

    for i in range(0, iterations):  # создаем заданное количество консов
        userName = api_stand(api, stand) # через выбранное апи на выбранном стенде регаем конса
        key = ora_sms(userName, stand) # получаем код подтверждения из смс в оракле
        userPassword = key[0][0].split()[3] # пароль пользователя
        sms = key[1][0].split()[3] # код из смс в оракле
        date = datetime.now() # дата регистрации конса
        print(key)
        api_sms(sms, userName, stand) # подтверждаем смс по апи

        if ui.checkBox_2.isChecked():
            cash = ora_cash(userName, many, provider, stand) # начисляем консу денег
            print(cash)
        if ui.checkBox_3.isChecked():
            cash2 = ora_cash(userName, many2, provider2, stand) # начисляем консу ОС
            print(cash2)
        if ui.checkBox.isChecked(): # проверяем стоит ли галочка на америконсе
            if ui.radioButton.isChecked(): # делаем покупателя на америке
                setusa = 'setusacustomer'
            elif ui.radioButton_2.isChecked(): # делаем консультанта на америке
                setusa = 'setusaconsultant'
            setus = api_customer(setusa, userName, stand)
            print(setus)

        if cash == '-': pro = '-'
        if cash2 == '-': pro2 = '-'
        kons = [userName, userPassword, stand['url'], setusa, cash, pro, cash2, pro2, date]
        log_txt("   ".join(map(str, kons)))
        mas.append(kons)

        for i, vol in enumerate(mas):
            for j, v in enumerate(vol):
                item = QTableWidgetItem()
                item.setText(str(v))
                ui.tableWidget.setItem(i, j, item)


def button2():
    stand = setup.stand_dict[ui.comboBox_2.currentText()]
    pro = ui.comboBox_5.currentText()
    provider = setup.provider_dict[pro]
    cash = ora_cash(ui.lineEdit_4.text(), ui.lineEdit_5.text(), provider, stand)
    print(cash)


def log_txt(kons):  # запись всех созданных консов в конец файла
    with open('log.txt', 'a') as file:
        file.writelines("\n" + kons)
        file.close()


ui.pushButton.clicked.connect(button)
ui.pushButton_2.clicked.connect(button2)

ui.show()
sys.exit(app.exec())
