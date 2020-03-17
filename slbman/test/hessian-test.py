from pyhessian.client import HessianProxy
import json

url = "http://172.16.1.204:8080/rpc/iPmsUserRpcService"


def modify_pwd(name, pwd):
    params = {'username': name, 'password': pwd}
    json_params = json.dumps(params)
    proxy = HessianProxy(url)
    res = proxy.updatePassword(json_params)  # 修改密码
    return res


def modify_contact(name, mobile, mail):
    contact_params = {'username': name, 'mobile': mobile, 'mail': mail}
    json_contact_params = json.dumps(contact_params)
    proxy = HessianProxy(url)
    res = proxy.updateContact(json_contact_params)  # 修改个人信息
    return res


if __name__ == '__main__':
    res = modify_pwd('zhoujunlong', '123456')
    # res = modify_contact('zhoujunlong', '13501141316', 'wuyanzu@linlinyi.cn')
    print(res.__dict__)
