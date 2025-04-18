import base64
import cv2
import numpy as np
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ImageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add this socket to a group so we can broadcast
        await self.channel_layer.group_add("image_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove socket from group
        await self.channel_layer.group_discard("image_group", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Parse incoming JSON
        data = json.loads(text_data)

        # Decode incoming base64 image
        b64_image = data.get('image')
        image_bytes = base64.b64decode(b64_image)

        # Convert to OpenCV image and process
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        # Encode processed image back to base64
        _, buffer = cv2.imencode('.jpg', edges)
        processed_b64 = base64.b64encode(buffer).decode('utf-8')

        # Broadcast the processed image to all group members
        await self.channel_layer.group_send(
            "image_group",
            {
                "type": "broadcast_image",
                "b64": processed_b64,
            }
        )

    async def broadcast_image(self, event):
        # Handler for messages sent to the group
        await self.send(text_data=json.dumps({
            'processed_image': event['b64'],
            'status': 'processed'
        }))
