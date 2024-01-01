# nlp_app_backend

main steps and motivation for any data engineering/processing on the raw data
before making it available to the API;
The data needs to be clean and readable to API.

the main functionalities of the API;
The api extracts the data from text_segments.csv which is already an extracted data for three different companies. and the api also recieves questions about them and answers them accordingly.

the key challenges you faced in solving the problem;
The most difficult challenge was that there was a limit to word for processing.

how would you improve the backend, if you had more time to work on it?
Add more functionality and increase accuracy, speed.

# better to install these first
1. pandas
2. flask
3. flask_cors
4. transformers
5. pytorch
   You can download conda and create your custom env too.

This is backend api with two endpoints one for extracting the names of the businesses from the doc_names in text_segments.csv and the other to get the answer to the asked question.
The data is limited, To get the answers faster as the model used for question answer feature has a limit of about 512 tokens at a time and for the purpose of increasing accuracy I have managed to get it to 2000 tokens at a time. But yes the time to process has increased too. The good news is that it is still in seconds.


after all that just use
python server.py to run the server.
That simple
