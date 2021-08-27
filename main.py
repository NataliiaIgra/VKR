import sys
from PySide2 import QtCore, QtWidgets, QtGui
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUi()

    def initUi(self):
        self.central_widget = QtWidgets.QWidget()

        self.scroll_area = QtWidgets.QScrollArea(self.central_widget)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget_contents = QtWidgets.QWidget()
        self.scroll_area_widget_contents.setGeometry(QtCore.QRect(0, 0, 780, 550))

        self.tab_layout = QtWidgets.QVBoxLayout(self.scroll_area_widget_contents)

        self.tab_widget = QtWidgets.QTabWidget(self.scroll_area_widget_contents)

        self.tab_1 = QtWidgets.QWidget()
        self.tab_2 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab_1, "Tab 1")
        self.tab_widget.addTab(self.tab_2, "Material properties")

        self.layout_tab_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.tab_2.setLayout(self.layout_tab_2)

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setText("5")
        #self.lineEdit2 = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel("f'c, ksi")
        self.lineEdit.setMaximumWidth(100)
        self.concrete_label = QtWidgets.QLabel("Concrete Properties")
        self.concrete_label.setFont(QtGui.QFont('Helvetica', 16))

        self.push_button = QtWidgets.QPushButton("Plot concrete model")

        self.frame_concrete = QtWidgets.QFrame(self.tab_2)
        self.frame_concrete.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_concrete.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_steel = QtWidgets.QFrame(self.tab_2)
        self.frame_steel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_steel.setFrameShadow(QtWidgets.QFrame.Raised)

        self.layout_inside_concrete = QtWidgets.QVBoxLayout()
        self.layout_inside_steel = QtWidgets.QVBoxLayout()
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc2 = MplCanvas(self, width=5, height=4, dpi=100)
        #sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.layout_inside_concrete_1 = QtWidgets.QHBoxLayout()
        self.layout_inside_concrete_1.addWidget(self.lineEdit)
        self.layout_inside_concrete_1.addWidget(self.label)
        self.layout_inside_concrete.addWidget(self.concrete_label)
        self.layout_inside_concrete.setAlignment(self.concrete_label, QtCore.Qt.AlignCenter)
        self.layout_inside_concrete.addLayout(self.layout_inside_concrete_1)
        self.layout_inside_concrete.setAlignment(QtCore.Qt.AlignCenter)
        # self.layout_inside_concrete.addWidget(self.lineEdit)
        # self.layout_inside_concrete.addWidget(self.label)
        self.layout_inside_concrete.addWidget(self.push_button)
        self.layout_inside_concrete.addWidget(sc)
        self.layout_inside_steel.addWidget(sc2)

        #self.layout_inside_steel.addWidget(self.lineEdit2)

        self.layout_tab_2.addWidget(self.frame_concrete)
        self.layout_tab_2.addWidget(self.frame_steel)

        self.frame_concrete.setLayout(self.layout_inside_concrete)
        self.frame_steel.setLayout(self.layout_inside_steel)

        self.tab_layout.addWidget(self.tab_widget)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.central_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar()
        self.file = self.menu_bar.addMenu("File")
        self.setMenuBar(self.menu_bar)

        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.showMessage("Status Bar Is Ready")
        self.setStatusBar(self.status_bar)
        self.resize(1200, 800)


if __name__ == "__main__":
    my_app = QtWidgets.QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    my_app.exec_()
