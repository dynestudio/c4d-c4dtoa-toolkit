import c4d

# AI tag id
C4DAIN_TAG = 1029989

# camera ids
C4DAIN_CYL_CAMERA        = 12630987
C4DAIN_FISHEYE_CAMERA    = 1127342118
C4DAIN_ORTHO_CAMERA      = 204996153
C4DAIN_PERSP_CAMERA      = 1559999735
C4DAIN_SPHERICAL_CAMERA  = 1758358152
C4DAIN_VR_CAMERA         = 1470986773

# persp cam
C4DAIP_PERSP_CAMERA_SHUTTER_START      = 547660095
C4DAIP_PERSP_CAMERA_SHUTTER_END        = 1921224566
# vr cam
C4DAIP_VR_CAMERA_SHUTTER_START         = 1436598367
C4DAIP_VR_CAMERA_SHUTTER_END           = 1994337624
# spherical cam
C4DAIP_SPHERICAL_CAMERA_SHUTTER_START  = 784072210
C4DAIP_SPHERICAL_CAMERA_SHUTTER_END    = 182126491
# ortho cam
C4DAIP_ORTHO_CAMERA_SHUTTER_START      = 28462205
C4DAIP_ORTHO_CAMERA_SHUTTER_END        = 2031178548
# fisheye cam
C4DAIP_FISHEYE_CAMERA_SHUTTER_START    = 495609116
C4DAIP_FISHEYE_CAMERA_SHUTTER_END      = 209500179
# cyl cam
C4DAIP_CYL_CAMERA_SHUTTER_START        = 746177151
C4DAIP_CYL_CAMERA_SHUTTER_END          = 74265400

#[c4d.AITAG_CAMERA_USE_TYPE]
#[c4d.AITAG_CAMERA_TYPE]

# que reconozca el tipo de camara para saber que shutters settings usar

#get all objects with children
def get_all_objects(op, filter, output):
    while op:
        if filter(op):
            output.append(op)
        get_all_objects(op.GetDown(), filter, output)
        op = op.GetNext()
    return output

def addAiTag():

    #get active objects
    """activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.')
        return """

    objectsList = get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(c4d.Ocamera), [])

    print objectsList

    # obtener los tags de los objetos para evitar sobre escrituras
    # si ya tiene el tag, que solo sobre escriba los parametros pero que no cree una nueva

    for obj in objectsList:
        obj_tags = obj.GetTags() ; cam_tag = None
        if not obj_tags:
            obj.MakeTag(C4DAIN_TAG) # new camera tag
        else:
            obj_tags_types = []
            for tag in obj_tags:
                print tag.GetType()
                obj_tags_types.append(tag.GetType())

            print obj_tags_types
            if not C4DAIN_TAG in obj_tags_types:
                cam_tag = obj.MakeTag(C4DAIN_TAG)

        # cam settings definitions based on each camera type
        if cam_tag[c4d.AITAG_CAMERA_TYPE] is C4DAIN_CYL_CAMERA:           # cyl camera
            CAMERA_SHUTTER_START = C4DAIP_CYL_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_CYL_CAMERA_SHUTTER_END
        elif cam_tag[c4d.AITAG_CAMERA_TYPE] is C4DAIN_FISHEYE_CAMERA:     # fisheye camera
            CAMERA_SHUTTER_START = C4DAIP_FISHEYE_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_FISHEYE_CAMERA_SHUTTER_END
        elif cam_tag[c4d.AITAG_CAMERA_TYPE] is C4DAIN_ORTHO_CAMERA:       # ortho camera
            CAMERA_SHUTTER_START = C4DAIP_ORTHO_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_ORTHO_CAMERA_SHUTTER_END
        elif cam_tag[c4d.AITAG_CAMERA_TYPE] is C4DAIN_SPHERICAL_CAMERA:   # spherical camera
            CAMERA_SHUTTER_START = C4DAIP_SPHERICAL_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_SPHERICAL_CAMERA_SHUTTER_END
        elif cam_tag[c4d.AITAG_CAMERA_TYPE] is C4DAIN_VR_CAMERA:          # vr camera
            CAMERA_SHUTTER_START = C4DAIP_VR_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_VR_CAMERA_SHUTTER_END
        else:                                                             # persp camera
            CAMERA_SHUTTER_START = C4DAIP_PERSP_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_PERSP_CAMERA_SHUTTER_END

        # motion vector settings
        cam_tag[c4d.C4DAI_CAMERA_CUSTOM_SHUTTER]  = True
        cam_tag[CAMERA_SHUTTER_START]             = 0.5
        cam_tag[CAMERA_SHUTTER_END]               = 0.5

    c4d.EventAdd()
    print "finish"

addAiTag()