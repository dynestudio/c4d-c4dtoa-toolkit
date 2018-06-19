"""
Set Optix AOVs - C4D script v0.1 wip 02
Thanks for download - for commercial and personal uses.
Set Optix AOVs granted shall not be copied, distributed, or-sold, offered for resale, transferred in whole or in part except that you may make one copy for archive purposes only.

http://dyne.studio/
Writen by: Carlos Dordelly
Special thanks: Pancho Contreras, Terry Williams & Roberto Gonzalez.

Turn ON Optix Denoiser in each aov from the scene.
Date start: 15/apr/2018
Date version: 15/apr/2018
Date end: --
Written and tested in Cinema 4D R19 / R18 / R17 / R16.

Set Optix AOVS belongs to C4DtoA Script Tools and Dyne Tools (group of digital tools from dyne).

"""

import c4d
from c4d import gui

#global render engines ids
#arnold ids
ARNOLD_RENDERER                   = 1029988
ARNOLD_RENDERER_COMMAND           = 1039333
ARNOLD_DRIVER                     = 1030141

#render data global ids
renderdata   = doc.GetActiveRenderData()
rdata        = renderdata.GetData()

#document global ids
doc          = c4d.documents.GetActiveDocument()

# get all objects with children
def get_all_objects(op, filter, output):
    while op:
        if filter(op):
            output.append(op)
        get_all_objects(op.GetDown(), filter, output)
        op = op.GetNext()
    return output

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
             
    return None

# drivers - Turn ON optix in each aov
def main():
    # find the Arnold video post data   
    arnoldRenderSettings = GetArnoldRenderSettings()
    if arnoldRenderSettings is None:
        raise BaseException("Failed to find Arnold render settings")

    # drivers objects list
    driversList = get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(ARNOLD_DRIVER), [])

    # find aovs with Optix setting
    for driver in driversList:
        driver_name = driver[c4d.ID_BASELIST_NAME]
        print "Driver: " + driver_name + "\n"

        driver_AOVs = driver.GetChildren()

        for aov in driver_AOVs:
            aov_name = aov[c4d.ID_BASELIST_NAME]
            print "AOV: " + aov_name

            aov[c4d.C4DAI_AOV_DENOISE] = True

    c4d.EventAdd()

if __name__=='__main__':
    main()