def remove_annotation(s):
    result = ''
    state, l, r = 0, 0, 0
    in_str = None
    i, n = 0, len(s)

    while i < n:
        c = s[i]

        if state == 0:         # state 0
            if c == '-':
                state = 1
            elif c == '\"' or c == '\'':
                state = 9
                in_str = c
                result += c
            else:
                result += c

        elif state == 1:       # state 1
            if c == '-':
                state = 2
            elif c == '\"' or c == '\'':
                raise Exception('remove annotation error')
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

        elif state == 9:       # state 9
            if c == in_str:
                state = 0
                result += c
            elif c == '\\':
                if i + 1 >= n:
                    raise Exception('remove annotation error')
                result += c
                result += s[i + 1]
                i += 1
            else:
                result += c

        i += 1

    if state == 1 or state == 5 or state == 6 or state == 7 or state == 9:
        raise Exception('remove annotation error')

    return result



def remove_space(s):
    result = ''
    in_str = None
    i, n = 0, len(s)

    while i < n:
        c = s[i]

        if c == '\"' or c == '\'':
            if in_str == None:
                in_str = c
            elif in_str == c:
                in_str = None
            result += c
            i += 1

        elif c == '\\':
            if in_str == None:
                raise Exception('remove space error')
            if i + 1 >= n:
                raise Exception('remove space error')
            result += c
            result += s[i + 1]
            i += 2

        elif c in ' \t\r\n':
            if in_str != None:
                result += c
                i += 1
            else:
                i += 1

        else:
            result += c
            i += 1

    return result


