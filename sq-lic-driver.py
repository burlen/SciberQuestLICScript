import sys
import os
import imp
from math import sqrt,fabs,atan,pi
from time import asctime

print sys.path

from paraview.servermanager import vtkPVXMLElement
from paraview.servermanager import vtkPVXMLParser

# config file is passed by environment variable.
configFileName = os.getenv('SQ_DRIVER_CONFIG')
if (configFileName is None):
  print 'Usage:'
  print 'export SQ_DRIVER_CONFIG=/path/to/config.py'
  print '%s'%(sys.argv[0])

print 'configFileName:'
print configFileName

config = imp.load_source('module.name',configFileName)

try: paraview.simple
except: from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

# load the pugins
# paraview install location is passed via env var
pvPath = os.getenv('PV_LIBRARY_PATH')

print 'pvPath'
print pvPath

licPath = '%s/libSurfaceLIC.so'%(pvPath)
LoadPlugin(licPath,False,globals())
LoadPlugin(licPath,True,globals())

sqtkPath = '%s/libSciberQuestToolKit.so'%(pvPath)
LoadPlugin(sqtkPath,False,globals())
LoadPlugin(sqtkPath,True,globals())

# print a stacktrace if pv crashes (only in debug builds)
pm = SQProcessMonitor()
pm.EnableBacktraceHandler = 1
Show(pm)
UpdatePipeline()


###############################################################################
class pvLUT:
  """
  sqLUT -- ParaView lookup table data
  """
  def __init__(self):
    self.Name=""
    self.Space=""
    self.Values=[]

  def SetName(self,aName):
    self.Name=aName

  def GetName(self):
    return self.Name

  def SetColorSpace(self,aSpace):
    self.Space=aSpace

  def GetColorSpace(self):
    return self.Space

  def SetRGBValues(self,aValues):
    self.Values=aValues

  def GetRGBValues(self):
    return self.Values;

  def PrintSelf(self):
    print self.Name
    print self.Space
    print self.Values

###############################################################################
class pvLUTReader:
  """
  sqLUTReader -- Reader and container for ParaView xml  lookup tables
  """

  def __init__(self):
    self.LUTS={}
    self.DefaultLUT='Eos_A'
    return

  def Clear(self):
    """
    Clear internal data structures.
    """
    self.LUTS={}
    return

  def Print(self):
    """
    print the internal object state
    """
    names=""
    i=0
    for k in sorted(self.LUTS.iterkeys(),cmp=lambda x,y: cmp(x.lower(), y.lower())):
      lut=self.LUTS[k]
      names+=lut.GetName()
      names+=", "
      if ((i%6)==5):
        names+="\n"
      i+=1
    print names
    return

  def Read(self, aFileName):
    """
    read in the luts defined in the named file. Each
    call to read extends the internal list of LUTs
    """
    parser=vtkPVXMLParser()
    parser.SetFileName(aFileName)
    if (not parser.Parse()):
      print 'ERROR: parsing lut file %s'%(aFileName)
      return
    root=parser.GetRootElement()
    nElems=root.GetNumberOfNestedElements()
    i=0
    while (i<nElems):
      cmapElem=root.GetNestedElement(i)
      if (cmapElem.GetName()=='ColorMap'):
        lut=pvLUT()
        lut.SetName(cmapElem.GetAttribute('name'))
        lut.SetColorSpace(cmapElem.GetAttribute('space'))

        values=[]
        nRGB=cmapElem.GetNumberOfNestedElements()
        j=0
        while (j<nRGB):
          rgbElem=cmapElem.GetNestedElement(j)
          if (rgbElem.GetName()=='Point'):
            val=[float(rgbElem.GetAttribute('r')),
              float(rgbElem.GetAttribute('g')),
              float(rgbElem.GetAttribute('b'))]
            values.append(val)
          j=j+1
        lut.SetRGBValues(values)
        #lut.PrintSelf()
        self.LUTS[lut.GetName()]=lut
      i=i+1
    return

  def GetLUT(self,aArray,aLutName,aRangeOveride):
    """
    return a lut that can be used by paraview.
    """
    try:
      self.LUTS[aLutName]
    except KeyError:
      print 'ERROR: no LUT named %s using %s'%(aLutName,self.DefaultLUT)
      aLutName = self.DefaultLUT
    range = self.__GetRange(aArray,aRangeOveride)
    return GetLookupTableForArray(aArray.GetName(),
               aArray.GetNumberOfComponents(),
               RGBPoints=self.__MapRGB(aLutName,range),
               ColorSpace=self.__GetColorSpace(aLutName),
               VectorMode='Magnitude',
               ScalarRangeInitialized=1.0)

  def __GetColorSpace(self,aName):
    """
    return the color space from the lookup table object.
    """
    return self.LUTS[aName].GetColorSpace()


  def __GetRGB(self,aName):
    """
    return the rgb values for the named lut
    """
    return self.LUTS[aName]

  def __MapRGB(self,aName,aRange):
    """
    map the rgb values for the named lut onto a scalar
    range in a format pv understands
    """
    lut=self.LUTS[aName].GetRGBValues()
    nRGB=len(lut)
    x0=float(aRange[0])
    dx=(float(aRange[1])-float(aRange[0]))/(float(nRGB-1.0))
    mappedLut=[]
    i=0
    while(i<nRGB):
      x=x0+i*dx
      val=[x]+lut[i]
      mappedLut+=val
      i=i+1
    return mappedLut

  def __GetRange(self,aArray,aRangeOveride):
    """
    get the range from an array proxy object or if
    an overide is provided use that.
    """
    nComps = aArray.GetNumberOfComponents()
    range = [0.0, 1.0]
    if (len(aRangeOveride) == 0):
      if (nComps == 1):
        range = aArray.GetRange()
      else:
        # TODO - this could be larger than the range of the magnitude aArray
        rx = aArray.GetRange(0)
        ry = aArray.GetRange(1)
        rz = aArray.GetRange(2)
        range = [0.0,
             sqrt(rx[1]*rx[1]+ry[1]*ry[1]+rz[1]*rz[1])]
    else:
      range = aRangeOveride
    return range

print '====================================='
print asctime()
sys.stdout.flush()

# record the run parameters
print 'config.lutFiles'
print config.lutFiles
#
print 'config.outputBaseFileName'
print config.outputBaseFileName
#print 'config.writeData'
#print config.writeData
print 'config.outputWidth'
print config.outputWidth
#
print 'config.inputFileName'
print config.inputFileName
print 'config.arraysToRead'
print config.arraysToRead
#print 'config.startTimeStep'
#print config.startTimeStep
#print 'config.endTimeStep'
#print config.endTimeStep
print 'config.subset'
print config.iSubset
print config.jSubset
print config.kSubset
#
print 'config.smoothingArraysToFilter'
print config.smoothingArraysToFilter
print 'config.smoothingWidth'
print config.smoothingWidth
#
print 'config.vorticityArrayToFilter'
print config.vorticityArrayToFilter
print 'config.vorticityArraysToCopy'
print config.vorticityArraysToCopy
print 'config.vorticitySplitComponents'
print config.vorticitySplitComponents
print 'config.vorticitySplitComponents'
print config.vorticitySplitComponents
print 'config.computeVorticity'
print config.computeVorticity
print 'config.computeHelicity'
print config.computeHelicity
print 'config.computeNHelicity'
print config.computeNHelicity
print 'config.computeDivergence'
print config.computeDivergence
print 'config.computeLambda2'
print config.computeLambda2
print 'config.computeMagnitudes'
print config.computeMagnitudes
print 'config.computeQ'
print config.computeQ
print 'config.computeGradient'
print config.computeGradient
print 'config.computeEigenDiagnostic'
print config.computeEigenDiagnostic
#
print 'config.camZoom'
print config.camZoom
print 'config.camPos'
print config.camPos
print 'config.camFoc'
print config.camFoc
print 'config.camUp'
print config.camUp
#
print 'config.LICColorByArray'
print config.LICColorByArray
print 'config.LICLutName'
print config.LICLutName
print 'config.LICLutRange'
print config.LICLutRange
print 'config.LICAlpha'
print config.LICAlpha
print 'config.LICField'
print config.LICField
print 'config.LICSteps'
print config.LICSteps
print 'config.LICStepSize'
print config.LICStepSize
print 'config.LICIntensity'
print config.LICIntensity
print 'config.sliceColorByArray'
print config.sliceColorByArray
print 'config.sliceLutName'
print config.sliceLutName
print 'config.sliceLutRange'
print config.sliceLutRange
print 'config.sliceAlpha'
print config.sliceAlpha

# read in luts
LUTs = pvLUTReader()
for lutFile in config.lutFiles:
  LUTs.Read(lutFile)
print 'available luts'
LUTs.Print()

# read the dataset
bovr = SQBOVReader(FileName=config.inputFileName)
licObj = bovr

iExtent = bovr.GetProperty('ISubsetInfo')
jExtent = bovr.GetProperty('JSubsetInfo')
kExtent = bovr.GetProperty('KSubsetInfo')

print 'whole extent'
print iExtent
print jExtent
print kExtent

if (config.iSubset[0] < 0):
  config.iSubset[0] = iExtent[0]
if (config.iSubset[1] < 0):
  config.iSubset[1] = iExtent[1]

if (config.jSubset[0] < 0):
  config.jSubset[0] = jExtent[0]
if (config.jSubset[1] < 0):
  config.jSubset[1] = jExtent[1]

if (config.kSubset[0] < 0):
  config.kSubset[0] = kExtent[0]
if (config.kSubset[1] < 0):
  config.kSubset[1] = kExtent[1]

bovr.ISubset = config.iSubset
bovr.JSubset = config.jSubset
bovr.KSubset = config.kSubset
bovr.Arrays  = config.arraysToRead

# run the pipeline here to get the bounds
rep = Show(bovr)
rep.Representation = 'Outline'
Render()
Hide(bovr)

nSteps = 0
steps = bovr.TimestepValues
try:
  nSteps = len(steps)
except:
  nSteps = 1
  steps = [steps]

print "steps"
print steps
print "nStep"
print nSteps

bounds = bovr.GetDataInformation().GetBounds()
bounds_dx = fabs(bounds[1] - bounds[0])
bounds_dy = fabs(bounds[3] - bounds[2])
bounds_dz = fabs(bounds[5] - bounds[4])
bounds_cx = (bounds[0] + bounds[1])/2.0
bounds_cy = (bounds[2] + bounds[3])/2.0
bounds_cz = (bounds[4] + bounds[5])/2.0

if (bounds_dx == 0):
  # yz
  dimMode = 2
  aspect = bounds_dz/bounds_dy

elif (bounds_dy == 0):
  # xz
  dimMode = 1
  aspect = bounds_dz/bounds_dx

elif (bounds_dz == 0):
  #xy
  dimMode = 0
  aspect = bounds_dy/bounds_dx

else:
  #3d
  dimMode = 3
  aspect = 1.0 # TODO

print 'extent'
print config.iSubset
print config.jSubset
print config.kSubset
print 'bounds'
print bounds
print 'dx'
print (bounds_dx, bounds_dy, bounds_dz)
print 'cx'
print (bounds_cx, bounds_cy, bounds_cz)
print 'dimMode'
print dimMode

# set the step range
step = 0
startTimeStep = os.getenv('SQ_TIME_STEP')
if (startTimeStep is not None):
  step = int(startTimeStep)
#elif (config.startTimeStep >= 0):
#  step = config.startTimeStep
else:
  step = nSteps-1
print 'step'
print step

#endStep = step
#endTimeStep = os.getenv('SQ_END_TIME_STEP')
#if (endTimeStep is not None):
#  step = int(endTimeStep)
#elif (config.endTimeStep >= 0):
#  endStep = min(config.endTimeStep, nSteps-1)
#else:
#  endStep = nSteps-1
#print 'endStep'
#print endStep

anim = GetAnimationScene()
anim.PlayMode = 'Snap To TimeSteps'
anim.AnimationTime = steps[step]

view = GetRenderView()
view.ViewTime = steps[step]

# use smoothing
if (len(config.smoothingArraysToFilter)):
  ghosts1 = SQImageGhosts()
  rep=Show(ghosts1)
  rep.Representation = 'Outline'
  Render()
  Hide(ghosts1)

  conv = SQKernelConvolution()
  licObj = conv

  conv.Width = config.smoothingWidth

  if (config.smoothingArraysToFilter[0]=='all'):
      conv.Arrays = config.arraysToRead
  else:
    conv.Arrays = config.smoothingArraysToFilter

  rep=Show(conv)
  rep.Representation = 'Outline'
  Render()
  Hide(conv)

# compute vorticity
if ((config.vorticityArrayToFilter!='') and
    (config.computeVorticity or config.computeHelicity or
     config.computeNHelicity or config.computeLambda2 or
     config.computeDivergence or config.computeQ or
     config.computeGradient)):

  ghosts2 = SQImageGhosts()
  rep=Show(ghosts2)
  rep.Representation = 'Outline'
  Render()
  Hide(ghosts2)

  vortex = SQVortexFilter()
  rep=Show(vortex)
  rep.Representation = 'Outline'
  Render()
  Hide(vortex)
  licObj = vortex

  vortex.Arraytofilter = [config.vorticityArrayToFilter]
  vortex.Splitcomponents = config.vorticitySplitComponents
  vortex.Rotation = config.computeVorticity
  vortex.Normalizedhelicity = config.computeNHelicity
  vortex.Helicity = config.computeHelicity
  vortex.Lambda2 = config.computeLambda2
  vortex.Divergence = config.computeDivergence
  vortex.Resultmagnitude = config.computeMagnitudes
  vortex.Q = config.computeQ
  vortex.Gradient = config.computeGradient
  vortex.Eigenvaluediagnostic = config.computeEigenDiagnostic

  if (len(config.vorticityArraysToCopy)):
    if (config.vorticityArraysToCopy[0]=='all'):
      vortex.Arraystocopy = config.arraysToRead
    else:
      vortex.Arraystocopy = config.vorticityArraysToCopy

## make a directory for the output dataset
#if (config.writeData):
#  try:
#    os.mkdir(config.outputBaseFileName)
#  except:
#    pass
#  print 'writing data to %s'%(config.outputBaseFileName)


licRep = Show(licObj)
licRep.Representation = 'Outline'
Render()

# log the available arrays
print 'arrays available for rendering'
nArrays = licObj.PointData.GetNumberOfArrays()
i = 0
while (i<nArrays):
  print licObj.PointData.GetArray(i).Name
  i = i + 1

# position the camera
camFar=1.0

if (dimMode == 0):
  # xy
  camUp = [0.0, 1.0, 0.0]
  camDir = 2
  pos = max(bounds_dx, bounds_dy)
  camPos = [bounds_cx, bounds_cy, -pos*camFar]
  camFoc = [bounds_cx, bounds_cy, bounds_cz]

elif (dimMode == 1):
  # xz
  camUp = [0.0, 0.0, 1.0]
  camDir = 1
  pos = max(bounds_dx, bounds_dz)
  camPos = [bounds_cx, -pos*camFar,  bounds_cz]
  camFoc = [bounds_cx, bounds_cy, bounds_cz]

elif (dimMode == 2):
  # yz
  camUp = [0.0, 0.0, 1.0]
  camDir = 0
  pos = max(bounds_dy, bounds_dz)
  camPos = [ pos*camFar, bounds_cy, bounds_cz]
  camFoc = [bounds_cx, bounds_cy, bounds_cz]

else:
  # 3d
  print '3d cam position is yet TODO'

# user overrides
if (len(config.camUp)):
  camUp = config.camUp

if (len(config.camPos)):
  camPos = config.camPos

if (len(config.camFoc)):
  camFoc = config.camFoc

# configure the view
width = 1024
if (config.outputWidth>0):
  width = int(config.outputWidth)

height = int(config.outputHeight)
if (config.outputHeight<1):
  height = int(width*aspect)

view.CameraViewUp = camUp
view.CameraPosition = camPos
view.CameraFocalPoint = camFoc
view.UseOffscreenRenderingForScreenshots = 0
view.CenterAxesVisibility = 0
view.OrientationAxesVisibility = 0
view.ViewSize = [width, height]
Render()
view.ResetCamera()

cam = GetActiveCamera()
cam.Zoom(config.camZoom)

print 'Camera'
print 'up'
print view.CameraViewUp
print 'position'
print view.CameraPosition
print 'focal point'
print view.CameraFocalPoint
print 'angle'
print view.CameraViewAngle
print 'clipping range'
print view.CameraClippingRange
print 'parallel scale'
print view.CameraParallelScale

# configure render
# render once as slice ? if I don't do this
# rendering crashes because tcoords array is empty
licRep.InterpolateScalarsBeforeMapping = 0
licRep.ColorArrayName = config.LICColorByArray
licRep.InterpolateScalarsBeforeMapping = 0
licRep.Representation = 'Slice'
if (config.LICColorByArray!=''):
  array = licObj.PointData.GetArray(config.LICColorByArray)
  licRep.LookupTable = LUTs.GetLUT(array,config.LICLutName,config.LICLutRange)
licRep.Opacity = config.LICAlpha
Render()
print 'rendered lic as slice'
sys.stdout.flush()

if (config.LICField!=''):
  licRep.SelectLICVectors = [config.LICField]
  licRep.LICStepSize = config.LICStepSize
  licRep.LICNumberOfSteps = config.LICSteps
  licRep.LICIntensity = config.LICIntensity
  licRep.Representation = 'Surface LIC'
  Render()
  print 'rendered surface lic'
  sys.stdout.flush()

sliceObj=None
sliceRep=None
if (config.sliceAlpha>0.001):
  sliceObj=SQImageGhosts(licObj)
  sliceRep=Show(sliceObj)
  sliceRep.Representation = 'Slice'
  sliceRep.ColorArrayName = config.sliceColorByArray
  sliceRep.InterpolateScalarsBeforeMapping = 0
  if (config.sliceColorByArray!=''):
    array = sliceObj.PointData.GetArray(config.sliceColorByArray)
    sliceRep.LookupTable = LUTs.GetLUT(array,config.sliceLutName,config.sliceLutRange)
  sliceRep.Opacity = config.sliceAlpha
  Render()
  print 'rendered slice'
  sys.stdout.flush()

# write image
outputFileName = '%s%09d.png'%(config.outputBaseFileName, int(steps[step]))
WriteImage(outputFileName,Magnification=2)
print 'output file'
print outputFileName
print 'width'
print width
print 'height'
print height

print 'sliceObj'
print sliceObj
print 'sliceRep'
print sliceRep

## loop over requested step range
#while (step <= endStep):
#
#  print '====================================='
#  print 'step'
#  print step
#  print 'time'
#  print steps[step]
#  print 'wall time'
#  print asctime()
#  sys.stdout.flush()
#
#  # run the pipeline to update  array information
#  anim.AnimationTime = steps[step]
#  view.ViewTime = steps[step]
#
#  # if writing, don't render just write and continue
#  if (config.writeData):
#    outputPath = '%s/%06d'%(config.outputBaseFileName, step)
#    os.mkdir(outputPath)
#    outputFileName = '%s/%06d.pvti'%(outputPath, step)
#    writer = CreateWriter(outputFileName)
#    writer.UpdatePipeline()
#    continue
#
#  # render LIC
#  if (sliceObj is not None):
#    Hide(sliceObj)
#
#  if (config.LICColorByArray!=''):
#    array = licObj.PointData.GetArray(config.LICColorByArray)
#    licRep.LookupTable = LUTs.GetLUT(array,config.LICLutName,config.LICLutRange)
#  Render()
#  print 'rendered LIC'
#  sys.stdout.flush()
#
#  # render slice
#  if (sliceObj is not None):
#    sliceRep=Show(sliceObj)
#    if (config.sliceColorByArray!=''):
#      array = sliceObj.PointData.GetArray(config.sliceColorByArray)
#      sliceRep.LookupTable = LUTs.GetLUT(array,config.sliceLutName,config.sliceLutRange)
#    Render()
#  print 'rendered slice'
#  sys.stdout.flush()
#
#  # write image
#  outputFileName = '%s%06d.png'%(config.outputBaseFileName, step)
#  WriteImage(outputFileName)
#  print 'output file'
#  print outputFileName
#  print 'width'
#  print width
#  print 'height'
#  print height
#
#  step = step + 1

print '====================================='
print 'run completed at'
print asctime()
