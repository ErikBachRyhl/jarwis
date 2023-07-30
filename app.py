import os
import re

# Retrieval
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper

# Prompting
from langchain.prompts import PromptTemplate
# LLM response
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
#model="gpt-3.5-turbo-16k-0613"
llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

template = """You are a helpful research assistant and teacher. I would like you to help me gain insight into complex topics.
I will provide you with the name of a topic and some information on the topic from wikipedia. 
Based on the wikipedia description of the topic, you will write your own explanation of that topic while following below rules:

1/ The explanation should be in the style of Richard Feynman.
2/ It should not include overly complex sentences. The more direct to the point, the better.
3/ If suitable, make use of analogies to simplify topics and make them more intuitive, just like Richard Feynman did.
4/ Wrap each element in the explanation that could be regarded as its own, separate topic like this: [[SUB TOPIC NAME]]
If the topic appears in a sentence, format it like this: "It predicted [[Black Hole|black holes]] and the [[Expansion of the Universe|expansion of the universe]]."
5/ Keep the answer concise (less than 200 words)

Here is an example response on "General Relativity" following above rules:
---- 
Alright, imagine you're in a large trampoline and you drop a heavy ball in the middle. The trampoline bends around the ball, right? That's a bit like [[General Relativity|general relativity]].

Instead of a trampoline, we have [[Spacetime|spacetime]], the fabric of our universe. Objects with mass, like our sun, warp this fabric creating a kind of well. Planets are like smaller balls rolling around the edge of this well. They're not just falling straight in, because they also have a sideways motion.

So general relativity is Einstein's way of explaining gravity. It says gravity is not so much a force pulling objects together, but more of a curving of spacetime caused by mass and energy. This gives us a neat explanation of orbits without needing a mysterious force acting at a distance like in [[Newton's Law of Universal Gravitation|Newton's laws]]. 

The cool thing about this is it predicted phenomena that were completely new like [[Gravitational Lensing|gravitational lensing]], where light bends as it passes massive objects. It even predicted [[Black Hole|black holes]], regions so heavy that not even light can escape from them.

However, there's a catch. While general relativity works great for big things like planets and galaxies, it doesn't play nice with [[Quantum Physics|quantum physics]], the rules for tiny things like atoms and particles. We're still scratching our heads on that one.
---- 

Here is your topic name: {topic}
Wikipedia exerpt on {topic}:
{wiki_info}

Begin!
"""

# Put together prompt
prompt = PromptTemplate(
    input_variables=["topic", "wiki_info"], 
    template=template
)

# Query chatGPT
chain = LLMChain(
    llm=llm,
    prompt=prompt
)

name = "Quantum Mechanics"
    
def generate_response(topic_name):
    wiki_info = wikipedia.run(topic_name)
    response = chain.run(topic=topic_name, wiki_info=wiki_info)
    return response

response = generate_response(name)

def extract_topics(text):
    # Regular expression pattern for matching the topic syntax
    pattern = re.compile(r'\[\[(.*?)(?:\|(.*?))?\]\]')
    
    # Find all matches in the text
    matches = pattern.findall(text)
    
    # Extract the topic names and add them to the list
    topics = [match[0] for match in matches]
    
    return topics

print(response)
print(extract_topics(response))


