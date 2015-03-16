import argparse

import vtk
import numpy as np
from PyQt4 import QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from palettable.colorbrewer import get_map

from spectral_cube import SpectralCube

class QtVTKRenderer(QtGui.QWidget):

    def __init__(self, data, vmin=None, vmax=None, levels=[], spectral_stretch=1.):

        super(QtVTKRenderer, self).__init__()

        # Prepare data
        if vmin is None:
            vmin = np.nanmin(data)
        if vmax is None:
            vmax = np.nanmax(data)
        nz, ny, nx = data.shape
        data = np.clip((data - vmin) / (vmax - vmin) * 255., 0., 255.)
        data = data.astype(np.uint8)
        data_string = data.tostring()

        # Prepare levels
        levels = np.asarray(levels)
        levels = np.clip((levels - vmin) / (vmax - vmin) * 255., 0., 255.)

        self.readerVolume = vtk.vtkImageImport()
        self.readerVolume.CopyImportVoidPointer(data_string, len(data_string))
        self.readerVolume.SetDataScalarTypeToUnsignedChar()
        self.readerVolume.SetNumberOfScalarComponents(1)
        self.readerVolume.SetDataExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        self.readerVolume.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        self.readerVolume.SetDataSpacing(1, 1, spectral_stretch)

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0, 0, 0)

        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren)

        self.ren.ResetCameraClippingRange()

        self.vtkw = QVTKRenderWindowInteractor(self, rw=self.renWin)
        self.vtkw.resize(800, 800)
        self.vtkw.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

        palette = get_map('RdYlBu', 'diverging', max(3,len(levels)))

        for ilevel, level in enumerate(levels):
            self.add_contour(level, color=palette.mpl_colors[ilevel], alpha=0.5)

        self.renWin.Render()
        self.renWin.PolygonSmoothingOn()
        self.vtkw.Initialize()
        self.vtkw.Start()

    def add_contour(self, level, color=(1., 1., 1.), alpha=1.):

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
        actor.GetProperty().SetColor(*color)
        actor.GetProperty().SetOpacity(alpha)

        self.ren.AddActor(actor)
        self.renWin.Render()


if __name__ == "__main__":

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

    app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

    levels = np.array(args.levels)
    vmin = levels.min() / 2.
    vmax = levels.max() * 2.

    w = QtVTKRenderer(data, vmin=vmin, vmax=vmax, levels=levels, spectral_stretch=float(args.stretch_spectral))
    w.show()

    app.exec_()
