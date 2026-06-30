import asyncio
import websockets
PORT=7890
print("server is listening on PORT" + str(PORT))

async def echo(websocket, path):
    print("Client just connected")
    # Handle an incoming message
    while True:
        msg = "Pong: " + str(echo.cnt)
        await websocket.send(msg)

        echo.cnt += 1
        await asyncio.sleep(1) 

echo.cnt = 0

#
#    async for message in websocket:
#        print("Received msg from client: " + message)
#        #Echo to all connected clients
#        await websocket.send("Pong: " + message)

start_server = websockets.serve (echo, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
print("Don't expect to see this")


