# Django VIN Extractor & Firebase Storage

A real-time backend API built with Django and Django Channels that:

- **Receives** base64-encoded car images over WebSockets
- **Extracts** the Vehicle Identification Number (VIN) using an OpenCV-based model
- **Broadcasts** the latest processed image to connected clients
- **Stores** a full history of detected VINs in a Firebase Firestore database
- **Serves** a static HTML dashboard displaying the most recent parked car image and a list of all stored VINs

---

## ️ Tech Stack

- **Backend:** Django, Django Channels (WebSocket support)
- **Computer Vision:** OpenCV, EasyOCR
- **Data Storage:** Firebase Firestore (via Web client SDK)
- **Frontend:** Static HTML/JavaScript (WebSocket & Firestore integration)
- **Python:** 3.8+

---

## Features

1. **WebSocket Image Ingestion**  
   Clients send base64-encoded images to `/ws/image/`.

2. **VIN Recognition**  
   An OpenCV + EasyOCR pipeline detects and reads the VIN on each frame.

3. **Real-Time Broadcasting**  
   Processed frames (edge-detected overlays) are pushed to all connected clients instantly.

4. **Persistent VIN History**  
   Each detected VIN string is written to a Firestore collection `cars`.

5. **Dashboard**  
   A static HTML page displays:
   - The most recent processed image
   - A “Load Parked Cars” button that fetches every stored VIN from Firestore

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/django-vin-extractor.git
cd django-vin-extractor
```

### 2. Create a Python virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the development server

```bash
daphne mysite.asgi:application
```

> **Note:** The WebSocket endpoint is available at `ws://localhost:8000/ws/image/`.

### 5. Serve the static dashboard

```

open `http://localhost:8000`

---

## 🔄 Usage Workflow

1. **Client** captures or loads an image and sends JSON `{ image: '<base64-data>' }` to the WebSocket.
2. **Django Channels** receives it, runs the OpenCV+EasyOCR pipeline to detect the VIN.
3. The **processed frame** is edge-detected and broadcast back to all WebSocket clients.
4. Django writes the detected VIN string into Firestore under the `cars` collection.
5. On the **dashboard**, click **Load Parked Cars** to fetch and display the full list of VINs.

---

```
