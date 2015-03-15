import sys
import vtk
import numpy as np
from astropy.io import fits
from PyQt4 import QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class QtVTKRenderer(QtGui.QWidget):

    def __init__(self, filename):

        super(VTKRenderer, self).__init__()

        data_matrix = fits.getdata(filename)
        data_matrix = data_matrix[145:245, :, :]
        data_matrix[data_matrix < 0.7] = 0.
        data_matrix = (data_matrix * 100).astype(np.uint8)
        nz, ny, nx = data_matrix.shape
        data_string = data_matrix.tostring()

        self.readerVolume = vtk.vtkImageImport()
        self.readerVolume.CopyImportVoidPointer(data_string, len(data_string))
        self.readerVolume.SetDataScalarTypeToUnsignedChar()
        self.readerVolume.SetNumberOfScalarComponents(1)
        self.readerVolume.SetDataExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        self.readerVolume.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        self.readerVolume.SetDataSpacing(1, 1, 1)

        self.contour = vtk.vtkMarchingCubes()
        self.contour.SetInput(self.readerVolume.GetOutput())
        self.contour.SetValue(0, 150)
        self.contour.ComputeNormalsOn()

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.contour.GetOutput())
        self.mapper.ScalarVisibilityOff()

        self.actor = vtk.vtkLODActor()
        self.actor.SetMapper(self.mapper)
        self.actor.SetNumberOfCloudPoints(100000)
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(1, 0.5, 0.5)
        self.actor.GetProperty().SetOpacity(0.3)

        self.ren = vtk.vtkRenderer()
        self.ren.AddActor(self.actor)
        self.ren.SetBackground(0, 0, 0)

        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren)

        self.ren.ResetCameraClippingRange()

        self.vtkw = QVTKRenderWindowInteractor(self, rw=self.renWin)
        self.vtkw.resize(800, 800)
        self.vtkw.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

        self.renWin.Render()
        self.renWin.PolygonSmoothingOn()
        self.vtkw.Initialize()
        self.vtkw.Start()


if __name__ == "__main__":

    app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

    w = QtVTKRenderer(sys.argv[1])
    w.show()

    app.exec_()
