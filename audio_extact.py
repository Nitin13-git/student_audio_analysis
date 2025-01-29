import ffmpeg
import os

def extract_audio_from_video(input_video_path):
    """
    Extracts audio from an input video (mp4) file and saves it in an 'audio' subdirectory.
    
    Parameters:
        input_video_path (str): Path to the input video file (e.g., .mp4).
    
    Returns:
        output_audio_path (str): Path to the extracted audio file.
    """
    try:
        # Get the directory and filename of the input video
        input_dir = os.path.dirname(input_video_path)
        input_filename = os.path.basename(input_video_path)
        
        # Create 'audio' subdirectory if it doesn't exist
        audio_dir = os.path.join(input_dir, 'audio')
        os.makedirs(audio_dir, exist_ok=True)
      

        # Generate output audio path
        base, _ = os.path.splitext(input_filename)
        output_audio_path = os.path.join(audio_dir, f"{base}.mp3")
        
        # Use FFmpeg to extract audio from the video
        (
            ffmpeg
            .input(input_video_path)
            .output(output_audio_path, **{'q:a': 0, 'map': 'a'})
            .global_args('-loglevel', 'quiet')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        
        print(f"Audio successfully extracted to {output_audio_path}")
        return output_audio_path
    
    except ffmpeg.Error as e:
        print(f"Error occurred while extracting audio: {e.stderr.decode()}")
        return None









