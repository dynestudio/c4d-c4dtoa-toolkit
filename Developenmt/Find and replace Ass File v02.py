import c4d

ARNOLD_PROCEDURAL = 1032509

def get_active_objs(): # get active objects from obj manager
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        return None
    return activeObjects

def main():

    objsList = get_active_objs()
    if objsList == None:
        return

    mayaProcedural_name = 'ArnoldStandIn'

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

            procedural[c4d.ID_BASEOBJECT_REL_SCALE] = c4d.Vector(0.1,0.1,0.1)
            procedural[c4d.C4DAI_PROCEDURAL_PATH] = 'test'
            doc.InsertObject(procedural)

            # insert the procedural as a child from each obj
            procedural.InsertUnder(obj)
            print 'Procedural inserted on: ' + procedural_name
        else:
            None

    print 'Procedurals added: ' + str(len(objsList))
    c4d.EventAdd()

if __name__=='__main__':
    main()