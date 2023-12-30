print("------------55555")
from agentlego.apis import load_tool

# load tool
tool = load_tool('OCR', device='cuda', lang='en', x_ths=3.)#, line_group_tolerance=30

from PIL import Image
img_path = 'demo_kie.jpeg'
img_pil=Image.open(img_path)

print(img_pil)
# apply tool
res = tool(img_path)
print(res)

# from lagent import ReAct, GPTAPI, ActionExecutor
# from agentlego.apis import load_tool

# # load tools and build agent
# # please set `OPENAI_API_KEY` in your environment variable.
# tool = load_tool('OCR', device='cuda').to_lagent()
# agent = ReAct(GPTAPI(temperature=0.), action_executor=ActionExecutor([tool]))

# # agent running with the tool.
# ret = agent.chat(f'Here is a receipt image `demo_kie.jpeg`, please tell me the total cost.')
# for step in ret.inner_steps[1:]:
#     print('------')
#     print(step['content'])