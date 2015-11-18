 #-*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Tue Nov 18 15:42:23 2014
#	  by: Fernando Teodoro de Lima
#
# WARNING! All changes made in this file will be lost!

from PySide.QtGui import *
from PySide.QtCore import *
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from time import sleep
import h5py
import sys
import random
import os
import pyqrcode
import votar
import zbar
import gtk
from time import gmtime, strftime
from PIL import Image
import subprocess
import generateKey
import pyaudio
import wave


h5pyFile = h5py.File('Urna.h5', 'r')
candidatos = h5pyFile['Urna/Candidatos']
perguntas = h5pyFile['Urna/Perguntas']
setupGeral = h5pyFile['Urna/SetupGeral']
tipoDeCandidato = h5pyFile['Urna/TipoDeCandidato']
tipoEleicao = setupGeral[0][8]

class mainWidget(QWidget):
	def __init__(self, ui, parent = None):
		super(mainWidget,  self).__init__(parent)
		self.ui = ui
		self.installEventFilter(self)

	def keyPressEvent(self, event):
		if event.text() == 'v':
			self.ui.button2Clicked()
		elif event.text() == 'a':
			self.ui.buttonClicked()
		elif event.text() == '1':
			self.ui.listWidget.setCurrentRow(0)
			self.ui.buttonClicked()
		elif event.text() == '2':
			self.ui.listWidget.setCurrentRow(1)
			self.ui.buttonClicked()
		elif event.text() == '3':
			self.ui.listWidget.setCurrentRow(2)
	 		self.ui.buttonClicked()
		elif event.text() == '4':
			self.ui.listWidget.setCurrentRow(3)
			self.ui.buttonClicked()
		elif event.text() == '5':
			self.ui.listWidget.setCurrentRow(4)
			self.ui.buttonClicked()
		elif event.text() == '6':
			self.ui.listWidget.setCurrentRow(5)
			self.ui.buttonClicked()
		elif event.text() == '7':
			self.ui.listWidget.setCurrentRow(6)
			self.ui.buttonClicked()
		elif event.text() == '8':
			self.ui.listWidget.setCurrentRow(7)
			self.ui.buttonClicked()
		elif event.text() == '9':
			self.ui.listWidget.setCurrentRow(8)
			self.ui.buttonClicked()

	def eventFilter(self, object, event):
		if event.type() == QEvent.WindowActivate:
			if self.ui.votarWindow is not None:
				if len(cargos()) == len(self.ui.votarWindow.getCargos()):
					if self.ui.thread.isRunning():
						self.ui.thread.exiting = True
					else:
						self.ui.label.setText('Imprimindo voto')
						self.ui.label.setEnabled(False)
						self.ui.thread.start()
						gerarString(self, self.ui.votarWindow.getCargos())
		'''elif event.type()== QEvent.WindowDeactivate:
			print "widget window has lost focus"
		elif event.type()== QEvent.FocusIn:
			print "widget has gained keyboard focus"
		elif event.type()== QEvent.FocusOut:
			print "widget has lost keyboard focus"'''
		return False

class Ui_MainWindow(object):
	def __init__(self, thread):
		self.thread = thread

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")

		if not os.path.isfile('./publickey.pem'):
			print('votacao não pode ser iniciada')
			print('chave publica faltando')
			sys.exit()

		self.screenWidth = gtk.gdk.screen_width()
		self.screenHeight = gtk.gdk.screen_height()

		MainWindow.showFullScreen()

		self.centralwidget = mainWidget(self, MainWindow)

		self.centralwidget.setObjectName("centralwidget")

		font = QFont()
		font.setFamily("Helvetica")
		font.setPointSize(32)
		font.setItalic(False)

		self.label = QLabel(self.centralwidget)
		self.label.setGeometry(QRect(50, 50, self.screenWidth - 100, 50))
		self.label.setObjectName('label')
		self.label.setText('Selecione um cargo para votar')
		self.label.setFont(font)
		self.label.setAlignment(Qt.AlignCenter)

		self.pushButton1 = QPushButton(self.centralwidget)
		self.pushButton1.setGeometry(QRect(self.screenWidth/2 - 100, self.screenHeight - 100, 200, 50))
		self.pushButton1.setObjectName("pushButton1")
		#chamar funcao ao clicar no botao 1
		self.pushButton1.clicked.connect(self.buttonClicked)
		self.pushButton1.setStyleSheet('QPushButton{\
					border: 2px solid #2d2dff;\
					border-radius: 6px;\
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #ffffff, stop: 1 #dddddd);\
					min-width: 80px;}')

		self.listWidget = QListWidget(self.centralwidget)
		self.listWidget.setGeometry(QRect(100, self.label.pos().y() + self.label.height() + 50, self.screenWidth - 200, self.screenHeight - self.label.height() - self.pushButton1.height() - 200))
		self.listWidget.setObjectName("listViewWidget")
		self.listWidget.setFont(font)
		self.listWidget.setWordWrap(True)

		#preencher listWidget com cargos para eleicao
		listCargos = cargos()
		for cargo in listCargos:
			item = QListWidgetItem(cargo)
			#item.setTextAlignment(Qt.AlignHCenter)
			self.listWidget.addItem(item)

		#label que ira mostrar mensagem "imprimindo voto"
		#ele fica invisivel no inicio e só aparece quando a listview é esvaziada
		#ou seja, quando o eleitor ja votou para todos os cargos possiveis
		self.label = QLineEdit(self.centralwidget)
		self.label.setGeometry(QRect(50, 50, self.screenWidth - 100, self.screenHeight - 100))
		self.label.setFont(font)
		self.label.setAlignment(Qt.AlignCenter)
		self.label.setObjectName("label")
		self.label.setVisible(False)

		self.votarWindow = None
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8))
		self.pushButton1.setText(QApplication.translate("MainWindow", "VOTAR", None, QApplication.UnicodeUTF8))
		self.label.setText(QApplication.translate("MainWindow", "", None, QApplication.UnicodeUTF8))

	#funcao que chama a tela para digitar os numeros ao selecionar um cargo para votar
	def buttonClicked(self):
		if self.listWidget.currentItem() is None:
			 print 'Nenhum candidato selecionado'
		else:
			item = self.listWidget.currentItem()
			self.votarWindow = votar.ControlMainWindow(item.text())
			self.listWidget.takeItem(self.listWidget.row(item))
			if self.listWidget.count() == 0:
				self.label.setVisible(True)
				self.pushButton1.setVisible(False)

#thread
class MyThread(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
		self.exiting = False
		self.index = 0

	def run(self):
		som(self,2)
		while self.exiting==False:
			self.index += 1
			sleep(1)
			if self.index == 6:
				self.exiting = True

class ControlMainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		#thread criada para aguardar 5 segundos antes de
		#	reiniciar o programa após um eleitor votar
		self.thread = MyThread()
		self.thread.finished.connect(self.fechar)
		self.ui =  Ui_MainWindow(self.thread)
		self.ui.setupUi(self)

	def fechar(self):
		python = sys.executable
		os.execl(python, python, * sys.argv)

#funcao para carregar cargos da base de dados
def cargos():
	listIndexCargos = []
	listCargos = []
	#caso eleicoes
	if tipoEleicao == '1':
		for i in candidatos:
			if i[0] not in listIndexCargos:
				listIndexCargos.append(i[0])

		for j in range(len(tipoDeCandidato)):
			for i in listIndexCargos:
				if j == i and tipoDeCandidato[j][0] not in listCargos:
					listCargos.append(tipoDeCandidato[j][0])
	#caso plebiscito
	elif tipoEleicao == '0':
		indexPergunta = 1
		for i in perguntas:
			if len(i[0]) > 0:
				listCargos.append(i[0])
				indexPergunta += 1
	return listCargos

def main():
	app = QApplication(sys.argv)
	mySW = ControlMainWindow()
	mySW.show()
	mySW.raise_()
	sys.exit(app.exec_())

def som(self, tipo):
	#define stream chunk
	chunk = 1024

	#open a wav format music
	if tipo == 1:
		f = wave.open(r"beep_urna.wav","rb")
	elif tipo == 2:
		f = wave.open(r"fim_urna.wav","rb")
	else:
		return
	#instantiate PyAudio
	p = pyaudio.PyAudio()
	#open stream
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
					channels = f.getnchannels(),
					rate = f.getframerate(),
					output = True)
	#read data
	data = f.readframes(chunk)

	#play stream
	while data != '':
		stream.write(data)
		data = f.readframes(chunk)

	#stop stream
	stream.stop_stream()
	stream.close()

	#close PyAudio
	p.terminate()
#funcao para gerar string para imprimir QRCode
def gerarString(self, votos):
	stringQRCode = ''
	'''stringQRCode += 'ID.'			+ ('0000') + ','
	stringQRCode += 'ANO.'			+ (setupGeral[0][0]) + ','
	stringQRCode += 'TURNO.'		+ (setupGeral[0][1]) + ','
	stringQRCode += 'UF.'			+ (setupGeral[0][2]) + ','
	stringQRCode += 'MUNICIPIO.'		+ (setupGeral[0][3]) + ','
	stringQRCode += 'ZONA ELEITORAL.'	+ (setupGeral[0][4]) + ','
	stringQRCode += 'LOCAL VOTACAO.'	+ (setupGeral[0][5]) + ','
	stringQRCode += 'SECAO ELEITORAL.'	+ (setupGeral[0][6]) + ','
	stringQRCode += 'DATA PLEITO.'		+ (setupGeral[0][7]) + '|'
	for voto in votos:
		stringQRCode +=	str(voto[0])	+ ':'
		stringQRCode += 'BRANCO.' 	+ str(voto[1]) + ','
		stringQRCode += 'NULO.'		+ str(voto[2]) + ','
		stringQRCode += 'LEGENDA.'	+ str(voto[3]) + ','
		stringQRCode += 'NUMERO.'	+ str(voto[4]) + ';'
	stringQRCode = stringQRCode.upper()
	stringQRCode = stringQRCode[:-1]'''

	stringQRCode += '#'
	#pres, gov, sen1, sen2, depf, depe, pref, ver, pleb
	for voto in votos:
		if 'presidente' == str(voto[0]).lower():
			if str(voto[1]) == '1':
				stringQRCode += '0'
			elif str(voto[2]) == '1':
				stringQRCode += '-1'
			else:
				stringQRCode += str(voto[4])
			votos.remove(voto)
	stringQRCode += ';'
	for voto in votos:
		if 'governador' == str(voto[0]).lower():
			if str(voto[1]) == '1':
				stringQRCode += '0'
			elif str(voto[2]) == '1':
				stringQRCode += '-1'
			else:
				stringQRCode += str(voto[4])
			votos.remove(voto)
	stringQRCode += ';'
	for voto in votos:
		if 'senador' == str(voto[0]).lower():
			if str(voto[1]) == '1':
				stringQRCode += '0'
			elif str(voto[2]) == '1':
				stringQRCode += '-1'
			else:
				stringQRCode += str(voto[4])
			votos.remove(voto)
	stringQRCode += ';'
	stringQRCode += ';'
	for voto in votos:
		if 'deputado federal' == str(voto[0]).lower():
			if str(voto[1]) == '1':
				stringQRCode += '0'
			elif str(voto[2]) == '1':
				stringQRCode += '-1'
			else:
				stringQRCode += str(voto[4])
			votos.remove(voto)
	stringQRCode += ';'
	for voto in votos:
		if 'deputado estadual' == str(voto[0]).lower():
			if str(voto[1]) == '1':
				stringQRCode += '0'
			elif str(voto[2]) == '1':
				stringQRCode += '-1'
			else:
				stringQRCode += str(voto[4])
			votos.remove(voto)
	stringQRCode += ';'
	for voto in votos:
		if 'prefeito' == str(voto[0]).lower():
			if str(voto[1]) == '1':
				stringQRCode += '0'
			elif str(voto[2]) == '1':
				stringQRCode += '-1'
			else:
				stringQRCode += str(voto[4])
			votos.remove(voto)
	stringQRCode += ';'
	for voto in votos:
		if 'vereador' == str(voto[0]).lower():
			if str(voto[1]) == '1':
				stringQRCode += '0'
			elif str(voto[2]) == '1':
				stringQRCode += '-1'
			else:
				stringQRCode += str(voto[4])
			votos.remove(voto)

	stringQRCode += ';'
	rng = random.SystemRandom()
	id_voto = rng.randint(0, 1000000000)
	stringQRCode += str(id_voto)
	encryptedMessage = generateKey.encrypt(stringQRCode, open('./publickey.pem','rb'))
	url = pyqrcode.create(encryptedMessage, error="L", encoding='utf-8')
	url.png('voto.png', scale=1)
	c = canvas.Canvas('voto.pdf')
	c.setPageSize((2.8*cm,8.9*cm))
	c.drawImage('voto.png', 0.2*cm, 3.1*cm, 2.5*cm, 2.5*cm)
	os.remove('voto.png')
	c.showPage()
	c.save()
	#subprocess.call(['lp','voto.pdf'])
	#os.remove('voto.pdf')


def decodificarString(string):
	#pres, gov, sen1, sen2, depf, depe, pref, ver
	info = string[1:].split(';')
	string = ''
	if info[0] is not '':
		string += 'Presidente: '
		if info[0] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[0] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[0] + '\n\n'
	if info[1] is not '':
		string += 'Governador: '
		if info[1] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[1] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[1] + '\n\n'
	if info[2] is not '':
		string += 'Senador 1: '
		if info[2] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[2] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[2] + '\n\n'
	if info[3] is not '':
		string += 'Senador 2: '
		if info[3] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[3] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[3] + '\n\n'
	if info[4] is not '':
		string += 'Deputado Federal: '
		if info[4] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[4] == '-1':
			string +='Voto nulo' + '\n\n'
		elif len(info[4]) == 2:
			string += 'Legenda:' + info[4] + '\n\n'
		else:
			string += 'Numero: ' + info[4] + '\n\n'
	if info[5] is not '':
		string += 'Deputado Estadual: '
		if info[5] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[5] == '-1':
			string +='Voto nulo' + '\n\n'
		elif len(info[5]) == 2:
			string += 'Legenda:' + info[5] + '\n\n'
		else:
			string += 'Numero: ' + info[5] + '\n\n'
	if info[6] is not '':
		string += 'Prefeito: '
		if info[6] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[6] == '-1':
			string +='Voto nulo' + '\n\n'
		else:
			string += 'Numero: ' + info[6] + '\n\n'
	if info[7] is not '':
		string += 'Vereador: '
		if info[7] == '0':
			string += 'Voto em branco' + '\n\n'
		elif info[7] == '-1':
			string +='Voto nulo' + '\n\n'
		elif len(info[7]) == 2:
			string += 'Legenda:' + info[7] + '\n\n'
		else:
			string += 'Numero: ' + info[7] + '\n\n'
	return string
if __name__ == "__main__":
	main()