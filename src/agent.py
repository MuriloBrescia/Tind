import json

def load_model(model_path):
    # In a real scenario, this would load the fine-tuned model.
    # For this simulation, we'll just check if the model file exists.
    try:
        with open(model_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No model found."

def generate_responses(context, model):
    # In a real scenario, this would use the model to generate responses.
    # For this simulation, we'll return a fixed set of responses based on the context.
    if "sad" in context.lower():
        return [
            "I'm sorry to hear that. Is there anything I can do to help?",
            "It's okay to feel sad sometimes. I'm here for you.",
            "Sending you a virtual hug.",
            "I'm here to listen if you want to talk about it.",
            "Remember that this feeling will pass. You're strong.",
        ]
    else:
        return [
            "You have a great smile.",
            "I'm not a photographer, but I can picture us together.",
            "Are you a magician? Because whenever I look at you, everyone else disappears.",
            "Do you believe in love at first sight, or should I walk by again?",
            "If you were a vegetable, you'd be a cute-cumber.",
        ]

def filter_responses(responses):
    offensive_words = ["hate", "kill", "die"]
    filtered_responses = []
    for response in responses:
        if any(word in response.lower() for word in offensive_words):
            filtered_responses.append("I'm sorry, I can't respond to that.")
        else:
            filtered_responses.append(response)
    return filtered_responses

def get_user_feedback(responses):
    print("Please choose the best response (1-5):")
    for i, response in enumerate(responses):
        print(f"{i+1}. {response}")

    while True:
        try:
            choice = int(input())
            if 1 <= choice <= 5:
                return responses[choice-1]
        except ValueError:
            pass
        print("Invalid choice. Please enter a number between 1 and 5.")

def save_conversation(context, responses, best_response):
    with open("data/training_data.json", "r+") as f:
        data = json.load(f)
        data.append({
            "context": context,
            "responses": responses,
            "best_response": best_response,
        })
        f.seek(0)
        json.dump(data, f, indent=2)

def main():
    model = load_model("./models/model.txt")
    print("Model loaded.")

    context = input("Enter the conversation context: ")
    responses = generate_responses(context, model)
    filtered_responses = filter_responses(responses)
    best_response = get_user_feedback(filtered_responses)
    save_conversation(context, filtered_responses, best_response)
    print("Feedback saved. Thank you!")

if __name__ == "__main__":
    main()
