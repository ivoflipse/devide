# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkXMLMultiGroupDataReader(SimpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        SimpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkXMLMultiGroupDataReader(), 'Reading vtkXMLMultiGroupData.',
            (), ('vtkXMLMultiGroupData',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)