# html_utils.py
import logging
from typing import List
import html
from audio_analysis import AudioAnalyzer, SentenceAnalysis


def create_html_analysis(overall_analysis: str, sentences_analysis: List[SentenceAnalysis]) -> str:
    """Create HTML output from the analysis"""
    html_output = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }
            .correct { color: #2ecc71; }
            .incorrect { color: #e74c3c; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border: 1px solid #ddd; }
            th { background-color: #f8f9fa; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .summary { background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .word-analysis { font-size: 0.9em; color: #666; }
            .needs-improvement { background-color: #fff3cd; }
        </style>
    </head>
    <body>
    """
    
    # Add overall analysis section
    html_output += "<h1>Speech Analysis Report</h1>"
    html_output += f"<div class='summary'><h2>Overall Analysis</h2>{overall_analysis}</div>"
    
    # Add sentence analysis table
    html_output += """
    <h2>Sentence-by-Sentence Analysis</h2>
    <table>
        <thead>
            <tr>
                <th>Original Sentence</th>
                <th>Grammar Status</th>
                <th>Corrected Version</th>
                <th>Word Analysis</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for sentence in sentences_analysis:
        status_class = "correct" if sentence.is_grammatically_correct else "incorrect"
        status_text = "Correct" if sentence.is_grammatically_correct else "Incorrect"
        
        html_output += f"""
        <tr>
            <td>{html.escape(sentence.original_sentence)}</td>
            <td class='{status_class}'>{status_text}</td>
            <td>{html.escape(sentence.corrected_sentence) if sentence.corrected_sentence else '—'}</td>
            <td class='word-analysis'>
        """
        
        # Add word analysis
        for word_info in sentence.word_analysis:
            word_class = 'needs-improvement' if word_info['needs_improvement'] else ''
            html_output += f"<span class='{word_class}'>{html.escape(word_info['word'])}</span> "
        
        html_output += "</td></tr>"
    
    html_output += "</tbody></table></body></html>"
    return html_output

def save_html_analysis(html_content: str, output_path: str) -> bool:
    """Save HTML analysis to a file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        logging.error(f"Error saving HTML analysis: {str(e)}")
        return False






