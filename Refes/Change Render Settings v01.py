import c4d

# arnold ids
ARNOLD_RENDERER                   = 1029988
ARNOLD_RENDERER_COMMAND           = 1039333
ARNOLD_DUMMYFORMAT                = 1035823
ARNOLD_DRIVER                     = 1030141
C4DAIP_DRIVER_EXR_HALF_PRECISION  = 317968755

# render data global ids
renderdata   = doc.GetActiveRenderData()
rdata        = renderdata.GetData()

# get arnold renderer
def GetArnoldRenderSettings(): #thanks to c4dtoa support for this code
    # find the active Arnold render settings
    videopost = renderdata.GetFirstVideoPost()
    while videopost:
        if videopost.GetType() == ARNOLD_RENDERER:
            return videopost;
        videopost = videopost.GetNext()
     
    # create a new one when does not exist
    if videopost is None:
        c4d.CallCommand(ARNOLD_RENDERER_COMMAND)
         
        videopost = rdata.GetFirstVideoPost()
        while videopost:
            if videopost.GetType() == ARNOLD_RENDERER:
                return videopost;
            videopost = videopost.GetNext()

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

    c4d.EventAdd() ; return True

arnold_mblur_rendersettings()