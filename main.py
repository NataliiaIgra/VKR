import sys
import math
from PySide2 import QtCore, QtWidgets, QtGui
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUi()

        self.push_button_plot_concrete.clicked.connect(self.plot_concrete)
        self.push_button_plot_steel.clicked.connect(self.plot_steel)

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

        self.concrete_label = QtWidgets.QLabel("Concrete Properties")
        self.concrete_label.setFont(QtGui.QFont('Helvetica', 16))
        self.line_edit_comp_strength = QtWidgets.QLineEdit()
        self.line_edit_comp_strength.setText("5")
        self.line_edit_comp_strength.setMaximumWidth(100)
        self.label_comp_strength = QtWidgets.QLabel("f'c, ksi")
        self.push_button_plot_concrete = QtWidgets.QPushButton("Plot concrete model")
        self.frame_concrete = QtWidgets.QFrame(self.tab_2)
        self.frame_concrete.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_concrete.setFrameShadow(QtWidgets.QFrame.Raised)
        self.layout_inside_concrete = QtWidgets.QVBoxLayout()
        self.canvas_concrete = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout_inside_concrete_1 = QtWidgets.QHBoxLayout()
        self.layout_inside_concrete_1.addWidget(self.line_edit_comp_strength)
        self.layout_inside_concrete_1.addWidget(self.label_comp_strength)
        self.layout_inside_concrete.addWidget(self.concrete_label)
        self.layout_inside_concrete.setAlignment(self.concrete_label, QtCore.Qt.AlignCenter)
        self.layout_inside_concrete.addLayout(self.layout_inside_concrete_1)
        # self.layout_inside_concrete.setAlignment(QtCore.Qt.AlignCenter)
        self.layout_inside_concrete.addWidget(self.push_button_plot_concrete)
        self.layout_inside_concrete.addWidget(self.canvas_concrete)

        self.steel_label = QtWidgets.QLabel("Steel Properties")
        self.steel_label.setFont(QtGui.QFont('Helvetica', 16))
        self.line_edit_yield_strength = QtWidgets.QLineEdit()
        self.line_edit_yield_strength.setText("60")
        self.line_edit_yield_strength.setMaximumWidth(100)
        self.label_yield_strength = QtWidgets.QLabel("fy, ksi")
        self.line_edit_steel_modulus = QtWidgets.QLineEdit()
        self.line_edit_steel_modulus.setText("29000")
        self.line_edit_steel_modulus.setMaximumWidth(100)
        self.label_steel_modulus = QtWidgets.QLabel("Es, ksi")
        self.push_button_plot_steel = QtWidgets.QPushButton("Plot steel model")
        self.frame_steel = QtWidgets.QFrame(self.tab_2)
        self.frame_steel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_steel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.layout_inside_steel = QtWidgets.QVBoxLayout()
        self.canvas_steel = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout_inside_steel_1 = QtWidgets.QHBoxLayout()
        self.layout_inside_steel_1.addWidget(self.line_edit_yield_strength)
        self.layout_inside_steel_1.addWidget(self.label_yield_strength)
        self.layout_inside_steel_2 = QtWidgets.QHBoxLayout()
        self.layout_inside_steel_2.addWidget(self.line_edit_steel_modulus)
        self.layout_inside_steel_2.addWidget(self.label_steel_modulus)
        self.layout_inside_steel.addWidget(self.steel_label)
        self.layout_inside_steel.setAlignment(self.steel_label, QtCore.Qt.AlignCenter)
        self.layout_inside_steel.addLayout(self.layout_inside_steel_1)
        self.layout_inside_steel.addLayout(self.layout_inside_steel_2)
        # self.layout_inside_steel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout_inside_steel.addWidget(self.push_button_plot_steel)
        self.layout_inside_steel.addWidget(self.canvas_steel)

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

    @QtCore.Slot()
    def plot_concrete(self):
        values = calculate_concrete(float(self.line_edit_comp_strength.text()))
        self.canvas_concrete.axes.cla()
        self.canvas_concrete.axes.plot(values[0], values[1])
        self.canvas_concrete.draw()

    @QtCore.Slot()
    def plot_steel(self):
        values = calculate_steel(float(self.line_edit_yield_strength.text()),
                                 float(self.line_edit_steel_modulus.text()))
        self.canvas_steel.axes.cla()
        self.canvas_steel.axes.plot(values[0], values[1])
        self.canvas_steel.draw()


def calculate_concrete(comp_strength_dash):
    strains = list()
    stresses = list()
    comp_strength_double_dash = 0.9 * comp_strength_dash
    limiting_strain = 0.0038
    elastic_modulus = 57000 * math.sqrt(comp_strength_dash * 1000) / 1000
    apex_strain = 1.8 * comp_strength_double_dash / elastic_modulus
    parabola_points = 100
    strain_increment = apex_strain / parabola_points
    for i in range(0, parabola_points + 1):
        calculated_strain = i * strain_increment
        strains.append(calculated_strain)
        calculated_stress = comp_strength_double_dash * (
                2 * calculated_strain / apex_strain - (calculated_strain / apex_strain) ** 2)
        stresses.append(calculated_stress)
    strains.append(limiting_strain)
    stresses.append(0.85 * comp_strength_double_dash)
    return strains, stresses

    # fig, ax = plt.subplots()
    # ax.plot(strains, stresses)
    # ax.grid()
    # plt.show()


def calculate_steel(yield_strength, elastic_modulus):
    strains = [0, yield_strength / elastic_modulus, 0.05]
    stresses = [0, yield_strength, yield_strength]
    return strains, stresses


def draw_rectangle():
    fig, ax = plt.subplots()
    rect = matplotlib.patches.Rectangle((0.0, 0.0), 20, 24, color='silver')
    circle = matplotlib.patches.Circle((2.75, 2.75), 1.27 / 2, color='black')
    circle2 = matplotlib.patches.Circle((20 - 2.75, 2.75), 1.27 / 2, color='black')
    ax.add_patch(rect)
    ax.add_patch(circle)
    ax.add_patch(circle2)
    # plt.axis('off')
    plt.xlim([0, 20])
    plt.ylim([0, 24])
    plt.gca().set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_xlabel("Width = 20")
    ax.set_yticks([])
    ax.set_ylabel("Height = 24")
    plt.show()


# draw_rectangle()

if __name__ == "__main__":
    my_app = QtWidgets.QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    my_app.exec_()
