#!/bin/python

import re

from sys import argv
from sys import stdin

def PrintUnrefArg(arg):
    print '\tUNREFERENCED_PARAMETER(' + arg + ');'

if len(argv) == 2:
    for line in stdin:

        s1 = re.sub(r'\s*STDMETHOD\((\w+)\)(.*);', 'STDMETHODIMP %s::\g<1>\g<2>' %(argv[1]), line)
        print s1,

        if s1 != line:
            print '{\n',

            # parse parameters
            m1 = re.search(r'\([\w*]+ (?P<arg>\w*)(?P<args>, .*)?\)', s1)
            args = None
            if m1:
                PrintUnrefArg(m1.groupdict()['arg'])
                args = m1.groupdict()['args']
            while args:
                m2 = re.match(r', [\w*]+ (?P<arg>\w*)(?P<args>, .*)?', args)
                if m2:
                    PrintUnrefArg(m2.groupdict()['arg'])
                    args = m2.groupdict()['args']

            print '\treturn E_NOTIMPL;\n}\n'
else:
    pattern = re.compile(r'\[(\w*)[\w, ()]*\] ')
    for line in stdin:

        # replace property function
        m1 = pattern.search(line)
        s1 = line;
        if m1 and m1.group(1) == 'propget':
            s1 = re.sub(r'HRESULT (\w*)', 'HRESULT get_\g<1>', line)
        elif m1 and m1.group(1) == 'propput':
            s1 = re.sub(r'HRESULT (\w*)', 'HRESULT put_\g<1>', line)

        s2 = re.sub(r'HRESULT (.*)\(', 'STDMETHOD(\g<1>)(', s1)

        if s2 != line:
            s3 = pattern.sub('', s2)
            print s3,
        else:
            print line,
