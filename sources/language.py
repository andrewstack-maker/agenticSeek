import langid
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class LanguageUtility:
    """LanguageUtility for language, or emotion identification"""
    def __init__(self):
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        self.sid = SentimentIntensityAnalyzer()
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text using langdetect
        Args:
            text: string to analyze
        Returns: ISO639-1 language code
        """
        langid.set_languages(['fr', 'en', 'zh'])
        lang, score = langid.classify(text)
        return lang

    def detect_emotion(self, text: str) -> str:
        """
        Detect the dominant emotion in the given text
        Args:
            text: string to analyze
        Returns: string of the dominant emotion
        """
        try:
            scores = self.sid.polarity_scores(text)
            emotions = {
                'Happy': max(scores['pos'], 0),
                'Angry': 0,
                'Sad': max(scores['neg'], 0),
                'Fear': 0,
                'Surprise': 0
            }
            if scores['compound'] < -0.5:
                emotions['Angry'] = abs(scores['compound']) * 0.5
                emotions['Fear'] = abs(scores['compound']) * 0.5
            elif scores['compound'] > 0.5:
                emotions['Happy'] = scores['compound']
                emotions['Surprise'] = scores['compound'] * 0.5
            dominant_emotion = max(emotions, key=emotions.get)
            if emotions[dominant_emotion] == 0:
                return 'Neutral'
            return dominant_emotion
        except Exception as e:
            raise e
    
    def analyze(self, text):
        """
        Combined analysis of language and emotion
        Args:
            text: string to analyze
        Returns: dictionary with language and emotion results
        """
        try:
            language = self.detect_language(text)
            emotions = self.detect_emotion(text)
            return {
                "language": language,
                "emotions": emotions
            }
        except Exception as e:
            raise e

if __name__ == "__main__":
    detector = LanguageUtility()
    
    test_texts = [
        "I am so happy today!",
        "Qué tristeza siento ahora",
        "我不要去巴黎",
        "La vie c'est cool"
    ]
    for text in test_texts:
        print(f"\nAnalyzing: {text}")
        result = detector.analyze(text)
        print(result)