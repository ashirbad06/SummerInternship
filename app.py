import pandas as pd
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

app = Flask(__name__, template_folder='templates')

dataset = pd.read_csv('C:\\Users\\admin\\Desktop\\PS1 docs\\Symptom-se.csv')

conversations = []

try:
    for _, row in dataset.iterrows():
        conversation = [row['user'], row['bot']]
        conversations.append(conversation)
except KeyError as e:
    print(f"Error accessing column: {e}")

# Create a ChatBot instance
chatbot = ChatBot('MyChatBot')

# Create a ListTrainer instance for custom dataset training
list_trainer = ListTrainer(chatbot)
list_trainer.train(conversations)

# Create a ChatterBotCorpusTrainer instance for built-in corpus training
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train('chatterbot.corpus.english')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chatbot.get_response(user_input)
    return str(response)

@app.route('/', methods=['GET', 'POST'])
def symptom_assessment():
    if request.method == 'POST':
        # Process the collected information (e.g., store in a database, perform calculations)
        # ...

        return render_template('summary.html',
                               intensity=request.form['intensity'],
                               location=request.form['location'],
                               duration=request.form['duration'],
                               aggravating_factors=request.form['aggravating_factors'],
                               alleviating_factors=request.form['alleviating_factors'],
                               other_symptoms=request.form['other_symptoms'],
                               previous_treatment=request.form['previous_treatment'],
                               additional_info=request.form['additional_info'])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
