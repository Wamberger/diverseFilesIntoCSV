

from ldap3 import Server, Connection, ALL
import pandas as pd


def readingLDAPandConvertingToCSV():

    SERVER = '...SERVER STRING...'
    USER = '...USER LOGIN STRING...'
    PASSWORD = '...USER LOGIN PASSWORD STRING...'
    server = Server(SERVER, get_info=ALL)
    connection = Connection(server, USER, PASSWORD, auto_bind=True)
    
    def getData(root, rows):

        while root:

            if 'CN=' in root:
                positionIndex = root.find('CN=')
                root = root[positionIndex:]
                if "\\" in root: 
                    positionIndex = root.find("\\") + 1
                    newPosition = root[:positionIndex - 1]
                    newRoot = root[positionIndex:]
                    root = newPosition + newRoot
                    if '\n' in root:
                        positionEndIndex = root.find('\n')
                        searchName = root[:positionEndIndex - 2]
                        if not 'DC=corp' in searchName:
                            searchName = root[:positionEndIndex - 1]
                        root = root[positionEndIndex:]
                    try:
                        if connection.search(searchName,'(objectclass=*)', attributes=['name','description']):
                            data = connection.response_to_json()
                            
                            if 'name' in data:
                                positionName = data.find('name') + 6
                                data = data[positionName:]
                                if '\n' in data:
                                    positionName = data.find('\n')
                                    name = data[:positionName]
                            if 'description' in data:
                                positionDescription = data.find('description') + 10
                                data = data[positionDescription:]
                                if '\n' in data:
                                    positionDescription = data.find('\n')
                                    description = data[:positionDescription]
                                    data = ''

                            if 'name' in rows:
                                rows['name'].append(name)
                                rows['description'].append(description)
                                
                            else:                                            
                                rows['name'] = [name]
                                rows['description'] = [description]
                                
                    except:
                        # instead of assert use log or alternative
                        assert False, "No data in: {}".format(data)
            else:
                root = ''

        return rows

    map = True
    rows = {} 

    while map:
        if connection.search('...LDAP STRING...', '(objectclass=*)', attributes = ['Names']): 
            root = connection.response_to_json()
            rows = getData(root=root, rows=rows)
            map = False

    df = pd.DataFrame.from_dict(rows, orient="columns")
    CSVfile = df.to_csv(path_or_buf=None, index=None, sep=';')

    return CSVfile