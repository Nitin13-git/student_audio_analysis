# main.py
import os
import logging
import re
from typing import List
from audio_extact import extract_audio_from_video
from trans_utils import transcribe_audio_with_openai
from html_utils import create_html_analysis, save_html_analysis
from audio_analysis import AudioAnalyzer, SentenceAnalysis

def analyze_audio_content(transcription: str) -> tuple[str, List[SentenceAnalysis]]:
    """Analyze audio content and return overall analysis and sentence-level analysis"""
    try:   
        analyzer = AudioAnalyzer()
        
      
        overall_analysis = analyzer.get_overall_analysis(transcription)
        if not overall_analysis:
            return None
            
        sentences = re.split(r'[.!?]+', transcription)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        sentences_analysis = []
        for sentence in sentences:
            analysis = analyzer.analyze_sentence(sentence)
            if analysis:
                sentences_analysis.append(analysis)
        
        return overall_analysis, sentences_analysis
        
    except Exception as e:
        logging.error(f"Error in audio content analysis: {str(e)}")
        return None

def main():
    # Set up logging
    logging.basicConfig(
        filename='audio_analysis.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Define input folder path
    folder_path = 'Input Video'
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.mkv', '.avi'))]
    
    if not video_files:
        logging.warning("No video files found in the specified folder.")
        return
    
    for video_file in video_files:
        input_video_path = os.path.join(folder_path, video_file)
        logging.info(f"Processing video: {input_video_path}")
        
        # Extract audio
        audio_file_path = extract_audio_from_video(input_video_path)
        if not audio_file_path:
            logging.error(f"Audio extraction failed for video: {video_file}")
            continue
        
        # Transcribe audio
        transcription = transcribe_audio_with_openai(audio_file_path)
        if not transcription:
            logging.error(f"Transcription failed for video: {video_file}")
            continue
        
        # Analyze transcription
        analysis_result = analyze_audio_content(transcription)
        if not analysis_result:
            logging.error(f"Analysis failed for video: {video_file}")
            continue
            
        overall_analysis, sentences_analysis = analysis_result
        
        student_name = os.path.splitext(video_file)[0]
        result_dir = os.path.join(folder_path, 'result')
        os.makedirs(result_dir, exist_ok=True)
        
        html_output_file = os.path.join(result_dir, f"{student_name}_analysis.html")
        html_content = create_html_analysis(overall_analysis, sentences_analysis)
        
        if save_html_analysis(html_content, html_output_file):
            logging.info(f"Analysis saved to: {html_output_file}")
        else:
            logging.error(f"Failed to save analysis for: {video_file}")

if __name__ == "__main__":
    main()





