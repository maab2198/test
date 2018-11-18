#from flanker.addresslib import address
import os
import json

class DB:
    tables=dict()
    def __init__(self, name_=None):
        self.name = name_

    def add_table(self, table):
        self.tables[table.name]=table

    def delete_table(self, name):
        print(name)
        if name in self.tables:
            del(self.tables[name])
        else:
            print('Name is not exist')

    def import_DB(self, name):
        self.name = name
        path = os.path.join('datasource/',name)
        with open(path,'r') as file:
            data = json.load(file)
            keys = data['tables']
            tables_=list()
            columns = []
            for table_name in keys:
                columns.append(data['tables'][table_name]['columns'])
                tables_.append(Table(table_name, columns[-1]))
                for rec in data['tables'][table_name]['records']:
                    record=Record(rec)
                    tables_[-1].add_record(record.content)
                self.add_table(tables_[-1])
            print('Imported')
        return data



    def export_DB(self, name):
        path = os.path.join('datasource/', name)
        with open(path,'w') as file:
            data={}
            data['database']=name
            data['tables'] = {}
            for table in self.tables:
                data['tables'][table]={}
                data['tables'][table]['columns']=self.tables[table].columns
                data['tables'][table]['records']=self.tables[table].records

            json_data=json.dump(data,file,indent=4)
            return ('Exported\n')

    def diff_of_tables(self, name1, name2):
        print('Columns: ', self.tables[name1].columns)
        if [col_name for col_name in self.tables[name1].columns if col_name not in  self.tables[name2].columns]:
            for record in self.tables[name1].records:
                print(record)
        else:
            rec1=set()
            rec2=set()
            for rec_1,rec_2 in zip(self.tables[name1].records,self.tables[name2].records):
                rec1.add(tuple(rec_1))
                rec2.add(tuple(rec_2))
            #rec1=set(tuple([rec for rec in self.tables[name1].records]))
            #rec2=set(tuple([rec for rec in self.tables[name2].records]))
            print('Diff:\n',rec1-rec2)
            return list(rec1-rec2)

    def union_of_tables(self, name1, name2):
        if [col_name for col_name in self.tables[name1].columns if col_name not in self.tables[name2].columns]:
            print('Can\'t union the tables. Different columns')
        else:
            rec1 = set()
            rec2 = set()
            for rec_1, rec_2 in zip(self.tables[name1].records, self.tables[name2].records):
                rec1.add(tuple(rec_1))
                rec2.add(tuple(rec_2))
            print('Union:\n ', rec1|rec2)
        return list(rec1|rec2)

class Table:
    def __init__(self, name_=None,columns_=None):
        self.name = name_
        self.columns = columns_
        self.records=list()

    def add_columns(self,columns_):
        self.columns = columns_


    def delete_record(self, index):
        if index<0 or index >= len(self.records):
            print('Index is out of range')
        else:
            self.records.remove(self.records[index])
        return self.records

    def edit_record(self, index, content):
        if index < 0 or index >= len(self.records):
            print('Index is out of range')
        else:
            if self.check_content(content):
                self.records[index] = content
            else:
                print('Incorrect data')
        return self.records
    #Flanker
    def check_for_email(self, content):
        # if address.parse(content) != None:
        #     return True
        return True #False

    def check_for_enum(self, content, enum_data):
        if content in enum_data:
            return True
        else:
            return False

    def check_for_IntrStr(self, content):
        if isinstance(tuple, content):
            if isinstance(str, content[0]) and isinstance(str, content[1]):
                return True
            else:
                return False
        else:
            return False

    def check_content(self,content):
        if len(content) != len(self.columns):
            return False
        else:
            for col_type,c in zip(self.columns,content):
                if col_type == 'email':
                    self.check_for_email(c)
                elif col_type == 'html' and not isinstance(c,str):
                        return False
                elif col_type == 'IntrStr':
                        self.check_for_IntrStr(c)
                elif col_type == 'enum':
                    self.check_for_enum(c, col_type)
                else:
                    if col_type == 'int':
                        if not c.isdigit():
                            return False
                    elif col_type == 'float':
                        if not isinstance(float(c),float):
                            return False
                    elif not isinstance(c,col_type):
                            return False
            return True

    def add_record(self, record):
        if self.check_content(record):
            self.records.append(record)
            return True
        return False

    def edit_cell_in_record(self, index, content):
        if index[0] < 0 or index[0] >= len(self.records):
            print('Index is out of range')
        else:
         self.records[index[0]].edit_cell(index[1], content)

class Record:
    def __init__(self, content_=None):
        self.content = content_

    def edit_cell(self, index, content_):
        if index < 0 or index >= len(self.content):
            print('Index is out of range')
        else:
            self.content[index] = content_

if __name__ == '__main__':
    event = input('what do u need?\n 1. import DB\n 2. create DB\n 3. delete DB\n Answer: ')
    if event != '3':
        name = input('Name of DB (*json): ')

        database_=DB(name)
        if event == '1':
            print(name)
            database_.import_DB(name)
            print(database_.name)
        if event == '2':
            print('DB \'%s\' created', name)

        event_ = input('1. add table\n2. delete table\n3. edit table\n4. break\n')
        if event_ == '1':
            name_t=input('Name of table: ')
            col_=['int','double','email']
            table_=Table(name_t,col_)
            database_.add_table(table_)
        elif event_ == '2':
            name_t = input('Name of table: ')
            database_.delete_table(name_t)
        elif event == '3':
            event_t = input('1.add record\n2.del record\n3.diff of tables\n4.union of tables\n5.edit cell\n6.edit record')
            name_t = input('Name of table1: ')
            name2_t = input('Name of table2: ')
            database_.diff_of_tables(name_t,name2_t)

                #TODO COLUMNS AND ETC...
        answer = input('Do u want to export a DB?[y/n]')
        if answer == 'y':
            database_.export_DB(name)
            print('DB \'%s\' exported', name)
    else:
        name = input('Name of DB (*json): ')
        answer = input('Are u sure?[y/n]')
        if answer == 'y':
            print('DB \'%s\' deleted', name)
        else:
            print('Canceled')
