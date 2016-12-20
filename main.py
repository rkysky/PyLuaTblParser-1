from PyLuaTblParser import PyLuaTblParser

a1 = PyLuaTblParser()
a2 = PyLuaTblParser()
a3 = PyLuaTblParser()

test_str = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'

a1.load(test_str)
print a1.dump()

d1 = a1.dumpDict()

file_path = 'store.lua'
a2.loadDict(d1)
a2.dumpLuaTable(file_path)
a3.loadLuaTable(file_path)

d3 = a3.dumpDict()