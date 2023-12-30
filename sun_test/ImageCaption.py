from agentlego.apis import load_tool

# load tool
tool = load_tool('ImageCaption', device='cuda')

# apply tool
caption = tool('demo.png')
print(caption)