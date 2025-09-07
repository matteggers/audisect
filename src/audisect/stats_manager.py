import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


# Reads from the file csv
# Original file csv structure: sentence,model_neg,model_neu,model_pos,model_weighted_avg,vader_neg,vader_neu,vader_pos,vader_compound

class StatsManager:
    def __init__(self, output_dir: str = '.'):
        column_names = [
            'Name',
            'Num Sentences',
            'Num Words',
            'Avg Sentiment',
            'Opening Sentiment',
            'Closing Sentiment',
            'Sentiment Oscillations',
            'Sentiment StdDev',
            'Avg Sentiment Magnitude',
            'Avg Sentence Length',
            'Avg Pos Intensity',
            'Avg Neg Intensity',
            'Pos Sentiment Freq',
            'Neg Sentiment Freq'
        ]
        self.stats_df = pd.DataFrame(columns=column_names).astype({
            'Name': 'object',
            'Num Sentences': 'int64',
            'Num Words': 'int64',
            'Avg Sentiment': 'float64',
            'Opening Sentiment': 'float64',
            'Closing Sentiment': 'float64',
            'Sentiment Oscillations': 'int64',
            'Sentiment StdDev': 'float64',
            'Avg Sentiment Magnitude': 'float64',
            'Avg Sentence Length': 'float64',
            'Avg Pos Intensity': 'float64',
            'Avg Neg Intensity': 'float64',
            'Pos Sentiment Freq': 'float64',
            'Neg Sentiment Freq': 'float64'
        })
        self.output_dir = Path(output_dir)
        self.file_path = self.output_dir / 'stats.csv'
        
    '''
        Function style:
        Pass only the column of the dataframe that you want to compute stats on.
        Thus, in the pipeline, symbolic names will be used to pass the correct column
    '''
    def num_sentences(self, df) -> int:
        return len(df)
    
    def num_words(self, sentences) -> int:
        total_words = 0
        for sentence in sentences:
            total_words += len(sentence.split())
        return total_words
    
    def average_len(self, num_sentences: int, num_words: int) -> float:
        total_words = num_words
        total_sentences = num_sentences
        if total_sentences == 0:
            return 0.0
        return total_words / total_sentences
    
    def weighted_avg_sentiment(self, df) -> float:
        if df.empty:
            return 0.0
        return df['model_weighted_avg'].mean()
    
    def average_sentiment_intensity(self, df) -> tuple:
        if df.empty:
            return (0.0, 0.0)
        avg_pos = df['model_pos'].mean()
        avg_neg = df['model_neg'].mean()
        return (avg_pos, avg_neg)

    def sentiment_frequency(self, df) -> tuple:
        if df.empty:
            return (0.0, 0.0)
        
        num_sentences = len(df)
        if num_sentences == 0:
            return (0.0, 0.0)
            
        sentiments = df['model_weighted_avg']
        
        num_pos = (sentiments > 0).sum()
        num_neg = (sentiments < 0).sum()
        
        pos_freq = num_pos / num_sentences
        neg_freq = num_neg / num_sentences
        
        return (pos_freq, neg_freq)
    
    
    def helper_stats(self, df):
        sentiments = df['model_weighted_avg'].tolist()
        num_sentences = len(sentiments)
        if num_sentences == 0:
            return (0.0, 0.0, 0, 0.0)
        
        opening_count = max(1, num_sentences // 10)
        closing_count = max(1, num_sentences // 10)
        
        opening_sentiment = np.mean(sentiments[:opening_count])
        closing_sentiment = np.mean(sentiments[-closing_count:])
        
        #oscillations = sum((sentiments[i] * sentiments[i+1] < 0) for i in range(len(sentiments)-1))
        
        sentiment_stddev = np.std(sentiments)
        
        #avg_sentiment_magnitude = np.mean([abs(s) for s in sentiments])
        
        return (opening_sentiment, closing_sentiment, sentiment_stddev) #(opening_sentiment, closing_sentiment, oscillations, sentiment_stddev, avg_sentiment_magnitude)
    
    def compute_and_store_stats(self, df: pd.DataFrame, file_name: str) -> None:
        num_sentences = self.num_sentences(df)
        num_words = self.num_words(df['sentence'])
        avg_sentiment = self.weighted_avg_sentiment(df)
        avg_sentence_length = self.average_len(num_sentences, num_words)
        avg_pos_intensity, avg_neg_intensity = self.average_sentiment_intensity(df)
        opening_sentiment, closing_sentiment, sentiment_stddev = self.helper_stats(df)
        pos_freq, neg_freq = self.sentiment_frequency(df)
        
        new_row = {
            'Name': file_name,
            'Num Sentences': num_sentences,
            'Num Words': num_words,
            'Avg Sentiment': round(avg_sentiment, 4),
            'Opening Sentiment': round(opening_sentiment, 4),
            'Closing Sentiment': round(closing_sentiment, 4),
            'Sentiment Oscillations': 0,  # Placeholder
            'Sentiment StdDev': round(sentiment_stddev, 4),
            'Avg Sentiment Magnitude': 0.0,  # Placeholder
            'Avg Sentence Length': round(avg_sentence_length, 4),
            'Avg Pos Intensity': round(avg_pos_intensity, 4),
            'Avg Neg Intensity': round(avg_neg_intensity, 4),
            'Pos Sentiment Freq': round(pos_freq, 4),
            'Neg Sentiment Freq': round(neg_freq, 4)
        }
        
        self.stats_df = pd.concat([self.stats_df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_stats(self.stats_df)
        
    def get_stats(self, file_name: str) -> dict:
        row = self.stats_df[self.stats_df['Name'] == file_name]
        if row.empty:
            return {}
        return row.iloc[0].to_dict()
    

    def save_stats(self, final_results_df):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        new_filename = f"{timestamp}_results.csv"

        new_path = self.output_dir / new_filename

        final_results_df.to_csv(new_path, sep=',', index=False, encoding='utf-8-sig')