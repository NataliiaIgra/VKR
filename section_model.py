from PySide2 import QtCore, QtWidgets, QtGui

DIAMETERS = [(2, 0.25), (3, 0.375), (4, 0.5), (5, 0.625), (6, 0.75), (7, 0.875), (8, 1), (9, 1.128), (10, 1.27),
             (11, 1.41), (14, 1.693), (18, 2.257)]

AREAS = [(2, 0.05), (3, 0.11), (4, 0.20), (5, 0.31), (6, 0.44), (7, 0.60), (8, 0.79), (9, 1), (10, 1.27),
         (11, 1.56), (14, 2.25), (18, 4.00)]


class RectangularSection:
    def __init__(self, depth=15, width=15, cover=2, number_rebars_bottom=2, number_rebars_top=2, diameter=6, area=0.44):
        self.depth = depth
        self.width = width
        self.cover = cover
        self.number_rebars_bottom = number_rebars_bottom
        self.number_rebars_top = number_rebars_top
        self.diameter = diameter
        self.area = area

    @staticmethod
    def checks_section(depth, width, cover, number_rebars_bottom, number_rebars_top, diameter):
        error_dialog_section = QtWidgets.QMessageBox()
        error_dialog_section.setWindowTitle("Error in 'Section properties' tab")
        error_dialog_section.setWindowIcon(QtGui.QIcon(':/img/Resources/emoji.png'))

        empty_check_depth = depth
        empty_check_width = width
        empty_check_cover = cover
        empty_check_number_rebars_bottom = number_rebars_bottom
        empty_check_number_rebars_top = number_rebars_top

        if empty_check_depth == "" or empty_check_width == "" or empty_check_cover == "" or empty_check_number_rebars_bottom == "" or empty_check_number_rebars_top == "":
            error_dialog_section.setText("Don't leave any blanks")
            error_dialog_section.exec_()
            return False
        elif float(empty_check_depth) < (current_width := float(empty_check_width)):
            error_dialog_section.setText("Width should not be greater than depth")
            error_dialog_section.exec_()
            return False
        elif (current_cover := float(empty_check_cover)) < 1.5:
            error_dialog_section.setText("According to ACI 318-14, clear cover should not be less than 1.5 in.")
            error_dialog_section.exec_()
            return False
        elif (current_number_rebars_bottom := int(empty_check_number_rebars_bottom)) == 1 or (
                current_number_rebars_top := int(empty_check_number_rebars_top)) == 1:
            error_dialog_section.setText("Number of rebars cannot be equal to 1")
            error_dialog_section.exec_()
            return False
        else:
            current_rebar = float(diameter)
            current_diameter = float()

            for i in DIAMETERS:
                if current_rebar == i[0]:
                    current_diameter = i[1]
                    break
            space_bottom_check = (current_width - current_diameter * current_number_rebars_bottom - 2 * current_cover) / (
                    current_number_rebars_bottom - 1)
            space_top_check = float("inf")
            if current_number_rebars_top != 0:
                space_top_check = (current_width - current_diameter * current_number_rebars_top - 2 * current_cover) / (current_number_rebars_top - 1)

            requirement = max(current_diameter, 1)
            # print(space_bottom_check, requirement, current_diameter)
            if space_bottom_check < requirement or space_top_check < requirement:
                error_dialog_section.setText("Minimum bar spacing requirement is not satisfied. Reduce number of rebars")
                error_dialog_section.exec_()
                return False
        return True

