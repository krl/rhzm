from twisted.web.resource import Resource as WebResource
from default import *
from krdf import *

class Queries(WebResource):
  isLeaf = True
  template = environment.get_template('queries.xml')

  def render_GET(self, request):
    return self.template.render()

def init():
  return ["queries", Queries()]
