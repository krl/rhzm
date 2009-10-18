from krdf import *
from jinja2 import Environment, PackageLoader
from hashlib import sha1

rdf     = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
foaf    = Namespace("http://xmlns.com/foaf/0.1/")
nodetag = Namespace("tag:rymdkoloni.se,2009-07-13:")
rhzm    = Namespace("http://rymdkoloni.se/rhzm/0.1/")

environment = Environment(loader=PackageLoader('rhzm', 'templates'))

###################################################

class Renderable(Resource):
  def render(self):
    return environment.get_template(self.template).render(this=self)

from modules.foaf      import Person
from modules.dashboard import Comment

###################################################

environment.node_user = Person(nodetag.Kristoffer)

def hash(value):
  return sha1(value).hexdigest()
environment.globals['hash'] = hash

def comments(uri):
  return Comment.get(reply_to=uri)
environment.globals['comments'] = comments

