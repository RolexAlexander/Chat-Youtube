from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

# Initialize API instance
app = FastAPI()

# Define request body model
class ChatRequest(BaseModel):
    message: str

# Define response model
class ChatResponse(BaseModel):
    message: str

# Define route with path parameter and request body
@app.post("/chat/{video_id}")
async def chat(body: ChatRequest, video_id: str = Path(..., title="Video ID"), ):
    """
    Function that takes a YouTube video ID and message,
    and returns a response based on the video contents.

    Args:
        video_id: ID of the YouTube video.
        body: JSON body containing the message.

    Returns:
        JSON response with a message.
    """
    # Process the message and generate a response
    response_message = "Response Returned. Just need to add the FastAPI stuff."
    
    # Return the response
    return {"message": response_message}

# Define the route for the root endpoint "/"
@app.get("/")
async def default_response():
    """
    Default response for the root endpoint.
    """
    return {"Status": 200, "message": "API Setup"}