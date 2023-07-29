import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

template = """You are a helpful assistant who generates text files giving explanations of complex topics.
A user will pass in the name of a topic, and you will write out a detailed explanation of the topic.
While writing this explanation, you should wrap each element in the explanation that could be regarded as its own, seperate topic like this: [[SUB TOPIC NAME]]
After finishing the explanations, do a double line break and provide a comma-seperated list of all elements wrapped like this: [[]]"
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
chain = LLMChain(
    llm=ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY")),
    prompt=chat_prompt,
)

print(chain.run("General Relativity"))

