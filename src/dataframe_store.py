import pandas as pd
class DataframeStore:
    def __init__(self, sentiment_model: str, model_alias: str):
        self.sentiment_model = sentiment_model
        self.model_alias = model_alias
        
        self._model_neg = f"{model_alias}_neg"
        self._model_neu = f"{model_alias}_neu"
        self._model_pos = f"{model_alias}_pos"
        
        self.df = pd.DataFrame(
            columns=[
                self._model_neg,
                self._model_neu,
                self._model_pos,
                "vader_neg",
                "vader_neu",
                "vader_pos",
                "sentence",
            ]
        )
    
    
    def merge_sentiment(self, model_scores: dict, vader_scores: dict) -> dict:
        return model_scores | vader_scores
    
    # TODO Make size agnostic, for more future columns
    def add_sentiment(self, model_scores: dict, vader_scores: dict, sentence: str) -> None:
        
        row = {
            self.model_alias + "_neg": model_scores[0],
            self.model_alias + "_neu": model_scores[1],
            self.model_alias + "_pos": model_scores[2],
            "vader_neg": vader_scores['neg'],
            "vader_neu": vader_scores['neu'],
            "vader_pos": vader_scores['pos'],
            "sentence": sentence,
        }
        self.df = pd.concat([self.df, pd.DataFrame([row])], ignore_index=True)
    
    