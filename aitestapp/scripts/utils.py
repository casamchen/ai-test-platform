
import yaml
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from PIL import Image as zhipu_image
import io as zhipu_io
import base64
import json

def append_to_yaml(file_path, data, encoding='utf-8'):
    # 读取现有的YAML文件内容
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            existing_data = yaml.safe_load(file)
    except FileNotFoundError:
        existing_data = {}  # 文件不存在，则创建一个新字典

    # 合并现有的数据和新数据
    if existing_data is None:
        existing_data = {}  # 文件为空，则创建一个新字典
        
    existing_data.update(data)

    # 将合并后的数据写回YAML文件
    with open(file_path, 'w', encoding=encoding) as file:
        yaml.dump(existing_data, file, default_flow_style=False, allow_unicode=True)


def write_to_excel(file_path, data_list):
    # 创建一个新的Excel工作簿
    wb = Workbook()
    ws = wb.active

    # 假设data_list是一个包含多个字典的列表，每个字典的格式与提供的数据相同
    if not data_list:
        print("数据列表为空，无法写入Excel")
        return

    # 获取所有可能的列名
    all_titles = set()
    for data in data_list:
        all_titles.update(data.keys())

    # 写入标题行
    titles = list(all_titles)
    ws.append(titles)

    # 用来存储行号
    row_index = {}

    # 写入数据行
    for data in data_list:
        # 获取当前数据的行号，如果不存在则创建新行
        if data['title'] not in row_index:
            row_index[data['title']] = ws.max_row + 1
            # 创建新行并填充None
            ws.append([None] * len(titles))

        # 获取当前行的数据
        row_number = row_index[data['title']]

        # 更新当前行的数据
        for col_index, title in enumerate(titles):
            value = data.get(title)
            if value is not None:
                # 使用ws.cell来写入数据
                ws.cell(row=row_number, column=col_index + 1, value=str(value))

    # 调整列宽以适应内容
    for col_index, title in enumerate(titles):
        col_letter = get_column_letter(col_index + 1)
        ws.column_dimensions[col_letter].width = 20  # 设置列宽

    # 保存工作簿到指定路径
    wb.save(file_path)


def encode_image_zhipu(image_path):
    with zhipu_image.open(image_path) as image:
        buffered = zhipu_io.BytesIO()
        image.save(buffered, format="PNG")  # or format="PNG", depending on your image.
        img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str


def filter_interface(key_list, data, ty):
    """
    通过Key筛选出来对应的接口
    """

    if ty == 1:
        data_list = []
        for key in key_list:
            for api_info in data:
                if api_info['url'] == key['api_path']:
                    data_list.append(api_info)
        
        return data_list
            
    if ty == 2:
        data_list = []
        for key in key_list:
            print(f'this is 104:{key}')
            print(f'this is 105{key_list}')
            first_key = list(data.keys())[0]
            print(f'this is 107{first_key}')
            if first_key == key['api_path']:
                data_list.append(data)
        return data_list
    
    if ty == 3:
        data_list = []
        for key in key_list:
                if data['url'] == key['api_path']:
                    data_list.append(data)
        return data_list

def excute_to_json(data):
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
            end_data = start_data[:end_index].strip().replace("'", '"')
            return json.loads(end_data)
        except (ValueError, json.JSONDecodeError):
            pass

    # 尝试提取普通代码块中的 JSON
    if '```' in data:
        try:
            start_index = data.index('```') + 3
            # 跳过语言标识符行
            newline = data.index('\n', start_index)
            end_index = data.index('```', newline)
            end_data = data[newline:end_index].strip().replace("'", '"')
            return json.loads(end_data)
        except (ValueError, json.JSONDecodeError):
            pass

    # 所有解析方式都失败，抛出异常而不是使用 eval()
    raise ValueError(f"无法安全解析AI返回的数据，请检查格式: {data[:200]}...")