# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkPolyDataToImageStencil(SimpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        SimpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkPolyDataToImageStencil(), 'Processing.',
            ('vtkPolyData',), ('vtkImageStencilData',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)