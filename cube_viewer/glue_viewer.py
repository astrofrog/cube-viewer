import numpy as np
from glue.qt.widgets.data_viewer import DataViewer

from .options_widget import IsosurfaceOptionsWidget
from .vtk_widget import QtVTKWidget


class GlueVTKViewer(DataViewer):

    LABEL = "VTK Isosurfaces"

    def __init__(self, session, parent=None):
        super(GlueVTKViewer, self).__init__(session, parent=parent)
        self._vtk_widget = QtVTKWidget()
        self.setCentralWidget(self._vtk_widget)
        self._options_widget = IsosurfaceOptionsWidget(vtk_widget=self._vtk_widget)

    def add_data(self, data):
        self._vtk_widget.set_data(data['PRIMARY'])
        initial_level = "{0:.3g}".format(np.percentile(data['PRIMARY'], 99))
        self._options_widget.levels = initial_level
        self._options_widget.update_viewer()
        return True

    def options_widget(self):
        return self._options_widget
