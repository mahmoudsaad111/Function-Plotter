import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QMessageBox
from PySide2.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
import numpy as np


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)
        
        #set icon for the app 
        icon = QIcon("./function_plotter_icon.png")
        self.setWindowIcon(icon)

        # Create input fields 
        self.functionLabel = QLabel("Function:    e.g: 5*x^3 + 2*x  ,  Supported operators :   + * ^ /")
        self.functionInput = QLineEdit()
        self.minValueLabel = QLabel("Min value of x:")
        self.minValueInput = QLineEdit()
        self.maxValueLabel = QLabel("Max value of x:")
        self.maxValueInput = QLineEdit()

        # Create plot and clear button
        self.plotButton = QPushButton("Plot")
        self.clearButton = QPushButton("Clear")
        
        #create error message 
        self.errorMessageBox = QMessageBox()
        
        # set button actions
        self.plotButton.clicked.connect(self.plot_function)
        self.clearButton.clicked.connect(self.clearInput)


        # Create layout for input fields and the buttons
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.functionLabel)
        self.layout.addWidget(self.functionInput)
        self.layout.addWidget(self.minValueLabel)
        self.layout.addWidget(self.minValueInput)
        self.layout.addWidget(self.maxValueLabel)
        self.layout.addWidget(self.maxValueInput)
        self.layout.addWidget(self.plotButton)
        self.layout.addWidget(self.clearButton)

        # Create main widget and set layout
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.layout)

        # Set main widget as central widget of main window
        self.setCentralWidget(self.mainWidget)
        
        #create canvas for plotting layout
        self.fig = Figure()
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
           
            
    def plot_function(self):
        
        #take values from input fields
        functionStr = self.functionInput.text()
        functionStr = functionStr.replace("**","y").replace("^", "**")
        minValueStr = self.minValueInput.text()
        maxValueStr = self.maxValueInput.text()
        
        # handle constant function
        if('x' not in functionStr and len(functionStr)>0):
            functionStr+='+0*x'
        
        # Validate input values
        try: 
            
            if functionStr=="":
                raise ValueError("You must Enter the function before plot")
            
            if minValueStr=="" or maxValueStr=="":
                raise ValueError("You must Enter min and max value for the function")
            
            try:
                minValue = float(minValueStr)
                maxValue = float(maxValueStr)
            except Exception as e:
                raise ValueError("min and max value must be numbers only")
           
        
            if minValue >= maxValue:
                raise ValueError("Minimum value must be less than maximum value")
        
        
        except ValueError as e:
            self.errorHandler(e)
            return
        
            
        try:
            # Create array of x values 
            x = np.linspace(minValue, maxValue, 100)
            
            # Evaluate function y for each x value and show error if function not correct 
            try:
                y = eval(functionStr)
            except Exception as e:
                raise ValueError("please enter valid function")
            
            # Create Matplotlib figure and plot function
            self.fig.clear()
            self.ax = self.fig.add_subplot()
            self.ax.plot(x, y)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.set_title("Function Plot")
            self.ax.axhline(y=0, color='black')
            self.ax.axvline(x=0, color='black')
            ymin = min(y)
            ymax = max(y)
            self.ax.grid(True)
            self.ax.set_xlim(minValue,maxValue)
            self.ax.set_ylim(ymin, ymax)
            
            # show the plot in the main window
            self.canvas.draw()
            
        except Exception as e:
            self.errorHandler(e)


    def clearInput(self):
        #clear input fields and the plot also
        self.functionInput.clear()
        self.minValueInput.clear()
        self.maxValueInput.clear()
        self.ax.clear()
        self.canvas.draw()
   
  
    def errorHandler(self, e):
        # Display error message for any error
        self.errorMessageBox.setWindowTitle("Error!")
        self.errorMessageBox.setText(str(e))
        self.errorMessageBox.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())