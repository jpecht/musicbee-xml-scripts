###
# TODO: This file is not being used currently.
# Creates a basic GUI using PyQt
#

import argparse
from PyQt5.QtWidgets import *
from lxml import etree

# Sets up GUI for application
def setupApplication():
  app = QApplication([])
  app.setApplicationName('MusicBee iTunes XML Parser')
  app.setStyle('Fusion')
  app.setStyleSheet('QWidget { padding: 20px 30px; }')
  app.setStyleSheet('QLabel { font-size: 22px; text-align: center; }')

  window = QWidget()
  window.resize(500, 350)

  layout = QVBoxLayout()

  labelText = 'This application is used for reformatting your MusicBee "iTunes Music Library.xml" file to be compatible with Traktor.'
  label = QLabel(labelText)
  layout.addWidget(label)

  def getFile():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFile)
    # dialog.setFilter('XML File (*.xml)')
    if (dialog.exec()):
      filenames = dialog.selectedFiles()

  button = QPushButton('Browse for MusicBee iTunes XML file')
  button.clicked.connect(getFile)
  layout.addWidget(button)

  window.setLayout(layout)
  window.show()
  app.exec_()
