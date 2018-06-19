import c4d

def add_layer(name, layer_color):
   root = doc.GetLayerObjectRoot()
   LayersList = root.GetChildren() 

   names=[]    
   layers=[]
   
   for l in LayersList:
       n=l.GetName()
       names.append(n)
       layers.append((n,l))

   if not name in names:
       layer = c4d.documents.LayerObject() #New Layer
       layer.SetName(name)  
       layer[c4d.ID_LAYER_COLOR] = layer_color
       layer_settings = {'solo': False, 'view': True, 'render': True, 'manager': True, 'locked': True, 'generators': False, 'deformers': False, 'expressions': True, 'animation': True}
       layer.SetLayerData(doc, layer_settings)
       layer.InsertUnder(root)

   else:
       for n, l in layers:
           if n ==name:
               layer=l
               break
   return layer

def main():
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.')
        return

    for obj in activeObjects:
        obj[c4d.ID_LAYER_LINK] = add_layer('AOV Shaders', c4d.Vector(1,0.5,0.5))

    print 'finish'
    c4d.EventAdd()

main()