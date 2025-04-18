import asyncio
import websockets
import base64
import json
import numpy as np
import cv2

# Replace with your WebSocket server URL
WS_SERVER = "ws://127.0.0.1:8000/ws/image/"

async def send_image():
    # Load image (simulate camera capture)
    image_path = "test.jpg"  # Use a test image
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()   

    # Encode image to gbase64
    b64_image = base64.b64encode(image_bytes).decode('utf-8')

    # Create JSON payload
    payload = {
        "image": b64_image
    }

    async with websockets.connect(WS_SERVER) as websocket:
        print("[+] Connected to server")
        await websocket.send(json.dumps(payload))
        print("[>] Image sent")

        # Wait for response
        response = await websocket.recv()
        print("[<] Received response")

        # Parse response and decode image
        data = json.loads(response)
        processed_b64 = data.get("processed_image")

        if processed_b64:
            # Decode the processed image
            processed_bytes = base64.b64decode(processed_b64)
            nparr = np.frombuffer(processed_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Show the image
            cv2.imshow("Processed Image", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("No image received in response")

if __name__ == "__main__":
    asyncio.run(send_image())
