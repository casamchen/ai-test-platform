

class Prompts:

    @staticmethod
    def api_desc_prompt(api_doc):
        """
        根据接口详细信息构造生成接口测试描述，也就是使用的提示词。

        参数:
        api_doc (str): 测试用例的描述。

        返回:
        str: 构造好的提示词。
        """
        example_api = """
{'title': '获取学员课程安排接口', 'method': 'GET', 'url': '/api/getUserCourse/', 'params': [], 'response': [['code', 'int', '状态码（0表示成功，1表示数据不存在）'], ['msg', 'string', '操作结果消息，如果code为0，则包含课程安排信
息']], 'status': [['200', '请求成功，返回课程安排信息'], ['401', '用户未登录']], 'example': 'GET /api/getUserCourse/', 'notes': ['用户必须登录才能访问此接口。', '接口会根据用户的最新评分记录来决定返回哪个课程安排。', '如果用户没
有评分记录，或者评分记录不符合条件，接口将返回第一个课程安排。', '如果用户有评分记录但不符合条件，接口将返回用户当前的课程安排。', '如果出现异常，接口将返回内部服务器错误。']}
"""

        example_desc = """
接口描述：

作用：获取学员课程安排接口用于获取用户的课程安排信息。当用户成功登录后，通过发送GET请求到指定URL，可以获取到与该用户相关的课程安排信息。
执行依赖：用户必须登录才能访问此接口。这意味着在执行此接口之前，需要先执行用户登录接口，以确保用户身份的合法性。
接口依赖先后顺序：首先执行用户登录接口，然后才能执行获取学员课程安排接口。用户登录接口的成功返回结果将作为获取学员课程安排接口的执行条件。
数据传递：用户登录接口的返回结果中可能包含了一些与用户身份相关的信息，如用户ID、登录凭证等。在执行获取学员课程安排接口时，需要将这些信息作为请求的一部分传递给服务器，以便服务器能够验证用户的身份并返回相应的课程安排信息。具体的数据传递方式可能是在请求头中添加认证信息，或者将用户ID作为请求参数传递。
总结：获取学员课程安排接口是一个用于获取用户课程安排信息的接口，需要先执行用户登录接口，并将用户身份信息传递给服务器，才能成功获取到课程安排信息。接口的返回结果中包含了状态码和操作结果消息，可以根据状态码来判断请求是否成功，并根据操作结果消息来获取课程安排信息。
"""
        
        system_content = """
你是一位专业的测试工程师，接下来请根据接口的内容生成对应的描述，从接口的作用、执行这个接口的依赖、执行接口依赖接口的先后顺序、依赖接口和被依赖接口的参数怎么传这几个角度，字数控制在200个汉字以内,
其中desc 要求从接口的作用、执行这个接口的依赖、执行接口依赖接口的先后顺序、依赖接口和被依赖接口的参数怎么传这几个角度考虑
请严格按照要求的格式生成数据，不要生成任何与要求无关的内容，仅根据信息内容生成，不要额外的臆造或者创造，一定要严谨。
"""

        prompt = [
            {"role": "user", "content": system_content},
            {"role": "assistant", "content": "好的，我会从接口的作用、执行这个接口的依赖、执行接口依赖接口的先后顺序、依赖接口和被依赖接口的参数怎么传这几个角度描述"},
            {"role": "user", "content": example_api},
            {"role": "assistant", "content": example_desc},
            {"role": "user", "content": str(api_doc)}
        ]
        
        return prompt
    

    @staticmethod
    def api_case_prompt(api_inf):
        """
        根据接口描述和测试用例分析生成筛选对应的接口和顺序，并给出对应的参数

        参数:
        api_inf (list): 

        返回:
        str: 构造好的提示词。
        """

        system_content = """你是一个专业的测试工程师，请根据我提供的接口描述和测试用例分析，帮我筛选出对应的接口和执行步骤顺序。
        我需要你做的事是，帮我分析并筛选出对应的测试用例需要用到哪些接口，并通过测试用例分析出所有接口的执行顺序。
        最终，你应该严格按照类似这样的格式和结果返回： [{"step":1, "api_path": "/api/register"}, {"step":2, "api_path": "/api/login"}]。
        其中step为执行顺序，api_path为接口的path。
        生成时请忽略接口描述中描述要求，接口描述只是为了帮助你理解接口，不起到限制作用，限制作用请用测试用例分析。
        举个例子加深你的理解，如测试用例描述为："测试点：不进行登录，检查学员当前课程进度，预期结果：获取学员当前进度课程信息失败"。
        那你的生成结果中就不应该包含登录接口，返回实例就应该为： [{"step":1, "api_path": "/api/get_course_progress"}]（此示例中因测试用例不要求登录所以就没有登录接口）。
        所以，生成接口测试的执行步骤时，请严格分析并按照测试用例的要求筛选接口和操作步骤，不要给与测试用例描述要求无关的接口，请一定要严谨，并且生成的格式需要严格按照json的格式。
        """

        example_api = """
        接口描述为：{'/api/login/': '接口描述：作用：登录接口用于用户登录系统，通过验证用户名和密码来允许用户访问受保护的资源。执行依赖：用户需要访问系统资源时，如果未被认证，则需要先执行登录接口。接口依赖先后顺序：在执行任何需要用户认证的操作之前，必须先执行登录接口。数据传递：用户通过POST请求发送用户名和密码到服务器，这些参数作为请求的表单数据传递。总结：登录接口是一个关键的安全接口，它验证用户的身份并创建会话。用户必须提供正确的用户名和密码才能登录成功。登录过程中，接口会对IP地址进行限制，限制每天访问次数以防止滥用。如果登录失败或出现异常，接口将返回相应的错误信息。'}。
        测试用例为：测试点：输入正确的账号和密码进行，预期结果：登录成功。
        """

        example_desc = """[{"step":1, "api_path": "/api/login/"}]"""

        prompt = [
            {"role": "user", "content": system_content},
            {"role": "assistant", "content": "好的，我会根据你提供的接口描述筛选和对测试用例进行分析，帮你做好执行步骤的排序，请提供你的接口描述和测试用例。"},
            # {"role": "user", "content": example_api},
            # {"role": "assistant", "content": example_desc},
            {"role": "user", "content": str(api_inf)}
        ]
        
        return prompt


    @staticmethod
    def api_operation_prompt(api_test_data):
        """
        根据接口信息和测试数据生成测试参数
        """

        system_content = """
        你是一个专业的测试工程师，我会给你提供的接口信息、测试数据、测试用例、测试用例对应的执行步骤这4项信息数据，帮我根据测试用例需要的数据筛选并生成并配置对应的测试参数。
        最终，你应该严格按照类似这样的格式和结果返回：[{'step': 1, 'api_path': '/api/login/', 'params': {'username': '18127039525', 'password': 'walker1990'}}, {'step': 2, 'api_path': '/api/getUserCourse/', 'params': {}}]。
        其中params为测试用例执行步骤对应url所需的参数，params中key（举例：如username）接口信息中的参数，对应的value（举例：如'18127039525'）)为测试数据中筛选出来的数据。
        当接口不需要任何参数时，请直接将setp对应的params填充为 {}。
        当接口需要参数时，请严格按照这样的格式[{'step': 1, 'api_path': '/api/login/', 'params': {'username': '18127039525', 'password': 'walker1990'}}, {'step': 2, 'api_path': '/api/getUserCourse/', 'params': {}}]格式生成，请严格按照格式要求生成。
        当params已经存在时，对应的value不需要再封装一个params键值对，params键值对应该是这样的表现形式：'params': {'username': '18127039525', 'password': 'walker1990'}，禁止出现：'params': {'param': {'username': '18127039525', 'password': 'walker1990'}}这样的格式，这是错误的格式
        """

        example_api = """
        接口信息为：{'title': '登录接口', 'method': 'POST', 'url': '/api/login/', 'params': [['username', 'string', '用户名（必填）'], ['password', 'string', '密码（必填）']], 'response': [['code', 'int', '状态码（0表示登录成功
，其他表示登录失败）'], ['msg', 'string', '操作结果消息'], ['user', 'string', '登录成功后返回的用户名'], ['error', 'string', '错误消息（当发生异常时存在）']], 'status': [['200', '请求成功，登录成功'], ['401', '用户未登录'], ['403', '用户名或密码错误'], ['404', '账号已过期'], ['500', '内部服务器错误']], 'example': 'POST /api/login/\nContent-Type: application/x-www-form-urlencoded\nBody: username=user123&password=pass123', 'notes': ['该接口对IP地址进行限制，每个IP每天最多访问30次。', '用户必须输入有效的用户名和密码才能登录。', '登录成功后，用户的session会被创建并记录在数据库中。', '如果登录过程中出现异常，接口将返回
错误信息。', '接口会记录用户的登录行为。']}。
        测试数据为：[{'data': {'username': '18127039525', 'password': 'walker1990'}, 'desc': '正确的账号和密码'}, {'data': {'username': 'walker', 'password': '123456'}, 'desc': '错误的账号和密码'}]。
        测试用例为：测试点：输入正确的账号和密码进行，预期结果：登录成功。
        测试用例对应的执行步骤为：[{'step': 1, 'api_path': '/api/login/'}]。
"""
        example_desc = """[{'step': 1, 'api_path': '/api/login/', 'params': {"username": "18127039525", "password": "walker1990"}}]"""

        prompt = [
            {"role": "user", "content": system_content},
            {"role": "assistant", "content": "好的，我会根据你提供的接口描述筛选和对测试用例进行分析，帮你做好执行步骤的排序，请提供你的接口描述和测试用例。"},
            {"role": "user", "content": example_api},
            {"role": "assistant", "content": example_desc},
            {"role": "user", "content": api_test_data}
        ]
        
        return prompt