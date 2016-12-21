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



def is_letter(c):
    if c >= 'a' and c <= 'z':
        return True
    if c >= 'A' and c <= 'Z':
        return True
    return False



def is_digit(c):
    if c >= '0' and c <= '9':
        return True
    return False



def is_identifier(s):
    if len(s) == 0:
        return False
    if s[0] != '_' and not is_letter(s[0]):
        return False
    for i in range(1, len(s)):
        if s[i] != '_' and not is_letter(s[i]) and not is_digit(s[i]):
            return False
    return True


