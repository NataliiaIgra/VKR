from math import sqrt
from PySide2 import QtCore, QtWidgets, QtGui


class Concrete:
    def __init__(self, comp_strength_dash=5):
        self.comp_strength_dash = comp_strength_dash

    def calculate_concrete(self):
        strains = list()
        stresses = list()
        comp_strength_double_dash = 0.9 * self.comp_strength_dash
        limiting_strain = 0.0038
        concrete_modulus = 57000 * sqrt(self.comp_strength_dash * 1000) / 1000
        apex_strain = 1.8 * comp_strength_double_dash / concrete_modulus
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

    @staticmethod
    def checks_concrete(comp_strength):
        empty_check_concrete = comp_strength
        error_dialog_concrete = QtWidgets.QMessageBox()
        error_dialog_concrete.setText("Value of concrete compressive strength should be between 1 and 6")
        error_dialog_concrete.setWindowTitle("Error in 'Material Properties' tab, concrete")
        error_dialog_concrete.setWindowIcon(QtGui.QIcon(':/img/Resources/emoji.png'))
        if empty_check_concrete == "":
            error_dialog_concrete.exec_()
            return False
        else:
            required_strength = float(empty_check_concrete)
            if required_strength < 1 or required_strength > 6:
                error_dialog_concrete.exec_()
                return False
        return True
