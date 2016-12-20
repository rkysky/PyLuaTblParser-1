# helper function
def ansi2unicode(s):
    return s.decode('ANSI')

def win2linux(s):
    return s.replace('\r\n', '\n')

def remove_annotation(s):
    result = ''
    state, l, r = 0, 0, 0

    for c in s:
        if state == 0:         # state 0
            if c == '-':
                state = 1
            else:
                result += c

        elif state == 1:       # state 1
            if c == '-':
                state = 2
            else:
                state = 0
                result += '-'
                result += c

        elif state == 2:       # state 2
            if c == '[':
                state = 3
            elif c == '\n':
                state = 0
            else:
                state = 8

        elif state == 3:       # state 3
            if c == '=':
                state = 4
                l = 1
            elif c == '[':
                state = 5
            else:
                state = 8

        elif state == 4:       # state 4
            if c == '=':
                l += 1
            elif c == '[':
                state = 5
            else:
                state = 8
                l = 0

        elif state == 5:       # state 5
            if c == ']':
                state = 6
            else:
                pass

        elif state == 6:       # state 6
            if c == '=':
                if l == 0:
                    state = 5
                else:
                    state = 7
                    r = 1
            elif c == ']':
                if l == 0:
                    state = 0
                else:
                    pass
            else:
                state = 5

        elif state == 7:       # state 7
            if c == '=':
                r += 1
                if r > l:
                    state = 5
                    r = 0
            elif c == ']':
                if l == r:
                    state = 0
                    l, r = 0, 0
                else:
                    state = 6
            else:
                state = 5
                r = 0

        elif state == 8:       # state 8
            if c == '\n':
                state = 0
                result += c
            else:
                pass

    if state == 5 or state == 6 or state == 7:
        return None

    return result

def remove_space(s):
    result = ''
    in_str = False
    for i in range(len(s)):
        c = s[i]
        if c == '"':
            in_str = not in_str
            result += c
        elif c == ' ' or c == '\t' or c == '\r' or c == '\n':
            if in_str:
                result += c
            else:
                pass
        else:
            result += c
    return result

def str2number(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return None

def is_number(s):
    return str2number(s) != None

def is_string(s):
    return True

# main class
class PyLuaTblParser:
    container = None

    def formatkey(self, key):
        # string
        if key.startswith('["') and key.endswith('"]'):
            return key[2:-2]

        # number
        if key.startswith('[') and key.endswith(']'):
            if is_number(key[1:-1]):
                return str2number(key[1:-1])

        if is_string(key):
            return key

        return None

    def formatvalue(self, value):
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
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            return value[1:-1]
        
        # number
        return str2number(value)

    def load(self, s):
        s = ansi2unicode(s)
        s = win2linux(s)
        s = remove_annotation(s)
        if s == None:
            raise Exception('LoadError')
        s = remove_space(s)

        l = 0
        stack = []
        key, value = None, None
        _list, _dict = None, None
        
        in_str = False

        for r in range(len(s)):
            c = s[r]
            if c == '{':
                if in_str:
                    continue

                if _list != None or _dict != None:
                    stack.append([key, _list, _dict])
                key, _list, _dict = None, [], {}
                l = r + 1

            elif c == '}':
                if in_str:
                    continue

                if l < r:
                    value = s[l:r]

                if value:
                    if key == None:
                        _list.append(self.formatvalue(value))
                    else:
                        if self.formatvalue(value) != None:
                            _dict[self.formatkey(key)] = self.formatvalue(value)
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
                if in_str:
                    continue

                key = s[l:r]
                l = r + 1

            elif c == ',':
                if in_str:
                    continue

                if l < r:
                    value = s[l:r]

                if value:
                    if key == None:
                        _list.append(self.formatvalue(value))
                    else:
                        if self.formatvalue(value) != None:
                            _dict[self.formatkey(key)] = self.formatvalue(value)
                    key, value = None, None

                l = r + 1

            elif c == '"':
                in_str = not in_str

            elif c == ' ':
                pass

            elif c == '[':
                pass

            elif c == ']':
                pass

        if _dict:
            self.container = _dict
            for i in range(len(_list)):
                if _list[i] != None:
                    self.container[i + 1] = _list[i]
        else:
            self.container = _list
        
    def show(self, container):
        out = ''
        if isinstance(container, list):
            out += '['
            for token in container:
                if isinstance(token, list) or isinstance(token, dict):
                    out += self.show(token)
                else:
                    out += str(token)
                out += ','
            out += ']'
        elif isinstance(container, dict):
            out += '{'
            for (key, value) in container.items():
                out += str(key)
                out += '='
                if isinstance(value, list) or isinstance(value, dict):
                    out += self.show(value)
                else:
                    out += str(value)
                out += ','
            out += '}'
        return out

    def dump(self):
        return self.show(self.container)

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

    def deep_copy(self, d): # key should be number or string
        if isinstance(d, dict):
            result = {}
            for (key, value) in d.items():
                if isinstance(key, int) or isinstance(key, float) or isinstance(key, str):
                    result[key] = self.deep_copy(value)
            return result
        elif isinstance(d, list):
            result = []
            for item in d:
                result.append(self.deep_copy(item))
            return result
        else:
            return d

    def loadDict(self, d):
        self.container = self.deep_copy(d)

    def dumpDict(self):
        return self.deep_copy(self.container)





