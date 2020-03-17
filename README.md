# managePlatform 运维自动化管理平台 主要调用阿里云的openapi实现对阿里云资源的管理

# 功能介绍:
    1.调用阿里云负载管理api实现发布代码前后的上下负载操作，研发人员可自行操作各自项目，无需运维干预；
    2.调用阿里云cdn管理api实现刷新cdn功能，研发人员可自主完成；
    3.域账号管理功能
    4.对接钉钉实现定制化通知功能

# 部署： 
    1.安装python3 源码安装即可
    
    2.安装项目依赖包 
        # pip install aliyun-api
        # pip install aliyun-api-gateway-sign-py3
        # pip install aliyun-python-sdk
        # pip install aliyun-python-sdk-core
        # pip install aliyun-python-sdk-ecs
        # pip install Django
        # pip install ldap3
        # pip install PyMySQL
        # pip install requests
        
    3.Clone code
        # git clone https://github.com/junlongzhou5566/managePlatform.git
        
    4.更改数据库连接地址
        # cd slbman;vim slbman/settings.py
        
    5.创建表
        # python manage.py makemigrations
        # python manage.py migrate
    
    6.启动项目
        # python manage.py runserver 0.0.0.0 & 也可自行编写启动脚本启动
        
    7.访问
        # curl localhost:8000
        
    本项目对接的是公司域控账号，使用域控账号即可登录  
