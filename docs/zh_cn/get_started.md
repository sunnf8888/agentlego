# 安装

根据您的情况选择安装方法：

## 安装完整工具包

安装完整工具包，你可以直接使用几乎所有工具（除了 ImageBind 和 SAM 等工具需要额外的依赖）。

1. 设置您的 torch 环境（如果已经完成则跳过此步骤）

```bash
conda create -n agentlego python=3.10
```

并按照[官方指南](https://pytorch.org/get-started/locally/#start-locally)安装 PyTorch 包（包括 torch,
torchvision 和 torchaudio）。

2. 安装 AgentLego 和一些常见的依赖项。

```bash
pip install agentlego[optional] openmim

# 用于图像理解工具。
pip install mmpretrain mmdet mmpose easyocr

# 用于图像生成工具。
pip install transformers diffusers mmagic
```

3. 某些工具需要额外的依赖项，在使用之前请查看 `Tool APIs` 中的 **Set up** 部分。

## 仅安装最简依赖

仅安装最简依赖，您可以使用类似于 GoogleSearch、Translation 和您自己的自定义工具的部分工具。此外，如果您从远程工具服务器调用工具，则客户端只需要简单的依赖项。

```bash
pip install agentlego
```

# 快速开始

## 直接使用工具

您可以在 AgentLego 中直接调用所有工具。

```Python
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
img_path = './examples/demo.png'
img_pil = Image.open(img_path)
print(image_caption_tool(img_path))
print(image_caption_tool(img_pil))
```

## 集成到智能体框架

### Lagent

[Lagent](https://github.com/InternLM/lagent) 是一个轻量级的开源框架，允许用户高效地构建基于大型语言模型（LLM）的智能体。

以下是一个示例脚本，将 agentlego 工具集成到 Lagent 中：

```python
from agentlego.apis import load_tool
from lagent import ReAct, GPTAPI, ActionExecutor

# 加载您想要使用的工具
tool = load_tool('Calculator').to_lagent()

# 构建 Lagent 智能体
model = GPTAPI(temperature=0.)
agent = ReAct(llm=model, action_executor=ActionExecutor([tool]))

user_input = '如果三角形的边长分别为 3cm、4cm 和 5cm，请告诉我三角形的面积。'
ret = agent.chat(user_input)

# 打印所有中间步骤结果
for step in ret.inner_steps[1:]:
   print('------')
   print(step['content'])
```

### LangChain

[LangChain](https://python.langchain.com/docs/get_started/introduction) 是一个用于创建利用语言模型的应用程序的框架。它提供了上下文感知和推理能力，为与语言模型一起使用和针对特定任务的预定义链提供了组件，使用户可以轻松地开始和自定义应用程序。

以下是一个示例脚本，将 agentlego 工具集成到 LangChain 中：

```python
from agentlego.apis import load_tool
from langchain.agents import AgentType, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

# 加载要使用的工具。
tool = load_tool('Calculator').to_langchain()

# 构建 LangChain 智能体链
model = ChatOpenAI(temperature=0., model='gpt-4')
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
agent = initialize_agent(
   agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
   llm=model,
   tools=[tool],
   memory=memory,
   verbose=True,
)

user_input = '如果三角形的边长分别为3cm、4cm和5cm，请用工具计算三角形的面积。'
agent.run(input=user_input)
```

### Transformers Agent

[HuggingFace Transformers agent](https://huggingface.co/docs/transformers/transformers_agents) 是一个可扩展的自然语言 API，它理解用户输入并挑选工具进行操作。它允许轻松地集成由社区开发的其他工具。

以下是一个示例脚本，将 agentlego 工具集成到 Transformers agent 中：

```python
from agentlego.apis import load_tool
from transformers import HfAgent

# 加载要使用的工具
tool = load_tool('Calculator').to_transformers_agent()

# 构建 Transformers Agent
prompt = open('examples/hf_agent/hf_demo_prompts.txt', 'r').read()
agent = HfAgent(
   'https://api-inference.huggingface.co/models/bigcode/starcoder',
   chat_prompt_template=prompt,
   additional_tools=[tool],
)

user_input = '如果三角形的边长分别为3厘米、4厘米和5厘米，请告诉我三角形的面积。'
agent.chat(user_input)
```

# 工具服务器

AgentLego 提供了一套工具服务器辅助程序，帮助您在服务器上部署工具，并在客户端上像使用本地工具一样调用这些工具。

## 启动服务器

我们提供了一个 `server.py` 脚本来启动工具服务器。您可以指定要启动的工具类别。

```bash
python server.py Calculator ImageCaption TextToImage
```

然后，服务器将启动所有工具。

```bash
INFO:    Started server process [1741344]
INFO:    Waiting for application startup.
INFO:    Application startup complete.
INFO:    Uvicorn running on http://0.0.0.0:16180 (Press CTRL+C to quit)
```

## 在客户端使用工具

在客户端，您可以使用工具服务器的 URL 创建所有远程工具。

```python
from agentlego.tools.remote import RemoteTool

# 从工具服务器 URL 创建所有远程工具。
tools = RemoteTool.from_server('http://127.0.0.1:16180')
for tool in tools:
   print(tool.name, tool.url)

# 从工具服务器端点创建单个远程工具。
# 所有端点都可以在工具服务器的文档中找到，例如 http://127.0.0.1:16180/docs
tool = RemoteTool('http://127.0.0.1:16180/ImageDescription')
print(tool.description)
```
