

import os.path
import pandas as pd
import xml.etree.ElementTree as Xet


def readingXMLfileConvertToCSV(prompts):

    name, extension = os.path.splitext(os.path.basename(prompts.importFile))
    if extension.lower() == '.xml':

        rows = {}

        def searchName(e):
            if e.tag == 'Name':
                for g in e.findall('Name'):
                    searchName(g)

            name = e.findtext('firstName')
            if name == None:
                return
            description = e.findtext('Description')
            
            if 'name' in rows: 
                rows['name'].append(name)
                rows['description'].append(description)
            else:
                rows['name'] = [name]
                rows['description'] = [description]

        xmlparse = Xet.parse(prompts.importFile)
        root = xmlparse.getroot()[1].findall('Name')
        for e in root:
            searchName(e)

        df = pd.DataFrame.from_dict(rows, orient="columns")
        csvFile = df.to_csv(path_or_buf=None, index=None, sep=';')

        return csvFile
    else:
        # instead of assert use log or alternative
        assert False, "Wrong file! Your file's suffix: {}.".format(extension.lower())