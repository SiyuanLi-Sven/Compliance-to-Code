import json
import re
import asyncio
import aiohttp
from typing import Tuple, Dict, Any
import requests


def split_reason_and_content(response_content: str) -> dict:
    """
    从模型返回内容中分离思考过程 (reasoning_content) 和最终回复 (content)    
    """
    # 匹配 <think> 标签内容（支持跨行匹配）
    reason_match = re.search(r'<think>(.*?)</think>', response_content, re.DOTALL)
    
    reasoning_content = ""
    content = response_content
    
    if reason_match:
        # 提取思考内容并去除首尾空白
        reasoning_content = reason_match.group(1).strip()
        
        # 分离最终回复内容（排除 <think> 部分）
        content = re.sub(r'<think>.*?</think>', '', response_content, flags=re.DOTALL).strip()
    
    return reasoning_content, content


def call_gpt(prompt):
    url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
    headers = { 
        "Content-Type": "application/json", 
        "Authorization": "Bearer 6cc0e985ed884aaa82ecf805ad961658fa6ebdd6a16548f9938c04378ae7c3db"
    }
    data = { 
        "model": "DeepSeek-R1-671B", 
        "messages": [{"role": "user", "content": prompt}], 
        "temperature": 0,
        "top_p":0.0000000001,
        "top_k":1,
        "seed": 1379
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    raw_content = response.json()['choices'][0]['message']['content']
    reasoning_content, content = split_reason_and_content(raw_content)

    api_usage = response.json()['usage']

    return content, reasoning_content, api_usage



async def split_reason_and_content(response_content: str) -> Tuple[str, str]:
    """
    Asynchronously split model response into reasoning process and final content
    
    Args:
        response_content (str): The raw response content from the model
        
    Returns:
        Tuple[str, str]: A tuple containing (reasoning_content, content)
    """
    # Match content within <think> tags (supports multi-line)
    reason_match = re.search(r'<think>(.*?)</think>', response_content, re.DOTALL)
    
    reasoning_content = ""
    content = response_content
    
    if reason_match:
        # Extract reasoning content and strip whitespace
        reasoning_content = reason_match.group(1).strip()
        
        # Separate final response content (exclude <think> part)
        content = re.sub(r'<think>.*?</think>', '', response_content, flags=re.DOTALL).strip()
    
    return reasoning_content, content

async def call_gpt_async(prompt: str) -> Tuple[str, str, Dict[str, Any]]:
    """
    Asynchronously get content from HKUST-GZ API
    
    Args:
        prompt (str): The input prompt for the model
        
    Returns:
        Tuple[str, str, Dict[str, Any]]: A tuple containing (content, reasoning_content, api_usage)
        
    Raises:
        aiohttp.ClientError: If there's an error with the HTTP request
        json.JSONDecodeError: If the response cannot be parsed as JSON
        KeyError: If expected keys are missing from the response
    """
    url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 6cc0e985ed884aaa82ecf805ad961658fa6ebdd6a16548f9938c04378ae7c3db"
    }
    data = {
        "model": "DeepSeek-R1-671B",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "top_p": 0.0000000001,
        "top_k": 1,
        "seed": 1379
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_json = await response.json()
            
            raw_content = response_json['choices'][0]['message']['content']
            reasoning_content, content = await split_reason_and_content(raw_content)
            api_usage = response_json['usage']
            
            return content, reasoning_content, api_usage

# Example usage
async def main():
    try:
        content, reasoning, usage = await call_gpt_async("What is 2+2?")
        print(f"Content: {content}")
        print(f"Reasoning: {reasoning}")
        print(f"API Usage: {usage}")
    except Exception as e:
        print(f"Error occurred: {e}")



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
    asyncio.run(main())