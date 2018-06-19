
import c4d
from c4d import documents, plugins, storage

def main():



    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    size = len(objs)
    i=0
    e=0


    
    for obj in objs:
        name = obj[c4d.ID_BASELIST_NAME]
        name = name.split(".")[0]
        i+=1
        e+=1
        print str(i) + "/" + str(size) + " " + name



        # Get Alembic export plugin, 1028082 is its ID
        plug = plugins.FindPlugin(1028082, c4d.PLUGINTYPE_SCENESAVER)
        if plug is None:
            return

        filePath = "//192.168.10.45/server_01/2018/claro_and_cia/shot_010/3d/houdini/footage/alembic/" + name + ".abc"


        doc.SetSelection( obj , c4d.SELECTION_NEW) #new active selection for each object
        c4d.EventAdd() #update selectoin

        op = {}

        if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):

            # BaseList2D object stored in "imexporter" key hold the settings
            abcExport = op["imexporter"]

            # Change Alembic export settings
            abcExport[c4d.ABCEXPORT_SELECTION_ONLY] = True


            # Finally export the document
            if documents.SaveDocument(doc, filePath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1028082):
                None

            else:
                print "Export failed!"

if __name__=='__main__':
    main()
