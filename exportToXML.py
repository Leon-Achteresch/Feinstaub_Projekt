import xml.etree.ElementTree as ET
import pathlib
from xml.dom import minidom
path = pathlib.Path('SQL.py').parent.resolve()

def create_XML(date, c, conn):

    root = ET.Element("sensordata")
    DHT22 = ET.SubElement(root, 'DHT22')
    SDS011 = ET.SubElement(root, 'SDS011')
    humidities = ET.SubElement(DHT22, 'humidities')
    temperatures = ET.SubElement(DHT22, 'temperatures')
    
    c.execute("SELECT feuchtigkeit, timestamp, temp FROM DHT22 WHERE TIMESTAMP LIKE :KEY", {'KEY': date + '%'})
    rows = c.fetchall()

    for row in rows:
        hum = ET.SubElement(humidities, 'hum')
        hum.set('date', str(row[1]))  
        hum.text = str(row[0])

        temp = ET.SubElement(temperatures, 'temp')
        temp.set("date", str(row[1]))  
        temp.text = str(row[2])

    particles1 = ET.SubElement(SDS011, 'particles1')
    particles2 = ET.SubElement(SDS011, 'particles2')

    c.execute("SELECT p1, p2, timestamp FROM SDS011 WHERE TIMESTAMP LIKE :KEY", {'KEY': date + '%'})
    rows = c.fetchall()
    for row in rows:
        p1 = ET.SubElement(particles1, 'p1')
        p1.set("date", str(row[2]))  
        p1.text = str(row[0])

        p2 = ET.SubElement(particles2, 'p2')
        p2.set("date", str(row[2]))  
        p2.text = str(row[1])

    tree = ET.ElementTree(root)

    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dtd_declaration = '<!DOCTYPE sensordata SYSTEM "sensordata.dtd">\n'
    xml_content = minidom.parseString(ET.tostring(root)).toprettyxml(indent=" ")#ET.tostring(root, encoding='utf-8').decode()
    index = 0
    for i in xml_content:
        index +=1
        if i == "\n":
            xml_content = xml_content[index: len(xml_content)]
            break
        
    xml_with_dtd = f"{xml_declaration}{dtd_declaration}{xml_content}"
    with open(f"{path}\XML\{date}.xml", "w") as f:
        f.write(xml_with_dtd)



# DTD
# <!ELEMENT sensordata (DHT22, SDS011)>
# <!ELEMENT DHT22 (humidities, temperatures)>
# <!ELEMENT humidities (hum+)>
# <!ELEMENT hum (#PCDATA)>
# <!ATTLIST hum date CDATA #REQUIRED>
# <!ELEMENT temperatures (temp+)>
# <!ELEMENT temp (#PCDATA)>
# <!ATTLIST temp date CDATA #REQUIRED>
# <!ELEMENT SDS011 (particles1, particles2)>
# <!ELEMENT particles1 (p1+)>
# <!ELEMENT p1 (#PCDATA)>
# <!ATTLIST p1 date CDATA #REQUIRED>
# <!ELEMENT particles2 (p2+)>
# <!ELEMENT p2 (#PCDATA)>
# <!ATTLIST p2 date CDATA #REQUIRED>


#chatGPT promt  
# erstelle ein bespiele xml dokument mit ElementTree

# import xml.etree.ElementTree as ET

# # Ein Element für das Root-Tag erstellen
# root = ET.Element("Kontakte")

# # Ein Kind-Element erstellen und zum Root hinzufügen
# kontakt1 = ET.SubElement(root, "Kontakt")
# name1 = ET.SubElement(kontakt1, "Name")
# name1.text = "John Doe"
# email1 = ET.SubElement(kontakt1, "Email")
# email1.text = "john@example.com"

# # Ein weiteres Kind-Element erstellen und zum Root hinzufügen
# kontakt2 = ET.SubElement(root, "Kontakt")
# name2 = ET.SubElement(kontakt2, "Name")
# name2.text = "Jane Smith"
# email2 = ET.SubElement(kontakt2, "Email")
# email2.text = "jane@example.com"

# # XML-Dokument erstellen
# tree = ET.ElementTree(root)

# # XML-Dokument in eine Datei schreiben
# tree.write("kontakte.xml")




