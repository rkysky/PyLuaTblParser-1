from escape import *
from luastring import *
from annotation import *



class PyLuaTblParser:
    container = None


    def decode_key(self, key):
        # string
        if key.startswith('[\"') and key.endswith('\"]'):
            return unescape(key[2:-2])

        if key.startswith('[\'') and key.endswith('\']'):
            return unescape(key[2:-2])

        # number
        if key.startswith('[') and key.endswith(']'):
            if is_number(key[1:-1]):
                return str2number(key[1:-1])
            else:
                raise Exception('decode key error')

        if is_identifier(key):
            return key
        else:
            raise Exception('decode key error')


    def encode_key(self, key):
        # number
        if isinstance(key, (int, float)):
            return '[' + str(key) + ']'

        # string
        return '["' + escape(key) + '"]'


    def decode_value(self, value):
        # table
        if isinstance(value, list) or isinstance(value, dict):
            return value

        # boolean
        if value == 'true':
            return True

        if value == 'false':
            return False

        # nil
        if value == 'nil':
            return None

        # string
        if len(value) >= 2 and value[0] == '\"' and value[-1] == '\"':
            return unescape(value[1:-1])

        if len(value) >= 2 and value[0] == '\'' and value[-1] == '\'':
            return unescape(value[1:-1])

        # number
        if is_number(value):
            return str2number(value)

        # string
        if is_identifier(value):
            return value
        else:
            raise Exception('decode value error')


    def encode_value(self, value):
        # boolean
        if isinstance(value, bool) and value == True:
            return 'true'

        if isinstance(value, bool) and value == False:
            return 'false'

        # nil
        if value == None:
            return 'nil'

        # number
        if isinstance(value, (int, float)):
            return str(value)

        # string
        return '"' + escape(value) + '"'


    def _load(self, s):
        s = win2linux(s)
        s = remove_annotation(s)
        s = remove_space(s)

        l, r, n = 0, 0, len(s)
        key, value = None, None
        _list, _dict = None, None
        stack = []
        in_str = None

        while r < n:
            c = s[r]

            if c == '{':
                if in_str != None:
                    r += 1
                    continue

                if _list != None or _dict != None:
                    stack.append([key, _list, _dict])

                key, value, _list, _dict = None, None, [], {}

                l = r + 1

            elif c == '}':
                if in_str != None:
                    r += 1
                    continue

                if l < r:
                    value = s[l:r]

                if value != None:
                    if key == None:
                        _list.append(self.decode_value(value))
                    else:
                        if self.decode_value(value) != None:
                            _dict[self.decode_key(key)] = self.decode_value(value)
                    key, value = None, None

                if stack:
                    if _dict:
                        value = _dict
                        for i in range(len(_list)):
                            if _list[i] != None:
                                value[i + 1] = _list[i]
                    else:
                        value = _list
                    key, _list, _dict = stack.pop()

                l = r + 1

            elif c == '=':
                if in_str != None:
                    r += 1
                    continue

                key = s[l:r]
                l = r + 1

            elif c == ',':
                if in_str != None:
                    r += 1
                    continue

                if l < r:
                    value = s[l:r]

                if value != None:
                    if key == None:
                        _list.append(self.decode_value(value))
                    else:
                        if self.decode_value(value) != None:
                            _dict[self.decode_key(key)] = self.decode_value(value)
                    key, value = None, None

                l = r + 1

            elif c == '\"' or c == '\'':
                if in_str == None:
                    in_str = c
                elif in_str == c:
                    in_str = None

            elif c == '\\':
                if in_str == None:
                    raise Exception('load error')
                r += 1

            r += 1

        if _dict:
            value = _dict
            for i in range(len(_list)):
                if _list[i] != None:
                    value[i + 1] = _list[i]
        else:
            value = _list

        return value


    def load(self, s):
        self.container = self._load(s)
    

    def _dump(self, container):
        out = ''
        if isinstance(container, list):
            out += '{'
            for token in container:
                if isinstance(token, list) or isinstance(token, dict):
                    out += self._dump(token)
                else:
                    out += self.encode_value(token)
                out += ','
            out += '}'
        elif isinstance(container, dict):
            out += '{'
            for (key, value) in container.items():
                out += self.encode_key(key)
                out += '='
                if isinstance(value, list) or isinstance(value, dict):
                    out += self._dump(value)
                else:
                    out += self.encode_value(value)
                out += ','
            out += '}'
        return out


    def dump(self):
        return self._dump(self.container)


    def loadLuaTable(self, f):
        sf = open(f, 'r')
        text = sf.read()
        self.load(text)
        sf.close()


    def dumpLuaTable(self, f):
        df = open(f, 'w')
        text = self.dump()
        df.write(text)
        df.close()


    def loadDict(self, d):
        for key in d:
            if not isinstance(key, (int, float, str)):
                del d[key]
        self.load(self._dump(d))


    def dumpDict(self):
        result = self._load(self.dump())
        if isinstance(result, list):
            tmp = {}
            for i in range(len(result)):
                if result[i] != None:
                    tmp[i+1] = result[i]
            return tmp
        return result


    def __getitem__(self, index):
        return self.container[index]


    def update(self, d):
        for key in d:
            if isinstance(key, (int, float, str)):
                self.container[key] = d[key]







