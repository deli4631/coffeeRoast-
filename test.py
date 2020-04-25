from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        uic.loadUi('roaster.ui', self)
        self.sliderSetup()
        self.plot()

    def sliderSetup(self):
        self.powerSlider.setMinimum(0)
        self.powerSlider.setMaximum(500)
        self.powerSlider.setTickInterval(3)
        

    def plot(self):
        self.graphWidget.setBackground('w')

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
                # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.startButton.clicked.connect(self.startClicked)

        # self.graphWidget.plot(hour, temp)
    
    def startClicked(self):
        print("start clicked")


    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first 
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()





