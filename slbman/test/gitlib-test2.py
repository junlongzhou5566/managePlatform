import requests

# url = 'http://172.16.1.15/api/v4/projects?private_token=jMcUscjt6znEqNmQcr_3&per_page=50'
url = 'http://172.16.1.15/api/v4/projects?private_token=jMcUscjt6znEqNmQcr_3&per_page=50'
# url = 'http://172.16.1.15/api/v4/projects/52/repository/files?private_token=jMcUscjt6znEqNmQcr_3'

user_url = 'http://172.16.1.15/api/v3/projects/15/users?private_token=jMcUscjt6znEqNmQcr_3&per_page=10'

my_gitlab_access_token = 'jMcUscjt6znEqNmQcr_3'
so_task_center_id = 52


r = requests.get(url)
print(r.text)
# data = r.json
# for i in data:
#     if i[u'name'] == 'Snack-Cherry':
#         print(i[u'id'])
