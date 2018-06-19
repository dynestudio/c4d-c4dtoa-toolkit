import c4d

def main():
    doc.StartUndo()

    # Flags
    # 0 GETACTIVEOBJECTFLAGS_0
    # 1 GETACTIVEOBJECTFLAGS_CHILDREN
    # 2 GETACTIVEOBJECTFLAGS_SELECTIONORDER
    objs = doc.GetActiveObjects(1)

    if not objs:
        print("No objects selected.")
        return

    for i in objs:
        tag = i.MakeTag(c4d.Texpresso)
        doc.AddUndo(c4d.UNDOTYPE_NEW, tag)
    
    c4d.EventAdd()

    doc.EndUndo()

if __name__=='__main__':
    main()