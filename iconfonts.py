import re
import json
from collections import OrderedDict

_register = OrderedDict()

def register(name, ttf_fname, fontd_fname):
    with open(fontd_fname, 'r') as f:
        fontd = json.loads(f.read())
        _register[name] = ttf_fname, fontd_fname, fontd

def icon(name, size=None, color=None, font_name=None):
    font = _register.keys()[0] if font_name is None else font_name
    font_data = _register[font]
    s = "[font=%s]%s[/font]"% (font_data[0], unichr(font_data[2][name]))
    if size is not None:
        s = "[size=%s]%s[/size]"%(size, s)
    if color is not None:
        s = "[color=%s]%s[/color]"%(color, s)

    return s


def create_fontdict_file(css_fname, output_fname):
    with open(css_fname,'r') as f:
        data = f.read()
        res = _parse(data)
        with open(output_fname, 'w') as o:
            o.write(json.dumps(res))
        return res

def _parse(data):
    # Find start line where icons rules start
    pat_start = re.compile('}.+content:', re.DOTALL)
    start = [ x for x in re.finditer(pat_start, data)][0].start()
    data = data[start:] #crop
    data = data.replace("\\", '0x') # replace unicodes

    #Find keys
    pat_keys = re.compile('[a-zA-Z0-9_-]+:before')
    keys = []
    lines = []
    for i in re.finditer(pat_keys, data):
        lineno = data.count("\n",0,i.start())+1
        lines.append(lineno) # save line position
        keys.append(i.group().replace(':before',''))

    # Find values (unicode value) and save it to values list as many times as needed
    values = []
    QUOTE = '"'
    data = data.replace("'", '"')
    pat_values = re.compile('content:.+')

    for i in re.finditer(pat_values, data):
        lineno = data.count("\n",0,i.start())+1
        v = i.group().split(QUOTE)[1]
        v = v.replace('content:','')
        for j, lnum in enumerate(lines):
            if lnum <= lineno:
                values.append(int(v.replace('content:',''),0))
            else:
                break
        [lines.pop(0) for x in lines[0:j]] # pop assigned lines

    # Create dict
    res = dict(zip(keys, values))

    return res
