import sys
from PySide2 import QtCore, QtWidgets, QtGui
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import resources
from concrete_model import calculate_concrete
from steel_model import calculate_steel
from moment_curvature import calculate_moment_curvature


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setWindowTitle("Momcurv")
        self.setWindowIcon(QtGui.QIcon(':/img/Resources/main-icon.png'))

        self.push_button_section_type_1.clicked.connect(self.activate_tab_3)

        self.push_button_plot_concrete.clicked.connect(self.plot_concrete)
        self.push_button_plot_steel.clicked.connect(self.plot_steel)
        self.push_button_draw_section.clicked.connect(self.draw_section)
        self.push_button_plot_momcurv.clicked.connect(self.plot_momcurv)

        self.push_button_save_figure.clicked.connect(self.save_figure)
        self.push_button_clean_canvas.clicked.connect(self.clear_figure)

    def initUi(self):
        self.central_widget = QtWidgets.QWidget()

        self.scroll_area = QtWidgets.QScrollArea(self.central_widget)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget_contents = QtWidgets.QWidget()
        # self.scroll_area_widget_contents.setGeometry(QtCore.QRect(0, 0, 780, 550))

        self.tab_layout = QtWidgets.QVBoxLayout(self.scroll_area_widget_contents)

        self.tab_widget = QtWidgets.QTabWidget(self.scroll_area_widget_contents)

        self.tab_1 = QtWidgets.QWidget()
        self.tab_2 = QtWidgets.QWidget()
        self.tab_3 = QtWidgets.QWidget()
        self.tab_4 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab_1, "Section type")
        self.tab_widget.addTab(self.tab_2, "Material properties")

        self.layout_tab_1 = QtWidgets.QGridLayout()
        section_types = ["Rectangular section", "Circular section",
                         "T-shape section", "User-defined section"]

        self.push_button_section_type_1 = QtWidgets.QPushButton(section_types[0])
        self.push_button_section_type_1.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.push_button_section_type_2 = QtWidgets.QPushButton(section_types[1])
        self.push_button_section_type_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.push_button_section_type_2.setDisabled(True)

        self.push_button_section_type_3 = QtWidgets.QPushButton(section_types[2])
        self.push_button_section_type_3.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.push_button_section_type_3.setDisabled(True)

        self.push_button_section_type_4 = QtWidgets.QPushButton(section_types[3])
        self.push_button_section_type_4.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.push_button_section_type_4.setDisabled(True)

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.push_button_section_type_1)
        self.button_group.addButton(self.push_button_section_type_2)
        self.button_group.addButton(self.push_button_section_type_3)
        self.button_group.addButton(self.push_button_section_type_4)
        self.push_button_section_type_1.setCheckable(True)

        self.push_button_section_type_1.setIcon(QtGui.QIcon(':/img/Resources/rect.png'))
        self.push_button_section_type_1.setIconSize(QtCore.QSize(200, 200))

        self.push_button_section_type_2.setIcon(QtGui.QIcon(':/img/Resources/circ.png'))
        self.push_button_section_type_2.setIconSize(QtCore.QSize(200, 200))

        self.push_button_section_type_3.setIcon(QtGui.QIcon(':/img/Resources/t-shape.png'))
        self.push_button_section_type_3.setIconSize(QtCore.QSize(200, 200))

        self.layout_tab_1.addWidget(self.push_button_section_type_1, 0, 0)
        self.layout_tab_1.addWidget(self.push_button_section_type_2, 0, 1)
        self.layout_tab_1.addWidget(self.push_button_section_type_3, 1, 0)
        self.layout_tab_1.addWidget(self.push_button_section_type_4, 1, 1)

        self.tab_1.setLayout(self.layout_tab_1)

        self.layout_tab_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.tab_2.setLayout(self.layout_tab_2)

        self.concrete_label = QtWidgets.QLabel("Concrete Properties")
        self.concrete_label.setFont(QtGui.QFont('Helvetica', 12))
        self.line_edit_comp_strength = QtWidgets.QLineEdit()
        # reg_concrete = QtCore.QRegExp("6|[1-5]{1}[.][0-9]{2}")
        reg_concrete = QtCore.QRegExp("[1-9][0-9]*[.][0-9]*")
        self.reg_validator_concrete = QtGui.QRegExpValidator()
        self.reg_validator_concrete.setRegExp(reg_concrete)
        self.line_edit_comp_strength.setValidator(self.reg_validator_concrete)
        self.line_edit_comp_strength.setText("5")
        self.line_edit_comp_strength.setMaximumWidth(100)
        self.line_edit_comp_strength.setToolTip("Concrete compressive strength")
        self.label_comp_strength = QtWidgets.QLabel("f'c, ksi")
        self.push_button_plot_concrete = QtWidgets.QPushButton("Plot concrete model")
        self.frame_concrete = QtWidgets.QFrame(self.tab_2)
        self.frame_concrete.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_concrete.setFrameShadow(QtWidgets.QFrame.Raised)
        self.layout_inside_concrete = QtWidgets.QVBoxLayout()
        self.canvas_concrete = MplCanvas(self, width=5, height=5, dpi=100)
        self.canvas_concrete.axes.set_xlabel(f"Strain, in./in.")
        self.canvas_concrete.axes.set_ylabel(f"Stress, ksi.")
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
        self.steel_label.setFont(QtGui.QFont('Helvetica', 12))
        self.line_edit_yield_strength = QtWidgets.QLineEdit()
        reg_steel_strength = QtCore.QRegExp("100|[4-9][0-9][.][0-9]{2}")
        self.reg_validator_steel_strength = QtGui.QRegExpValidator()
        self.reg_validator_steel_strength.setRegExp(reg_steel_strength)
        self.line_edit_yield_strength.setValidator(self.reg_validator_steel_strength)
        self.line_edit_yield_strength.setText("60")
        self.line_edit_yield_strength.setMaximumWidth(100)
        self.label_yield_strength = QtWidgets.QLabel("fy, ksi")
        self.line_edit_steel_modulus = QtWidgets.QLineEdit()
        reg_steel_modulus = QtCore.QRegExp("31200|"
                                           "27[5-9][0-9][0-9]|2[89][0-9][0-9][0-9]|30[0-9][0-9][0-9]|31[01][0-9][0-9]")
        self.reg_validator_steel_modulus = QtGui.QRegExpValidator()
        self.reg_validator_steel_modulus.setRegExp(reg_steel_modulus)
        self.line_edit_steel_modulus.setValidator(self.reg_validator_steel_modulus)
        self.line_edit_steel_modulus.setText("29000")
        self.line_edit_steel_modulus.setMaximumWidth(100)
        self.label_steel_modulus = QtWidgets.QLabel("Es, ksi")
        self.push_button_plot_steel = QtWidgets.QPushButton("Plot steel model")
        self.frame_steel = QtWidgets.QFrame(self.tab_2)
        self.frame_steel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_steel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.layout_inside_steel = QtWidgets.QVBoxLayout()
        self.canvas_steel = MplCanvas(self, width=5, height=5, dpi=100)
        self.canvas_steel.axes.set_xlabel(f"Strain, in./in.")
        self.canvas_steel.axes.set_ylabel(f"Stress, ksi.")
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

        self.layout_tab_3 = QtWidgets.QHBoxLayout(self.tab_3)
        self.tab_3.setLayout(self.layout_tab_3)

        self.canvas_section = MplCanvas(self, width=8, height=4, dpi=100)
        self.canvas_section.axes.set_frame_on(False)
        self.canvas_section.axes.set(xticks=[], yticks=[])
        self.frame_draw_section = QtWidgets.QFrame(self.tab_3)
        self.frame_draw_section.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_draw_section.setFrameShadow(QtWidgets.QFrame.Raised)
        self.layout_inside_frame_draw_section = QtWidgets.QVBoxLayout()
        self.layout_inside_frame_draw_section.addWidget(self.canvas_section)
        self.frame_draw_section.setLayout(self.layout_inside_frame_draw_section)

        self.line_edit_height = QtWidgets.QLineEdit()
        self.line_edit_height.setMaximumWidth(100)
        self.label_height = QtWidgets.QLabel("Height, in.")
        self.layout_inside_section_1 = QtWidgets.QHBoxLayout()
        self.layout_inside_section_1.addWidget(self.line_edit_height)
        self.layout_inside_section_1.addWidget(self.label_height)

        self.line_edit_width = QtWidgets.QLineEdit()
        self.line_edit_width.setMaximumWidth(100)
        self.label_width = QtWidgets.QLabel("Width, in.")
        self.layout_inside_section_2 = QtWidgets.QHBoxLayout()
        self.layout_inside_section_2.addWidget(self.line_edit_width)
        self.layout_inside_section_2.addWidget(self.label_width)

        self.line_edit_cover = QtWidgets.QLineEdit()
        self.line_edit_cover.setMaximumWidth(100)
        self.label_cover = QtWidgets.QLabel("Clear cover, in.")
        self.layout_inside_section_3 = QtWidgets.QHBoxLayout()
        self.layout_inside_section_3.addWidget(self.line_edit_cover)
        self.layout_inside_section_3.addWidget(self.label_cover)

        self.combobox_rebars = QtWidgets.QComboBox()
        self.combobox_rebars.addItems(["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "14", "18"])
        self.combobox_rebars.setMaximumWidth(100)
        self.label_rebars = QtWidgets.QLabel("Long. rebar size, #")
        self.layout_inside_section_4 = QtWidgets.QHBoxLayout()
        self.layout_inside_section_4.addWidget(self.combobox_rebars)
        self.layout_inside_section_4.addWidget(self.label_rebars)

        self.line_edit_number_rebars = QtWidgets.QLineEdit()
        self.line_edit_number_rebars.setText("2")
        self.line_edit_number_rebars.setMaximumWidth(100)
        self.label_number_rebars = QtWidgets.QLabel("# Bottom bars (minimum 2)")
        self.layout_inside_section_5 = QtWidgets.QHBoxLayout()
        self.layout_inside_section_5.addWidget(self.line_edit_number_rebars)
        self.layout_inside_section_5.addWidget(self.label_number_rebars)

        self.push_button_draw_section = QtWidgets.QPushButton("Draw section")

        self.layout_inside_section = QtWidgets.QVBoxLayout()
        self.layout_inside_section.addLayout(self.layout_inside_section_1)
        self.layout_inside_section.addLayout(self.layout_inside_section_2)
        self.layout_inside_section.addLayout(self.layout_inside_section_3)
        self.layout_inside_section.addLayout(self.layout_inside_section_4)
        self.layout_inside_section.addLayout(self.layout_inside_section_5)
        self.layout_inside_section.addWidget(self.push_button_draw_section)
        self.frame_section = QtWidgets.QFrame(self.tab_3)
        self.frame_section.setLayout(self.layout_inside_section)

        self.layout_tab_3.addWidget(self.frame_draw_section)
        self.layout_tab_3.addWidget(self.frame_section)

        self.layout_tab_4 = QtWidgets.QHBoxLayout(self.tab_4)
        self.tab_4.setLayout(self.layout_tab_4)

        self.canvas_momcurv = MplCanvas(self, width=8, height=4, dpi=100)
        self.canvas_momcurv.axes.set_xlabel(f"Curvature, 1/in.")
        self.canvas_momcurv.axes.set_ylabel(f"Moment, kip-in.")
        self.frame_plot_momcurv = QtWidgets.QFrame(self.tab_4)
        self.frame_plot_momcurv.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_plot_momcurv.setFrameShadow(QtWidgets.QFrame.Raised)
        self.layout_inside_frame_plot_momcurv = QtWidgets.QVBoxLayout()
        self.layout_inside_frame_plot_momcurv.addWidget(self.canvas_momcurv)
        self.frame_plot_momcurv.setLayout(self.layout_inside_frame_plot_momcurv)

        self.choice_plot = QtWidgets.QGroupBox()
        self.layout_inside_choice_plot = QtWidgets.QVBoxLayout()
        self.radio_button_including = QtWidgets.QRadioButton(self.choice_plot)
        self.radio_button_including.setText("Including compression rebar")
        self.radio_button_not_including = QtWidgets.QRadioButton(self.choice_plot)
        self.radio_button_not_including.setText("No compression rebar")
        self.radio_button_not_including.setChecked(True)
        self.layout_inside_choice_plot.addWidget(self.radio_button_not_including)
        self.layout_inside_choice_plot.addWidget(self.radio_button_including)
        self.push_button_plot_momcurv = QtWidgets.QPushButton("Plot relationship")

        self.layout_inside_savings = QtWidgets.QHBoxLayout()
        self.push_button_save_figure = QtWidgets.QPushButton("Save figure")
        self.push_button_save_momcurv = QtWidgets.QPushButton("Save .txt file")
        self.layout_inside_savings.addWidget(self.push_button_save_figure)
        self.layout_inside_savings.addWidget(self.push_button_save_momcurv)

        self.push_button_clean_canvas = QtWidgets.QPushButton("Clear")
        self.push_button_clean_canvas.setIcon(qApp.style().standardIcon(QtWidgets.QStyle.SP_DialogResetButton))

        self.layout_inside_frame_momcurv = QtWidgets.QVBoxLayout()
        self.layout_inside_frame_momcurv.addLayout(self.layout_inside_choice_plot)
        self.layout_inside_frame_momcurv.addWidget(self.push_button_plot_momcurv)
        self.layout_inside_frame_momcurv.addLayout(self.layout_inside_savings)
        self.layout_inside_frame_momcurv.addWidget(self.push_button_clean_canvas)

        self.frame_momcurv = QtWidgets.QFrame(self.tab_4)
        self.frame_momcurv.setLayout(self.layout_inside_frame_momcurv)

        self.layout_tab_4.addWidget(self.frame_plot_momcurv)
        self.layout_tab_4.addWidget(self.frame_momcurv)

        self.tab_layout.addWidget(self.tab_widget)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.central_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.central_widget)

        # self.menu_bar = QtWidgets.QMenuBar()
        # self.file = self.menu_bar.addMenu("File")
        # self.setMenuBar(self.menu_bar)

        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.showMessage("Status Bar Is Ready")
        self.setStatusBar(self.status_bar)
        self.resize(1300, 820)

        self.bar = QtWidgets.QToolBar()
        self.bar.setOrientation(QtCore.Qt.Vertical)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.bar)
        # self.bar = self.addToolBar("Menu")

        self.bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self._save_action = self.bar.addAction(
            qApp.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton), "Save", self.on_save
        )
        # self._save_action.setShortcut(QtGui.QKeySequence.Save)

    @QtCore.Slot()
    def on_save(self):
        ...

    @QtCore.Slot()
    def activate_tab_3(self):
        if self.tab_widget.count() == 2:
            self.tab_widget.addTab(self.tab_3, "Section properties")

    @QtCore.Slot()
    def plot_concrete(self):
        empty_check = self.line_edit_comp_strength.text()
        error_dialog_concrete = QtWidgets.QMessageBox()
        error_dialog_concrete.setText('Input a value between 0.725 and 6')
        error_dialog_concrete.setWindowTitle('Error')
        if empty_check == "":
            error_dialog_concrete.exec_()
        else:
            required_strength = float(empty_check)
            values = calculate_concrete(required_strength)
            if required_strength < 0.725 or required_strength > 6:
                error_dialog_concrete.exec_()
            else:
                self.canvas_concrete.axes.cla()
                self.canvas_concrete.axes.plot(values[0], values[1])
                self.canvas_concrete.axes.set_xlabel(f"Strain, in./in.")
                self.canvas_concrete.axes.set_ylabel(f"Stress, ksi.")
                self.canvas_concrete.draw()
                # self.status_bar.showMessage("Concrete model plotted")


    @QtCore.Slot()
    def plot_steel(self):
        values = calculate_steel(float(self.line_edit_yield_strength.text()),
                                 float(self.line_edit_steel_modulus.text()))
        self.canvas_steel.axes.cla()
        self.canvas_steel.axes.plot(values[0], values[1])
        self.canvas_steel.axes.set_xlabel(f"Strain, in./in.")
        self.canvas_steel.axes.set_ylabel(f"Stress, ksi.")
        self.canvas_steel.draw()

    @QtCore.Slot()
    def draw_section(self):
        self.canvas_section.axes.cla()
        self.canvas_section.axes.set(xticks=[], yticks=[])

        height = float(self.line_edit_height.text())
        width = float(self.line_edit_width.text())
        cover = float(self.line_edit_cover.text())
        number_rebars = int(self.line_edit_number_rebars.text())

        rect = matplotlib.patches.Rectangle((0.0, 0.0), width, height, color='silver')
        self.canvas_section.axes.add_patch(rect)

        diameters = [(2, 0.25), (3, 0.375), (4, 0.5), (5, 0.625), (6, 0.75), (7, 0.875), (8, 1), (9, 1.128), (10, 1.27),
                     (11, 1.41), (14, 1.693), (18, 2.257)]
        current_rebar = int(self.combobox_rebars.currentText())
        current_diameter = float()

        for i in diameters:
            if current_rebar == i[0]:
                current_diameter = i[1]
                break

        rebar_left = matplotlib.patches.Circle((cover + current_diameter / 2, cover + current_diameter / 2),
                                               current_diameter / 2, color='black')
        rebar_right = matplotlib.patches.Circle((width - cover - current_diameter / 2, cover + current_diameter / 2),
                                                current_diameter / 2, color='black')

        self.canvas_section.axes.add_patch(rebar_left)
        self.canvas_section.axes.add_patch(rebar_right)

        if number_rebars > 2:
            space = (width - current_diameter - 2 * cover) / (number_rebars - 1)
            for j in range(number_rebars - 2):
                distances_for_left_rebar = cover + current_diameter / 2
                rebar_middle = matplotlib.patches.Circle(
                    (distances_for_left_rebar + (j + 1) * space, distances_for_left_rebar),
                    current_diameter / 2, color='black')
                self.canvas_section.axes.add_patch(rebar_middle)

        self.canvas_section.axes.set_xlim(xmin=0, xmax=width)
        self.canvas_section.axes.set_ylim(ymin=0, ymax=height)
        self.canvas_section.axes.set_aspect('equal', adjustable='box')
        self.canvas_section.axes.set_xlabel(f"Width = {width} in.")
        self.canvas_section.axes.set_ylabel(f"Height = {height} in.")
        self.canvas_section.axes.set_frame_on(True)
        self.canvas_section.draw()
        self.tab_widget.addTab(self.tab_4, "Moment-curvature analysis")

    @QtCore.Slot()
    def plot_momcurv(self):
        self.canvas_momcurv.axes.cla()
        height = float(self.line_edit_height.text())
        width = float(self.line_edit_width.text())
        comp_strength_dash = float(self.line_edit_comp_strength.text())
        yield_strength = float(self.line_edit_yield_strength.text())
        steel_modulus = float(self.line_edit_steel_modulus.text())
        cover = float(self.line_edit_cover.text())
        diameter = float(self.combobox_rebars.currentText())
        number_rebars = int(self.line_edit_number_rebars.text())
        values = calculate_moment_curvature(height, width, comp_strength_dash, yield_strength, steel_modulus, cover,
                                            diameter, number_rebars)
        self.canvas_momcurv.axes.plot(values[0], values[1])
        self.canvas_momcurv.axes.set_xlabel(f"Curvature, 1/in.")
        self.canvas_momcurv.axes.set_ylabel(f"Moment, kip-in.")
        self.canvas_momcurv.draw()

    # save method for figure
    @QtCore.Slot()
    def save_figure(self):
        # selecting file path
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "",
                                                            "PNG(*.png);;JPEG(*.jpg *.jpeg);;PDF(*.pdf);;All Files(*.*)")
        # if file path is blank return back
        if filePath == "":
            return

        # saving canvas at desired path
        self.canvas_momcurv.print_figure(filePath)

    @QtCore.Slot()
    def clear_figure(self):
        self.canvas_momcurv.axes.cla()
        self.canvas_momcurv.axes.set_xlabel(f"Curvature, 1/in.")
        self.canvas_momcurv.axes.set_ylabel(f"Moment, kip-in.")
        self.canvas_momcurv.draw()


if __name__ == "__main__":
    my_app = QtWidgets.QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    my_app.exec_()
