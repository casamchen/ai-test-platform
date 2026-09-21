import json


def fix_parentheses(s):
        # 计数器，用来追踪括号的匹配情况
        counter = 0
        # 新字符串，用来存储修复后的字符串
        new_s = ''
        
        for char in s:
            # 遇到左括号时增加计数器
            if char == '[':
                counter += 1
            # 遇到右括号时减少计数器
            elif char == ']':
                counter -= 1
            # 将字符添加到新字符串中
            new_s += char
        
        # 如果计数器不为零，说明括号不匹配
        if counter != 0:
            # 如果计数器大于零，说明缺少右括号
            if counter > 0:
                new_s += ']' * counter
            # 如果计数器小于零，说明缺少左括号
            elif counter < 0:
                new_s = '[' * abs(counter) + new_s
        
        return new_s

def fix_json_loads(data):
    testcase_str = data['response']
    json_testcase = testcase_str.replace("‘operation’", '"operation"')
    json_testcase_1 = json_testcase.replace("‘operation’", '"operation"')
    json_testcase_2 = json_testcase_1.replace("‘expectedresult’", '"expectedresult"')
    json_testcase_3 = json_testcase_2.replace("，", ',')
    json_testcase_4 = json_testcase_3.replace("'", '"')
    json_testcase_5 = json_testcase_4.replace("‘", '"')
    json_testcase_6 = json_testcase_5.replace("、", '.')
    json_testcase_7 = json_testcase_6.replace("“", '')
    json_testcase_8 = json_testcase_7.replace("”", '')
    json_testcase_9 = json_testcase_8.replace("\\", ',')
    json_testcase_10 = json_testcase_9.replace('"expectedresult": "微信支付请求时checksum, timestamp, sign 三者必须存在,nname, price, order_id, description 四项可选但至少存在一项,nformat: "POST /pay/wxpay HTTP/1.1",nurl 必须是 https 协议开头且是以 pay 结尾 ", "item": [1]}','"expectedresult": "微信支付请求时checksum, timestamp, sign 三者必须存在,nname, price, order_id, description 四项可选但至少存在一项,nformat,POST /pay/wxpay HTTP/1.1,nurl必须是https协议开头且是以pay结尾,item,[1]"}')
    print(f'this is json_testcase_10:{json_testcase_10}')
    try:
        need_data = json.loads(json_testcase_10)
        return need_data
    except json.JSONDecodeError as e:
        line_number = e.lineno
        column_number = e.colno
        print(f"JSONDecodeError: {e}")
        context = json_testcase_10[max(0, column_number - 50):column_number + 50]
        print(f"Context around error: {context}")
        return f"JSONDecodeError: {e}"

def check_data_integrity(data):
    # 我们期望每个字典都有三个字段
    expected_fields = {'testpoint', 'operation', 'expectedresult'}

    # 检查每个字典的字段数量
    for item in data:
        # 创建一个集合来存储字典的字段
        item_fields = set(item.keys())
        miss_fields = expected_fields - item_fields
        if not miss_fields :
            right_message = f"{item} 符合预期，包含{expected_fields}字段。"
            return True,right_message
        else:
            error_message = f"{item} 不符合预期，以下字段{miss_fields}字段。"
            print(f'this is error_message:{error_message}')
            return False, error_message