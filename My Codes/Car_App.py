#region imports
from Car_GUI import Ui_Form
import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from QuarterCarModel import CarController
#endregion

class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        input_widgets = (
            self.le_m1, self.le_v, self.le_k1, self.le_c1, self.le_m2, self.le_k2,
            self.le_ang, self.le_tmax, self.chk_IncludeAccel
        )
        display_widgets = (
            self.gv_Schematic, self.chk_LogX, self.chk_LogY, self.chk_LogAccel,
            self.chk_ShowAccel, self.lbl_MaxMinInfo, self.layout_Plot
        )

        self.controller = CarController((input_widgets, display_widgets))

        self.btn_calculate.clicked.connect(self.controller.calculate)
        self.pb_Optimize.clicked.connect(self.doOptimize)
        self.chk_LogX.stateChanged.connect(self.controller.doPlot)
        self.chk_LogY.stateChanged.connect(self.controller.doPlot)
        self.chk_LogAccel.stateChanged.connect(self.controller.doPlot)
        self.chk_ShowAccel.stateChanged.connect(self.controller.doPlot)

        self.controller.setupEventFilter(self)
        self.controller.setupCanvasMoveEvent(self)
        self.setWindowTitle("Quarter Car Model")
        self.show()

    def eventFilter(self, obj, event):
        if obj == self.gv_Schematic.scene():
            if event.type() == qtc.QEvent.GraphicsSceneMouseMove:
                scenePos = event.scenePos()
                self.setWindowTitle("x = {}, y = {}".format(round(scenePos.x(), 2), round(-scenePos.y(), 2)))
            if event.type() == qtc.QEvent.GraphicsSceneWheel:
                zm = self.controller.getZoom()
                zm = max(0.1, zm + 0.1 if event.delta() > 0 else zm - 0.1)
                self.controller.setZoom(zm)
        self.controller.updateSchematic()
        return super(MainWindow, self).eventFilter(obj, event)

    def mouseMoveEvent_Canvas(self, event):
        if event.inaxes:
            self.controller.animate(event.xdata)
            ywheel, ybody, yroad, accel = self.controller.getPoints(event.xdata)
            self.setWindowTitle(f"t={event.xdata:.2f}s, y-road={yroad*1000:.2f}mm, y-wheel={ywheel*1000:.2f}mm, y-car={ybody*1000:.2f}mm, accel={accel:.2f}g")

    def doOptimize(self):
        app.setOverrideCursor(qtc.Qt.WaitCursor)
        self.controller.OptimizeSuspension()
        app.restoreOverrideCursor()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
