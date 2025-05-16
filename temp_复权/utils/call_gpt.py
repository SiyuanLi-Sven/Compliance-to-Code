import openai
import re

def call_gpt(prompt, 
             model='gpt-4o-2024-05-13',
             api_key=None, base_url=None, if_print=False,
             system_prompt="You are a helpful assistant.",
             temperature=0
             ):
    '''
    本函数用于获取大语言模型的回答. 默认模型为gpt-4o-2024-05-13, api_key已经预先设置. 如果模型不为openai模型, 会采用ollama调用. 
    输入:
        prompt: 提示词
    输出:
        content: 模型回复内容
        api_usage: api用量
    
    分类为openai模型: ['gpt-4o-2024-05-13', 'gpt-4o-mini-2024-07-18']
    部分的ollama模型: ['qwen2.5:0.5b', 'qwen2.5:1.5b', 'qwen2.5:3b', 'qwen2.5:latest', 'qwen2.5:14b']
    '''
    
    # 如果没有设置apikey, 就根据模型名字加载apikey
    if api_key==None:
        if model in ['gpt-4o-2024-05-13', 'gpt-4o-mini-2024-07-18']:
            api_key='pass'
        else:
            api_key='ollama'
    
    if base_url==None:
        if model in ['gpt-4o-2024-05-13', 'gpt-4o-mini-2024-07-18']:
            base_url=''
        else:
            base_url="http://10.4.182.51:11434/v1/"

    # 设置 API 基础 URL 和密钥
    client = openai.Client(api_key=api_key, base_url=base_url)

    # 调用 OpenAI SDK 生成对话
    completion = client.chat.completions.create(
        model=model,
        stream=False,
        temperature=temperature, 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    # 提取内容和使用情况
    content = completion.choices[0].message.content
    api_usage = completion.usage  # API 使用信息
    
    try:
        reasoning_content = completion.choices[0].message.reasoning_content
    except:
        reasoning_content = "reasoning_content not found"

    if if_print:
        print('QQQQQQQQQQ')
        print(prompt)
        print('AAAAAAAAAA')
        print(content)

    return content, reasoning_content, api_usage


async def call_gpt_async(prompt, 
                  model='gpt-4o-2024-05-13',
                  api_key=None, 
                  base_url=None, 
                  if_print=False,
                  temperature=0,
                  system_prompt="You are a helpful assistant."):
    '''
    异步版本 - 本函数用于获取大语言模型的回答. 默认模型为gpt-4o-2024-05-13, api_key已经预先设置. 
    如果模型不为openai模型, 会采用ollama调用. 
    输入参数与返回值与同步版本保持一致。
    '''
    
    # API 配置
    if api_key is None:
        api_key = 'pass' if model in ['gpt-4o-2024-05-13', 'gpt-4o-mini-2024-07-18'] else 'ollama'
    
    if base_url is None:
        base_url = 'pass' if model in ['gpt-4o-2024-05-13', 'gpt-4o-mini-2024-07-18'] else "http://10.4.182.51:11434/v1/"

    # 初始化异步客户端
    client = openai.AsyncClient(api_key=api_key, base_url=base_url)

    # 异步调用 API
    completion = await client.chat.completions.create(
        model=model,
        stream=False,
        temperature=temperature, 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    # 处理响应结果
    content = completion.choices[0].message.content
    api_usage = completion.usage
    
    try:
        reasoning_content = completion.choices[0].message.reasoning_content
    except AttributeError:
        reasoning_content = "reasoning_content not found"

    if if_print:
        print('QQQQQQQQQQ\n', prompt, '\nAAAAAAAAAA\n', content)

    return content, reasoning_content, api_usage


def safe_eval(content):
    """
    安全解析 content，将潜在元组字符串安全转化为 Python 对象。
    :param content: 字符串表示的潜在元组，例如 "(0, 'reason')"
    :return: 解析后的元组 (是否违反, 原因)，解析失败返回默认值
    """
    try:
        # 正则提取出可能的元组结构
        match = re.match(r"\(\s*(\d+)\s*,\s*['\"](.*)['\"]\s*\)", content, re.DOTALL)
        if match:
            # 提取元组中的第一个数字和第二个字符串部分
            is_violated = int(match.group(1))
            reason = match.group(2).strip()
            return is_violated, reason
        else:
            raise ValueError("Content does not match the expected tuple pattern")
    except Exception as e:
        # 打印错误日志并返回默认值
        print(f"Error parsing content: {content}, Error: {e}")
        return -1, "无法解析 content"
    

import pandas as pd
import os

def read_table_file(file_path):
    """
    自动识别并读取Excel或CSV文件，返回pandas DataFrame
    
    参数:
        file_path (str): 文件的完整路径
        
    返回:
        pandas.DataFrame: 读取的数据表
        
    异常:
        ValueError: 当文件格式不支持时抛出
        FileNotFoundError: 当文件不存在时抛出
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 获取文件扩展名（转换为小写以便比较）
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        # Excel文件 (.xlsx, .xls)
        if file_extension in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
            
        # CSV文件 (.csv)
        elif file_extension == '.csv':
            # 尝试不同的编码方式读取
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
            for encoding in encodings:
                try:
                    return pd.read_csv(file_path, encoding=encoding)
                except UnicodeDecodeError:
                    continue
            raise ValueError(f"无法以支持的编码方式读取CSV文件: {file_path}")
            
        else:
            raise ValueError(f"不支持的文件格式: {file_extension}")
            
    except Exception as e:
        raise Exception(f"读取文件时发生错误: {str(e)}")




if __name__ == "__main__":

    # content, api_usage = call_gpt(prompt='我刚才问你什么了',model='gpt-4o-2024-05-13',if_print=True)

    content, api_usage = call_gpt(prompt='我刚才问你什么了',model='qwen2.5:14b',if_print=True)

    # print(content)