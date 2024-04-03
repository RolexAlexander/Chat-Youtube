from typing import Dict
import os
import yt_dlp
import whisper_timestamped as whisper
import torch


# Initialize device for torch
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def get_youtube_audio(video_id: str, save_dir: str = "./yt_audio") -> Dict[str, str]:
    """
    Downloads audio from a YouTube video.
    
    Args:
        video_id (str): The YouTube video ID.
        save_dir (str): Directory to save the audio file.
    
    Returns:
        dict: Status and message.
    """
    try:
        # Check if yt_dlp package is installed
        import yt_dlp
    except ImportError:
        raise ImportError("yt_dlp package not found, please install it with `pip install yt_dlp`")

    if os.path.exists(os.path.join(save_dir, f"{video_id}.m4a")):
        return {"status": 200, "message": "Audio downloaded"}
    else: 
        # Use yt_dlp to download audio given a YouTube video id
        ydl_opts = {
            "format": "m4a/bestaudio/best",
            "noplaylist": True,
            "outtmpl": os.path.join(save_dir, f"{video_id}.%(ext)s"),
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}],
        }

        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading " + f"https://www.youtube.com/watch?v={video_id}")
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

        # Check if audio file exists
        if os.path.exists(os.path.join(save_dir, f"{video_id}.m4a")):
            return {"status": 200, "message": "Audio downloaded"}
        else:
            return {"status": 500, "message": "Audio download failed"}

def setup(variant: str = "tiny") -> None:
    """
    Sets up the global variables `model` and `options` for the whisper API.
    
    Args:
        variant (str, optional): The variant of the model to load. Defaults to "tiny".
    """
    global model
    model = whisper.load_model("tiny", device=DEVICE)

# Initialize model
setup()

def transcribe(audio_file: str = None, language: str = "en") -> Dict[str, str]:
    """
    Transcribes audio from a given file or URL using the whisper library.
    
    Args:
        audio_file (str): Path to the audio file to transcribe.
        language (str): Language code to use for transcription. Default is "en".
    
    Returns:
        dict: A dictionary containing the transcription result.
    """
    if audio_file is None:
        return {'error': 'audio file path is required'}

    audio = whisper.load_audio(audio_file)
    result = whisper.transcribe(model, audio, language=language)

    # Remove the audio file after transcription
    os.remove(audio_file)

    return result

def get_and_save_youtube_transcript(video_id: str, transcript_dir: str = "./yt_transcript", audio_dir: str = "./yt_audio") -> Dict[str, str]:
    """
    Downloads YouTube audio, transcribes it, and saves the transcript and audio into separate directories.

    Args:
        video_id (str): The YouTube video ID.
        transcript_dir (str): Directory to save the transcript file.
        audio_dir (str): Directory to save the audio file.

    Returns:
        dict: Status, message, and transcript text.
    """

    # Download audio
    response = get_youtube_audio(video_id, audio_dir)

    if response["status"] == 200:
        # Transcribe audio
        response = transcribe(os.path.join(audio_dir, f"{video_id}.m4a"))

        if response:
            # Save transcript
            transcript_path = os.path.join(transcript_dir, f"{video_id}.txt")
            with open(transcript_path, "w") as f:
                f.write(response["text"])

            return {"status": 200, "message": "Transcript downloaded", "transcript": response["text"], "transcript_path": transcript_path}
        else:
            return {"status": 500, "message": "Transcription failed", "transcript": None}
    else:
        return {"status": 500, "message": "Audio download failed", "transcript": None}
    

def get_local_or_download_youtube_transcript(video_id: str, transcript_dir: str = "./yt_transcript", audio_dir: str = "./yt_audio") -> Dict[str, str]:
    """
    Retrieves the local YouTube transcript using its ID if it exists in the specified folder,
    otherwise downloads and saves it.

    Args:
        video_id (str): The YouTube video ID.
        transcript_dir (str): Directory where transcripts are stored. Defaults to "./yt_transcript".
        audio_dir (str): Directory where audio files are stored. Defaults to "./yt_audio".

    Returns:
        dict: Status, message, and transcript text.
    """
    # create directory if it doesn't exist
    if not os.path.exists(transcript_dir):
        os.makedirs(transcript_dir)

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    # Check if transcript file exists locally
    local_transcript_path = os.path.join(transcript_dir, f"{video_id}.txt")
    if os.path.exists(local_transcript_path):
        with open(local_transcript_path, "r") as f:
            transcript_text = f.read()
        return {"status": 200, "message": "Transcript found locally", "transcript": transcript_text, "transcript_path": local_transcript_path}
    
    # If transcript not found locally, download audio and transcribe
    else:
        # Download audio
        response = get_youtube_audio(video_id, audio_dir)

        if response["status"] == 200:
            # Transcribe audio
            response = transcribe(os.path.join(audio_dir, f"{video_id}.m4a"))

            if response:
                # Save transcript
                transcript_text = response["text"]
                with open(local_transcript_path, "w") as f:
                    f.write(transcript_text)

                return {"status": 200, "message": "Transcript downloaded", "transcript": transcript_text, "transcript_path": local_transcript_path}
            else:
                return {"status": 500, "message": "Transcription failed", "transcript": None}
        else:
            return {"status": 500, "message": "Audio download failed", "transcript": None}