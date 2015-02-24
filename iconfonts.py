import re
import json
from collections import OrderedDict

_register = OrderedDict()


def register(name, ttf_fname, fontd_fname):
    """Register an Iconfont
    :param name: font name identifier.
    :param ttf_fname: ttf filename (path)
    :param fontd_fname: fontdic filename. (See create_fontdic)
    """
    with open(fontd_fname, 'r') as f:
        fontd = json.loads(f.read())
        _register[name] = ttf_fname, fontd_fname, fontd


def icon(code, size=None, color=None, font_name=None):
    """ Gets an icon from iconfont.
    :param code: Icon codename (ex: 'icon-name')
    :param size: Icon size
    :param color: Icon color
    :param font_name: Registered font name. If None first one is used.
    :returns: icon text (with markups)
    """
    font = _register.keys()[0] if font_name is None else font_name
    font_data = _register[font]
    s = "[font=%s]%s[/font]" % (font_data[0], unichr(font_data[2][code]))
    if size is not None:
        s = "[size=%s]%s[/size]" % (size, s)
    if color is not None:
        s = "[color=%s]%s[/color]" % (color, s)

    return s


def create_fontdict_file(css_fname, output_fname):
    """Creates a font dictionary file. Basically creates a dictionary filled
    with icon_code: unicode_value entries
    obtained from a CSS file.
    :param css_fname: CSS filename where font's rules are declared.
    :param output_fname: Fontd file destination
    """
    with open(css_fname, 'r') as f:
        data = f.read()
        res = _parse(data)
        with open(output_fname, 'w') as o:
            o.write(json.dumps(res))
        return res


def _parse(data):
    # This is probably a bad way to get the rules. but works.
    # Find start line where icons rules start
    pat_start = re.compile('}.+content:', re.DOTALL)
    start = [x for x in re.finditer(pat_start, data)][0].start()
    data = data[start:]  # crop
    data = data.replace("\\", '0x')  # replace unicodes
    # Find keys
    pat_keys = re.compile('[a-zA-Z0-9_-]+:before')
    keys = []
    lines = []
    for i in re.finditer(pat_keys, data):
        lineno = data.count("\n", 0, i.start()) + 1
        lines.append(lineno)  # save line position
        keys.append(i.group().replace(':before', ''))

    # Find values (unicode value) and save it to values list as many times as
    # needed
    values = []
    QUOTE = '"'
    data = data.replace("'", '"')
    pat_values = re.compile('content:.+')

    for i in re.finditer(pat_values, data):
        lineno = data.count("\n", 0, i.start()) + 1
        v = i.group().split(QUOTE)[1]
        v = v.replace('content:', '')
        for j, lnum in enumerate(lines):
            if lnum <= lineno:
                try:
                    val = int(v.replace('content:', ''), 0)
                except:
                    val = 0
                values.append(val)
            else:
                break
        [lines.pop(0) for x in lines[0:j]]  # pop assigned lines

    # Create dict
    res = dict(zip(keys, values))

    return res
