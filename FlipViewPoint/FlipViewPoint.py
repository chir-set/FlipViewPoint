import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# FlipViewPoint
#

class FlipViewPoint(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Flip viewpoint"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Utilities"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["SET (Hobbyist)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
Flip 2D views by 180°.
See more information in <a href="https://github.com/chir-set/FlipViewPoint">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

#
# FlipViewPointWidget
# These functions can easily be hooked to keyboard shortcuts in
# slicerrc.py. At one point, we run out of shortcuts,
# or there are too many to fit in the mind.
#

class FlipViewPointWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/FlipViewPoint.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = FlipViewPointLogic()

    # Connections

    self.ui.sliceNodeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.logic.process)
    self.ui.flipPushButton.connect('clicked(bool)', self.onFlipButton)
    self.ui.restorePushButton.connect('clicked(bool)', self.onRestoreButton)
    
  def onFlipButton(self):
    sliceNode = self.ui.sliceNodeSelector.currentNode()
    self.logic.process(sliceNode)
    
  def onRestoreButton(self):
    self.logic.restoreViews()

#
# FlipViewPointLogic
#

class FlipViewPointLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

  #https://www.slicer.org/wiki/Documentation/Nightly/ScriptRepository#Change_slice_orientation
  def process(self, sliceNode):
    if sliceNode is None:
        return;
    SliceToRAS = sliceNode.GetSliceToRAS()
    transform=vtk.vtkTransform()
    transform.SetMatrix(SliceToRAS)
    transform.RotateY(180)
    SliceToRAS.DeepCopy(transform.GetMatrix())
    sliceNode.UpdateMatrices()

  def restoreViews(self):
    views = slicer.app.layoutManager().sliceViewNames()
    for view in views:
        slicer.app.layoutManager().sliceWidget(view).mrmlSliceNode().SetOrientationToDefault()

#
# FlipViewPointTest
#

class FlipViewPointTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_FlipViewPoint1()

  def test_FlipViewPoint1(self):
    """
    """
