import c4d

C4DAIN_TAG = 1029989
C4DAIN_PERSP_CAMERA = 1559999735

# que reconozca el tipo de camara para saber que shutters settings usar

# persp cam
C4DAIP_PERSP_CAMERA_SHUTTER_START = 547660095
C4DAIP_PERSP_CAMERA_SHUTTER_END = 1921224566

#[c4d.AITAG_CAMERA_USE_TYPE]

def addAiTag():

    #get active objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.')
        return

    # obtener los tags de los objetos para evitar sobre escrituras
    # si ya tiene el tag, que solo sobre escriba los parametros pero que no cree una nueva

    for obj in activeObjects:
        cam_tag = obj.MakeTag(C4DAIN_TAG)

        cam_tag[1030392064] = 10
        cam_tag[c4d.C4DAI_CAMERA_CUSTOM_SHUTTER]    = True
        cam_tag[C4DAIP_PERSP_CAMERA_SHUTTER_START]  = 0.5
        cam_tag[C4DAIP_PERSP_CAMERA_SHUTTER_END]    = 0.5

    c4d.EventAdd()
    print "checkpoint"

addAiTag()