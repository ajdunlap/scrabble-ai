import cherrypy
import os
from genshi.template import TemplateLoader
import board
from ws4py.server.cherrypyserver import WebSocketPlugin,WebSocketTool
from ws4py.websocket import WebSocket

class ScrabbleWebSocket(WebSocket):
    def received_message(self, message):
        print("Got something!")
        print(message)

class Root:
    def __init__(self):
        self.bs = board.BoardState(board.make_official_scrabble_board())

    @cherrypy.expose
    def index(self):
        tmpl = loader.load('index.html')
        return tmpl.generate(title="Scrabble!",bs = self.bs,rack=list("RLSTNEX")).render("html",doctype="html")

    @cherrypy.expose
    def ws(self):
        handler = cherrypy.request.ws_handler

def main():
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
        'server.socket_port': 9000,
    })

    WebSocketPlugin(cherrypy.engine).subscribe()

    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(Root(), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        },
        '/ws' : {'tools.websocket.on': True,
                 'tools.websocket.handler_cls': ScrabbleWebSocket}

    })

loader = TemplateLoader(
        os.path.join(os.path.dirname(__file__),'templates'),
        auto_reload=True)

main()
