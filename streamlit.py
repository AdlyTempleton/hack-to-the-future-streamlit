import os
import re

import cohere

import streamlit as st

# set the page title and favicon
st.set_page_config(page_title="co.forecast", page_icon="🔮")
# initialize the Cohere SDK
COHERE_API_KEY = os.environ["COHERE_API_KEY"]
co = cohere.Client(COHERE_API_KEY)
st.header("co.forecast 🔮")
question = st.text_input("Question", value="Will Cohere raise a successful Series C?", type="default")
context = st.text_input(
    "Context",
    value=
    "Toronto-based artificial intelligence (AI) startup Cohere has secured $125 million USD ($159 million CAD) in Series B financing to fuel its United States expansion plans. Cohere, which aims to make natural language processing (NLP) more accessible, first emerged from stealth in May 2021 and announced a $40 million USD Series A round in September. Since then, Cohere has opened up general access to its API and inked a partnership to leverage Google Cloud’s AI infrastructure.",
    type="default")

# set the page title and favicon
# initialize the Cohere SDK
COHERE_API_KEY = "m9WUjCkf7T2MJcXJciyKUk8i6A6eIOraSZ8xfl5e"
co = cohere.Client(COHERE_API_KEY)

prompt = f"""This forecasting program will assign probabilities (between 0.00 and 1.00) to future events. The probability should never be exactly 0.0 or 1.0.



Question: Will Nickelback have a new album release in 2022
Context: We haven’t really heard anything new from the rock band Nickelback for quite a while, but that’s about to change, as word has come out that they are working on a new album but it's going to be a while.
Explanation: Nickelback is working on a new album, but it might not be ready by the end of 2022
Answer: 0.5

Question: Will dinosaurs be back before the year 2100
Context: There have been a lot of scary creatures that have walked planet Earth ever since its inception. Although the variety of man-eating species has dwindled as humanity has progressed, there was a point in time where merely stepping outside was a fight for life and limb. This was largely thanks to dinosaurs, the massive reptilian creatures that ruled the planet for millions of years before humans took the reins.
Explanation: It's possible to engineer dinosaurs, but it's very difficult
Answer: 0.2

Question: Will there be a manned mission to Mars in 2024
Context: The race to Mars is getting crowded. Two startup space companies in California, Relativity Space and Impulse Space, announced today (July 19) that they are teaming up to launch the first commercial mission to Mars in 2024, years before the first potential trip by the more established SpaceX, which is known for its long-term plans to establish a human settlement of the Red Planet.
Explanation: Companies plan to launch mars missions by 2024, but it is likely that these plans will be unsuccessful.
Answer: 0.3

Question: {question}
Context: {context}
Explanation:"""


def get_prob_from_generation(generation):
    try:
        generation_after_answer = generation.split("Answer:")[1]
        predicted_prob = float(generation_after_answer.split()[0])
        if predicted_prob > 0.0 and predicted_prob < 1.0:
            return predicted_prob
    except Exception:
        pass
    return None


# use the prompt to create a generation
probs = []
prob_to_explanation = {}
for i in range(1):

    def generate():
        generation = co.generate(model='xlarge',
                                 prompt=prompt,
                                 max_tokens=35,
                                 temperature=.8,
                                 p=.75,
                                 stop_sequences=["Question:"]).generations[0].text
        generation = generation.replace("Question:", "")
        return generation

    generation = generate()
    while get_prob_from_generation(generation) is None:
        generation = generate()

    prob = get_prob_from_generation(generation)
    explanation = generation[:generation.find("Answer:")]
    probs.append(prob)
    prob_to_explanation[prob] = explanation

probs.sort()
median_prob = probs[int(len(probs) // 2)]
explanation = prob_to_explanation[median_prob]
# output the generation
st.markdown(f"co.forecast says: **{int(median_prob * 100)}%** chance")
st.markdown(f"Explanation: {explanation}")
