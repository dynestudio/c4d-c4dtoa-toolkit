import c4d
from c4d import gui

ARNOLD_PROCEDURAL = 1032509

class OptionsDialog(gui.GeDialog):

    IDC_LABELNAME = 1000
    IDC_EDITNAME = 1001

    def CreateLayout(self):

        self.SetTitle('Crypto User AOV')

        self.AddStaticText(self.IDC_LABELNAME, c4d.BFH_LEFT, name='Set User Data Name:') 
        self.AddEditText(self.IDC_EDITNAME, c4d.BFH_SCALEFIT)
        self.SetString(self.IDC_EDITNAME, 'Write Crypto User Data AOV')

        # Ok/Cancel buttons
        self.AddDlgGroup(c4d.DLG_OK|c4d.DLG_CANCEL)
        self.ok = False
        return True

    def Command(self, id, msg):

        if id == c4d.IDC_OK:
            self.ok = True
            self.findGName = self.GetString(self.IDC_EDITNAME)
            self.Close()

        elif id == c4d.IDC_CANCEL:
            self.Close()
            gui.MessageDialog('Please select a user Cryptomatte input user data.')

        return True

def get_active_objs(): # get active objects from obj manager
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        return None
    return activeObjects

def main():

    objsList = get_active_objs()
    if objsList == None:
        return

    # Open the string dialog
    """dlg = OptionsDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
    if not dlg.ok:
        return

    procedural_folder = dlg.findGName"""

    mayaProcedural_name = 'ArnoldStandIn'
    procedurals_list = []

    for obj in objsList:
        if mayaProcedural_name in obj[c4d.ID_BASELIST_NAME]:
            procedural_name = obj[c4d.ID_BASELIST_NAME].split(':') ; procedural_name = procedural_name[0]
            # procedural parameters
            procedural = c4d.BaseObject(ARNOLD_PROCEDURAL)
            procedural.SetName(procedural_name)

            # scale unit parameters
            #procedural.GetOpContainerInstance().SetFloat((c4d.C4DAI_PROCEDURAL_SCALE, 0.1)
            #procedural[c4d.C4DAI_PROCEDURAL_SCALE] = 0.1
            #UnitScaleData.SetUnitScale(scale, unit)
            """procedural_scale = procedural[c4d.C4DAI_PROCEDURAL_SCALE]
            print 'checkpoint 01'
            print procedural_scale.GetUnitScale()
            print 'checkpoint 02'
            procedural_scale.SetUnitScale(0.1, c4d.DOCUMENT_UNIT_CM)
            print procedural_scale
            print 'checkpoint 03"""

            procedural[c4d.ID_BASEOBJECT_REL_SCALE] = c4d.Vector(0.01,0.01,0.01)
            procedural[c4d.C4DAI_PROCEDURAL_OBJECT_DISPLAY_MODE] = 2 # point cloud mode
            path = c4d.storage.LoadDialog(title = 'select: ' + procedural_name)
            procedural[c4d.C4DAI_PROCEDURAL_PATH] = path
            doc.InsertObject(procedural)

            # insert the procedural as a child from each obj
            procedural.InsertUnder(obj) ; procedurals_list.append(procedural_name)
            print 'Procedural inserted on: ' + procedural_name
        else:
            None

    print 'Procedurals added: ' + str(len(procedurals_list))
    c4d.EventAdd()

if __name__=='__main__':
    main()


'D:\01_Documents\Dyne\Dyne - Works\Quality Metal - Product Shots\Maya\qm_modeling\assets\ass files\level.ass.gz'

'D:\01_Documents\Dyne\Dyne - Works\Quality Metal - Product Shots\Maya\qm_modeling\assets\ass files\level_ass.ass.gz'

'D:\01_Documents\Dyne\Dyne - Works\Quality Metal - Product Shots\Maya\qm_modeling\assets\ass files\level_ass.gz'

'D:\01_Documents\Dyne\Dyne - Works\Quality Metal - Product Shots\Maya\qm_modeling\assets\ass files\level.ass.gz'

