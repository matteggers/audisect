import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch.nn.functional as F
from .dataframe_store import DataframeStore
from .file import File

nltk.download('vader_lexicon')

# Vader can't be called, need wrapper
class CallableVader(SentimentIntensityAnalyzer):
    def __call__(self, sentence: str) -> dict:
        return self.polarity_scores(sentence)


class SentimentAnalyzer:
    def __init__(self, sentiment_model: str, df: DataframeStore):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.sentiment_model = sentiment_model
        self.tokenizer = AutoTokenizer.from_pretrained(self.sentiment_model)
        self.model = AutoModelForSequenceClassification.from_pretrained(sentiment_model)
        self.model.to(self.device)
        self.model.eval()
        self.vader_analyzer = CallableVader()
        self.labels = ["neg", "neu", "pos"]
        
        
    def tokenize_to_sentences(self, contents: str):
        return PunktSentenceTokenizer().tokenize(contents)

    # FIXME Change this name to reflect the custom model
    def model_sentiment_scores(self, sentence: str) -> dict:
        encoded = self.tokenizer(
            sentence,
            return_tensors = 'pt',
        )
        
        encoded = {k: v.to(self.device) for k, v, in encoded.items()}
        
        with torch.no_grad():
            output = self.model(**encoded)
            probs = F.softmax(output.logits, dim = -1).squeeze(0)
            probs = probs.cpu().tolist()
        
        return probs # FIXME outputting tensors not normal numbers
    
    def vader_sentiment_scores(self, sentence: str) -> dict:
        return self.vader_analyzer.polarity_scores(sentence)
    