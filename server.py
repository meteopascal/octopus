#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://localhost:8080

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
import pprint
from db import SitesDb

# external html form
FORMFILE = 'request_form.html'

# output encoding
ENCODING = 'utf-8'

base = SitesDb('Sites.sqlite')


class RequestServer(resource.Resource):
    isLeaf = True

    # noinspection PyPep8Naming
    def render_GET(self, request):
        """La demande : un formulaire html lu dans un fichier externe."""
        request.setHeader(b"content-type", b"text/html")
        content = ''.join(open(FORMFILE).readlines()).encode(ENCODING)
        return content

    # noinspection PyPep8Naming
    def render_POST(self, request):
        """La réponse:
           * on récupère les doonnées du formulaire
           * on interroge la base pour avoir les données
           * on les met en forme en html
        """
        pprint.pprint(request.__dict__)
        criterium = dict(
            xmin=float(request.args.get(b'xmin', [56])[0]),
            xmax=float(request.args.get(b'xmax', [60])[0]),
            ymin=float(request.args.get(b'ymin', [21])[0]),
            ymax=float(request.args.get(b'ymax', [25])[0]),
        )
        request.setHeader(b"content-type", b"text/html")
        return self.contents(criterium)

    def table(self, sites):
        """Return html code for the list of Sites in a Table.
        <table>
            <th>
                <td>header1</td>
                <td>header2</td>
            </th>
            <tr>
                <td>value1</td>
                <td>value2</td>
            </tr>
        </table>
        """
        fields = set(sites[0].keys())
        for site in sites:
            fields &= site.keys()
        print(fields)

        contents = '<font size="-1">\n'
        contents += '<table border="1">\n'
        contents += '\t<tr>\n'
        for key in sorted(fields):
            contents += '\t\t<th>{}</th>\n'.format(key)
        contents += '\t</tr>\n'

        for n, site in enumerate(sites):
            contents += '\t<tr>\n'
            for key in sorted(fields):
                print(key, site.get(key, ''))
                contents += '\t\t<td class={}>{}</td>\n'.format('odd' if n % 2 else 'even', site.get(key, ''))
            contents += '\t</tr>\n'

        contents += '</table>\n'
        contents += '</font>\n'
        return contents

    def select(self, c):
        """Return the list of sites matching the criterium."""
        x = (c['xmin'] + c['xmax'])/2
        dx = c['xmax'] - c['xmin']
        y = (c['ymin'] + c['ymax'])/2
        dy = c['ymax'] - c['ymin']
        return base.get_by_loc(y, x, dy, dx)
        # return base.get_all()

    def contents(self, criterium):
        contents = '<html><body>'
        contents += """
        <style type='text/css'>
table {
  font-size: 12;
  font-family: verdana;
}

td.even {
  color: blueviolet;
}

td.odd {
  color: orange;
}
        </style>
        """
        sites = self.select(criterium)
        if len(sites) == 0:
            contents += 'no match'
        else:
            contents += self.table(sites)
        contents += '</body></html>'
        return contents.encode('utf-8')


if not False:
    endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(RequestServer()))
    reactor.run()
else:
    res = base.get_all()
    for line in res:
        print()
        pprint.pprint(line)
