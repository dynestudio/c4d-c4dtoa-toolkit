"""
Export to Render Farm - C4D script 0.9 wip 09
Thanks for download - for commercial and personal uses.
Export to Render Farm granted shall not be copied, distributed, or-sold, offered for resale, transferred in whole or in part except that you may make one copy for archive purposes only.

http://dyne.studio/
Writen by: Carlos Dordelly
Special thanks: Pancho Contreras, Terry Williams & Roberto Gonzalez.

Export to Render Farm provides a alternative way to collect a c4d file with additional features.
Date start: 05/jun/2018
Date version: 08/apr/2018
Date end: --
Written and tested in Cinema 4D R19 / R18 / R17 / R16.

Export to Render Farm belongs to Dyne Tools (group of digital tools from dyne).

"""

import c4d
from c4d import gui

#global render engines ids
#arnold ids
ARNOLD_RENDERER                   = 1029988
ARNOLD_RENDERER_COMMAND           = 1039333
ARNOLD_DUMMYFORMAT                = 1035823
ARNOLD_DRIVER                     = 1030141
C4DAIP_DRIVER_EXR_HALF_PRECISION  = 317968755

#driver types
C4DAIN_DRIVER_EXR      = 9504161
C4DAIN_DRIVER_DEEPEXR  = 1058716317
C4DAIN_DRIVER_JPEG     = 313466666
C4DAIN_DRIVER_PNG      = 9492523
C4DAIN_DRIVER_TIFF     = 313114887
C4DAIN_DRIVER_DISPLAY  = 1927516736

#drivers file names
C4DAIP_DRIVER_EXR_FILENAME      = 1285755954
C4DAIP_DRIVER_JPEG_FILENAME     = 766183461
C4DAIP_DRIVER_DEEPEXR_FILENAME  = 1429220916
C4DAIP_DRIVER_PNG_FILENAME      = 1807654404
C4DAIP_DRIVER_TIFF_FILENAME     = 1913388456

#octane ids
OCTANE_RENDERER    = 1029525
OCTANE_LIVEPLUGIN  = 1029499

#other render engines ids
REDSHIFT_RENDERER  = 1036219
PRO_RENDERER       = 1037639
PHYSICAL_RENDERER  = 1023342
STANDARD_RENDERER  = 0

#render data global ids
renderdata   = doc.GetActiveRenderData()
rdata        = renderdata.GetData()
Beauty_path  = "./$prj/$prj_Beauty"
MP_path      = "./$prj/$prj_MP"

#document global ids
doc        = c4d.documents.GetActiveDocument()
docname    = doc.GetDocumentName()
docpath    = doc.GetDocumentPath()
docfolder  = docname[:-4]

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

    for driver in driversList:
        driver_name = driver[c4d.ID_BASELIST_NAME]
        print driver_name

        driver_AOVs = driver.GetChildren()

        for aov in driver_AOVs:
            aov_name = aov[c4d.ID_BASELIST_NAME]
            print aov_name

            aov[c4d.C4DAI_AOV_DENOISE] = True

    c4d.EventAdd()

if __name__=='__main__':
    main()