from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.globals import set_debug

load_dotenv()
# set_debug(True)


# to research
# temperature - control the randomness of the model's output
# lower temperature - more deterministic output, factual + repeatable
# higher temperature - more creative output, less predictable / less repeatable
# chain pipe runnable concept
# LCEL - LangChain Express Language

information = """
Birds
Birds are warm-blooded vertebrates characterised by feathers, beaks, and the ability to lay hard-shelled eggs. Most
birds can fly, although some species, such as penguins and ostriches, have evolved to live without flight. Birds are
found on every continent and inhabit environments ranging from tropical rainforests to frozen polar regions. Their diets
include seeds, insects, fish, and small mammals. Interesting facts: The peregrine falcon is the fastest animal on Earth,
reaching speeds of over 320 km/h during a hunting dive. Hummingbirds are the only birds capable of sustained backward
flight, while some migratory birds, such as the Arctic tern, travel tens of thousands of kilometres each year between
breeding and wintering grounds.
Fish
Fish are aquatic vertebrates that typically breathe through gills and use fins to swim. They live in freshwater and
saltwater environments, from shallow streams and coral reefs to the deepest parts of the ocean. Most fish are
cold-blooded, meaning their body temperature changes with the surrounding water. They vary enormously in size,
appearance, and behaviour. Interesting facts: Some species of fish, such as the clownfish, can change sex during their
lifetime. Sharks have existed for over 400 million years, making them older than trees. Certain deep-sea fish produce
their own light through a process called bioluminescence, which helps them attract prey, communicate, or avoid
predators. The whale shark, the world's largest living fish, can grow to over 18 metres in length despite feeding mainly
on plankton and small animals.
Reptiles
Reptiles are vertebrates characterised by dry, scaly skin and a reliance on external heat sources to regulate their body
temperature. This diverse group includes snakes, lizards, turtles, crocodiles, and tortoises. Reptiles inhabit deserts,
forests, grasslands, wetlands, and oceans. Most reproduce by laying eggs, although some species give birth to live
young. Interesting facts: Crocodiles are more closely related to birds than to lizards or snakes. Some turtles can
absorb oxygen from water through specialised tissues near their tails, allowing them to remain submerged for extended
periods. Chameleons can move their eyes independently, giving them an unusually wide field of vision. The Komodo dragon,
the world's largest living lizard, can reach approximately three metres in length and uses venom to help subdue its
prey.

"""

prompt_template_text = """
given the following information: {information}, 
and the category of the animal: {category},
summarize the given animal category briefly and provide an interesting fact about it.
"""

prompt_template = PromptTemplate(
    template=prompt_template_text,
    input_variables=["information", "category"]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = (prompt_template | llm).with_config(run_name="animal-summary")

# result = chain.invoke({"information": infromartion, "category": "Birds"})

# print(result.content)

# batch requests data
chat_requests = [
    {"information": information, "category": "Birds"}, 
    {"information": information, "category": "Fish"}, 
    {"information": information, "category": "Reptiles"}]

chat_results = chain.batch(chat_requests)

for result in chat_results:
    print()
    print(result.content)
    
