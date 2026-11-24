
import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

# 1. LLM
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0
)

questions = [
    "What is 5 + 7?",
    "What is the capital of Japan?",
    "How many days are in a week?",
    "What color do you get by mixing red and white?",
    "Which planet is known as the Red Planet?",
    "Explain photosynthesis in two sentences.",
    "What is the difference between RAM and ROM?",
    "Why does ice float on water?",
    "What happens when you divide a number by zero?",
    "Name three programming languages.",
    "Explain how the internet works.",
    "What is the difference between authentication and authorization?",
    "Why is Python considered dynamically typed?",
    "Explain synchronous and asynchronous programming.",
    "What happens when you enter a URL in a browser?",
    "Why can two identical API requests sometimes produce different responses?",
    "Explain how a database index improves query performance.",
    "How would you design a URL-shortening service?",
    "Explain horizontal and vertical scaling.",
    "How would you investigate an API that becomes slower as users increase?",
    "A server receives 1000 requests per second but processes only 700. What happens?",
    "How would you prevent Service B failure from bringing down Service A when A depends on B?",
    "A bank transaction deducts money but fails before crediting the receiver. How would you handle it?",
    "How would you build a system that processes 10 million documents daily?",
    "An AI agent repeatedly calls the same tool without completing its task. How would you debug it?",
    "A farmer has 17 sheep. All but 9 run away. How many remain?",
    "If a plane crashes exactly on the border between India and Nepal, where do they bury the survivors?",
    "You have 3 switches outside a closed room and 3 bulbs inside. You can enter only once. How do you identify which switch controls each bulb?"
]
answers = []
inptoken = 0
outtoken = 0
count = 1

for question in questions:
        result = llm.invoke(question)
        answers.append(result.content)
        print(result.content)
        inptoken += result.usage_metadata["input_tokens"]
        outtoken += result.usage_metadata["output_tokens"]
        count +=1

print("*"*50)
print(f"Total input tokens: {inptoken}")
print(f"Total output tokens: {outtoken}")
print(answers)

