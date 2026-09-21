import os

# 从环境变量读取 API Key，避免硬编码敏感信息
API_key = os.environ.get('ZHIPUAI_API_KEY', '')
