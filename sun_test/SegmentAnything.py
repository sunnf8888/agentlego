from agentlego.apis import load_tool

# load tool
tool = load_tool('SegmentAnything', device='cuda')

# apply tool
segmentation = tool('cups.png')
print(segmentation)