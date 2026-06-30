import websockets
import asyncio
import sys
import time                                    
#
#async def listen():
#    url = "ws://127.0.0.1:7890"
#    # connect with server
#    # "
#    async with websockets.connect(url) as ws:
#        #send a greeting msg
#        while True:
#            if len(player) == 0:
#                await ws.send("Hello world!" + str(listen.count))
#                listen.count += 1
#                data = await ws.recv()
#                player.append(data)
#            #print(msg)
#listen.count = 0
#start the connection
#asyncio.get_event_loop().run_until_complete(listen())

#if __name__ == '__main__':
#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)
#try:
#    asyncio.get_event_loop().run_until_complete(listen())
#
#    #asyncio.run(listen())
#except KeyboardInterrupt:
#    pass
#if sys.version_info < (3, 10):
#    loop1 = asyncio.get_event_loop()
#else:
#    try:
#        loop1 = asyncio.get_running_loop()
#    except RuntimeError:
#        loop1 = asyncio.new_event_loop()
#
#    asyncio.set_event_loop(loop1)
#    loop1.run_until_complete(listen())

async def main():
    url = "ws://127.0.0.1:7890"
    # connect with server
    # "
    async with websockets.connect(url) as ws:
        go = True
        numTimeouts = 0
        while go == True:
            if len(main.player) == 0:
                try:
                    data = await asyncio.wait_for(ws.recv(), 0.1)
                    main.player.append(data)
                    #print("len(main.player)", len(main.player), data)
                except:
                    #print("rx timeout")
                    numTimeouts += 1
            else:
                data = main.player.pop(0) 
                print(data, ": ", numTimeouts)

main.player = []
##############


##############
asyncio.run(main())

print("hello")
