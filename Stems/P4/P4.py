#region imports
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QRadioButton, QGroupBox, QGridLayout
#region imports
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QApplication
from OttoDiesel_GUI import Ui_Form
from Otto import ottoCycleController
from Diesel import dieselCycleController
from Dual import dualCycleController  # This must exist and follow same structure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
#endregion

class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.calculated = False

        # Create canvas
        self.figure = Figure(figsize=(8, 8), tight_layout=True, frameon=True, facecolor='none')
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot()
        self.main_VerticalLayout.addWidget(self.canvas)

        # Create controllers
        self.otto = ottoCycleController()
        self.diesel = dieselCycleController()
        self.dual = dualCycleController()  # You must have this class implemented
        self.controller = self.otto

        # Collect widgets to pass to controllers
        self.someWidgets = [
            self.lbl_THigh, self.lbl_TLow, self.lbl_P0, self.lbl_V0, self.lbl_CR,
            self.le_THigh, self.le_TLow, self.le_P0, self.le_V0, self.le_CR,
            self.le_T1, self.le_T2, self.le_T3, self.le_T4,
            self.lbl_T1Units, self.lbl_T2Units, self.lbl_T3Units, self.lbl_T4Units,
            self.le_PowerStroke, self.le_CompressionStroke, self.le_HeatAdded, self.le_Efficiency,
            self.lbl_PowerStrokeUnits, self.lbl_CompressionStrokeUnits, self.lbl_HeatInUnits,
            self.rdo_Metric, self.cmb_Abcissa, self.cmb_Ordinate,
            self.chk_LogAbcissa, self.chk_LogOrdinate, self.ax, self.canvas
        ]

        # Set widgets in each controller
        self.otto.setWidgets(w=self.someWidgets)
        self.diesel.setWidgets(w=self.someWidgets)
        self.dual.setWidgets(w=self.someWidgets)

        # Connect signals
        self.rdo_Metric.toggled.connect(self.setUnits)
        self.btn_Calculate.clicked.connect(self.calcCycle)
        self.cmb_Abcissa.currentIndexChanged.connect(self.doPlot)
        self.cmb_Ordinate.currentIndexChanged.connect(self.doPlot)
        self.chk_LogAbcissa.stateChanged.connect(self.doPlot)
        self.chk_LogOrdinate.stateChanged.connect(self.doPlot)
        self.cmb_OttoDiesel.currentIndexChanged.connect(self.selectCycle)

        # Show
        self.show()

    def clamp(self, val, low, high):
        if self.isfloat(val):
            val = float(val)
            if val > high:
                return float(high)
            if val < low:
                return float(low)
            return val
        return float(low)

    def isfloat(self, value):
        if value == 'NaN':
            return False
        try:
            float(value)
            return True
        except ValueError:
            return False

    def doPlot(self):
        self.controller.updateView()

    def selectCycle(self):
        current = self.cmb_OttoDiesel.currentText().lower()
        if "otto" in current:
            self.controller = self.otto
            self.gb_Input.setTitle('Input for Air Standard Otto Cycle:')
        elif "diesel" in current:
            self.controller = self.diesel
            self.gb_Input.setTitle('Input for Air Standard Diesel Cycle:')
        elif "dual" in current:
            self.controller = self.dual
            self.gb_Input.setTitle('Input for Air Standard Dual Cycle:')
        self.controller.updateView()

    def setUnits(self):
        self.controller.updateView()

    def calcCycle(self):
        self.controller.calc()

# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Otto / Diesel / Dual Cycle Calculator')
    sys.exit(app.exec())
