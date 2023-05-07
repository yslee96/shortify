import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        text = request.form["input"]
        limit = request.form["limit"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(text, limit),
            temperature=0.7,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(text, limit):
    return """
    
    I want you to act as a sentence shortener.
    Here are original sentences: {}
    Your task is to take the given text and turn this into shorter sentences in {} characters or less. 
    Do not change the original meaning of the sentence.
    
    """.format(
        text, limit
    )
