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
C4DAIN_DRIVER_EXR                 = 9504161

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
'''def GetArnoldRenderSettings(): #thanks to c4dtoa support for this code
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
             
    return None'''

# drivers - Turn ON optix in each aov
def main():
    '''# find the Arnold video post data   
    arnoldRenderSettings = GetArnoldRenderSettings()
    if arnoldRenderSettings is None:
        raise BaseException("Failed to find Arnold render settings")'''

    # drivers objects list
    driversList = get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(ARNOLD_DRIVER), [])

    aov_list = []

    # find aovs with Optix setting
    for driver in driversList:
        driver_type = driver[c4d.C4DAI_DRIVER_TYPE]
        driver_variance = driver[c4d.C4DAI_DRIVER_VARIANCE_AOV]

        if driver_type == C4DAIN_DRIVER_EXR:

            if driver_variance == True:

                driver_AOVs = driver.GetChildren()

                for aov in driver_AOVs:
                    aov_name = aov[c4d.ID_BASELIST_NAME]
                    aov_list.append(aov_name)

    aov_delete = ["diffuse_albedo","N","Z"]

    aov_list_tempindex = []

    for i in range(len(aov_list)):
        for e in aov_delete:
            if aov_list[i] == e:
                aov_list_tempindex.append(i)

    i = 0

    for b in aov_list_tempindex:   
        del aov_list[b - i]
        i+=1

    print aov_list

    aov_string_export = ""

    for i in aov_list:
        aov_string_export += i + ", "

    print aov_string_export[:-2]

    #save the txt file


if __name__=='__main__':
    main()