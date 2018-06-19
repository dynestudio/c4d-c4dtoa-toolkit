"""
Set LQ Render Setting - C4D script v0.1 wip 01
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

Set LQ Render Setting belongs to C4DtoA Script Tools and Dyne Tools (group of digital tools from dyne).

"""

import c4d
from c4d import gui

# arnold ids
ARNOLD_RENDERER                         = 1029988

#samples ids
C4DAIP_OPTIONS_AA_SAMPLES               = 554323531
C4DAIP_OPTIONS_GI_DIFFUSE_SAMPLES       = 2117430376
C4DAIP_OPTIONS_GI_SPECULAR_SAMPLES      = 291620449
C4DAIP_OPTIONS_GI_TRANSMISSION_SAMPLES  = 70867916
C4DAIP_OPTIONS_GI_SSS_SAMPLES           = 608868475
C4DAIP_OPTIONS_GI_VOLUME_SAMPLES        = 1154793606

# ray depths ids
C4DAIP_OPTIONS_GI_TOTAL_DEPTH           = 967682138
C4DAIP_OPTIONS_GI_DIFFUSE_DEPTH         = 493072936
C4DAIP_OPTIONS_GI_SPECULAR_DEPTH        = 2005875169
C4DAIP_OPTIONS_GI_TRANSMISSION_DEPTH    = 1843627892
C4DAIP_OPTIONS_GI_VOLUME_DEPTH          = 1706714950 
C4DAIP_OPTIONS_AUTO_TRANSPARENCY_DEPTH  = 1235817797

# other ids
C4DAIP_OPTIONS_DEFAULT_GPU_NAMES  = 1689327486
C4DAIP_OPTIONS_SSS_USE_AUTOBUMP   = 2087879824

# render data global ids
renderdata   = doc.GetActiveRenderData()
rdata        = renderdata.GetData()

# document global ids
doc          = c4d.documents.GetActiveDocument()

# arnold renderer
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
             
    return None

def Set_RenderSetting():
    # find the Arnold video post data   
    arnoldRenderSettings = GetArnoldRenderSettings()
    if arnoldRenderSettings is None:
        raise BaseException("Failed to find Arnold render settings")
     
    # setup the settings
    arnoldRenderSettings[C4DAIP_OPTIONS_AA_SAMPLES]               = 2
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_DIFFUSE_SAMPLES]       = 1
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_SPECULAR_SAMPLES]      = 1
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_TRANSMISSION_SAMPLES]  = 1
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_SSS_SAMPLES]           = 1
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_VOLUME_SAMPLES]        = 1

    # ray depths settings
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_TOTAL_DEPTH]           = 10
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_DIFFUSE_DEPTH]         = 1
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_SPECULAR_DEPTH]        = 1
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_TRANSMISSION_DEPTH]    = 8
    arnoldRenderSettings[C4DAIP_OPTIONS_GI_VOLUME_DEPTH]          = 1
    arnoldRenderSettings[C4DAIP_OPTIONS_AUTO_TRANSPARENCY_DEPTH]  = 10

    # other settings
    arnoldRenderSettings[C4DAIP_OPTIONS_DEFAULT_GPU_NAMES]        = "*"
    arnoldRenderSettings[C4DAIP_OPTIONS_SSS_USE_AUTOBUMP]         = True
    arnoldRenderSettings[c4d.C4DAI_OPTIONS_USE_TX_TEXTURES]       = True
    
    # update the scene
    c4d.EventAdd()

#--------------------------

Set_RenderSetting()
