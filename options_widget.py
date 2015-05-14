import os

from PyQt4 import QtGui
from glue.qt.qtutil import load_ui
from glue.qt import get_qapp

import six
import numpy as np

from palettable.colorbrewer import COLOR_MAPS

__all__ = ["IsosurfaceOptions"]

UI_MAIN = os.path.join(os.path.dirname(__file__), 'options.ui')


class IsosurfaceOptionsWidget(QtGui.QWidget):

    def __init__(self, parent=None, vtk_widget=None):

        super(IsosurfaceOptionsWidget, self).__init__(parent=parent)

        self.ui = load_ui(UI_MAIN, self)

        for map_name in COLOR_MAPS['Diverging']:
            self.ui.cmap_menu.addItem(map_name)

        self.ui.apply.clicked.connect(self.update_viewer)

        self._vtk_widget = vtk_widget
        self.levels = []
        self.spectral_stretch = 1.
        self.alpha = 0.5

        print(dir(self.ui.cmap_menu))
        self.ui.cmap_menu.currentIndexChanged.connect(self.update_live)
        self.ui.alpha_slider.valueChanged.connect(self.update_live)
        self.ui.values_field.returnPressed.connect(self.update_live)
        self.ui.spectral_stretch_field.returnPressed.connect(self.update_live)

    def update_live(self):
        if self.live:
            self.update_viewer()

    def update_viewer(self):
        self._vtk_widget.spectral_stretch = self.spectral_stretch
        self._vtk_widget.cmap = self.cmap
        self._vtk_widget.alpha = self.alpha
        self._vtk_widget.levels = self.levels
        self._vtk_widget.render()

    @property
    def live(self):
        return self.ui.live_checkbox.isChecked()

    @property
    def spectral_stretch(self):
        return float(self.ui.spectral_stretch_field.text())

    @spectral_stretch.setter
    def spectral_stretch(self, spectral_stretch):
        self.ui.spectral_stretch_field.setText("{0:g}".format(spectral_stretch))

    @property
    def alpha(self):
        return self.ui.alpha_slider.value() / 100.

    @alpha.setter
    def alpha(self, value):
        return self.ui.alpha_slider.setValue(value * 100.)

    @property
    def cmap(self):
        return self.ui.cmap_menu.currentText()

    @cmap.setter
    def cmap(self, value):
        index = self.ui.cmap_menu.fingText(value)
        self.ui.cmap_menu.setCurrentIndex(index)

    @property
    def levels(self):
        return np.array(self.ui.values_field.text().split(','), dtype=float)

    @levels.setter
    def levels(self, levels):
        if isinstance(levels, six.string_types):
            self.ui.values_field.setText(levels)
        else:
            self.ui.values_field.setText(", ".join([str(x) for x in levels]))



if __name__ == "__main__":
    app = get_qapp()
    d = IsosurfaceOptionsWidget()
    d.show()
    app.exec_()
    app.quit()
