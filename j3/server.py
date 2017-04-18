#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://localhost:8080

from twisted.internet import reactor, endpoints
from twisted.web import server, resource

from .db import SitesDb

# external html form
FORMFILE = 'request_form.html'

CSS_FILE = 'server.css'

# output encoding
ENCODING = 'utf-8'

BASEFILE = 'Sites.sqlite'


class RequestServer(resource.Resource):
    isLeaf = True

    def __init__(self, basefile):
        super(RequestServer, self).__init__()
        self.base = SitesDb(basefile)

    # noinspection PyPep8Naming,PyMethodMayBeStatic
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
        # pprint.pprint(request.__dict__)
        criterium = dict(xmin=float(request.args.get(b'xmin', [56])[0]),
                         xmax=float(request.args.get(b'xmax', [60])[0]),
                         ymin=float(request.args.get(b'ymin', [21])[0]),
                         ymax=float(request.args.get(b'ymax', [25])[0]), )
        request.setHeader(b"content-type", b"text/html")
        return self.contents(criterium)

    # noinspection PyMethodMayBeStatic
    def table(self, sites):
        """Return html code for the list of Sites in a Table."""
        fields = set(sites[0].keys())
        for site in sites:
            fields &= site.keys()

        contents = '<font size="-1">\n'
        contents += '<table border="1">\n'
        contents += '\t<tr>\n'
        for key in sorted(fields):
            contents += '\t\t<th>{}</th>\n'.format(key)
        contents += '\t</tr>\n'

        for n, site in enumerate(sites):
            contents += '\t<tr>\n'
            for key in sorted(fields):
                contents += '\t\t<td class={}>{}</td>\n'.format('odd' if n % 2 else 'even', site.get(key, ''))
            contents += '\t</tr>\n'

        contents += '</table>\n'
        contents += '</font>\n'
        return contents

    def select(self, c):
        """Return the list of sites matching the criterium."""
        x = (c['xmin'] + c['xmax']) / 2
        dx = c['xmax'] - c['xmin']
        y = (c['ymin'] + c['ymax']) / 2
        dy = c['ymax'] - c['ymin']
        return self.base.get_by_loc(y, x, dy, dx)
        # return base.get_all()

    # noinspection PyMethodMayBeStatic
    def css(self):
        txt = "<style type='text/css'>"
        txt += open(CSS_FILE).read()
        txt += "</style>"
        return txt

    def contents(self, criterium):
        contents = '<html><body>'
        title = 'extrait de la base'
        contents += '<head><meta charset="UTF-8"><title>{}</title></head>'.format(title)
        contents += self.css()
        sites = self.select(criterium)
        if len(sites) == 0:
            contents += 'no match'
        else:
            contents += self.table(sites)
        contents += '</body></html>'
        return contents.encode('utf-8')


if __name__ == '__main__':
    rs = RequestServer(BASEFILE)
    endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(rs))
    reactor.run()
