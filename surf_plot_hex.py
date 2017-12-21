import numpy as np
from scipy.interpolate import griddata
import pandas as pd
import pyodbc
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_symbol(sym):
    with open('spec/VolSurf.sql', "r") as f:
        sql = f.read()
    split = sql.split('SPY')
    sql = split[0]
    for i in split[1:]:
        sql += sym + i
    cnxn = pyodbc.connect("Driver={SQL Server};Server=[server];UID=[user];PWD=[pw];Database=stocks;")
    data = pd.read_sql_query(sql, cnxn)
    cnxn.close()

    plt.clf()
    ax = fig.add_subplot(111)
    hb = ax.hexbin(x=data['TDTE'], y=data['Strike'], C=data['IV'], cmap='rainbow', gridsize=10)

    plt.title(sym.upper())
    ax.set_xlabel('TDTE')
    ax.set_ylabel('Strike')

    plt.colorbar(hb).set_label('IV', rotation='vertical')

    plt.tight_layout()

fig = plt.figure()

# control panel #
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


def update():
    textbox.selectAll()
    textbox.setFocus()
    try:
        plot_symbol(textbox.text())
        print('updating')
        fig.canvas.draw()
    except Exception:
        print('invalid symbol')

root = fig.canvas.manager.window
panel = QtWidgets.QWidget()
hbox = QtWidgets.QHBoxLayout(panel)
textbox = QtWidgets.QLineEdit(parent=panel)
textbox.returnPressed.connect(update)
hbox.addWidget(textbox)
panel.setLayout(hbox)

dock = QtWidgets.QDockWidget("Symbol", root)
dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
root.addDockWidget(Qt.BottomDockWidgetArea, dock)
dock.setWidget(panel)

toolbar = root.findChild(QtWidgets.QToolBar)
toolbar.setVisible(False)

textbox.setText('SPY')
textbox.selectAll()
textbox.setFocus()
######################

plot_symbol('SPY')
plt.show()
