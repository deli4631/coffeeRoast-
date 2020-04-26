from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QLabel, QSlider
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import csv
import abc

#slider
class Subject():
    """
    Know its observers. Any number of Observer objects may observe a
    subject.
    Send a notification to its observers when its state changes.
    """

    def __init__(self, slider):
        self._observers = set()

        self._subject_state = None

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    @property
    def subject_state(self):
        return self._subject_state

    @subject_state.setter
    def subject_state(self, arg):
        self._subject_state = arg
        self._notify()


#graph
class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class ConcreteObserver(Observer):
    """
    Implement the Observer updating interface to keep its state
    consistent with the subject's.
    Store state that should stay consistent with the subject's.
    """

    def update(self, arg):
        self._observer_state = arg
        # ...


class MainWindow(QtWidgets.QMainWindow):
    run_program = False
    loc = 0
    tmp_limit = 430
    data = {}
    val = 0
    slider_move = False

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        uic.loadUi('roaster.ui', self)
        self.sliderSetup()
        self.data_setup()
        self.startButton.clicked.connect(self.startClicked)
        self.pauseButton.clicked.connect(self.pauseClicked)
        self.recordButton.clicked.connect(self.recordButtonClicked)
        self.plot()
        

    def data_setup(self):
        with open('roasting_data.csv',  newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data[int(row['time'])] = int(row['tmp'])
            

    def sliderSetup(self):
        self.powerSlider.setMinimum(0)
        self.powerSlider.setMaximum(430)
        self.powerSlider.setTickInterval(3)


    def sliderVal(self):
        print(self.powerSlider.value)
        


    def plot(self):


        self.graphWidget.setBackground('w')

        self.x = [0]  # 100 time points
        self.y = [0]

        # self.y = [randint(0,100) for _ in range(100)]  # 100 data points
        # self.y = list()

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
                # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


        self.powerSlider.valueChanged[int].connect(self.changeValue)
        # self.graphWidget.plot(hour, temp)
    
    def changeValue(self, value):
        self.tmpLimit.setText("Temp Limit : %s" % (value))
        self.tmp_limit = value  

    
    def startClicked(self):
        self.run_program = True
        # self.run_program = False
    
    def pauseClicked(self):
        self.run_program = False
    
    def recordButtonClicked(self):
        self.slider_move = True


    def update_plot_data(self):
        if(self.run_program):
            # self.x = self.x[1:]  # Remove the first y element.
            self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
            # print(self.x[self.loc])
            self.loc += 1
            if(self.loc >= 720):
                run_program = False
                return 
            # self.y = self.y[1:]  # Remove the first 
            # val = randint(0,100)
            if(self.slider_move):
                val = self.tmp_limit
            else:
                val = self.data[self.x[self.loc]]
            
            self.y.append(val)  # Add a new random value.
            self.temp.setText("Temp: %s" % (val))
        
            self.data_line.setData(self.x, self.y)  # Update the data.

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()





