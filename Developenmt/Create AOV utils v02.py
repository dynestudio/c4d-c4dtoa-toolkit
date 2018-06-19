import c4d
from c4d import gui

""" Pending features:

-Full features per shaders.
-Facing ration IDs
-Add shaders to layers.
-Motion vector motion blur in render settings and camera (custom dialog)
-Custom cryptomattes?
- Default selection on display driver (del primer dialog)
-checkear nombre del aov
-corregir AOVs y funciones de motion vector, cryptomatte y facing ratio
-administrar drivers (display, info y crypto driver)
-Un Do y Re Do
-que los AOV solo se pongan en el info driver
-el wireframe no esta poniendose en quadas
-Cryptomatte se conecta mal

"""

# from api/util/Constants.h
C4DTOA_MSG_TYPE = 1000
C4DTOA_MSG_PARAM1 = 2001
C4DTOA_MSG_PARAM2 = 2002
C4DTOA_MSG_PARAM3 = 2003
C4DTOA_MSG_PARAM4 = 2004
C4DTOA_MSG_RESP1 = 2011
C4DTOA_MSG_ADD_SHADER = 1029
C4DTOA_MSG_ADD_CONNECTION = 1031
C4DTOA_MSG_CONNECT_ROOT_SHADER = 1033

# from c4dtoa_symbols.h
ARNOLD_RENDERER = 1029988
ARNOLD_RENDERER_COMMAND = 1039333
ARNOLD_SHADER_NETWORK = 1033991
ARNOLD_SHADER_GV = 1033990
ARNOLD_REFERENCE_GV = 1035541

# from api/util/ArnolShaderNetworkUtil.h
ARNOLD_BEAUTY_PORT_ID = 537905099
ARNOLD_DISPLACEMENT_PORT_ID = 537905100

# from api/util/NodeIds.h
C4DAIN_STANDARD_SURFACE = 314733630
C4DAIN_NOISE = 268710787
C4DAIN_WIREFRAME = 963864967
C4DAIN_AMBIENT_OCCLUSION = 213691123
C4DAIN_CHECKERBOARD = 1208643042
C4DAIN_MOTION_VECTOR = 973550765

#utility IDs
C4DAIN_UTILITY = 1214045817
C4DAIP_UTILITY_SHADE_MODE  = 1475208304
C4DAIP_UTILITY_COLOR_MODE  = 716698282
C4DAIP_UTILITY_COLOR_MODE__UV = 5
C4DAIP_UTILITY_SHADE_MODE__FLAT = 2

#aov writes IDs
C4DAIN_AOV_WRITE_FLOAT = 878744470
C4DAIN_AOV_WRITE_INT = 1243149505
C4DAIN_AOV_WRITE_RGB = 1243139953

C4DAIN_AOV_WRITE_RGB_AOV_NAME = 1961385827
C4DAIN_AOV_WRITE_RGB_AOV_INPUT = 295764338


C4DAIN_AOV_WRITE_FLOAT_AOV_NAME = 1578967454
C4DAIN_AOV_WRITE_FLOAT_AOV_INPUT = 560859917

# from res/description/ainode_standard_surface.h
C4DAIP_STANDARD_SURFACE_BASE_COLOR = 1044225467
C4DAIP_STANDARD_SURFACE_SPECULAR = 1046994997
C4DAIP_STANDARD_SURFACE_SPECULAR_COLOR = 801517079

# from res/description/ainode_noise.h
C4DAIP_NOISE_OCTAVES = 35478650
C4DAIP_NOISE_DISTORTION = 1840107712

C4DAIP_OPTIONS_AOV_SHADERS = 2113089010

# drivers and AOVs IDs
ARNOLD_DRIVER = 1030141
ARNOLD_AOV = 1030369
C4DAIN_CRYPTOMATTE = 1563242911
C4DAIN_DRIVER_C4D_DISPLAY = 1927516736
C4DAIN_DRIVER_EXR = 9504161

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
C4DAIP_CHECKERBOARD_U_FREQUENCY                    = 2092366454
C4DAIP_CHECKERBOARD_V_FREQUENCY                    = 34844599

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

def getArnoldRenderSettings():
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
    arnoldRenderSettings = getArnoldRenderSettings()
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

    dialog = dlg.findCName ; pdialog = dlg.findPName

    if pdialog == IDC_POINTSOP01:
        pdialog = True
    else:
        pdialog = False

    print dialog
    print pdialog

    shaders_AOVs_names = ['UV', 'Wireframe', 'AO', 'Crypto', 'Fresnel', 'Motion Vector', 'Checkerboard']

    if dialog == IDC_AOV_00:
        shader_AOV_name = shaders_AOVs_names[0] ; shader = C4DAIN_UTILITY           ; AOV_type = 'RGB'
    elif dialog == IDC_AOV_01:
        shader_AOV_name = shaders_AOVs_names[1] ; shader = C4DAIN_WIREFRAME         ; AOV_type = 'Float'
    elif dialog == IDC_AOV_02:
        shader_AOV_name = shaders_AOVs_names[2] ; shader = C4DAIN_AMBIENT_OCCLUSION ; AOV_type = 'Float'
    elif dialog == IDC_AOV_03:
        shader_AOV_name = shaders_AOVs_names[3] ; shader = C4DAIN_CRYPTOMATTE       ; AOV_type = 'Crypto'
    elif dialog == IDC_AOV_04:
        shader_AOV_name = shaders_AOVs_names[4] ; shader = None                     ; AOV_type = 'Float'
    elif dialog == IDC_AOV_05:
        shader_AOV_name = shaders_AOVs_names[5] ; shader = C4DAIN_MOTION_VECTOR     ; AOV_type = 'RGB'
    elif dialog == IDC_AOV_06:
        shader_AOV_name = shaders_AOVs_names[6] ; shader = C4DAIN_CHECKERBOARD      ; AOV_type = 'Float'
    else:
        shader_AOV_name = 'none'

    # create material
    mat = doc.SearchMaterial(shader_AOV_name)
    if mat is None:
        mat = c4d.BaseMaterial(ARNOLD_SHADER_NETWORK)
        if mat is None:
            raise Exception("Failed to create material")
        mat.SetName(shader_AOV_name) ; doc.InsertMaterial(mat) ; mat_exist = False ; # agregar material al layer
    else:
        mat_exist = True

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
        # cryptomatte exceptoin
        if shader_AOV_name is 'Crypto':
            SetRootShader(mat, shader_AOV, ARNOLD_BEAUTY_PORT_ID)
        else:
            # create write AOV shaders
            write_AOV = CreateArnoldShader(mat, C4DAIN_AOV_WRITE_RGB, 150, 100)
            if write_AOV is None:
                raise Exception("Failed to create write_AOV shader")

            # set shader parameters
            write_AOV.SetName("Write_" + shader_AOV_name + "_AOV")
            write_AOV.GetOpContainerInstance().SetString(C4DAIN_AOV_WRITE_RGB_AOV_NAME, shader_AOV_name)

            shader_AOV.SetName(shader_AOV_name + "_AOV")

            # patameters for each AOV shader
            if shader_AOV_name is 'UV':
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_UTILITY_SHADE_MODE, C4DAIP_UTILITY_SHADE_MODE__FLAT)
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_UTILITY_COLOR_MODE, C4DAIP_UTILITY_COLOR_MODE__UV)
            elif shader_AOV_name is 'wireframe':
                shader_AOV.GetOpContainerInstance().SetFloat(C4DAIP_WIREFRAME_LINE_WIDTH, 0.5)
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_WIREFRAME_EDGE_TYPE, 1)
            elif shader_AOV_name is 'AO':
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_AMBIENT_OCCLUSION_SAMPLES, 4)
            elif shader_AOV_name is 'Crypto':
                None
            elif shader_AOV_name is 'fresnel':
                None
            elif shader_AOV_name is 'Motion Vector':
                shader_AOV.GetOpContainerInstance().SetBool(C4DAIP_MOTION_VECTOR_RAW, True)
                shader_AOV.GetOpContainerInstance().SetFloat(C4DAIP_MOTION_VECTOR_MAX_DISPLACE, 64)
            elif shader_AOV_name is 'Checkerboard':
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_CHECKERBOARD_U_FREQUENCY, 5)
                shader_AOV.GetOpContainerInstance().SetInt32(C4DAIP_CHECKERBOARD_V_FREQUENCY, 5)
            else:
                None

            # connect shaders
            SetRootShader(mat, write_AOV, ARNOLD_BEAUTY_PORT_ID)
            AddConnection(mat, shader_AOV, write_AOV, C4DAIN_AOV_WRITE_RGB_AOV_INPUT)
    else:
        None
    
    # motion vectore configurations
    """if shader_AOV_name is 'Motion Vector':
        open question dialog
        mblur_question = c4d.gui.QuestionDialog('do you want to make a camera an render setting for motion blur?')
        if mblur_question is True:
            ejecutar render settings
            ejecturar camera tag
        else:
            None"""


    # redraw
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
   
if __name__=='__main__':
    main()