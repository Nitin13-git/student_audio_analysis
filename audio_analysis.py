# audio_analysis.py
import os
import logging
from dataclasses import dataclass
from typing import List, Optional
from together import Together

@dataclass
class SentenceAnalysis:
    original_sentence: str
    is_grammatically_correct: bool
    corrected_sentence: Optional[str]
    word_analysis: List[dict]

class AudioAnalyzer:
    def __init__(self):
        self.api_key = "API key"
        os.environ["TOGETHER_API_KEY"] = self.api_key
        self.client = Together()
        
    def analyze_sentence(self, sentence: str) -> SentenceAnalysis:
        """Analyze a single sentence using Together AI"""
        try:
            prompt = f"""
            Analyze this sentence and provide the following:
            1. Is it grammatically correct? (yes/no)
            2. If incorrect, provide the corrected version
            3. Analyze each word for pronunciation issues
            
            Sentence: "{sentence}"
            
            Format your response exactly like this:
            Grammar: [yes/no]
            Corrected: [corrected sentence or 'None' if already correct]
            Word Analysis: [word-by-word analysis]
            """
            
            response = self.client.chat.completions.create(
                # model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
                messages=[
                    {"role": "system", "content": "You are an expert English language analyzer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            
            analysis = response.choices[0].message.content.split('\n')
            is_correct = 'yes' in analysis[0].lower()
            corrected = None if is_correct else analysis[1].replace('Corrected: ', '').strip()
            
            
            words = sentence.split()
            word_analysis = [
                {
                    'word': word,
                    'pronunciation_correct': True,  
                    'needs_improvement': False
                }
                for word in words
            ]
            
            return SentenceAnalysis(
                original_sentence=sentence,
                is_grammatically_correct=is_correct,
                corrected_sentence=corrected,
                word_analysis=word_analysis
            )
            
        except Exception as e:
            logging.error(f"Error in sentence analysis: {str(e)}")
            return None

    def get_overall_analysis(self, text: str) -> str:
        """Get overall analysis of the audio transcript"""
        try:
            prompt = f"""
            Provide a comprehensive analysis of this speech:
            
            {text}
            
            Focus on:
            1. Overall clarity and coherence
            2. Grammar patterns and common errors
            3. Pronunciation patterns
            4. Specific areas for improvement
            5. General fluency level
            """
            
            response = self.client.chat.completions.create(
                # model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
                messages=[
                    {"role": "system", "content": "You are an expert English language analyzer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error in overall analysis: {str(e)}")
            return None



