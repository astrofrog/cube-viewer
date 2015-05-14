import os

from PyQt4 import QtGui
from glue.qt.qtutil import load_ui
from glue.qt import get_qapp

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
        self.set_levels([])
        self.set_spectral_stretch(1)

    def set_levels(self, levels):
        if isinstance(levels, (list, tuple)):
            self.ui.values_field.setText(", ".join([str(x) for x in levels]))
        else:
            self.ui.values_field.setText(levels)
            
    def set_spectral_stretch(self, spectral_stretch):
        self.ui.spectral_stretch_field.setText("{0:g}".format(spectral_stretch))

    def update_viewer(self):
        self._vtk_widget.set_spectral_stretch(self.spectral_stretch)
        self._vtk_widget.set_cmap(self.cmap, 'diverging', alpha=self.get_alpha())
        self._vtk_widget.set_levels(self.values)
        self._vtk_widget.render()

    @property
    def spectral_stretch(self):
        return float(self.ui.spectral_stretch_field.text())

    @property
    def alpha(self):
        return self.ui.alpha_slider.value() / 100.

    def get_alpha(self):
        return self.ui.alpha_slider.value() / 100.

    @property
    def cmap(self):
        return self.ui.cmap_menu.currentText()

    @property
    def values(self):
        return (float(self.ui.scaling_field.text())
                * np.array(self.ui.values_field.text().split(','), dtype=float))


if __name__ == "__main__":
    app = get_qapp()
    d = IsosurfaceOptionsWidget()
    d.show()
    app.exec_()
    app.quit()
