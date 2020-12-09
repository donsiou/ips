
from PyQt5 import QtWidgets
from trame import get_ports


class SelectPortDialog(QtWidgets.QDialog):

    def __init__(self, parent: QtWidgets.QWidget):
        super(QtWidgets.QDialog, self).__init__(parent)

        self.setWindowTitle("Select a port")

        grid = QtWidgets.QGridLayout(self)

        self.combo = QtWidgets.QComboBox()
        self.port_names = get_ports()
        self.combo.addItems(["%s (%s)" % (port, name)
                             for (port, name) in self.port_names])

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        grid.addWidget(self.combo, 0, 0)
        grid.addWidget(self.buttons, 1, 0)

    def showYourself(self):
        self.exec()
        i = self.combo.currentIndex()
        return None if i == -1 or self.result() != QtWidgets.QDialog.Accepted else self.port_names[i][0]
