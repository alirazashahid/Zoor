import random
from collections import defaultdict

# Knowledge base to store learned data
knowledge_base = defaultdict(list)

# Train the model with provided data
def train_model(data):
    for sentence in data.split('.'):
        keywords = sentence.lower().split()
        for word in keywords:
            knowledge_base[word].append(sentence)
    print(f"Knowledge base after training: {knowledge_base}")

# Generate a response based on the user input
def generate_response(user_input):
    words = user_input.lower().split()
    responses = [knowledge_base[word] for word in words if word in knowledge_base]
    flattened_responses = [resp for sublist in responses for resp in sublist]
    return random.choice(flattened_responses) if flattened_responses else "I don't know about that yet."