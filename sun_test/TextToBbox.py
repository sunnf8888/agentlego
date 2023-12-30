from agentlego.apis import load_tool

# load tool
tool = load_tool('TextToBbox', device='cuda')

# apply tool
visualization, result = tool('road.jpg', 'The largest white truck')

print(visualization)
print(result)