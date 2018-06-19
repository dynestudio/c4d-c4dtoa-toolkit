import c4d

"""

v01


"""

#arnold ids
ARNOLD_RENDERER                   = 1029988
ARNOLD_RENDERER_COMMAND           = 1039333
ARNOLD_DRIVER                     = 1030141
ARNOLD_OPERATOR                   = 1040497

# organizer ids 
color_ArnoldDrivers  = c4d.Vector(0.8,0.2,0.4) # layer Color
arnold_divider_name  = '_Arnold Elements_'     # divider name 

def get_all_objects(op, filter, output): # get all objects with children
    while op:
        if filter(op):
            output.append(op)
        get_all_objects(op.GetDown(), filter, output)
        op = op.GetNext()
    return output

def add_ArnoldDrivers(name, color):
   #layers ops
   root = doc.GetLayerObjectRoot()
   layersList = root.GetChildren() 

   names=[]    
   layers=[]
   
   #start undo action
   doc.StartUndo()

   for l in layersList:
       n=l.GetName()
       names.append(n)
       layers.append((n,l))

   if not name in names:
       layer = c4d.documents.LayerObject() #new Layer
       layer.SetName(name)  
       layer[c4d.ID_LAYER_COLOR] = color
       layer_settings = {'solo': False, 'view': False, 'render': True, 'manager': True, 'locked': False, 'generators': False, 'deformers': False, 'expressions': False, 'animation': False}
       layer.SetLayerData(doc, layer_settings)
       layer.InsertUnder(root)
   else:
       for n, l in layers:
           if n == name:
               layer=l
               break 

   #prevent copies in obj manager
   null = doc.SearchObject(name)
   if not null:
     #divider ops
     null = c4d.BaseObject(c4d.Onull)
     null[c4d.ID_BASELIST_NAME] = name #name of null
     null[c4d.ID_LAYER_LINK] = layer
     null[c4d.NULLOBJECT_DISPLAY] = 14
     doc.InsertObject(null)
   else:
        None

   #put the divider last in the obj manager
   objectsList = doc.GetObjects()
   firstObj = doc.GetFirstObject()
   lastObj = objectsList[-1]
   firstObj.InsertAfter(lastObj)

   doc.AddUndo(c4d.UNDOTYPE_NEW, null)

   #end undo action
   doc.EndUndo()
   
   #update scene
   c4d.EventAdd() ; return null

def main():
    # get scene drivers
    driversList = get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(ARNOLD_DRIVER), [])
    # get scene operators
    operatorsList = get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(ARNOLD_OPERATOR), [])
    # search or create the arnold divider group
    arnold_group = doc.SearchObject(arnold_divider_name)
    if not arnold_group:
        arnold_group = add_ArnoldDrivers(arnold_divider_name,color_ArnoldDrivers)

    for driver in driversList:
        driver.InsertUnder(arnold_group)

    c4d.EventAdd()

if __name__=='__main__':
    main()