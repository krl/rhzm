# -*- encoding:utf-8 -*-
import os, re

from twisted.web.resource import Resource as WebResource
from twisted.application import internet
from twisted.web import server
from twisted.web.static import File
from twisted.internet import reactor

from default import *

from krdf import *

################################################

class WebInterface(WebResource):
  def getChild(self, name, request):
    return WebResource.getChild(self, name, request)

class Renderer(WebResource):
  isLeaf = True
  body = environment.get_template('body.xml')

  def render_GET(self, request):
    if modulelist.has_key(request.path):
      return self.body.render(modulelist=modulelist, content=modulelist[request.path].render_GET(request)).encode('utf-8')

  def render_POST(self, request):
    if modulelist.has_key(request.path):
      return self.body.render(modulelist=modulelist, content=modulelist[request.path].render_POST(request)).encode('utf-8')

main = WebInterface()
renderer = Renderer()
main.putChild('inc', File("inc"))

modulelist = {}
valid = re.compile("[^_].*\.py$")
for x in os.listdir("modules"):
  if valid.match(x):
    imp = __import__("modules."+x[:-3])
    mod = getattr(imp, x[:-3]).init()
    modulelist["/"+mod[0]] = mod[1]
    main.putChild(mod[0], renderer)

################################################

def getWebService():
  return internet.TCPServer(9000, server.Site(main))
