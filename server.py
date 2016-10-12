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

    def render_GET(self, request):
        """La demande : un formulaire html lu dans un fichier externe."""
        request.setHeader(b"content-type", b"text/html")
        content = ''.join(open(FORMFILE).readlines()).encode(ENCODING)
        return content

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

    def contents(self, criterium):
        content = '<html><body>'
        content += pprint.pformat(criterium)
        content += '</body></html>'
        # return content.encode("ascii")
        return content.encode('utf-8')

if False:
    endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(RequestServer()))
    reactor.run()

res = base.getall()
for line in res:
    print()
    pprint.pprint(line)