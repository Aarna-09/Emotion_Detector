from flask import Flask, render_template, request
import nltk
from nltk.corpus import stopwords
import string

from urllib.parse import quote


# Initialize Flask app
main = Flask(__name__)

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Lemmatization
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Function to process text
def process_text(text):
    lower_case = text.lower()
    clean_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    sentences = nltk.sent_tokenize(clean_text)
    non_stopwords = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        words = [lemmatizer.lemmatize(word, pos='v') for word in words if word not in set(stopwords.words('english'))]
        non_stopwords.extend(words)

    return non_stopwords

# Function to map words to emotions
def map_emotions(words):
    emotion_list = []
    with open('emotions.txt', 'r') as file:
        for line in file:
            clear_line = line.replace('\n', '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')
            if word in words:
                emotion_list.append(emotion)
    return emotion_list

@main.route('/', methods=['GET', 'POST'])
def layout():
    if request.method == 'POST':
        text = request.form['text']
        non_stopwords = process_text(text)
        emotion_list = map_emotions(non_stopwords)
        return render_template('index.html', emotions=emotion_list, text=text)
    return render_template('index.html', emotions=None, text=None)

if __name__ == '__main__':
    main.run(debug=True)

