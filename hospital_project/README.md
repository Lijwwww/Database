## 数据库系统原理期末大作业——医院挂号系统

### 环境  
openGauss 5.1.0  
Django 3.0.0  / 5.0.0

```bash
pip install Django==3.0.0
```

创建Django项目：
`django-admin startproject 项目名`
创建app：
`python manage.py startapp 应用名`

确保配置并建立好数据库，然后将`connect_db`中`settings.py`的`DATABASE`修改为  
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_project', # 数据库名
        'USER': 'admin', # 用户名
        'PASSWORD': 'Gauss@123', # 密码
        'HOST': '192.168.56.109', # 虚拟机ip
        'PORT': 26000 # openGauss数据口的端口
    }
}
```
后端测试可用mysql暂时代替：
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital', # 改为数据库名字
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}
```

在`INSTALLED_APPS`注册app，即加上
```py
"hospital_site",  # hospital_site改为应用名
```
在`MIDDLEWARE`注册中间件，即加上
```py
"hospital_site.middleware.auth.AuthMiddleware",  # hospital_site改为应用名
```
可以选择将语言改为中文：
```py
LANGUAGE_CODE = "zh-hans"
```

执行以下命令生成表和运行服务器  
```
# 生成迁移文件
python manage.py makemigrations
# 执行sql语句生成数据表
python manage.py migrate
# 运行服务器
python manage.py runserver
```