import requests, json, re, os, traceback

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

##############################################################
# url = 'https://ikuuu.art'
# email_passwd = {'poterliu@163.com': '19690726qq.com',
#                 'poterliu@126.com': '19690726qq.com',
#                 'poterliu@foxmail.com': '19690726qq.com',
#                 'xsliuos@gmail.com': '19690726qq.com',
#                 'juniuslau@126.com': '19690726qq.com',
#                 'ipoterliu@gmail.com': '19690726qq.com',
#                 'poterliu@outlook.com': '19690726qq.com',
#                 'poterliu@hotmail.com': '19690726gmail.com',
#                 'plwater@outlook.com': '19690726gmail.com',
#                 'likepoter@gmail.com': '19901010gmail.com',
#                 'bcmfullstacker@gmail.com': '19690726outlook.com',
#                 'liudanpo@gmail.com': '19901010gmail.com',
#                 'poterliu@qq.cm': '19690726qq.com'
#                 }
# email = 'poterliu@163.com'
# passwd = '19690726qq.com'
# SCKEY = 'SCT213232TKPvYwIZmzFymRChgU9MHMsgG'
# Bark_Token = 'RWsgW5brfK3eKqFjmvYRwW'
##############################################################

# data = {
#     'email': email,
#     'passwd': passwd
# }


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
            # print()
            pass
        # 进行签到
        post_result2 = session.post(url=check_url, headers=header)
        text2 = post_result2.text
        try:
            result = json.loads(text2)
            print(result['msg'])
        except Exception as ex:
            # print()
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
    json_str = json.dumps(email_passwd) 
    # print("Python 原始数据：", repr(email_passwd)) 
    # print("JSON 对象：", json_str)

    emailAndPasswd = json.loads(json_str) 
    print("Python 原始数据：", repr(email_passwd)) 
    print("JSON 对象：", json_str) 
    print("JSON 对象2：", emailAndPasswd)  

    for email in emailAndPasswd:
        print(email)
        passwd = emailAndPasswd[email]
        print(passwd)
        isSuccess = check_in(url, email, passwd)
        # 启用多个URL重试机制
        if not isSuccess:
            url2 = os.environ.get('URL2')
            if url2 is None:
                isSuccess = check_in(url2, email, emailAndPasswd[email])
        if not isSuccess:
            url3 = os.environ.get('URL3')
            if url3 is None:
                isSuccess = check_in(url3, email, emailAndPasswd[email])
        if not isSuccess:
            content = email + ',签到失败，原因是所有URL不可用'
            print(content)
            push_to_bark(content)
        print()


except Exception as ex:
    # logging.exception(ex)
    # print('--------------------')
    # traceback.print_exc()
    # print('--------------------')
    msg = traceback.format_exc()
    print(msg)
    # print('--------------------')

    content = email + ',签到失败'
    content += ',出现如下异常：' + str(ex)
    print(content)
    if SCKEY != '':
        push_to_wechat(content)
    push_to_bark(content)
