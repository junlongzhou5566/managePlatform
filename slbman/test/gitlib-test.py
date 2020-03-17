import gitlab
import requests

url = 'http://http://172.16.1.15/api/v3/projects?private_token=jMcUscjt6znEqNmQcr_3&per_page=50'
user_url = 'http://172.16.1.15/api/v3/projects/15/users?private_token=jMcUscjt6znEqNmQcr_3&per_page=10'

my_gitlab_access_token = 'jMcUscjt6znEqNmQcr_3'


# 获取项目id和项目名称
def get_project_id(project_url):
    r = requests.get(project_url)
    data = r.json()
    project_id_list = []
    project_name_list = []
    for i in data:
        project_id_list.append(i['id'])
        project_name_list.append(i['name'])
    return project_id_list, project_name_list


# 根据项目id获取项目下的用户信息
def get_project_user_list():
    id_list = get_project_id(url)
    project_id = id_list[0]
    project_name = id_list[1]
    for p_id in project_id:
        l = []
        project_user = requests.get(user_url.format(p_id))
        # 生成完整的用于显示项目下所有user的连接
        req_data = project_user.json()
        for i in req_data:
            l.append(i['name'])
        print(project_name[project_id.index(p_id)], l)


get_project_user_list()
