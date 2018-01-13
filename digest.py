from bs4 import BeautifulSoup

import pdfkit

import glob
import sys
import os

TEMPLATE = open('template.html', 'rb').read()
BODY_TEMPLATE = '''<div>
    <h1>$TITLE$</h1>
    <table>
        $DATA$
    </table>
</div>
'''

def _extract_data(f):
    soup = BeautifulSoup(f.read(), 'lxml')
    title = soup.find('div', {'class': 'BookName'}).text

    data = ''
    index = 0
    latin = soup.findAll('span', {'class': 'Latin'})
    english = soup.findAll('span', {'class': 'Jerome'})
    for ls, es in zip(latin, english):
        l = ls.text.strip()
        e = es.text.strip()

        if index == 0:
            bclass = 'index1'
            if l:
                l = l[0].title() + l[1:]

        else:
            bclass = 'index2'

        index += 1
        data += '''<tr>
            <td>
                <p><b class="%s">%d</b> %s</p>
            </td>
            <td>
                <p><b class="index3">%d</b> %s</p>
            </td>
        </tr>
''' % (bclass, index, l, index, e)

    body = BODY_TEMPLATE.replace('$TITLE$', title).replace('$DATA$', data)
    return title, body

def handle_path(path):
    num = len(glob.glob(path + '/*.htm'))
    print path, num

    data = ''
    for i in xrange(num):
        with open(path + '/%d.htm' % (i + 1), 'rb') as f:
            title, pagedata = _extract_data(f)
            data += pagedata

    bookname = title.rsplit('-', 1)[0].strip()
    pdfkit.from_string(TEMPLATE.replace('$BODY$', data), '%s/%s.pdf' % (path, bookname))

for root, dirs, _ in os.walk('original'):
    if not dirs:
        handle_path(root)
