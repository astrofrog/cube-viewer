
import vtk
import numpy as np
from PyQt4 import QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from palettable.colorbrewer import get_map


class QtVTKWidget(QtGui.QWidget):

    def __init__(self, parent=None):

        super(QtVTKWidget, self).__init__(parent=parent)

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0, 0, 0)

        self.render_window = vtk.vtkRenderWindow()

        self.window_interactor = QVTKRenderWindowInteractor(self, rw=self.render_window)

        self.render_window.Render()
        self.render_window.PolygonSmoothingOn()

        self.window_interactor.Initialize()
        self.window_interactor.Start()

        self.data = None
        self.levels = []
        self.cmap = 'RdYlBu'
        self.alpha = 0.5
        self.spectral_stretch = 1.

    def resizeEvent(self, event):
        super(QtVTKWidget, self).resizeEvent(event)
        print(self.height(), self.width())
        self.window_interactor.resize(self.width(), self.height())

    def set_data(self, data):
        self.data = data
        self.nz, self.ny, self.nx = data.shape
        self._update_scaled_data()

    @property
    def spectral_stretch(self):
        return self._spectral_stretch

    @spectral_stretch.setter
    def spectral_stretch(self, value):
        self._spectral_stretch = value
        self._update_scaled_data()

    def _update_scaled_data(self, vmin=None, vmax=None):

        if self.data is None:
            return

        if vmin is None:
            self.vmin = np.nanmin(self.data)
        else:
            self.vmin = vmin

        if vmax is None:
            self.vmax = np.nanmax(self.data)
        else:
            self.vmax = vmax

        data = np.clip((self.data - self.vmin) / (self.vmax - self.vmin) * 255., 0., 255.)
        data = data.astype(np.uint8)
        data_string = data.tostring()

        self.reader_volume = vtk.vtkImageImport()
        self.reader_volume.CopyImportVoidPointer(data_string, len(data_string))
        self.reader_volume.SetDataScalarTypeToUnsignedChar()
        self.reader_volume.SetNumberOfScalarComponents(1)
        self.reader_volume.SetDataExtent(0, self.nx - 1, 0, self.ny - 1, 0, self.nz - 1)
        self.reader_volume.SetWholeExtent(0, self.nx - 1, 0, self.ny - 1, 0, self.nz - 1)
        self.reader_volume.SetDataSpacing(1, 1, self._spectral_stretch)
        self.reader_volume.SetDataOrigin(self.nx / 2., self.ny / 2., self.nz / 2.)

        self.render_window.AddRenderer(self.ren)

        self.ren.ResetCameraClippingRange()

    @property
    def levels(self):
        return self._levels

    @levels.setter
    def levels(self, values):

        self._reset_levels()

        if len(values) == 0:
            return

        values = np.asarray(values)
        values = np.clip((values - self.vmin) / (self.vmax - self.vmin) * 255., 0., 255.)

        for ilevel, level in enumerate(values):
            self.add_contour(level, ilevel)

        self._update_level_colors()

    def _reset_levels(self):
        self.ren.RemoveAllViewProps()
        self._levels = []

    @property
    def cmap(self):
        return self._cmap

    @cmap.setter
    def cmap(self, name):
        self._cmap = get_map(name, 'diverging', 5).mpl_colormap
        self._update_level_colors()

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        self._update_level_colors()

    def _update_level_colors(self):

        if len(self._levels) == 0:
            return

        vmin = 0
        vmax = len(self._levels) - 1

        for level, actor in self._levels:
            if vmin == vmax:
                x = 0.5
            else:
                x = (level - vmin) / float(vmax - vmin)
            color = self._cmap(x)
            prop = actor.GetProperty()
            prop.SetColor(*color[:3])
            prop.SetOpacity(self.alpha)

    def add_contour(self, level, ilevel, color=(1., 1., 1.), alpha=1.):

        contour = vtk.vtkMarchingCubes()
        contour.SetInput(self.reader_volume.GetOutput())
        contour.SetValue(0, level)
        contour.ComputeNormalsOn()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInput(contour.GetOutput())
        mapper.ScalarVisibilityOff()

        actor = vtk.vtkLODActor()
        actor.SetMapper(mapper)
        actor.SetNumberOfCloudPoints(100000)
        actor.SetMapper(mapper)

        self._levels.append((ilevel, actor))

        self.ren.AddActor(actor)

    def render(self):
        self.render_window.Render()
