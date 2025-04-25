import json
from easyocr import Reader
import base64
import numpy as np
import cv2
from easyocr import Reader
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
        car = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # read vin code

        car = cv2.resize(car, (800, 600))
        gray = cv2.cvtColor(car, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blur, 10, 200)
        cont, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cont = sorted(cont, key=cv2.contourArea, reverse=True)[:5]

        plate_cnt = None
        for c in cont:
            arc = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * arc, True)
            if len(approx) == 4:
                plate_cnt = approx
                break

        if plate_cnt is not None:
            x, y, w, h = cv2.boundingRect(plate_cnt)
            plate = gray[y:y + h, x:x + w]
        else:
            plate = gray

        reader = Reader(['en'], gpu=False, verbose=False)
        detection = reader.readtext(plate)

        if len(detection) == 0:
            text = "Impossible to read the text from the license plate"
        else:
            cv2.drawContours(car, [plate_cnt], -1, (0, 255, 0), 3)
            text = f"{detection[0][1]}"
            cv2.putText(car, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            print(f"\n\n detected 2 {text}")

#################################################

        # edges = cv2.Canny(car, 100, 200)

        # Encode processed image back to base64
        _, buffer = cv2.imencode('.jpg', car)
        processed_b64 = base64.b64encode(buffer).decode('utf-8')

        # Broadcast the processed image to all group members
        await self.channel_layer.group_send(
            "image_group",
            {
                "type": "broadcast_image",
                "b64": processed_b64,
                "carNum":text,
            }
        )

    async def broadcast_image(self, event):
        # Handler for messages sent to the group
        await self.send(text_data=json.dumps({
            'processed_image': event['b64'],
            'status': 'processed',
            'carNum':event['carNum'],
            # 'carNum':car

        }))
