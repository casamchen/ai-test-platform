import json

def check_json_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            try:
                data = json.loads(line)
                # 假设我们期望每个条目都有一个名为"conversations"的键
                if 'conversations' not in data:
                    print(f"Missing 'conversations' key in line {i}")
                else:
                    # 进一步检查"conversations"字段的内容
                    conversations = data['conversations']
                    for conversation in conversations:
                        if 'content' not in conversation:
                            print(f"Missing 'content' key in line {i}")
                        elif not isinstance(conversation['content'], str):
                            print(f"Non-string 'content' in line {i}: {conversation['content']}")
            except json.JSONDecodeError as e:
                print(f"Error in line {i}: {e}")

check_json_content('/Users/casamchen/Desktop/桌面 - Casam的笔记本电脑/train.json')