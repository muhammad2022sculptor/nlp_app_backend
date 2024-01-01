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
    print("Doc Name: "+doc_name)
    print("Question: "+question)

    # Filter the text data based on the document name
    relevant_text_segments = df[df['doc_name'] == doc_name]['text'].astype(str).tolist()

    # Concatenate all text segments into a single string
    document_text = " ".join(relevant_text_segments)

    # Remove punctuation
    document_text = document_text.translate(str.maketrans('', '', string.punctuation))

    # Limit the total input to 2000 tokens
    document_text = " ".join(document_text.split()[:2000])

    # Split the limited document_text into segments of approximately 500 tokens each
    token_limit = 500
    segmented_text = [document_text[i:i+token_limit] for i in range(0, len(document_text), token_limit)]

    # Process each segment and collect the answers
    answers = []
    for segment in segmented_text:
        result = qa_pipeline(question=question, context=segment)
        answers.append(result['answer'])

    # Return the aggregated answers
    return jsonify({'answers': answers})

# API endpoint to get unique doc_names
@app.route('/unique_doc_names', methods=['GET'])
def unique_doc_names():
    unique_names = df['doc_name'].unique()
    return jsonify({'doc_names': list(unique_names)})

if __name__ == '__main__':
    app.run()