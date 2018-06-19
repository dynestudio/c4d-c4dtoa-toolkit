"""
Add Drivers Group - C4D script v0.1
Thanks for download - for commercial and personal uses.
This script / tool granted shall not be copied, distributed, or-sold, offered for resale, transferred in whole or in part except that you may make one copy for archive purposes only.

http://dyne.studio/
Writen by: Carlos Dordelly
Special thanks: Pancho Contreras, Terry Williams & Roberto Gonzalez.

Organize your arnold drivers in one group
Date start: 15/apr/2018
Date version: 15/apr/2018
Date end: --
Written and tested in Cinema 4D R19 / R18 / R17 / R16.

Add Drivers Group belongs to C4DtoA Script Tools and Dyne Tools (group of digital tools from dyne).

"""

import c4d
 
#global ids
color_ArnoldDrivers               = c4d.Vector(0.8,0.2,0.4) # layer Color
ARNOLD_DRIVER                     = 1030141

# get all objects with children
def get_all_objects(op, filter, output):
  while op:
      if filter(op):
          output.append(op)
      get_all_objects(op.GetDown(), filter, output)
      op = op.GetNext()
  return output

def add_ArnoldDrivers(name, color):

  # layers ops
  root = doc.GetLayerObjectRoot()
  layersList = root.GetChildren() 

  names=[]    
  layers=[]

  # start undo action
  #doc.StartUndo()

  for l in layersList:
     n=l.GetName()
     names.append(n)
     layers.append((n,l))

  if not name in names:

     c4d.CallCommand(100004738) # new Layer
     layersList = root.GetChildren() 
     layer=layersList[-1]
     layer.SetName(name)  

     layer[c4d.ID_LAYER_COLOR] = color 

  else:
     for n, l in layers:
         if n ==name:
             layer=l
             break 

  # prevent copies in obj manager
  objectsList = doc.GetObjects()
  for obj in objectsList:
    if obj[c4d.ID_BASELIST_NAME] == name:
      return

  # divider ops
  null = c4d.BaseObject(5140)
  null[c4d.ID_BASELIST_NAME] = name #name of null
  null[c4d.ID_LAYER_LINK] = layer
  null[c4d.NULLOBJECT_DISPLAY] = 14
  doc.InsertObject(null)

  # put the divider last in the obj manager
  firstObj = doc.GetFirstObject()
  lastObj = objectsList[-1]
  firstObj.InsertAfter(lastObj)

  # drivers objects list
  driversList = get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(ARNOLD_DRIVER), [])
  dgroup = doc.SearchObject(name)
  for driver in driversList:
    driver[c4d.ID_LAYER_LINK] = layer

    #get aovs
    driver_AOVs = driver.GetChildren()

    for aov in driver_AOVs:
        aov[c4d.ID_LAYER_LINK] = layer

    #insert drivers inside driver group null
    driver.InsertUnder(dgroup)
    #doc.AddUndo(c4d.UNDOTYPE_NEW, driver)

  #doc.AddUndo(c4d.UNDOTYPE_NEW, null)

  # end undo action
  #doc.EndUndo()

  # update scene
  c4d.EventAdd()

if __name__=='__main__':
  add_ArnoldDrivers("_Arnold Drivers_",color_ArnoldDrivers)