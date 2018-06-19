"""
Crypto Custom Data - Script v0.7
Thanks for download - for commercial and personal uses.
Crypto Custom Data granted shall not be copied, distributed, or-sold, offered for resale, transferred in whole or in part except that you may make one copy for archive purposes only.

Some parts of this script are from Solid Angle support website (get render setting, set driver, set aov, and shader ops).

dyne.studio
Writen by: Carlos Dordelly

Version: 0.7 wip01
Date start: 07/apr/2018
Date version: 15/apr/2018
Date end: --
Written and tested in Cinema 4D R19 / R18 / R17 / R16 - Maybe works in older versions.

Crypto Custom Data - Script v0.7 belongs to Dyne Tools (group of digital tools from dyne).

"""

import c4d
from c4d import gui

# dialog ids
IDC_LABELNAME           = 10000
IDC_EDITNAME            = 10001
IDC_LIST                = 10002
IDC_CRYPTOUSERINPUT_00  = 10003
IDC_CRYPTOUSERINPUT_01  = 10004
IDC_CRYPTOUSERINPUT_02  = 10005
IDC_CRYPTOUSERINPUT_03  = 10006
IDC_IDS                 = 10007
IDC_IDS_OP01            = 10008
IDC_IDS_OP02            = 10009

# c4dtoa ids
ARNOLD_RENDERER            = 1029988
ARNOLD_RENDERER_COMMAND    = 1039333
ARNOLD_SHADER_NETWORK      = 1033991
ARNOLD_SHADER_GV           = 1033990
ARNOLD_BEAUTY_PORT_ID      = 537905099
ARNOLD_DRIVER              = 1030141
ARNOLD_AOV                 = 1030369
C4DAIN_CRYPTOMATTE         = 1563242911
C4DAIN_DRIVER_C4D_DISPLAY  = 1927516736
C4DAIN_DRIVER_EXR          = 9504161

C4DTOA_MSG_TYPE                 = 1000
C4DTOA_MSG_PARAM1               = 2001
C4DTOA_MSG_PARAM2               = 2002
C4DTOA_MSG_PARAM3               = 2003
C4DTOA_MSG_PARAM4               = 2004
C4DTOA_MSG_RESP1                = 2011
C4DTOA_MSG_RESP3                = 2013
C4DTOA_MSG_ADD_SHADER           = 1029
C4DTOA_MSG_CONNECT_ROOT_SHADER  = 1033

C4DAIP_OPTIONS_AOV_SHADERS       = 2113089010
C4DTOA_MSG_QUERY_SHADER_NETWORK  = 1028

CRYPTO_0_AOV       = 340467198
CRYPTO_0_UserData  = 319033500
CRYPTO_1_AOV       = 340467197
CRYPTO_1_UserData  = 319033499
CRYPTO_2_AOV       = 340467196
CRYPTO_2_UserData  = 319033498
CRYPTO_3_AOV       = 340467195
CRYPTO_3_UserData  = 319033497

# user input dialog elements
class OptionsDialog(gui.GeDialog):

    def CreateLayout(self):
        # title
        self.SetTitle('Crypto User AOV')
        # statics text - description UI
        self.AddStaticText(IDC_LABELNAME, c4d.BFH_LEFT, name = 'Which Cryptomatte user input are you going to use?') 
        # radiogroup UI - objects IDs definition
        self.AddRadioGroup(IDC_IDS, c4d.BFV_SCALEFIT, 2, 1)
        self.AddChild(IDC_IDS, IDC_IDS_OP01, "Different IDs")
        self.AddChild(IDC_IDS, IDC_IDS_OP02, "Same ID")
        # combo box UI - cryptomatte user input
        self.AddComboBox(IDC_LIST, c4d.BFH_SCALEFIT, initw = 200, inith = 10, specialalign = True)
        self.AddChild(IDC_LIST, IDC_CRYPTOUSERINPUT_00, "input 0")
        self.AddChild(IDC_LIST, IDC_CRYPTOUSERINPUT_01, "input 1")
        self.AddChild(IDC_LIST, IDC_CRYPTOUSERINPUT_02, "input 2")
        self.AddChild(IDC_LIST, IDC_CRYPTOUSERINPUT_03, "input 3")
        # Ok/Cancel buttons
        self.AddDlgGroup(c4d.DLG_OK|c4d.DLG_CANCEL)
        self.ok = False
        return True

    def Command(self, id, msg):

        if id == c4d.IDC_OK:
            self.ok = True
            self.findPName = self.GetInt32(IDC_IDS)
            self.findCName = self.GetInt32(IDC_LIST)
            self.Close()

        elif id == c4d.IDC_CANCEL:
            self.Close()
            gui.MessageDialog('Please select a user Cryptomatte input user data.')

        return True

def cryptoinput_dialog():
    # Open the options dialog to let users choose their options.
    dlg = OptionsDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
    if not dlg.ok:
        return False

    # returned user option int
    user_input = dlg.findCName
    ID_input  = dlg.findPName

    if ID_input == IDC_IDS_OP01:
        ID_input = True
    else:
        ID_input = False

    if user_input == IDC_CRYPTOUSERINPUT_00:
        Crypto_AOV = CRYPTO_0_AOV
        Crypto_UData = CRYPTO_0_UserData
        Crypto_UData_string = "CryptoCustom_0"
        Crypto_UAOV_string = "User_Crypto0"
    elif user_input == IDC_CRYPTOUSERINPUT_01:
        Crypto_AOV = CRYPTO_1_AOV
        Crypto_UData = CRYPTO_1_UserData
        Crypto_UData_string = "CryptoCustom_1"
        Crypto_UAOV_string = "User_Crypto1"
    elif user_input == IDC_CRYPTOUSERINPUT_02:
        Crypto_AOV = CRYPTO_2_AOV
        Crypto_UData = CRYPTO_2_UserData
        Crypto_UData_string = "CryptoCustom_2"
        Crypto_UAOV_string = "User_Crypto2"
    elif user_input == IDC_CRYPTOUSERINPUT_03:
        Crypto_AOV = CRYPTO_3_AOV
        Crypto_UData = CRYPTO_3_UserData
        Crypto_UData_string = "CryptoCustom_3"
        Crypto_UAOV_string = "User_Crypto3"
    else:
        gui.MessageDialog('Please select one input.')
        return False

    cryptoinput_list = [Crypto_AOV, Crypto_UData, Crypto_UData_string, Crypto_UAOV_string, ID_input]

    return cryptoinput_list

# c4dtoa ops
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

def createArnoldShader(material, nodeId, posx, posy):
    msg = c4d.BaseContainer()
    msg.SetInt32(C4DTOA_MSG_TYPE, C4DTOA_MSG_ADD_SHADER)
    msg.SetInt32(C4DTOA_MSG_PARAM1, ARNOLD_SHADER_GV)
    msg.SetInt32(C4DTOA_MSG_PARAM2, nodeId)
    msg.SetInt32(C4DTOA_MSG_PARAM3, posx)
    msg.SetInt32(C4DTOA_MSG_PARAM4, posy)
    material.Message(c4d.MSG_BASECONTAINER, msg)
    return msg.GetLink(C4DTOA_MSG_RESP1)

def setRootShader(material, shader, rootPortId):
    msg = c4d.BaseContainer()
    msg.SetInt32(C4DTOA_MSG_TYPE, C4DTOA_MSG_CONNECT_ROOT_SHADER)
    msg.SetLink(C4DTOA_MSG_PARAM1, shader)
    msg.SetInt32(C4DTOA_MSG_PARAM2, 0)
    msg.SetInt32(C4DTOA_MSG_PARAM3, rootPortId)
    material.Message(c4d.MSG_BASECONTAINER, msg)
    return msg.GetBool(C4DTOA_MSG_RESP1)
  
def createCryptomatteShader(aovName):
    # create material
    mat = c4d.BaseMaterial(ARNOLD_SHADER_NETWORK)
    if mat is None:
        raise Exception("Failed to create material")
    mat.SetName("cryptomatte")
    doc.InsertMaterial(mat)

    # create shaders
    shader = createArnoldShader(mat, C4DAIN_CRYPTOMATTE, 150, 100)
    if shader is None:
        raise Exception("Failed to create the cryptomatte shader")

    # set shader parameters
    shader.SetName("cryptomatte")
    shader[aovName[0]] = aovName[3] #crypto aov
    shader[aovName[1]] = aovName[2] #crypto user data
   
    # connect shaders
    setRootShader(mat, shader, ARNOLD_BEAUTY_PORT_ID)
    
    return mat;

def modifyCryptomatteSahder(material, aovName):   
    # query the network
    msg = c4d.BaseContainer()
    msg.SetInt32(C4DTOA_MSG_TYPE, C4DTOA_MSG_QUERY_SHADER_NETWORK)
    material.Message(c4d.MSG_BASECONTAINER, msg)
    
    # modify parameter
    shader = msg.GetLink(C4DTOA_MSG_RESP3)
    shader[aovName[0]] = aovName[3] #crypto aov
    shader[aovName[1]] = aovName[2] #crypto user data

    return material

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
    
def arnold_ops(aovName):
    # find the Arnold video post data    
    arnoldRenderSettings = getArnoldRenderSettings()
    if arnoldRenderSettings is None:
        raise BaseException("Failed to find Arnold render settings")

    # set Arnold as the active render engine
    rdata = doc.GetActiveRenderData()
    rdata[c4d.RDATA_RENDERENGINE] = 1029988

    # create or modify the cryptomatte shader
    material = doc.SearchMaterial("cryptomatte")

    if material is None:
        material = createCryptomatteShader(aovName)
    else:
        material = modifyCryptomatteSahder(material, aovName)
    
    # add the shader to the AOV shader list
    aovShaders = arnoldRenderSettings.GetData().GetData(C4DAIP_OPTIONS_AOV_SHADERS)
    isMaterialAdded = False
    for i in range(0,aovShaders.GetObjectCount()):
        if aovShaders.ObjectFromIndex(doc, i) == material:
            isMaterialAdded = True
            break
    if isMaterialAdded is False:
        aovShaders.InsertObject(material, 0)
        arnoldRenderSettings[C4DAIP_OPTIONS_AOV_SHADERS] = aovShaders
    
    # create an EXR driver
    exrDriver = doc.SearchObject("crypto")
    if exrDriver is None:
        exrDriver = c4d.BaseObject(ARNOLD_DRIVER)
        exrDriver.SetName("crypto")
        exrDriver[c4d.C4DAI_DRIVER_TYPE] = C4DAIN_DRIVER_EXR
        exrDriver[c4d.C4DAI_DRIVER_MERGE_AOVS] = True
        doc.InsertObject(exrDriver)

    # create the display driver
    displayDriver = doc.SearchObject("<display driver>")
    if displayDriver is None:
        displayDriver = c4d.BaseObject(ARNOLD_DRIVER)
        displayDriver.SetName("<display driver>")
        displayDriver[c4d.C4DAI_DRIVER_TYPE] = C4DAIN_DRIVER_C4D_DISPLAY
        doc.InsertObject(displayDriver)
            
    # add the cryptomatte AOVs to the drivers
    addAov(displayDriver, aovName[3])

    addAov(exrDriver, aovName[3])
        
    # update the scene
    c4d.EventAdd()

def main():
    # get Active Objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.')
        return

    # user input dialog
    cryptoinput_dlg = cryptoinput_dialog()
    if cryptoinput_dlg == False:
        return

    # list iterator
    i = 0

    for obj in activeObjects:
        if cryptoinput_dlg[4] == True:
            i +=1
        else:
            i = 0

        userdata = obj.GetUserDataContainer()

        # skip when the user data is already added
        skip = False
        for id, bc in obj.GetUserDataContainer():
            if bc[c4d.DESC_NAME] == cryptoinput_dlg[2]:
                skip = True
                break

        # add the new user data
        if skip is False:
           bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_STRING)
           bc[c4d.DESC_NAME] = cryptoinput_dlg[2]
           element2 = obj.AddUserData(bc)
           obj[element2] = "Obj 0" + str(i) 
        else:
           gui.MessageDialog('User data %s already exists on object %s.' % (cryptoinput_dlg[2], obj.GetName()))

    c4d.EventAdd()

    arnold_ops(cryptoinput_dlg)

if __name__=='__main__':
 main()