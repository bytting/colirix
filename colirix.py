#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui
from xml.dom.minidom import *
from datetime import *
import uuid


class Colirix(QtGui.QMainWindow):

    def __init__(self):
        super(Colirix, self).__init__()

        self.init_ui()

    def init_ui(self):

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Colirix')
        self.center()

        frame = QtGui.QWidget(self)

        self.statusBar()

        open_action = QtGui.QAction(QtGui.QIcon('open.png'), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open log file')
        open_action.triggered.connect(self.select_file)

        exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtGui.qApp.quit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exit_action)
        self.toolbar.addAction(open_action)

        grid = QtGui.QGridLayout()
        grid.setSpacing(6)

        names = ['Log file', 'Report Organization', 'Report Context', 'Group/Team', 'Organization',
                 'Organization Country', 'DoseRate Type', 'Location', 'Municipality', 'Country', 'Uncertainty']

        grid.addWidget(QtGui.QLabel(names[0]), 0, 0)
        grid.addWidget(QtGui.QLabel(names[1]), 1, 0)
        grid.addWidget(QtGui.QLabel(names[2]), 2, 0)
        grid.addWidget(QtGui.QLabel(names[3]), 3, 0)
        grid.addWidget(QtGui.QLabel(names[4]), 4, 0)
        grid.addWidget(QtGui.QLabel(names[5]), 5, 0)
        grid.addWidget(QtGui.QLabel(names[6]), 6, 0)
        grid.addWidget(QtGui.QLabel(names[7]), 7, 0)
        grid.addWidget(QtGui.QLabel(names[8]), 8, 0)
        grid.addWidget(QtGui.QLabel(names[9]), 9, 0)
        grid.addWidget(QtGui.QLabel(names[10]), 10, 0)

        self.edit_file = QtGui.QLineEdit()
        self.edit_rep_org = QtGui.QLineEdit()
        self.edit_rep_con = QtGui.QLineEdit()
        self.edit_group = QtGui.QLineEdit()
        self.edit_org = QtGui.QLineEdit()
        self.edit_org_country = QtGui.QLineEdit()
        self.edit_dose_type = QtGui.QLineEdit()
        self.edit_loc = QtGui.QLineEdit()
        self.edit_munic = QtGui.QLineEdit()
        self.edit_country = QtGui.QLineEdit()
        self.edit_unc = QtGui.QLineEdit()

        self.edit_file.setReadOnly(True)

        btn_select_file = QtGui.QPushButton('Select file')
        btn_select_file.clicked.connect(self.select_file)
        box_file = QtGui.QHBoxLayout()
        box_file.addWidget(self.edit_file)
        box_file.addWidget(btn_select_file)

        grid.addItem(box_file, 0, 1)
        grid.addWidget(self.edit_rep_org, 1, 1)
        grid.addWidget(self.edit_rep_con, 2, 1)
        grid.addWidget(self.edit_group, 3, 1)
        grid.addWidget(self.edit_org, 4, 1)
        grid.addWidget(self.edit_org_country, 5, 1)
        grid.addWidget(self.edit_dose_type, 6, 1)
        grid.addWidget(self.edit_loc, 7, 1)
        grid.addWidget(self.edit_munic, 8, 1)
        grid.addWidget(self.edit_country, 9, 1)
        grid.addWidget(self.edit_unc, 10, 1)
        grid.setRowStretch(11, 1)

        btn_clear = QtGui.QPushButton('Clear')
        btn_clear.clicked.connect(self.clear_fields)

        btn_convert = QtGui.QPushButton('Convert')
        btn_convert.clicked.connect(self.convert_file)

        panel = QtGui.QHBoxLayout()
        vspacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        panel.addItem(vspacer)
        panel.addWidget(btn_clear)
        panel.addWidget(btn_convert)

        box = QtGui.QVBoxLayout()
        box.addItem(grid)
        box.addItem(panel)
        frame.setLayout(box)
        self.setCentralWidget(frame)

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def select_file(self):
        fname = QtGui.QFileDialog.getOpenFileName(self)
        if len(fname) > 0:
            self.edit_file.setText(fname)

    def clear_fields(self):
        self.edit_file.setText('')
        self.edit_rep_org.setText('')
        self.edit_rep_con.setText('')
        self.edit_group.setText('')
        self.edit_org.setText('')
        self.edit_org_country.setText('')
        self.edit_dose_type.setText('')
        self.edit_loc.setText('')
        self.edit_munic.setText('')
        self.edit_country.setText('')
        self.edit_unc.setText('')

    def convert_file(self):
        fname = self.edit_file.text()
        if len(fname) < 1:
            print("Missing filename")
            return

        fname_xml = fname + ".xml"

        doc = xml.dom.minidom.Document()
        el = doc.createElementNS('http://www.iaea.org/2012/IRIX/Format', 'irix:Report')
        el.setAttributeNS('http://www.iaea.org/2012/IRIX/Format', 'xmlns:irix', 'http://www.iaea.org/2012/IRIX/Format')
        el.setAttributeNS('http://www.iaea.org/2012/IRIX/Base', 'xmlns:base', 'http://www.iaea.org/2012/IRIX/Base')
        el.setAttributeNS('http://www.iaea.org/2012/IRIX/Identification', 'xmlns:id', 'http://www.iaea.org/2012/IRIX/Identification')
        el.setAttributeNS('http://www.iaea.org/2012/IRIX/Measurements', 'xmlns:meas', 'http://www.iaea.org/2012/IRIX/Measurements')
        el.setAttributeNS('http://www.iaea.org/2012/IRIX/Locations', 'xmlns:loc', 'http://www.iaea.org/2012/IRIX/Locations')
        el.setAttribute('version', '1.0')
        doc.appendChild(el)

        id = doc.createElementNS('http://www.iaea.org/2012/IRIX/Identification', 'id:Identification')
        el.appendChild(id)

        self.create_and_append_text_element(doc, id, 'id:OrganisationReporting', self.edit_rep_org.text())
        self.create_and_append_text_element(doc, id, 'id:DateAndTimeOfCreation', datetime.now().isoformat())
        self.create_and_append_text_element(doc, id, 'id:ReportContext', self.edit_rep_con.text())
        self.create_and_append_text_element(doc, id, 'id:ReportUUID', uuid.uuid4())

        ids = doc.createElement('id:Identifications')
        id.appendChild(ids)

        org_contact = doc.createElement('base:OrganisationContactInfo')
        ids.appendChild(org_contact)

        self.create_and_append_text_element(doc, org_contact, 'base:Name', self.edit_group.text())
        self.create_and_append_text_element(doc, org_contact, 'base:OrganisationID', self.edit_rep_org.text())
        self.create_and_append_text_element(doc, org_contact, 'base:Country', self.edit_country.text())

        print(doc.toprettyxml())
        #print(doc.toprettyxml(indent="\t", encoding="utf-8"))

        #pi = doc.createProcessingInstruction('xml', 'version="1.0" encoding="utf-8"')
        #doc.insertBefore(pi, doc.firstChild)
        #pxml = doc.toprettyxml()

    def create_and_append_text_element(self, doc, node, name, text):
        elem = doc.createElement(name)
        node.appendChild(elem)
        text_node = doc.createTextNode(str(text))
        elem.appendChild(text_node)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Colirix()
    sys.exit(app.exec_())