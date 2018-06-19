import c4d , ctypes
from c4d import gui ; from ctypes import *

""" Pending features:

-Custom cryptomattes?
- Default selection on display driver (del primer dialog)
-administrar drivers (display, info y crypto driver)
-Un Do y Re Do
-revisar posicion de shaders cuando se crean.
-Agregar una opcion que agregue todos los AOVs de la lista de dialogo.
-Considerar el write RGBA?
-Half float para los Drivers
- que en el shader de motion vector el Max displace este en 64
- https://support.solidangle.com/display/A5AFCUG/Motion+Vector revisar workflow correcto del mb
- hacer que el add ai tag agregue una camara por si no hay camaras en l escena

"""

# ai constants
C4DTOA_MSG_TYPE = 1000
C4DTOA_MSG_PARAM1 = 2001
C4DTOA_MSG_PARAM2 = 2002
C4DTOA_MSG_PARAM3 = 2003
C4DTOA_MSG_PARAM4 = 2004
C4DTOA_MSG_RESP1 = 2011
C4DTOA_MSG_ADD_SHADER = 1029
C4DTOA_MSG_ADD_CONNECTION = 1031
C4DTOA_MSG_CONNECT_ROOT_SHADER = 1033

#c4dtoa symbols
ARNOLD_RENDERER = 1029988
ARNOLD_RENDERER_COMMAND = 1039333
ARNOLD_SHADER_NETWORK = 1033991
ARNOLD_SHADER_GV = 1033990
ARNOLD_REFERENCE_GV = 1035541

# ASN utils
ARNOLD_BEAUTY_PORT_ID = 537905099
ARNOLD_DISPLACEMENT_PORT_ID = 537905100

# nodes ids
C4DAIN_WIREFRAME = 963864967
C4DAIN_AMBIENT_OCCLUSION = 213691123
C4DAIN_CHECKERBOARD = 1208643042
C4DAIN_MOTION_VECTOR = 973550765

# drivers and AOVs IDs
ARNOLD_DRIVER = 1030141
ARNOLD_AOV = 1030369
C4DAIN_CRYPTOMATTE = 1563242911
C4DAIN_DRIVER_C4D_DISPLAY = 1927516736
C4DAIN_DRIVER_EXR = 9504161

# aov shaders ID
C4DAIP_OPTIONS_AOV_SHADERS = 2113089010

# utility IDs
C4DAIN_UTILITY = 1214045817
C4DAIP_UTILITY_SHADE_MODE  = 1475208304
C4DAIP_UTILITY_COLOR_MODE  = 716698282
C4DAIP_UTILITY_COLOR_MODE__UV = 5
C4DAIP_UTILITY_SHADE_MODE__FLAT = 2

# aov writes IDs
# main nodes ids
C4DAIN_AOV_WRITE_FLOAT = 878744470
C4DAIN_AOV_WRITE_INT = 1243149505
C4DAIN_AOV_WRITE_RGB = 1243139953
# write rgb
C4DAIN_AOV_WRITE_RGB_AOV_NAME = 1961385827
C4DAIN_AOV_WRITE_RGB_AOV_INPUT = 295764338
# write float
C4DAIN_AOV_WRITE_FLOAT_AOV_NAME = 1578967454
C4DAIN_AOV_WRITE_FLOAT_AOV_INPUT = 560859917
# write int
C4DAIN_AOV_WRITE_INT_AOV_NAME = 1432272877
C4DAIN_AOV_WRITE_INT_AOV_INPUT = 25823198

# wireframe node IDs
C4DAIP_WIREFRAME_LINE_WIDTH = 1755341116
C4DAIP_WIREFRAME_EDGE_TYPE = 593776139

# ambient oclussion IDs
C4DAIP_AMBIENT_OCCLUSION_SAMPLES = 811307094

# motion vector IDs
C4DAIP_MOTION_VECTOR_RAW = 1630081403
C4DAIP_MOTION_VECTOR_TIME0 = 1334502790
C4DAIP_MOTION_VECTOR_TIME1 = 1334502789
C4DAIP_MOTION_VECTOR_MAX_DISPLACE = 700796859

# checkerboard IDs
C4DAIP_CHECKERBOARD_U_FREQUENCY  = 2092366454
C4DAIP_CHECKERBOARD_V_FREQUENCY  = 34844599

# facing ratio IDs
C4DAIP_FACING_RATIO_INVERT = 1403163377

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

# render data global ids
renderdata   = doc.GetActiveRenderData()
rdata        = renderdata.GetData()

# gui IDs
IDC_LABELNAME           = 10000
IDC_POINTS              = 10007
IDC_POINTSOP01          = 10008
IDC_POINTSOP02          = 10009

IDC_LIST                = 10002
IDC_AOV_00              = 10003
IDC_AOV_01              = 10004
IDC_AOV_02              = 10005
IDC_AOV_03              = 10006
IDC_AOV_04              = 10007
IDC_AOV_05              = 10008
IDC_AOV_06              = 10009

#--------------------------------------------------------------------------------

class OptionsDialog(gui.GeDialog):

    def CreateLayout(self):
        #title
        self.SetTitle('Create custom AOV')
        #statics text - description UI
        self.AddStaticText(IDC_LABELNAME, c4d.BFH_LEFT, name = 'Which AOV do you want to create?') 
        #radiogroup UI - objects IDs definition
        self.AddRadioGroup(IDC_POINTS, c4d.BFV_SCALEFIT, 2, 1)
        self.AddChild(IDC_POINTS, IDC_POINTSOP01, "display driver")
        self.AddChild(IDC_POINTS, IDC_POINTSOP02, "info and display driver")
        #combo box UI - cryptomatte user input
        self.AddComboBox(IDC_LIST, c4d.BFH_SCALEFIT, initw = 200, inith = 10, specialalign = True)
        self.AddChild(IDC_LIST, IDC_AOV_00, "UV")
        self.AddChild(IDC_LIST, IDC_AOV_01, "Wireframe")
        self.AddChild(IDC_LIST, IDC_AOV_02, "AO")
        self.AddChild(IDC_LIST, IDC_AOV_03, "Cryptomatte")
        self.AddChild(IDC_LIST, IDC_AOV_04, "Fresnel")
        self.AddChild(IDC_LIST, IDC_AOV_05, "Motion Vector")
        self.AddChild(IDC_LIST, IDC_AOV_06, "Checkerboard")
        # Ok/Cancel buttons
        self.AddDlgGroup(c4d.DLG_OK|c4d.DLG_CANCEL)
        self.ok = False
        return True

    def Command(self, id, msg):

        if id == c4d.IDC_OK:
            self.ok = True
            self.findPName = self.GetInt32(IDC_POINTS)
            self.findCName = self.GetInt32(IDC_LIST)
            self.Close()

        elif id == c4d.IDC_CANCEL:
            self.Close()

        return True

def addLayer(name, layer_color):
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
       layer_settings = {'solo': False, 'view': True, 'render': True, 'manager': True, 'locked': False, 'generators': False, 'deformers': False, 'expressions': True, 'animation': True}
       layer.SetLayerData(doc, layer_settings)
       layer.InsertUnder(root)

   else:
       for n, l in layers:
           if n ==name:
               layer=l
               break
   return layer

def addTexTag(obj, layer, mat):
    textag = c4d.TextureTag()
    textag.SetMaterial(mat)
    textag[c4d.ID_BASELIST_NAME] = mat[c4d.ID_BASELIST_NAME]
    textag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
    textag[c4d.ID_LAYER_LINK] = layer
    obj.InsertTag(textag)
    return textag

def addAOV_null (name, layer, mat):
    null = doc.SearchObject(name)
    if not null:
        null = c4d.BaseObject(c4d.Onull)
        null[c4d.ID_BASELIST_NAME] = name
        null[c4d.ID_LAYER_LINK] = layer
        null[c4d.NULLOBJECT_DISPLAY] = 14
        doc.InsertObject(null)

    # add the material tag and avoid material tag repetitions
    null_tags = null.GetTags()
    if not null_tags:
        addTexTag(null, layer, mat)
    else:
        null_tags_names = []
        for tag in null_tags:
            null_tags_names.append(tag[c4d.ID_BASELIST_NAME])
        if not mat[c4d.ID_BASELIST_NAME] in null_tags_names:
            addTexTag(null, layer, mat)
        else:
            None

    # move null in the object manager
    parent = doc.SearchObject(layer[c4d.ID_BASELIST_NAME])
    if not parent:
        objectsList = doc.GetObjects() ; firstObj = doc.GetFirstObject() ; lastObj = objectsList[-1]
        if not lastObj == null:
            null.InsertAfter(lastObj)
    else:
        null.InsertUnder(parent)

    return null

def get_all_objects(op, filter, output):  #get all objects from each type
    while op:
        if filter(op):
            output.append(op)
        get_all_objects(op.GetDown(), filter, output)
        op = op.GetNext()
    return output

def hashid(name):
    if name is None: return 0
     
    h = 5381
    for c in name:
        h = (h << 5) + h + ord(c)
    h = ctypes.c_int32(h).value
    if h < 0: h = -h
    return h

def GetArnoldRenderSettings():
    rdata = doc.GetActiveRenderData()
    videopost = rdata.GetFirstVideoPost()
    while videopost:
        if videopost.GetType() == ARNOLD_RENDERER:
            return videopost;
        videopost = videopost.GetNext()
    
    if videopost is None:
        c4d.CallCommand(ARNOLD_RENDERER_COMMAND)
        
        videopost = rdata.GetFirstVideoPost()
        while videopost:
            if videopost.GetType() == ARNOLD_RENDERER:
                return videopost;
            videopost = videopost.GetNext()
            
    return None

def arnold_mblur_rendersettings():
    # find the Arnold video post data   
    arnoldRenderSettings = GetArnoldRenderSettings()
    if arnoldRenderSettings is None:
        raise BaseException("Failed to find Arnold render settings") ; return False
     
    # setup the settings
    arnoldRenderSettings[c4d.C4DAI_OPTIONS_ENABLE_MOTION_BLUR]     = True
    arnoldRenderSettings[c4d.C4DAI_OPTIONS_ENABLE_MB_DEFORMATION]  = True
    arnoldRenderSettings[c4d.C4DAI_OPTIONS_ENABLE_MB_CAMERA]       = True
    arnoldRenderSettings[c4d.C4DAI_OPTIONS_MB_STEPS]               = 2
    arnoldRenderSettings[c4d.C4DAI_OPTIONS_MB_SHUTTER_POSITION]    = 1
    arnoldRenderSettings[c4d.C4DAI_OPTIONS_MB_SHUTTER_SIZE]        = 0.5

    return True

def addDriver(driver_name, driver_type):
    driver = doc.SearchObject(driver_name)
    if driver is None:
        driver = c4d.BaseObject(ARNOLD_DRIVER)
        driver.SetName(driver_name)
        driver[c4d.C4DAI_DRIVER_TYPE] = driver_type
        driver[c4d.C4DAI_DRIVER_MERGE_AOVS] = True
        doc.InsertObject(driver)
        # delete the BEauty AOV
        if not driver_name == "<display driver>" and "Crypto":
            beauty_aov = driver.GetDown()
            beauty_aov.Remove()
    return driver

def addAov(driver, aovName):
    # skip when the aov is already added
    aov = driver.GetDown()
    while aov:
        if aov.GetName() == aovName:
            return;
        aov = aov.GetNext()
        
    # create the aov
    aov = c4d.BaseObject(ARNOLD_AOV)
    aov.SetName(aovName)
    aov.InsertUnderLast(driver)   

def addAiTag():
    camerasList = get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(c4d.Ocamera), []) # get all cameras from the scene

    for obj in camerasList:
        obj_tags = obj.GetTags()
        if not obj_tags:
            cam_tag = obj.MakeTag(C4DAIN_TAG) # new camera tag
        else:
            obj_tags_types = []
            for tag in obj_tags:
                obj_tags_types.append(tag.GetType())
                if tag.GetType() == C4DAIN_TAG:
                    cam_tag = tag

            if not C4DAIN_TAG in obj_tags_types:
                cam_tag = obj.MakeTag(C4DAIN_TAG)

        if cam_tag[c4d.AITAG_CAMERA_USE_TYPE] == False:
            cam_tag[c4d.AITAG_CAMERA_USE_TYPE] = True ; cam_tag[c4d.AITAG_CAMERA_TYPE] = C4DAIN_PERSP_CAMERA

        # cam settings definitions based on each camera type
        if cam_tag[c4d.AITAG_CAMERA_TYPE] == C4DAIN_CYL_CAMERA:           # cyl camera
            CAMERA_SHUTTER_START = C4DAIP_CYL_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_CYL_CAMERA_SHUTTER_END
        elif cam_tag[c4d.AITAG_CAMERA_TYPE] == C4DAIN_FISHEYE_CAMERA:     # fisheye camera
            CAMERA_SHUTTER_START = C4DAIP_FISHEYE_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_FISHEYE_CAMERA_SHUTTER_END
        elif cam_tag[c4d.AITAG_CAMERA_TYPE] == C4DAIN_ORTHO_CAMERA:       # ortho camera
            CAMERA_SHUTTER_START = C4DAIP_ORTHO_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_ORTHO_CAMERA_SHUTTER_END
        elif cam_tag[c4d.AITAG_CAMERA_TYPE] == C4DAIN_SPHERICAL_CAMERA:   # spherical camera
            CAMERA_SHUTTER_START = C4DAIP_SPHERICAL_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_SPHERICAL_CAMERA_SHUTTER_END
        elif cam_tag[c4d.AITAG_CAMERA_TYPE] == C4DAIN_VR_CAMERA:          # vr camera
            CAMERA_SHUTTER_START = C4DAIP_VR_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_VR_CAMERA_SHUTTER_END
        else:                                                             # persp camera
            CAMERA_SHUTTER_START = C4DAIP_PERSP_CAMERA_SHUTTER_START ; CAMERA_SHUTTER_END = C4DAIP_PERSP_CAMERA_SHUTTER_END

        # motion vector settings
        cam_tag[c4d.C4DAI_CAMERA_CUSTOM_SHUTTER]  = True
        cam_tag[CAMERA_SHUTTER_START]             = 0.5
        cam_tag[CAMERA_SHUTTER_END]               = 0.5

    return cam_tag

def CreateArnoldShader(material, nodeId, posx, posy):
    msg = c4d.BaseContainer()
    msg.SetInt32(C4DTOA_MSG_TYPE, C4DTOA_MSG_ADD_SHADER)
    msg.SetInt32(C4DTOA_MSG_PARAM1, ARNOLD_SHADER_GV)
    msg.SetInt32(C4DTOA_MSG_PARAM2, nodeId)
    msg.SetInt32(C4DTOA_MSG_PARAM3, posx)
    msg.SetInt32(C4DTOA_MSG_PARAM4, posy)
    material.Message(c4d.MSG_BASECONTAINER, msg)
    return msg.GetLink(C4DTOA_MSG_RESP1)

def CreateReference(material, ref, posx, posy):
    msg = c4d.BaseContainer()
    msg.SetInt32(C4DTOA_MSG_TYPE, C4DTOA_MSG_ADD_SHADER)
    msg.SetInt32(C4DTOA_MSG_PARAM1, ARNOLD_REFERENCE_GV)
    msg.SetLink(C4DTOA_MSG_PARAM2, ref)
    msg.SetInt32(C4DTOA_MSG_PARAM3, posx)
    msg.SetInt32(C4DTOA_MSG_PARAM4, posy)
    material.Message(c4d.MSG_BASECONTAINER, msg)
    return msg.GetLink(C4DTOA_MSG_RESP1)

def AddConnection(material, srcNode, dstNode, dstPortId):
    msg = c4d.BaseContainer()
    msg.SetInt32(C4DTOA_MSG_TYPE, C4DTOA_MSG_ADD_CONNECTION)
    msg.SetLink(C4DTOA_MSG_PARAM1, srcNode)
    msg.SetInt32(C4DTOA_MSG_PARAM2, 0)
    msg.SetLink(C4DTOA_MSG_PARAM3, dstNode)
    msg.SetInt32(C4DTOA_MSG_PARAM4, dstPortId)
    material.Message(c4d.MSG_BASECONTAINER, msg)
    return msg.GetBool(C4DTOA_MSG_RESP1)

def SetRootShader(material, shader, rootPortId):
    msg = c4d.BaseContainer()
    msg.SetInt32(C4DTOA_MSG_TYPE, C4DTOA_MSG_CONNECT_ROOT_SHADER)
    msg.SetLink(C4DTOA_MSG_PARAM1, shader)
    msg.SetInt32(C4DTOA_MSG_PARAM2, 0)
    msg.SetInt32(C4DTOA_MSG_PARAM3, rootPortId)
    material.Message(c4d.MSG_BASECONTAINER, msg)
    return msg.GetBool(C4DTOA_MSG_RESP1)

def addAov(driver, aovName):
    # skip when the aov is already added
    aov = driver.GetDown()
    while aov:
        if aov.GetName() == aovName:
            return;
        aov = aov.GetNext()
        
    # create the aov
    aov = c4d.BaseObject(ARNOLD_AOV)
    aov.SetName(aovName)
    aov.InsertUnderLast(driver)  
   
def main():
    # find the Arnold video post data    
    arnoldRenderSettings = GetArnoldRenderSettings()
    if arnoldRenderSettings is None:
        raise BaseException("Failed to find Arnold render settings")

    # set Arnold as the active render engine
    rdata = doc.GetActiveRenderData()
    rdata[c4d.RDATA_RENDERENGINE] = ARNOLD_RENDERER

    # Open the options dialog to let users choose their options.
    dlg = OptionsDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw = 300, defaulth = 50)
    if not dlg.ok:
        return

    # AOV shaders dialog excecution
    dialog = dlg.findCName ; pdialog = dlg.findPName
    if pdialog == IDC_POINTSOP01:
        pdialog = True
    else:
        pdialog = False

    # facing ratio - get ID
    C4DAIN_FACING_RATIO = hashid('facing_ratio')

    # main AOVs IDs
    shaders_AOVs_names = ['UV', 'Wireframe', 'AO', 'Crypto', 'Fresnel', 'mblur', 'Checkerboard'] ; AOV_types = ['RGB', 'Float', 'Int', 'RGBA']

    # main definitions for shaders, materials and AOVs
    if dialog == IDC_AOV_00:
        shader_AOV_name = shaders_AOVs_names[0] ; shader = C4DAIN_UTILITY           ; AOV_type = AOV_types[0] # RGB
    elif dialog == IDC_AOV_01:
        shader_AOV_name = shaders_AOVs_names[1] ; shader = C4DAIN_WIREFRAME         ; AOV_type = AOV_types[2] # int
    elif dialog == IDC_AOV_02:
        shader_AOV_name = shaders_AOVs_names[2] ; shader = C4DAIN_AMBIENT_OCCLUSION ; AOV_type = AOV_types[1] # float
    elif dialog == IDC_AOV_03:
        shader_AOV_name = shaders_AOVs_names[3] ; shader = C4DAIN_CRYPTOMATTE       ; AOV_type = AOV_types[0] # RGB
    elif dialog == IDC_AOV_04:
        shader_AOV_name = shaders_AOVs_names[4] ; shader = C4DAIN_FACING_RATIO      ; AOV_type = AOV_types[1] # float
    elif dialog == IDC_AOV_05:
        shader_AOV_name = shaders_AOVs_names[5] ; shader = C4DAIN_MOTION_VECTOR     ; AOV_type = AOV_types[0] # RGB
    elif dialog == IDC_AOV_06:
        shader_AOV_name = shaders_AOVs_names[6] ; shader = C4DAIN_CHECKERBOARD      ; AOV_type = AOV_types[1] # float
    else:
        shader_AOV_name = 'none'

    # create material
    mat = doc.SearchMaterial(shader_AOV_name)
    if mat is None:
        mat = c4d.BaseMaterial(ARNOLD_SHADER_NETWORK)
        if mat is None:
            raise Exception("Failed to create material")
        mat.SetName(shader_AOV_name) ; doc.InsertMaterial(mat) ; mat_exist = False
        mat[c4d.ID_LAYER_LINK] = addLayer('AOV Shaders', c4d.Vector(1,0.5,0.5)) ; # agregar material al layer
    else:
        mat_exist = True

    # create AOV shaders null
    addAOV_null('AOV shaders', addLayer('_Arnold Drivers_', c4d.Vector(0.8,0.2,0.4)), mat)

    # add the shader to the AOV shader list
    aovShaders = arnoldRenderSettings.GetData().GetData(C4DAIP_OPTIONS_AOV_SHADERS)
    isMaterialAdded = False
    for i in range(0,aovShaders.GetObjectCount()):
        if aovShaders.ObjectFromIndex(doc, i) == mat:
            isMaterialAdded = True
            break
    if isMaterialAdded is False:
        aovShaders.InsertObject(mat, 0)
        arnoldRenderSettings[C4DAIP_OPTIONS_AOV_SHADERS] = aovShaders

    # drivers operations
    displayDriver = addDriver("<display driver>", C4DAIN_DRIVER_C4D_DISPLAY)

    if shader_AOV_name is 'Crypto':
        if displayDriver:
            addAov(displayDriver, "crypto_asset")
            addAov(displayDriver, "crypto_object")
            addAov(displayDriver, "crypto_material")

        cryptoDriver = addDriver("Crypto", C4DAIN_DRIVER_EXR)

        if cryptoDriver:
            addAov(cryptoDriver, "crypto_asset")
            addAov(cryptoDriver, "crypto_object")
            addAov(cryptoDriver, "crypto_material")
    else:
        if displayDriver:
            addAov(displayDriver, shader_AOV_name)

    # extra info driver
    if not pdialog:
        if not shader_AOV_name == 'Crypto':
            exrDriver = addDriver("info", C4DAIN_DRIVER_EXR)
            if exrDriver:
                addAov(exrDriver, shader_AOV_name)

    # shaders operations
    if not mat_exist:
        # create main shaders
        shader_AOV = CreateArnoldShader(mat, shader, 0, 50)
        if shader_AOV is None:
            raise Exception("Failed to create shader_AOV shader")

        # cryptomatte exception
        if shader_AOV_name is 'Crypto':
            SetRootShader(mat, shader_AOV, ARNOLD_BEAUTY_PORT_ID)
        else:
            # get write shader type
            if AOV_type is AOV_types[1]: # float
                wirte_shader_type = C4DAIN_AOV_WRITE_FLOAT
                wirte_shader_input = C4DAIN_AOV_WRITE_FLOAT_AOV_INPUT
                write_shader_AOVname = C4DAIN_AOV_WRITE_FLOAT_AOV_NAME
            elif AOV_type is AOV_types[2]: # int
                wirte_shader_type = C4DAIN_AOV_WRITE_INT
                wirte_shader_input = C4DAIN_AOV_WRITE_INT_AOV_INPUT
                write_shader_AOVname = C4DAIN_AOV_WRITE_INT_AOV_NAME
            else:                          # RGB
                wirte_shader_type = C4DAIN_AOV_WRITE_RGB
                wirte_shader_input = C4DAIN_AOV_WRITE_RGB_AOV_INPUT
                write_shader_AOVname = C4DAIN_AOV_WRITE_RGB_AOV_NAME

            # create write AOV shaders
            write_shader = CreateArnoldShader(mat, wirte_shader_type, 150, 100)
            if write_shader is None:
                raise Exception("Failed to create write_AOV shader")

            # set shader parameters
            write_shader.SetName("Write_" + shader_AOV_name + "_AOV")
            write_shader.GetOpContainerInstance().SetString(write_shader_AOVname, shader_AOV_name)

            # set shader name
            shader_AOV.SetName(shader_AOV_name + "_AOV")

            # patameters for each AOV shader
            if shader_AOV_name is shaders_AOVs_names[0]: # UV
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_UTILITY_SHADE_MODE, C4DAIP_UTILITY_SHADE_MODE__FLAT)
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_UTILITY_COLOR_MODE, C4DAIP_UTILITY_COLOR_MODE__UV)
            elif shader_AOV_name is shaders_AOVs_names[1]: # wireframe
                shader_AOV.GetOpContainerInstance().SetFloat(C4DAIP_WIREFRAME_LINE_WIDTH, 0.75)
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_WIREFRAME_EDGE_TYPE, 1)
            elif shader_AOV_name is shaders_AOVs_names[2]: # AO
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_AMBIENT_OCCLUSION_SAMPLES, 4)
            elif shader_AOV_name is shaders_AOVs_names[3]: # crypto
                None
            elif shader_AOV_name is shaders_AOVs_names[4]: # fresnel
                shader_AOV.GetOpContainerInstance().SetBool(C4DAIP_FACING_RATIO_INVERT, True)
            elif shader_AOV_name is shaders_AOVs_names[5]: # motion vector
                shader_AOV.GetOpContainerInstance().SetBool(C4DAIP_MOTION_VECTOR_RAW, True)
                shader_AOV.GetOpContainerInstance().SetFloat(C4DAIP_MOTION_VECTOR_MAX_DISPLACE, 0)
            elif shader_AOV_name is shaders_AOVs_names[6]: # checkerboard
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_CHECKERBOARD_U_FREQUENCY, 5)
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_CHECKERBOARD_V_FREQUENCY, 5)
            else:
                None

            # connect shaders
            SetRootShader(mat, write_shader, ARNOLD_BEAUTY_PORT_ID)
            AddConnection(mat, shader_AOV, write_shader, wirte_shader_input)

    else:
        None
    
    # motion vector additional settings
    if shader_AOV_name is shaders_AOVs_names[5]: # motion vector
        mblur_question = c4d.gui.QuestionDialog('do you want to make a camera an render setting for motion blur?')
        if mblur_question is True:
            arnold_mblur_rendersettings()
            addAiTag()
            aovs = get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(ARNOLD_AOV), []) # get all cameras from the scene
            for aov in aovs:
                if aov[c4d.ID_BASELIST_NAME] == 'mblur':
                    aov[c4d.C4DAI_AOV_DATATYPE] = 7 # vector AOV
                else:
                    None
        else:
            None

    # redraw
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
   
if __name__=='__main__':
    main()