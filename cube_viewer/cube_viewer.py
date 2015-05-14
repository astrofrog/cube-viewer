import os
import argparse

import numpy as np

from glue.external.qt import QtGui
from glue.qt.qtutil import load_ui
from glue.qt import get_qapp

from spectral_cube import SpectralCube

from .options_widget import IsosurfaceOptionsWidget
from .vtk_widget import QtVTKWidget

UI_MAIN = os.path.join(os.path.dirname(__file__), 'standalone.ui')


class StandaloneViewer(QtGui.QWidget):

    def __init__(self, parent=None):

        super(StandaloneViewer, self).__init__(parent=parent)

        self.ui = load_ui(UI_MAIN, self)

        self.ui.setFixedSize(800, 1000)

        self.vtk_widget = QtVTKWidget()
        self.ui.main.addWidget(self.vtk_widget)
        self.vtk_widget.setFixedSize(750, 750)

        self.options_widget = IsosurfaceOptionsWidget(vtk_widget=self.vtk_widget)
        self.ui.main.addWidget(self.options_widget)


def main():

    parser = argparse.ArgumentParser(description='View a spectral cube')
    parser.add_argument('filename', type=str,
                        help='the name of the file to read in')
    parser.add_argument('levels', nargs="+", type=float,
                        help='the levels to show')
    parser.add_argument('--stretch-spectral', help='Factor by which to stretch spectral dimension', default=1)

    args = parser.parse_args()
    if len(args.levels) > 8:
        raise ValueError("Too many levels (maximum allowed is 8)")

    data = SpectralCube.read(args.filename, format='fits')

    app = get_qapp()

    levels = np.array(args.levels)

    w = StandaloneViewer()

    w.options_widget.levels = levels
    w.options_widget.spectral_stretch = float(args.stretch_spectral)

    w.vtk_widget.set_data(data.unmasked_data[:, :, :].value)

    w.options_widget.update_viewer()

    w.show()

    app.exec_()
    app.quit()
