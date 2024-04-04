from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import get_local_or_download_youtube_transcript
from dotenv import dotenv_values
import random


# Load environment variables
env_vars = dotenv_values()


# Define failed responses for chat endpoint
failed_responses = [
    "I'm sorry, I can't answer your query because you're not on a YouTube video.",
    "Oops! It seems like you're not on a YouTube video, so I can't provide an answer.",
    "Sorry, I can only answer queries related to YouTube videos. You might not be on one right now.",
    "Looks like you're not watching a YouTube video. Please try again when you're on one!",
    "Unfortunately, I can't provide an answer as you're not currently watching a YouTube video.",
    "Hmm, it seems you're not on a YouTube video. I'm unable to assist in this context.",
    "Sorry, I can't assist you right now. You're not watching a YouTube video.",
    "I'm unable to answer your query because it seems you're not on a YouTube video.",
    "I apologize, but I'm designed to answer queries related to YouTube videos only.",
    "It appears you're not on a YouTube video. I'm unable to provide assistance at the moment."
]

# Initialize API instance
app = FastAPI()

# Define request body model
class ChatRequest(BaseModel):
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
    # initialise response message to empty string
    response_message = ""

    try:
        # grab api key
        openai_api_key = env_vars["OPENAI_API_KEY"]
        print("OpenAI API key:", openai_api_key, flush=True)
        # fetch transcript from YouTube
        response = get_local_or_download_youtube_transcript(video_id)

        if(response["status"] == 200):
            text = response["transcript"] # transcript text

            # Split the text
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
            splits = text_splitter.split_text(text)

            # Build an index
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            vectordb = FAISS.from_texts(splits, embeddings)

            # Build a QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key),
                chain_type="stuff",
                retriever=vectordb.as_retriever()
            )

            # Ask a question!
            response_message = qa_chain.run(body.message)
    except Exception as e:
        print(f"Error: {e}", flush=True)
        response_message = random.choice(failed_responses)
    
    
    # Return the response
    return {"message": response_message}

# Define the route for the root endpoint "/"
@app.get("/")
async def default_response():
    """
    Default response for the root endpoint.
    """
    return {"Status": 200, "message": "API Setup"}