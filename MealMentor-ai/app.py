import os
import openai
from flask import Flask, request, render_template_string

app = Flask(__name__, static_folder='static', static_url_path='')

openai.api_key = "your-openai-api-key"

html_template = '''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MealMentor.ai</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #F0F0F0;
        }
        .container {
            max-width: 800px;
            margin: 0px auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
            color: #333333;
        }
        .chat-box {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 5px;
            overflow-y: auto;
            height: 275px;
            margin-bottom: 20px;
            box-shadow: inset 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .chat-entry {
            margin-bottom: 15px;
        }
        .you {
            text-align: right;
        }
        .MealMentor {
            text-align: left;
        }
        .you p, .MealMentor p {
            display: inline-block;
            padding: 10px;
            border-radius: 5px;
        }
        .you p {
            background-color: #6C95CF;
            color: #ffffff;
        }
        .MealMentor p {
            background-color: #999999;
            color: #ffffff;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333333;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: #ffffff;
            color: #333333;
        }
        input[type="submit"] {
            background-color: #6C95CF;
            color: #ffffff;
            font-weight: bold;
            text-transform: uppercase;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #4b73b1;
        }
    </style>
</head>
<body>
<div class="container">
<img src="{{ url_for('static', filename='Logo.png') }}" alt="(chatbot-logo)" style="display: block; margin-left: auto; margin-right: auto; width: 400px; height: auto; padding-bottom: 20px;">
    <div class="chat-box">
        {% for entry in chat_history %}
            <div class="chat-entry {{ 'you' if entry[0] == 'You' else 'MealMentor' }}">
                <p><strong>{{entry[0] }}:</strong> {{ entry[1] }}</p>
            </div>
        {% endfor %}
    </div>
    <form method="post">
        <label for="message1" class="userPrompt">What are you diet plan goals?</label>
        <input type="text" name="message1" id="message1" required>

        <label for="message2" class="userPrompt">What are your dietary restrictions? If none write 'none'.</label>
        <input type="text" name="message2" id="message2" required>

        <input type="submit" value="Send">
    </form>
</div>
</body>
</html>
'''
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def chat():
    global chat_history
    if request.method == 'POST':
        user_message1 = request.form['message1']
        user_message2 = request.form['message2']

        user_message_combined = "My goal is to " + user_message1 + "and my dietary restrictions are " + user_message2

        chat_history.append(('You', user_message_combined))

        ai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{user_message_combined}\n\nPretend you are a dietitian (but don't refer to yourself), give advice and give a simple meal plan.\n\n",
            temperature=0.5,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        chat_history.append(('MealMentor', ai_response.choices[0].text.strip()))

    return render_template_string(html_template, chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)

