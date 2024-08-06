from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QGridLayout, QToolButton, QSizePolicy
from PyQt5 import QtCore
import krita
#from krita import *
from krita import DockWidget

class TabUI(krita.DockWidget):

    def __init__(self):
        super(TabUI, self).__init__()

        self.firstTimeRun = True
        self.colorPickActivated = False

        self.baseWidget = QWidget()
        self.layout = QGridLayout()

        self.btnundo = QToolButton()
        self.btnundo.setStyleSheet("background-color:#300000;")
        self.btnundo.setText("Undo")
        self.btnundo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btnundo.clicked.connect(lambda: Krita.instance().action("edit_undo").trigger())
        self.layout.addWidget(self.btnundo, 0, 0)

        self.btnsave = QToolButton()
        self.btnsave.setStyleSheet("background-color:#002800;")
        self.btnsave.setText("Save")
        self.btnsave.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btnsave.clicked.connect(lambda: Krita.instance().action("file_save").trigger())
        self.layout.addWidget(self.btnsave, 0, 1)

        self.btnmirror = QToolButton()
        self.btnmirror.setStyleSheet("background-color:#000000;")
        self.btnmirror.setText("Mir.\nCanv.")
        self.btnmirror.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btnmirror.clicked.connect(lambda: Krita.instance().action("mirror_canvas").trigger())
        self.layout.addWidget(self.btnmirror, 0, 2)

        self.btnclear = QToolButton()
        self.btnclear.setStyleSheet("background-color:#000000;")
        self.btnclear.setText("Clear")
        self.btnclear.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btnclear.clicked.connect(lambda: Krita.instance().action("clear").trigger())
        self.layout.addWidget(self.btnclear, 1, 0)

        self.btndeselect = QToolButton()
        self.btndeselect.setStyleSheet("background-color:#000000;")
        self.btndeselect.setText("Desel.")
        self.btndeselect.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btndeselect.clicked.connect(lambda: Krita.instance().action("deselect").trigger())
        self.layout.addWidget(self.btndeselect, 1, 1)

        self.btnbrush = QToolButton()
        self.btnbrush.setStyleSheet("background-color:#000000;")
        self.btnbrush.setText("Brush")
        self.btnbrush.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btnbrush.clicked.connect(lambda: Krita.instance().action("KritaShape/KisToolBrush").trigger())
        self.layout.addWidget(self.btnbrush, 1, 2)

        self.btntransform = QToolButton()
        self.btntransform.setStyleSheet("background-color:#000000;")
        self.btntransform.setText("Transf.")
        self.btntransform.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btntransform.clicked.connect(lambda: Krita.instance().action("KisToolTransform").trigger())
        self.layout.addWidget(self.btntransform, 2, 0)

        self.btnfill = QToolButton()
        self.btnfill.setStyleSheet("background-color:#000000;")
        self.btnfill.setText("Fill")
        self.btnfill.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btnfill.clicked.connect(lambda: Krita.instance().action("fill_selection_foreground_color").trigger())
        self.layout.addWidget(self.btnfill, 2, 1)

        self.btncolorpicker = QToolButton()
        self.btncolorpicker.setStyleSheet("background-color:#000000;")
        self.btncolorpicker.setText("Col.\nPckr")
        self.btncolorpicker.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btncolorpicker.clicked.connect(lambda: Krita.instance().action('KritaSelected/KisToolColorSampler').trigger())
        self.btncolorpicker.clicked.connect(self.addMouseEventsToColorChange)
        self.layout.addWidget(self.btncolorpicker, 2, 2)

        self.btnselectionol = QToolButton()
        self.btnselectionol.setStyleSheet("background-color:#000000;")
        self.btnselectionol.setText("Outl.\nSel.")
        self.btnselectionol.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btnselectionol.clicked.connect(lambda: Krita.instance().action("KisToolSelectOutline").trigger())
        self.layout.addWidget(self.btnselectionol, 3, 0)

        self.baseWidget.setLayout(self.layout)
        self.setWidget(self.baseWidget)

        self.setWindowTitle(i18n("TabUI"))

    def canvasChanged(self, canvas):
        pass

    def addMouseEventsToColorChange(self):
        qwin = Krita.instance().activeWindow().qwindow()
        self.addConsoleMessage("starting to inject myself to color changes")
        self.colorPickActivated = True

        if self.firstTimeRun:
            self.firstTimeRun = False
            mouse_observer = MouseObserver(qwin.windowHandle())

            #mouse_observer.pressed.connect(lambda pos: print(f"pressed: {pos}"))
            #mouse_observer.released.connect(lambda pos: print(f"released: {pos}"))
            #mouse_observer.moved.connect(lambda pos: print(f"moved: {pos}"))

            mouse_observer.released.connect(self.activateBrushOnMouseRelease)

    def addConsoleMessage(self, message):
        print(message)

    def activateBrushOnMouseRelease(self):
        if self.colorPickActivated:
            Krita.instance().action("KritaShape/KisToolBrush").trigger()
            self.colorPickActivated = False
            self.addConsoleMessage("Color has been chosen; Returning to Brush tool.")

class MouseObserver(QtCore.QObject):
    pressed = QtCore.pyqtSignal(QtCore.QPoint)
    released = QtCore.pyqtSignal(QtCore.QPoint)
    moved = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, window):
        super().__init__(window)
        self._window = window

        self.window.installEventFilter(self)

    @property
    def window(self):
        return self._window

    def eventFilter(self, obj, event):
        if self.window is obj:
            if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.TabletPress:
                self.pressed.emit(event.pos())
            elif event.type() == QtCore.QEvent.MouseMove or event.type() == QtCore.QEvent.TabletMove:
                self.moved.emit(event.pos())
            elif event.type() == QtCore.QEvent.MouseButtonRelease or event.type() == QtCore.QEvent.TabletRelease:
                self.released.emit(event.pos())
        return super().eventFilter(obj, event)
    

Application.addDockWidgetFactory(krita.DockWidgetFactory("tabui", krita.DockWidgetFactoryBase.DockRight, TabUI))
