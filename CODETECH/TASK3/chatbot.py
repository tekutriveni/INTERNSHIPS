import wikipedia
import nltk
import random
import string

# Download NLTK resources
nltk.download('punkt')

# Greeting words
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "hey", "what's up")
GREETING_RESPONSES = ["Hi there!", "Hello!", "Hey!", "Hi!", "Greetings!"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def get_wikipedia_summary(query):
    """Fetch summary from Wikipedia"""
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.DisambiguationError as e:
        return f"Your query is too broad. Did you mean: {e.options[:5]}?"
    except wikipedia.PageError:
        return "I couldn't find any information on that."
    except Exception as e:
        return f"Error: {e}"

print("🤖 AI Chatbot with Wikipedia (type 'bye' to exit)")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['bye', 'exit', 'quit']:
        print("Bot: Goodbye! 👋")
        break
    elif greeting(user_input) is not None:
        print("Bot:", greeting(user_input))
    else:
        print("Bot:", get_wikipedia_summary(user_input))
