# -*- encoding:utf-8 -*-
from twisted.web.resource import Resource as WebResource
from default import *
from krdf import *

from foaf import Person

class Note(Renderable):
  type      = Single(rdf.type, rhzm.Note, uri)
  maker     = Single(foaf.maker, None, Person)
  body      = Single(rhzm.body)
    
  template  = "note.xml"
    
class Comment(Renderable):
  type      = Single(rdf.type, rhzm.Comment, uri)
  maker     = Single(foaf.maker, None, Person)
  reply_to  = Single(rhzm.reply_to, None, uri)
  body      = Single(rhzm.body)
      
  template  = "note.xml"

class Dashboard(WebResource):
  isLeaf = True
  template = environment.get_template('dashboard.xml')

  def render_POST(self, request):
    body = request.args["body"][0]
    if request.args["type"][0] == "comment":
      comment = Comment(makeuri(str(nodetag)+body))
      comment.body = body
      comment.maker = environment.node_user
      comment.reply_to = request.args["reply_to"][0]
      comment.commit()      
    else:
      note = Note(makeuri(str(nodetag)+body))
      note.body  = body
      note.maker = environment.node_user
      note.commit()
    request.redirect("/dashboard")
    request.finish()
        
  def render_GET(self, request):
    notes = Note.get()
    notes.reverse()
    return self.template.render(notes=notes)

def init():
  return ["dashboard", Dashboard()]
