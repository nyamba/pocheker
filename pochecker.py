# -*- coding: utf8 -*-
import re, polib


def is_valid_named_var(p):
    '''
    >>> is_valid_named_var('name %(name)s', u'нэр %(name)s')
    True
    >>> is_valid_named_var('name %(name)s', u'нэр %(name)')
    False
    >>> is_valid_named_var('name %(name)s age: %(age)s', u'нэр %(name)s нас: age')
    False
    '''
    pattern = r'.*%\((\w+)\)s.*'
    variables = []
    p_gen = lambda a: '%(' + a + ')s'
    f_gen = lambda a: '%(' + a +')'
    msgid = p.msgid

    match = re.search(pattern, msgid)
    while match:
        vname = match.groups()[0]
        variables.append(vname)
        msgid = msgid.replace(p_gen(vname), '')
        match = re.search(pattern, msgid)

    fixed = False
    for vname in variables:
        if p_gen(vname) not in p.msgstr:
            if f_gen(vname) in p.msgstr:
                fixed = True
                p.msgstr = p.msgstr.replace(f_gen(vname), p_gen(vname))

    if fixed:
        print 'fixed', p.msgstr


def is_valid_str(msgid, msgstr):
    '''
    >>> is_valid_str('name %s', u'нэр %s')
    True
    >>> is_valid_str('name %s, age %s', u'нэр %s, age')
    False
    >>> is_valid_str('name %s, age %s', u'нэр %s, age %s')
    True
    '''
    return msgid.count('%s') == msgstr.count('%s')

def check_new_line(p):
    st = p.msgid[0]
    end = p.msgid[-1]
    if st == '\n' and p.msgstr.startswith('\n'):
        print 'both not begin new line', p
        #print p.msgid, p.msgstr
        p.msgstr = u'\n' + p.msgstr
    if end == '\n' and p.msgstr.endswith('\n'):
        print 'both not ends new line', p
        #print p.msgid, p.msgstr
        p.msgstr =  p.msgstr + u'\n'


if __name__ == '__main__':
    po = polib.pofile('django.po')
    checkers = [is_valid_named_var, check_new_line]

    for p in po:
        if len(p.msgstr):
            result = [c(p) for c in checkers]

    #po.save()
