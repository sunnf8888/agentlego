print()
from transformers import HfAgent
from agentlego.apis import load_tool
from PIL import Image

# load tools and build transformers agent
tool = load_tool('ImageCaption', device='cuda').to_transformers_agent()
agent = HfAgent('https://api-inference.huggingface.co/models/bigcode/starcoder', additional_tools=[tool])

# agent running with the tool (For demo, we directly specify the tool name here.)
caption = agent.run(f'Use the tool `{tool.name}` to describe the image.', image=Image.open('demo.png'))
print(caption)