from PySide2 import QtCore, QtWidgets, QtGui


class Steel:
    def __init__(self, yield_strength=60, steel_modulus=29000):
        self.yield_strength = yield_strength
        self.steel_modulus = steel_modulus

    def calculate_steel(self):
        strains = [0, self.yield_strength / self.steel_modulus, 0.05]
        stresses = [0, self.yield_strength, self.yield_strength]
        return strains, stresses

    @staticmethod
    def checks_steel(yield_strength, steel_modulus):
        empty_check_yield = yield_strength
        empty_check_modulus = steel_modulus
        error_dialog_steel = QtWidgets.QMessageBox()
        error_dialog_steel.setWindowTitle("Error in 'Material Properties' tab, steel")
        error_dialog_steel.setWindowIcon(QtGui.QIcon(':/img/Resources/emoji.png'))

        if empty_check_yield == "":
            error_dialog_steel.setText("Value of steel yield strength should be between 40 and 100")
            error_dialog_steel.exec_()
            return False
        elif empty_check_modulus == "":
            error_dialog_steel.setText("Value of steel Young's modulus should between 27500 and 31200")
            error_dialog_steel.exec_()
            return False
        else:
            if float(empty_check_yield) < 40 or float(empty_check_yield) > 100:
                error_dialog_steel.setText("Value of steel yield strength should be between 40 and 100")
                error_dialog_steel.exec_()
                return False
            elif float(empty_check_modulus) < 27500 or float(empty_check_modulus) > 31200:
                error_dialog_steel.setText("Value of steel Young's modulus should between 27500 and 31200")
                error_dialog_steel.exec_()
                return False
        return True
