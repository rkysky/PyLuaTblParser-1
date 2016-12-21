from PyLuaTblParser import PyLuaTblParser

# basic test
a1 = PyLuaTblParser()
a2 = PyLuaTblParser()
a3 = PyLuaTblParser()

test_str = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
a1.load(test_str)
d1 = a1.dumpDict()

file_path = 'table.lua'
a2.loadDict(d1)
a2.dumpLuaTable(file_path)
a3.loadLuaTable(file_path)

d3 = a3.dumpDict()

print a1.dump()
print a2.dump()
print a3.dump()



# test_1.lua
test_1 = PyLuaTblParser()
test_1.loadLuaTable('test_1.lua')
print test_1.dump()

# test_2.lua
test_2 = PyLuaTblParser()
test_2.loadLuaTable('test_2.lua')
print test_2.dump()

# test_3.lua
test_3 = PyLuaTblParser()
test_3.loadLuaTable('test_3.lua')
print test_3.dump()

# test_4.lua
test_4 = PyLuaTblParser()
test_4.loadLuaTable('test_4.lua')
print test_4.dump()

# test_5.lua
try:
    test_5 = PyLuaTblParser()
    test_5.loadLuaTable('test_5.lua')
    print test_5.dump()
except Exception, e:
    print e


