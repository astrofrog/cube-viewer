import sys
import vtk
import numpy as np
from astropy.io import fits
from PyQt4 import QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class QtVTKRenderer(QtGui.QWidget):

    def __init__(self, filename):

        super(QtVTKRenderer, self).__init__()

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

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0, 0, 0)

        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren)

        self.ren.ResetCameraClippingRange()

        self.vtkw = QVTKRenderWindowInteractor(self, rw=self.renWin)
        self.vtkw.resize(800, 800)
        self.vtkw.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

        self.add_contour(50., color=(252./255., 141./255., 89./255.), alpha=0.4)
        self.add_contour(130., color=(1,1,191./255), alpha=0.4)
        self.add_contour(200, color=(145./255, 191./255., 219./255.), alpha=0.4)

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

    app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

    w = QtVTKRenderer(sys.argv[1])
    w.show()

    app.exec_()
