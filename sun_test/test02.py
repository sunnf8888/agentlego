from agentlego import list_tools, load_tool

# 列出 AgentLego 中的所有工具
print(list_tools())

# 加载要使用的工具
calculator_tool = load_tool('Calculator')
print(calculator_tool.description)

# 直接调用工具
print(calculator_tool('cos(pi / 6)'))

# 图像或音频输入支持多种格式
from PIL import Image

image_caption_tool = load_tool('ImageCaption', device='cuda')
img_path = 'demo.png'
img_pil = Image.open(img_path)
print(image_caption_tool(img_path))
print(image_caption_tool(img_pil))