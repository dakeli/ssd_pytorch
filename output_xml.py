from xml.dom import minidom


def op_xml(minc, minr, maxc, maxr, count, doc, Annotations, img_id):
    coor = str(img_id).split(r'\\')[-1].split('\'')[-2].split('----')[-1].split('_')
    d = {}
    d["Id"] = str(count)
    d["Name"] = "Annotation" + " " + str(count)
    # d["Color"] = "#F4FA58"
    d["Color"] = "#F2CB24"
    d["Type"] = "Polygon"
    d["Order1"] = "0"
    d["X1"] = str(minc + int(coor[0]) )
    d["Y1"] = str(minr + int(coor[1]) )
    d["Order2"] = "1"
    d["X2"] = str(maxc + int(coor[0]) )
    d["Y2"] = str(minr + int(coor[1]) )
    d["Order3"] = "2"
    d["X3"] = str(maxc + int(coor[0]) )
    d["Y3"] = str(maxr + int(coor[1]) )
    d["Order4"] = "3"
    d["X4"] = str(minc + int(coor[0]) )
    d["Y4"] = str(maxr + int(coor[1]) )
    # count = count + 1
    create_coordinate(doc, Annotations, d)


def create_coordinate(doc, Annotations, example):
    Annotation = doc.createElement("Annotation")
    Annotation.setAttribute("Name", example["Name"])
    Annotation.setAttribute("Type", example["Type"])
    Annotation.setAttribute("PartOfGroup", "None")
    Annotation.setAttribute("Color", example["Color"])
    Annotations.appendChild(Annotation)
    Coordinates = doc.createElement("Coordinates")
    # Coordinates.setAttribute("Text",example["Text"])
    Annotation.appendChild(Coordinates)
    Coordinate1 = doc.createElement("Coordinate")
    Coordinate1.setAttribute("Order", example["Order1"])
    Coordinate1.setAttribute("X", example["X1"])
    Coordinate1.setAttribute("Y", example["Y1"])
    Coordinates.appendChild(Coordinate1)
    Coordinate2 = doc.createElement("Coordinate")
    Coordinate2.setAttribute("Order", example["Order2"])
    Coordinate2.setAttribute("X", example["X2"])
    Coordinate2.setAttribute("Y", example["Y2"])
    Coordinates.appendChild(Coordinate2)
    Coordinate3 = doc.createElement("Coordinate")
    Coordinate3.setAttribute("Order", example["Order3"])
    Coordinate3.setAttribute("X", example["X3"])
    Coordinate3.setAttribute("Y", example["Y3"])
    Coordinates.appendChild(Coordinate3)
    Coordinate4 = doc.createElement("Coordinate")
    Coordinate4.setAttribute("Order", example["Order4"])
    Coordinate4.setAttribute("X", example["X4"])
    Coordinate4.setAttribute("Y", example["Y4"])
    Coordinates.appendChild(Coordinate4)
    return Coordinates
