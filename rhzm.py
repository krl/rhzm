# -*- encoding:utf-8 -*-
from twisted.web.resource import Resource as WebResource
from twisted.web import server
from twisted.web.static import File
from twisted.internet import reactor

from hashlib import sha1
from krdf import *
from jinja2 import Environment, PackageLoader

################################################

env = Environment(loader=PackageLoader('rhzm', 'templates'))

def hash(value):
  return sha1(value).hexdigest()
env.globals['hash'] = hash

def comments(uri):
  return Comment.get(reply_to=uri)
env.globals['comments'] = comments
body = env.get_template('body.xml')

################################################

rdf     = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
foaf    = Namespace("http://xmlns.com/foaf/0.1/")
nodetag = Namespace("tag:rymdkoloni.se,2009-07-13:")
rhzm    = Namespace("http://rymdkoloni.se/rhzm/0.1/")

class Renderable(Resource):
  def render(self):
    return self.template.render(this=self)

class Person(Renderable):
  type      = Single(rdf.type, foaf.Person, uri)
  name      = Single(foaf.name)
  depiction = Single(foaf.depiction)

class Note(Renderable):
  type      = Single(rdf.type, rhzm.Note, uri)
  maker     = Single(foaf.maker, None, Person)
  body      = Single(rhzm.body)

  template  = env.get_template('note.xml')

class Comment(Renderable):
  type      = Single(rdf.type, rhzm.Comment, uri)
  maker     = Single(foaf.maker, None, Person)
  reply_to  = Single(rhzm.reply_to, None, uri)
  body      = Single(rhzm.body)

  template  = env.get_template('note.xml')

node_user = Person(nodetag.Kristoffer)

################################################

class WebInterface(WebResource):
  def getChild(self, name, request):
    return WebResource.getChild(self, name, request)

main = WebInterface()
main.putChild('inc', File("inc"))

class Index(WebResource):
  isLeaf = True
  template = env.get_template('startpage.xml')
  def render_GET(self, request):
    return body.render(content=self.template.render()).encode('utf-8')

main.putChild('', Index())

class Dump(WebResource):
  isLeaf = True
  template = env.get_template('dump.xml')
  def render_GET(self, request):
    content = self.template.render(triples=dumpdb())
    return body.render(content=content).encode('utf-8')

main.putChild('dump', Dump())

class Foaf(WebResource):
  isLeaf = True
  template = env.get_template('foaf.xml')

  def render_GET(self, request):
    return body.render(content=self.template.render(
        person=node_user)).encode('utf-8')

  def render_POST(self, request):
    node_user.name=request.args["name"][0]
    node_user.depiction=request.args["depiction"][0]
    node_user.commit()
    request.redirect("/foaf")
    request.finish()

main.putChild('foaf', Foaf())

class Dashboard(WebResource):
  isLeaf = True
  template = env.get_template('dashboard.xml')

  def render_POST(self, request):
    body = request.args["body"][0]
    if request.args["type"][0] == "comment":
      comment = Comment(makeuri(str(nodetag)+body))
      comment.body = body
      comment.maker = node_user
      comment.reply_to = request.args["reply_to"][0]
      comment.commit()      
    else:
      note = Note(makeuri(str(nodetag)+body))
      note.body  = body
      note.maker = node_user
      note.commit()
    request.redirect("/dashboard")
    request.finish()

  def render_GET(self, request):
    notes = Note.get()
    notes.reverse()
    content = self.template.render(notes=notes)    
    return body.render(content=content).encode('utf-8')

main.putChild('dashboard', Dashboard())

site = server.Site(main)
reactor.listenTCP(9000, site)
reactor.run()
