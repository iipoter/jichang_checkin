import requests, json, re, os, traceback, ast

session = requests.session()
# 机场的地址
url = os.environ.get('URL1')
# 配置用户名（一般是邮箱）
# email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
# passwd = os.environ.get('PASSWD')
# server酱
SCKEY = os.environ.get('SCKEY')
# 推送BARK的token
Bark_Token = os.environ.get('BARK_TOKEN')
email_passwd = os.environ.get('EMAIL_PASSWD')



def check_in(url, email, passwd):
    login_url = '{}/auth/login'.format(url)
    check_url = '{}/user/checkin'.format(url)
    header = {
        'origin': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    data = {
        'email': email,
        'passwd': passwd
    }
    try:
        print('进行登录...')
        post_result = session.post(url=login_url, headers=header, data=data)
        text = post_result.text
        content0 = post_result.content
        try:
            response = json.loads(text)
            print(response['msg'])
        except Exception as ex:
            pass
        # 进行签到
        post_result2 = session.post(url=check_url, headers=header)
        text2 = post_result2.text
        try:
            result = json.loads(text2)
            print(result['msg'])
        except Exception as ex:
            pass
        # 进行推送
        content = email + ',' + result['msg']
        if SCKEY != '':
            push_to_wechat(content)
        push_to_bark(content)
        return True
    except Exception as ex:
        content = '出现如下异常：' + str(ex)
        print(content)
        return False


# 推送到微信公众号
def push_to_wechat(content):
    push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
    print('wechat url=' + push_url)
    msg = requests.post(url=push_url)
    message = msg.__getattribute__('content')
    print(message.decode('unicode_escape'))
    print('wechat推送成功')


# 推送到 Bard iOS APP
def push_to_bark(content):
    push_url = 'https://api.day.app/{}/机场签到/{}'.format(Bark_Token, content)
    print('bark url=' + push_url)
    msg = requests.get(url=push_url)
    message = msg.__getattribute__('content')
    print(message.decode('unicode_escape'))
    print('bark推送成功')


try:
    if url is None:
        print("url is empty")
        exit(1)
    if email_passwd is None:
        print("email_passwd is empty")
        exit(1)

    # 将 JSON 对象转换为 Python 字典
    # json_str = json.dumps(email_passwd)

    # print(type(email_passwd))
    print('email_passwd type=', type(email_passwd))
    emailAndPasswd = ast.literal_eval(email_passwd)
    print('emailAndPasswd type=', type(emailAndPasswd))
    emailAndPasswd1 = eval(email_passwd)
    print('emailAndPasswd1 type=', type(emailAndPasswd1))

    jsonRepr = repr(email_passwd)
    print('jsonRepr type=', type(jsonRepr))    
    emailAndPasswd = json.loads(email_passwd)
    print('emailAndPasswd type=', type(emailAndPasswd))
    
    # if(isinstance(email_passwd, str) | isinstance(email_passwd, bytes)):
        # emailAndPasswd1 = eval(email_passwd)
        # print(type(emailAndPasswd1))
        # emailAndPasswd = ast.literal_eval(email_passwd)
        # print(type(emailAndPasswd))

    for email in emailAndPasswd:
        # print('email=' + email)
        passwd = emailAndPasswd[email]
        # print('passwd=' + passwd)
        isSuccess = check_in(url, email, passwd)
        # 启用多个URL重试机制
        if not isSuccess:
            url2 = os.environ.get('URL2')
            if url2 is None:
                isSuccess = check_in(url2, email, passwd)
        if not isSuccess:
            url3 = os.environ.get('URL3')
            if url3 is None:
                isSuccess = check_in(url3, email, passwd)
        if not isSuccess:
            content = email + ',签到失败，原因是所有URL不可用'
            print(content)
            push_to_bark(content)
        print()
except Exception as ex:
    msg = traceback.format_exc()
    print(msg)

    content = '签到失败'
    content += ',出现如下异常：' + str(ex)
    print(content)
    if SCKEY != '':
        push_to_wechat(content)
    push_to_bark(content)
