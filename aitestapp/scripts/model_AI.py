
from abc import abstractmethod
from typing import List
from zhipuai import ZhipuAI
from aitestapp.scripts.utils import encode_image_zhipu
import concurrent.futures
from aitestapp.scripts.config_interface import loadConfig
import json


class BaseModel:
    def __init__(self):
        pass

    @abstractmethod
    def get_model_response(self, prompt: str, images: List[str]):
        pass


class ZhiPuModel4V(BaseModel):
    def __init__(self):
        super().__init__()
        loadconfig = loadConfig()
        self.config_data = loadconfig.load_config()
        self.api_key = self.config_data['OPENAI_API_KEY']
        self.model = self.config_data['OPENAI_API_MODEL_4']


    def get_model_response(self, prompt: str, images: List[str]):
        """
        调用zhipuai的API接口，实现文本生成和图片解析功能
        :param prompt: 输入的文本
        :param images: 输入的图片
        :return: 返回的文本
        """
        client = ZhipuAI(api_key=self.api_key)

        content = [
            {
                "type": "text",
                "text": str(prompt)
            }
        ]

        for img in images:
            base64_img = encode_image_zhipu(img)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_img}"
                }
            })
            
        try:
            response = client.chat.completions.create(
                model = self.model,
                messages = [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                temperature = 0.1
            )

            return True, response.choices[0].message.content
        except Exception as e:
            return False, f'zhipuai request is fail:{str(e)}'


class ZhiPu4:
    def __init__(self) -> None:
        loadconfig = loadConfig()
        self.config_data = loadconfig.load_config()
        self.api_key = self.config_data['OPENAI_API_KEY']
        self.model = self.config_data['OPENAI_API_MODEL_4']
        self.max_threads = self.config_data['MAX_THREADING']

    def zhipuai_request(self, prompt):
        try:
            client = ZhipuAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model = self.model,
                messages = prompt,
                temperature = 0.1,
            )
            return True, response.choices[0].message.content
        except Exception as e:
            return False, f'zhipuai request is fail: {str(e)}'

    def get_model_response(self, prompts_list):
        """
        使用多线程方式调用zhipuai的API接口
        :param prompts_list: 输入的文本列表
        :return: 请求是否成功，返回的文本或错误信息
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_prompt = {executor.submit(self.zhipuai_request, prompt): prompt for prompt in prompts_list}
            for future in concurrent.futures.as_completed(future_to_prompt):
                prompt = future_to_prompt[future]
                try:
                    success, response = future.result()
                    yield prompt, success, response
                except Exception as e:
                    yield prompt, False, f'Error occurred: {str(e)}'

    def process_prompts(self, prompts_list):
        
        need_response = []
        for prompt, success, response in self.get_model_response(prompts_list):
            need_response.append(response)

        return need_response

    def excute_to_json(self, data):
        """
        安全地解析AI返回的JSON数据
        使用 json.loads 替代危险的 eval()，防止远程代码执行攻击
        """
        if not data or not isinstance(data, str):
            raise ValueError(f"无效的输入数据: {type(data)}")

        # 尝试直接解析（去除首尾空白）
        data = data.strip()
        if (data.startswith('[') and data.endswith(']')) or (data.startswith('{') and data.endswith('}')):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                pass

        # 尝试提取 markdown 代码块中的 JSON
        if '```json' in data:
            try:
                start_index = data.index('```json') + 7
                start_data = data[start_index:]
                end_index = start_data.index('```')
                end_data = str(start_data[:end_index]).replace("'", '"')

                json_data = json.loads(end_data)
                return json_data
            except (ValueError, json.JSONDecodeError):
                pass

        # 所有解析方式都失败，抛出异常而不是使用 eval()
        raise ValueError(f"无法安全解析AI返回的数据: {data[:200]}...")



