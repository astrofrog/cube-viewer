
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

        self._levels = []
        self.set_cmap('RdYlBu', 'diverging')
        
    def resizeEvent(self, event):
        super(QtVTKWidget, self).resizeEvent(event)
        self.window_interactor.resize(self.height(), self.width())

    def set_data(self, data, vmin=None, vmax=None, spectral_stretch=1.):

        if vmin is None:
            self.vmin = np.nanmin(data)
        else:
            self.vmin = vmin

        if vmax is None:
            self.vmax = np.nanmax(data)
        else:
            self.vmax = vmax

        nz, ny, nx = data.shape
        data = np.clip((data - self.vmin) / (self.vmax - self.vmin) * 255., 0., 255.)
        data = data.astype(np.uint8)
        data_string = data.tostring()

        self.readerVolume = vtk.vtkImageImport()
        self.readerVolume.CopyImportVoidPointer(data_string, len(data_string))
        self.readerVolume.SetDataScalarTypeToUnsignedChar()
        self.readerVolume.SetNumberOfScalarComponents(1)
        self.readerVolume.SetDataExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        self.readerVolume.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        self.readerVolume.SetDataSpacing(1, 1, spectral_stretch)

        self.render_window.AddRenderer(self.ren)

        self.ren.ResetCameraClippingRange()

    def reset_levels(self):
        self.ren.RemoveAllViewProps()
        self._levels = []

    def set_levels(self, levels):
    
        self.reset_levels()
    
        levels = np.asarray(levels)
        levels = np.clip((levels - self.vmin) / (self.vmax - self.vmin) * 255., 0., 255.)

        for ilevel, level in enumerate(levels):
            self.add_contour(level, ilevel)

        self.levels = levels

        self._update_level_colors()

    def set_cmap(self, name, type, alpha=1):
        self._cmap = get_map(name, type, 5).mpl_colormap
        self._alpha = alpha
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
            print(x, color)
            actor.GetProperty().SetColor(*color[:3])
            actor.GetProperty().SetOpacity(self._alpha)

    def add_contour(self, level, ilevel, color=(1., 1., 1.), alpha=1.):

        contour = vtk.vtkMarchingCubes()
        contour.SetInput(self.readerVolume.GetOutput())
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
        print('rendering')
        self.render_window.Render()
        