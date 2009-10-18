from twisted.application import service
import rhzm

application = service.Application("Rhzm")

service = rhzm.getWebService()
service.setServiceParent(application)
