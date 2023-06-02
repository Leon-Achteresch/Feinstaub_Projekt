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
    #with open(f'{path}\{date}.xml', 'w') as f:
    #    tree.write(f, encoding='unicode')
    #f.close()
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent=" ")
    with open(f"{path}\XML\{date}.xml", "w") as f:
        f.write(xmlstr)



