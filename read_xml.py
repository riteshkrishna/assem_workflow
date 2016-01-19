__author__ = 'ritesh'

import xml.etree.ElementTree as ET
import logging

def extractLocationFromExecutables(xmlFile, nodeName):

    """
    Specifically written for XML structures as in configs/executable.xml. Finds the location of executable for the asked tool.
    :param xmlFile: usually 'configs/executables.xml'
    :param nodeName: Tool name, e.g.'FASTQC'
    :return:Location of the binary as noted in the XML file
    """

    tree = ET.parse(xmlFile)
    logging.info('XML file - ' + xmlFile + ' parsed')

    root = tree.getroot()

    for tools in root.findall('tool'):
        if tools.get('name') == nodeName:
            location = tools.find('location')
            logging.info('Executable location for ' + nodeName + ' found -' + location.text)
            return location.text

if __name__=="__main__":

    xmlFile = 'configs/executables.xml'
    nodeName = 'FASTQC'
    print 'Executable for ' + nodeName + ' = ' + extractLocationFromExecutables(xmlFile,nodeName)

    xmlFile = 'configs/executables.xml'
    nodeName = 'SICKLE'
    print 'Executable for ' + nodeName + ' = ' + extractLocationFromExecutables(xmlFile,nodeName)