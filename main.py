import requests, json, re, os

session = requests.session()
# 机场的地址
# url = os.environ.get('URL1')
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')
# server酱
SCKEY = os.environ.get('SCKEY')
# 推送BARK的token
Bark_Token = os.environ.get('BARK_TOKEN')


data = {
    'email': email,
    'passwd': passwd
}


def check_in(url):
    login_url = '{}/auth/login'.format(url)
    check_url = '{}/user/checkin'.format(url)
    header = {
        'origin': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    try:
        print('进行登录...')
        response = json.loads(session.post(url=login_url, headers=header, data=data).text)
        print(response['msg'])
        # 进行签到
        result = json.loads(session.post(url=check_url, headers=header).text)
        print(result['msg'])
        content = email + ' ' + result['msg']
        # 进行推送
        if SCKEY != '':
            push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
            requests.post(url=push_url)
        # 推送到 Bard iOS APP
        # if Bark_Token != '':
        push_url = 'https://api.day.app/{}/机场签到/{}'.format(Bark_Token, content)
        requests.get(url=push_url)
        print('推送成功')
        return True
    except Exception as ex:
        content = '出现如下异常：' + str(ex)
        print(content)
        return False


try:
    url = os.environ.get('URL1')
    if url is None:
        print("url is empty")
        exit(1)
    if email is None:
        print("email is empty")
        exit(1)
    if passwd is None:
        print("passwd is empty")
        exit(1)
    isSuccess = check_in(url)
    # 启用多个URL重试机制
    if not isSuccess:
        url = os.environ.get('URL2')
        isSuccess = check_in(url)
    if not isSuccess:
        url = os.environ.get('URL3')
        isSuccess = check_in(url)
    if not isSuccess:
        content = email + ' 签到失败，原因是所有URL不可用'
        push_url = 'https://api.day.app/{}/机场签到/{}'.format(Bark_Token, content)
        print(content)
        requests.get(url=push_url)
except Exception as ex:
    content = email + ' ' + '签到失败'
    content += '. 出现如下异常：' + str(ex)
    print(content)
    if SCKEY != '':
        push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
        requests.post(url=push_url)
    # 推送到 Bard iOS APP
    # if Bark_Token != '':
    push_url = 'https://api.day.app/{}/机场签到/{}'.format(Bark_Token, content)
    requests.get(url=push_url)
