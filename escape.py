def escape(s):
    result = ''
    for c in s:
        if c == '\a':
            result += '\\a'
        elif c == '\b':
            result += '\\b'
        elif c == '\f':
            result += '\\f'
        elif c == '\n':
            result += '\\n'
        elif c == '\r':
            result += '\\r'
        elif c == '\t':
            result += '\\t'
        elif c == '\v':
            result += '\\v'
        elif c == '\\':
            result += '\\\\'
        elif c == '\"':
            result += '\\\"'
        elif c == '\'':
            result += '\\\''
        else:
            result += c
    return result



def unescape(s):
    result = ''
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        aft_c = (i + 1 < n) and s[i + 1] or None
        if c == '\\':
            if aft_c == None:
                raise Exception('unescape error')
            elif aft_c == 'a':
                result += '\a'
            elif aft_c == 'b':
                result += '\b'
            elif aft_c == 'f':
                result += '\f'
            elif aft_c == 'n':
                result += '\n'
            elif aft_c == 'r':
                result += '\r'
            elif aft_c == 't':
                result += '\t'
            elif aft_c == 'v':
                result += '\v'
            elif aft_c == '\\':
                result += '\\'
            elif aft_c == '\"':
                result += '\"'
            elif aft_c == '\'':
                result += '\''
            else:
                raise Exception('unescape error')
            i += 1
        else:
            result += c
        i += 1
    return result



def win2linux(s):
    return s.replace('\r\n', '\n')


