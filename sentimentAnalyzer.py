from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification # RoBERTa
from scipy.special import softmax
import nltk
from nltk.tokenize import PunktSentenceTokenizer
import pandas as pd
from transcriber import add_files_to_list
from pathlib import Path

# refactor at some point using np to reduce time to run this



#### CITATION ####
# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

# VADER Compound Score
# POSITIVE: > 0.05
# NEGATIVE: < -0.05
# NEUTRAL: < 0.05 && > -0.05

def read_text(fileDirectory):
    with open(fileDirectory, 'r') as file:
        data = file.read()
        return data

def hold_text(text):
    text_dict = {}
    allText = read_text(text)
    fileName = Path(text).stem
    sentences = PunktSentenceTokenizer().tokenize(allText)
    text_dict.update({fileName: sentences})
    return text_dict, fileName

def make_dataframe(_, value):
    df = pd.DataFrame({"sentence": sentence for sentence in value})
    df['roberta_neg'] = ''
    df['roberta_neu'] = '' 
    df['roberta_pos'] = ''
    df['vader_neg']   = ''
    df['vader_neu']   = ''
    df['vader_pos']   = ''
    return df

def sentiment_analysis(df):
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment" #removed the f string - may come in handy for others
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    analyzer = SentimentIntensityAnalyzer()
    # pre allocate [] to the size of sentences to remove dynamic allocation
    
    scores_dict = {
        'roberta_neg': [],
        'roberta_neu': [],
        'roberta_pos': [],
        'vader_neg': [],
        'vader_neu': [],
        'vader_pos': []
    }
    
    for sentence in df["sentence"]:
        encoded = tokenizer(sentence, return_tensors='pt')
        output = model(**encoded)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores) #normalize
        
        vs1 = analyzer.polarity_scores(sentence)
        scores_dict['roberta_neg'].append(scores[0])
        scores_dict['roberta_neu'].append(scores[1])
        scores_dict['roberta_pos'].append(scores[2])
        scores_dict['vader_neg'].append(vs1['neg'])
        scores_dict['vader_neu'].append(vs1['neu'])
        scores_dict['vader_pos'].append(vs1['pos'])
        
    df['roberta_neg'] = scores_dict['roberta_neg']
    df['roberta_neu'] = scores_dict['roberta_neu']
    df['roberta_pos'] = scores_dict['roberta_pos']
    df['vader_neg']   = scores_dict['vader_neg']
    df['vader_neu']   = scores_dict['vader_neu']
    df['vader_pos']   = scores_dict['vader_pos']
    return df
         
def analysis_wrapper(textFiles):
    script_dir = Path(__file__).parent.resolve()
    dataDir = script_dir / "data"

    for file in textFiles:
        text_dict, fileName = hold_text(file) 
        name = Path(fileName).stem
        outputFile = Path(dataDir).joinpath(name)
        df = make_dataframe(text_dict.keys(), text_dict.values())
        df = sentiment_analysis(df)
        df.to_csv(f'{outputFile}' + '.csv', index=True)
        print(f'CSV: {name} saved!')

