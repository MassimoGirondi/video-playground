import aiohttp
from aiohttp import TCPConnector
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRecorder
from aiortc.contrib.signaling import TcpSocketSignaling
import time


class TimeCodeTrack(VideoStreamTrack):
    pass


    # async def attach(self, plugin_name: str) -> JanusPlugin:
    #     message = {
    #         "janus": "attach",
    #         "plugin": plugin_name,
    #         "transaction": transaction_id(),
    #     }
    #     async with self._http.post(self._session_url, json=message) as response:
    #         data = await response.json()
    #         assert data["janus"] == "success"
    #         plugin_id = data["data"]["id"]
    #         plugin = JanusPlugin(self, self._session_url + "/" + str(plugin_id))
    #         self._plugins[plugin_id] = plugin
    #         return plugin

    # async def create(self):
    #     self._http = aiohttp.ClientSession()
    #     message = {"janus": "create", "transaction": transaction_id()}
    #     async with self._http.post(self._root_url, json=message) as response:
    #         data = await response.json()
    #         assert data["janus"] == "success"
    #         session_id = data["data"]["id"]
    #         self._session_url = self._root_url + "/" + str(session_id)

    #     self._poll_task = asyncio.ensure_future(self._poll())

    # async def destroy(self):
    #     if self._poll_task:
    #         self._poll_task.cancel()
    #         self._poll_task = None

    #     if self._session_url:
    #         message = {"janus": "destroy", "transaction": transaction_id()}
    #         async with self._http.post(self._session_url, json=message) as response:
    #             data = await response.json()
    #             assert data["janus"] == "success"
    #         self._session_url = None

    #     if self._http:
    #         await self._http.close()
    #         self._http = None

    # async def _poll(self):
    #     while True:
    #         params = {"maxev": 1, "rid": int(time.time() * 1000)}
    #         async with self._http.get(self._session_url, params=params) as response:
    #             data = await response.json()
    #             if data["janus"] == "event":
    #                 plugin = self._plugins.get(data["sender"], None)
    #                 if plugin:
    #                     await plugin._queue.put(data)
    #                 else:
    #                     print(data)





     # await pc.setLocalDescription(await pc.createOffer())
     # print(pc.localDescription)
     #await signaling.send(pc.localDescription)


class HTTPSSignaling:
    def __init__(self, url="https://localhost:8080", insecure=False ):
        self._url = url
        self._server = None
        self._reader = None
        self._writer = None
        self._client = aiohttp.ClientSession(connector=TCPConnector(ssl= not insecure))

    async def connect(self):
        pass

    async def _connect(self, server):
        print("_connect")
        # if self._writer is not None:
        #     return

        # if server:
        #     connected = asyncio.Event()

        #     def client_connected(reader, writer):
        #         self._reader = reader
        #         self._writer = writer
        #         connected.set()

        #     self._server = await asyncio.start_server(
        #         client_connected, host=self._host, port=self._port
        #     )
        #     await connected.wait()
        # else:
        #     self._reader, self._writer = await asyncio.open_connection(
        #         host=self._host, port=self._port
        #     )

    async def close(self):
        print("close")
        if self._writer is not None:
            await self.send(BYE)
            self._writer.close()
            self._reader = None
            self._writer = None
        if self._server is not None:
            self._server.close()
            self._server = None

    async def receive(self):
        print("receive")
        answer = await self.last_response
        #return answer["sdp"]
        #return self.last_response

    async def send(self, descr):
        print("send")
        data = {"sdp": descr.sdp, "type": descr.type, "video_transform": "passthrough"}
        async with self._client.post(self._url+"/offer", json = data) as response:
            self.last_response = response.json()
        #print("got response", self.last_response)

        # async with self._client.post(self._url+"/offer", json = data) as response:
        #     response = await response.json()

        # await self._connect(True)
        # data = object_to_string(descr).encode("utf8")
        # self._writer.write(data + b"\n")

class WebRTCClient():
    def __init__(self, args):
        self.args = args
        self.pc = RTCPeerConnection()
        #self.signaling = TcpSocketSignaling("192.168.2.27", 8080)
        self.signaling  = HTTPSSignaling("https://192.168.2.27:8080", True)
        self.source_track = TimeCodeTrack()

    async def run(self):
        await self.offer()
    # async def run(self, pc, player, recorder, signaling):
    #      print("HEY")
    #      # # connect signaling
    #      # await signaling.connect()
    #      # pc.addTrack(TimeCodeTrack())

    #      # offer = await pc.createOffer()
    #      # await pc.setLocalDescription(offer)

    #      # data = {"sdp": offer.sdp, "type": "offer", "video_transform": self.args.transform}
    #      # async with self.httpclient.post(self.args.url+"/offer", json = data) as response:
    #      #        response = await response.json()
    #      #        print(data)

    #      # while True:
    #      #        obj = await signaling.receive()
    #      #        print(obj)

    async def offer(self):

        @self.pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                print("ON MESSAGE")
                if isinstance(message, str) and message.startswith("ping"):
                    channel.send("pong" + message[4:])

        @self.pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("iceconnectionstatechange", self.pc.iceConnectionState)
            # if pc.iceConnectionState == "failed":
            #     await pc.close()
            #     pcs.discard(pc)

        @self.pc.on("track")
        def on_track(track):
            print("track", track)
            self.pc.addTrack(track)
            if track.kind == "audio":
                print("No audio!")
                self.pc.addTrack(player.audio)
            elif track.kind == "video":
                self.pc.addTrack(self.source_track.video)



        await self.signaling.connect()
        self.pc.addTrack(TimeCodeTrack())
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)

        await self.signaling.send(self.pc.localDescription)
        await self.source_track.recv()
        offer = await self.signaling.receive()
        print("GOT OFFER", offer)
        while True:
            time.sleep(1)
        # data = {"sdp": offer.sdp, "type": "offer", "video_transform": self.args.transform}
        # async with self.httpclient.post(self.args.url+"/offer", json = data) as response:
        #     answer = await response.json()
        #     print(answer)
        #     self.pc.state = "have-remote-offer"
        #     await self.pc.setRemoteDescription(RTCSessionDescription(answer["sdp"], answer["type"]))
