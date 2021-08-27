
import os.path
import magic
import pandas as pd

def readingNotStandardFileAsStringAndConvertToCSV(prompts):

    name, extension = os.path.splitext(os.path.basename(prompts.importFile))
    if extension.lower() == '.test':

        openFile = open(prompts.importFile, 'rb').read()
        m = magic.Magic(mime_encoding=True)
        encoding = m.from_buffer(openFile)
        with open(prompts.importFilen, encoding=encoding) as buffer:
            data = buffer.read()

        rows = {}
        while '[NAME]' in data:
            posIndex = data.find('[NAME]') + 5
            data = data[posIndex:]
            if '|' in data:
                posIndex = data.find('|') + 1
                newPosition = posIndex - 1
                checkingName = data.find('no name')
                if not checkingName == posIndex:
                    if newPosition < 5:
                        name = data[:newPosition]
                        data = data[posIndex:]
                        descriptionsPosition = data.find('|')
                        description = data[:descriptionsPosition]
                        data = data[descriptionsPosition:]
                        if name and description:
                            if 'name' in rows:
                                rows['name'].append(name)
                                rows['description'].append(description)
                            else:
                                rows['name'] = [name]
                                rows['description'] = [description]
                        positionName = data.find('[NAME]')
                        data = data[positionName:]
                elif '[NAME]' in data:
                    positionName = data.find('[NAME]')
                    data = data[positionName:]

            df = pd.DataFrame.from_dict(rows, orient="columns")
            csvFile = df.to_csv(path_or_buf=None, index=None, sep=';')
            return csvFile
    else:
        # instead of assert use log or alternative
        assert False, "Wrong file! Your file's suffix: {}.".format(extension.lower())
