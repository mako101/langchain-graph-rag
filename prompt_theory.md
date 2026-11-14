## Prompt Composition

What does a prompt consist of?

- Instructions
- Context
- Input Data
- Sentiment
- Output Indicator
    - Implicit or Explicit

## Prompting Engineering Techniques

### Zero Shot Prompting

- A prompt with no examples

### One Shot Prompting
- A prompt with 1 examples

### Multi Shot Prompting
- A prompt with multiple examples

### Chain Of Thought (COT)

- A method that allows LLM to break down complex tasks into a series of intermediate steps
- Mimics a "human" way of solving such problems
- Can be invoked with "lets think step by step"
- Models can be given a "reasoning engine" by providing a step-by-step solution to a similar problem
- Can be a Zero/One/Multi Shot prompt

### ReAct Prompting

- Stands for Reasoning and Acting
- Allows for dynamic reasoning and interaction with external environments to solve complex problems
- COT + ability to perform actions

### Prompt Enginnering Tips
- Provide useful context data
    - Just enough relevant information
- Clear, unambigous goals
- Iterate to get the perfect prompt that provides the best results