# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkMultiBlockPLOT3DReader(SimpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        SimpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkMultiBlockPLOT3DReader(), 'Reading vtkMultiBlockPLOT3D.',
            (), ('vtkMultiBlockPLOT3D',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)
