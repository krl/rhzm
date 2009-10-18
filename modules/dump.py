from twisted.web.resource import Resource as WebResource
from default import *
from krdf import *

class Dump(WebResource):
  isLeaf = True
  template = environment.get_template('dump.xml')

  def render_GET(self, request):
    return self.template.render(triples=dumpdb())

def init():
  return ["dump", Dump()]
