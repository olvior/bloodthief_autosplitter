from aiohttp import web
import json

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

ws = None
async def wshandle(request):
    global ws
    ws = web.WebSocketResponse()
    await ws.prepare(request)
   
    print("Connected")
    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            #print(msg)
            pass
        elif msg.type == web.WSMsgType.close:
            break
    return ws


async def split():
    message = json.dumps({"command": "split"})
    await ws.send_json({"command": "split"})

async def start():
    message = json.dumps({"command": "reset"})
    await ws.send_json({"command": "reset"})
    #print(await websocket.recv())

    message = json.dumps({"command": "start"})
    await ws.send_json({"command": "start"})
    #print(await websocket.recv())

async def set_game_time(game_time):
    message = json.dumps({"command": "setGameTime", "time": str(game_time)})
    await ws.send_json({"command": "setGameTime", "time": str(game_time)})
    #print(await websocket.recv())


app = web.Application()
app.add_routes([web.get('/', wshandle)])

if __name__ == '__main__':
    web.run_app(app, port=8001)

