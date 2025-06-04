from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.websocket("/ws-cube")
async def websocket_cube(websocket: WebSocket):
    await websocket.accept()
    try:
        # Read the cube.obj file in binary mode
        with open("models/model.zip", "rb") as file:
            cube_data = file.read()

        # Send the binary data through the WebSocket
        await websocket.send_bytes(cube_data)
    except Exception as e:
        # Send an error message if something goes wrong
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        print("done!")
        # await websocket.close()


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})

def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}