# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkExtractSelectedGraph(SimpleVTKClassModuleBase):
    def __init__(self, module_manager):
        SimpleVTKClassModuleBase.__init__(
            self, module_manager,
            vtk.vtkExtractSelectedGraph(), 'Processing.',
            ('vtkAbstractGraph', 'vtkSelection'), ('vtkGraph',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)
