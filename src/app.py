from flask import Flask, render_template, request, redirect, url_for
from src.agent import load_model, generate_responses, save_conversation

app = Flask(__name__)
model = load_model("./models/model.txt")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_responses", methods=["POST"])
def get_responses():
    context = request.form["context"]
    responses = generate_responses(context, model)
    return render_template("responses.html", context=context, responses=responses)

@app.route("/save_feedback", methods=["POST"])
def save_feedback():
    context = request.form["context"]
    responses = request.form.getlist("responses")
    best_response = request.form["best_response"]
    save_conversation(context, responses, best_response)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
