# siliconflow
# top_p 可用
base_url='https://api.siliconflow.cn/v1/'
api_key = 'sk-pjehghewarxxefoobqaswnxfehvygtronxghqiuahasfgadq'
model="deepseek-ai/DeepSeek-R1"



# volces bytedance
# top_p 不可用
prompt='请撰写一段关于北极熊的冷笑话',
api_key="35684824-1776-48b6-94fd-96c2e99d0724",
base_url="https://ark.cn-beijing.volces.com/api/v3",
model="ep-20250217153824-9xcbx",



# from openai import OpenAI
# url = 'https://api.siliconflow.cn/v1/'
# api_key = 'sk-pjehghewarxxefoobqaswnxfehvygtronxghqiuahasfgadq'

# client = OpenAI(
#     base_url=url,
#     api_key=api_key
# )

# # 发送非流式输出的请求
# messages = [
#     {"role": "user", "content": "讲一个北极熊笑话"}
# ]
# response = client.chat.completions.create(
#     model="deepseek-ai/DeepSeek-R1",
#     messages=messages,
#     stream=False, 
#     top_p=0.95
    
#     # max_tokens=4096
# )

# content = response.choices[0].message.content
# reasoning_content = response.choices[0].message.reasoning_content

# print("__________reasoning_content__________")
# print(reasoning_content)
# print("__________content__________")
# print(content)