# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkXMLRectilinearGridReader(SimpleVTKClassModuleBase):
    def __init__(self, module_manager):
        SimpleVTKClassModuleBase.__init__(
            self, module_manager,
            vtk.vtkXMLRectilinearGridReader(), 'Reading vtkXMLRectilinearGrid.',
            (), ('vtkXMLRectilinearGrid',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)
