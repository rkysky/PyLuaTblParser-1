-- escape test

{
    ["\r\t\n"] = "\r\t\n",
    ['\\\r\\\t\\\n'] = '\\\r\\\t\\\n',
    ["\"\'"] = "{}[]|\\:;\'\"',.?/"
}