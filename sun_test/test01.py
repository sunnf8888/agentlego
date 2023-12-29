from agentlego.apis import load_tool

# load tool
tool = load_tool('TextToImage', device='cuda')

# apply tool
image = tool('cute cat')
print("----------")
print(image)