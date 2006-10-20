# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkXMLPDataSetWriter(SimpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        SimpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkXMLPDataSetWriter(), 'Writing vtkXMLPDataSet.',
            ('vtkXMLPDataSet',), (),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)
