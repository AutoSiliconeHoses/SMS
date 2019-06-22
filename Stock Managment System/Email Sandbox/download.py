import poplib
import string, random
import rfc822
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def readMail():
    SERVER = "mail.autosiliconehoses.com"
    USER = "stock@autosiliconehoses.com"
    
    # connect to server
    server = poplib.POP3(SERVER)

    # login
    server.user(USER)
    server.pass_(PASSWORD)

    # list items on server
    resp, items, octets = server.list()

    for i in range(0,10):
        id, size = string.split(items[i])
        resp, text, octets = server.retr(id)

        text = string.join(text, "\n")
        file = StringIO.StringIO(text)

        message = rfc822.Message(file)

        for k, v in message.items():
            print(k, "=", v)

readMail()
