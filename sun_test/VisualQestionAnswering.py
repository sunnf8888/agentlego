from agentlego.apis import load_tool

# load tool
tool = load_tool('VisualQuestionAnswering', device='cuda')

# apply tool
answer = tool('demo.png', 'What is the color of the cat?')
print(answer)

answer = tool('demo.png', 'What kind of animals are they all?')
print(answer)