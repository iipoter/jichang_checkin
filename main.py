import requests, json, re, os

session = requests.session()
# 机场的地址
url = os.environ.get('URL')
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')
# server酱
SCKEY = os.environ.get('SCKEY')
# 推送BARK的token
Bark_Token = os.environ.get('BARK_TOKEN')

login_url = '{}/auth/login'.format(url)
check_url = '{}/user/checkin'.format(url)


header = {
        'origin': url,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
data = {
        'email': email,
        'passwd': passwd
}
try:
    print('进行登录...')
    response = json.loads(session.post(url=login_url,headers=header,data=data).text)
    print(response['msg'])
    # 进行签到
    result = json.loads(session.post(url=check_url,headers=header).text)
    print(result['msg'])
    content = email + ' ' + result['msg']
    # 进行推送
    if SCKEY != '':
        push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
        requests.post(url=push_url)
    # 推送到 Bard iOS APP
    if Bark_Token != '':
        push_url = 'https://api.day.app/{}/机场签到/{}'.format(Bark_Token, content)
        requests.get(url=push_url)
        print('推送成功')
except Exception as ex:
    content = email + ' ' + '签到失败'
    content +=  '. 出现如下异常：' + str(ex)
    print(content)
    if SCKEY != '':
        push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
        requests.post(url=push_url)
    # 推送到 Bard iOS APP
    if Bark_Token != '':
        push_url = 'https://api.day.app/{}/机场签到/{}'.format(Bark_Token, content)
        requests.get(url=push_url)
