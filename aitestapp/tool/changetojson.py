import pandas as pd
import json

# 读取xlsx文件
df = pd.read_excel('/Users/casamchen/Desktop/桌面 - Casam的笔记本电脑/AItest/AItestplatform/AItestapp/document/训练用测试用例.xlsx')

# 初始化conversations列表
conversations = {}

# 遍历DataFrame的每一行
for index, row in df.iterrows():
    # 创建一个字典来存储当前行数据
    # conversation_dict = {"conversations":[{"role": "user","content": row['用例名称']},{"role": "assistant","content": "{'testpoint': {0}, 'operation': {1}, 'expectedresult': {2}}".format(row['用例名称'], row['用例步骤'], row['预期结果'])}]}
    conversation_dict = {"conversations":[
    {"role": "user", "content": row['用例名称']},
    {"role": "assistant", "content": json.dumps({
        "testpoint": row['用例名称'],
        "operation": "1、输入：用户名{0}、密码{1}、确认密码\n2、操作：点击注册按钮".format(row['用例名称'], row['用例步骤']),
        "expectedresult": row['预期结果']
    }, ensure_ascii=False)}
]}
    # 将字典添加到conversations列表中
    # conversations.append(conversation_dict)
    # 将字典转换为JSON字符串
    json_output = json.dumps(conversation_dict, ensure_ascii=False, indent=None)
    # 打印JSON字符串或者写入到文件中
    print(json_output)
    # 或者写入到文件
    with open('output1.json', 'a', encoding='utf-8') as f:
        f.write(json_output)
        f.write('\n')

# 创建最终的字典结构
# final_dict = {"conversations": conversations}

# # 将字典转换为JSON字符串
# json_output = json.dumps(final_dict, ensure_ascii=False, indent=4)

# 打印JSON字符串或者写入到文件中
# print(json_output)
# # 或者写入到文件
# with open('output.json', 'w', encoding='utf-8') as f:
#     f.write(json_output)