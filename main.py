
import json
from base64 import b64decode

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.position import update

# =========================================================================== #

app = FastAPI()

# --------------------------------------------------------------------------- #

@app.post('/update')
async def update_positions(request: Request):
    try:
        envelope = await request.json()

        message = envelope.get('message', {})
        
        data = b64decode(message.get('data')).decode('utf-8')
        data = json.loads(data)

        update(data)

        return 204

    except Exception as ex:
        return JSONResponse(status_code=500, content={'error': str(ex)})

# =========================================================================== #