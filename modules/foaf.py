from twisted.web.resource import Resource as WebResource
from default import *
from krdf import *

class Person(Renderable):
  type      = Single(rdf.type, foaf.Person, uri)
  name      = Single(foaf.name)
  depiction = Single(foaf.depiction)

class Foaf(WebResource):
  isLeaf = True
  template = environment.get_template('foaf.xml')

  def render_GET(self, request):
    return self.template.render(person=environment.node_user)

  def render_POST(self, request):
    environment.node_user.name=request.args["name"][0]
    environment.node_user.depiction=request.args["depiction"][0]
    environment.node_user.commit()
    request.redirect("/foaf")
    request.finish()

def init():
  return ["foaf", Foaf()]
