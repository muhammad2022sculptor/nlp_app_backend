from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS
import pandas as pd
import string

app = Flask(__name__)
CORS(app)

# Load the question answering model
qa_pipeline = pipeline(
    'question-answering',
    model='bert-large-uncased-whole-word-masking-finetuned-squad',
    tokenizer='bert-large-uncased-whole-word-masking-finetuned-squad'
)

# Load the text data
df = pd.read_csv('text_segments.csv')

# API endpoint to answer a question
@app.route('/answer_question', methods=['POST'])
def answer_question():
    data = request.get_json()
    doc_name = data['doc_name']
    question = data['question']
    document_text = " ".join(df.loc[df['doc_name'] == doc_name, 'text'].astype(str).tolist())  # Concatenate the text as a string
    document_text = document_text.translate(str.maketrans('', '', string.punctuation))
    print("Doc Name:", doc_name)
    print("Question:", question)
    print("Document Text:", document_text)
    result = qa_pipeline(question=question, context=document_text)
    return jsonify({'answer': result['answer']})

# API endpoint to get unique doc_names
@app.route('/unique_doc_names', methods=['GET'])
def unique_doc_names():
    unique_names = df['doc_name'].unique()
    return jsonify({'doc_names': list(unique_names)})

if __name__ == '__main__':
    app.run()