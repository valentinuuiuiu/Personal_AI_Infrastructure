# This script is designed to be executed as a standalone module or imported and called directly.
import argparse
import sys
import os

def analyze_emotion(image_path):
    """
    Placeholder for Hume AI emotion analysis.
    """
    if not os.path.exists(image_path):
        # Raise an exception instead of exiting, so it can be caught by the web service.
        raise FileNotFoundError(f"Error: Image file not found at {image_path}")

    mock_emotions = {
        "Joy": 0.7, "Sadness": 0.1, "Surprise": 0.2,
    }

    analysis_text = "Detected emotions from the provided image:\n"
    for emotion, score in mock_emotions.items():
        analysis_text += f"- {emotion}: {score*100:.1f}%\n"

    return analysis_text

def run(args):
    """
    Analyzes an image file for emotions from a given path.
    """
    try:
        emotion_analysis = analyze_emotion(args.image_path)

        output = "\n--- Sharaba Kavacham Analysis ---\n"
        output += emotion_analysis
        output += "---------------------------------\n"
        return output
    except Exception as e:
        # Re-raise the exception so it can be handled by the caller (the web service)
        raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze emotions from an image file.")
    parser.add_argument("image_path", help="The full path to the image file to analyze.")
    args = parser.parse_args()

    try:
        result = run(args)
        print(result)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
