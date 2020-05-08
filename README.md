从 react_tailwind_boilerplate 库 和 https://github.com/nicholaskajoh/React-Django   改装，tailwindcss版本改为1.4.0 以上。
react_tailwind_boilerplate 直接从create-react-app 开始

# 背景
本库的目的是解决在django中使用react和tailwindcss的问题。在django中使用react，主要解决模版文件夹指定和react独立开发时保持热启动和api连接。react中使用tailwindcss，主要解决css热启动、自定义theme及tree shaking。

### 1. 基本思路

-  react可以独立开发，热启动，能用tailwindcss的自定义功能。这些在simpleDjangoReact库里是做不到的。参考  https://github.com/nicholaskajoh/React-Django    这个库的做法，在react app里放django，而不是django app里放react，可以最大化发挥create-react-app的强大功能。

- 利用django的注册系统，所以选择通过django的view访问react的html的方式。html来自react的build文件夹下的index.html，因此django的template文件夹定义为

```python
        'DIRS': [
            os.path.join(BASE_DIR, 'build')
        ],
```
- 通过django-rest-framework的API传数据到react。

  react build成的html被当作是django的一个正常的html template，因此react访问的域名按道理只需要相对域名，即http://127.0.0.1:8000/api/lead/  后面的api/lead部分；

  但在react dev阶段，因为我们都是通过http://127.0.0.1:3000/   来热启动react，因此需要在react里显式指定http://127.0.0.1:8000   部分，并且在django的dev模式下需要安装django-cors-headers允许跨域请求。

- dev下的API域名处理，参考 https://medium.com/@tacomanator/environments-with-create-react-app-7b645312c09d ， 将package.json里的

```
    "start": "react-scripts start",
```
改为
```
    "start": "REACT_APP_API_DOMAIN='http://127.0.0.1:8000' react-scripts start",
```
在react app的开发过程中，对于API的使用，一律用 process.env.REACT_APP_API_DOMAIN + '/api/lead' 形式代表API的url，如
```
const url = process.env.REACT_APP_API_DOMAIN + '/api/lead'
    fetch(url)
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
```

### 2. 操作流程

```shell
git clone https://github.com/neversay4ever/django_react_tailwind_boilerplate django_react_project
cd django_react_project
npm i install
npm run build
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements -i https://pypi.tuna.tsinghua.edu.cn/simple
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
```

### 3. django包说明

- 使用Django2.2.10 LTS版本，注意2.2.10之前版本有sql注入安全问题，GitHub 上有警示。
- 使用django-rest-framwork（附带安装markdown和django-filter）提供API

```shell
pip install Django==2.2
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```

- 安装 whitenoise，可以在production阶段对static文件server，不需要通过nginx。whitenoises使用方法见http://whitenoise.evans.io/en/stable/  ，注意版本的差异。本库使用5.0.1版

```shell
pip install whitenoise==5.0.1
```

- django的admin部分，引入djangoql和django-import-export，分别是admin下复杂检索和导入excel用的。
```shell
pip install djangoql===0.13.1
pip install django-import-export===2.1.0
```
   在admin.py中的代码为

```python
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin

class CustomModelAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"]
        self.search_fields = [
            field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdmin, self).__init__(model, admin_site)

from .models import DemoModel
@admin.register(DemoModel)
class DemoAdmin(CustomModelAdmin):
    pass

```

- 如上第3步所述，安装django-cors-headers允许dev形式下的跨域请求。

```shell
pip install django-cors-headers==3.2.1
```

### 4. npm安装包说明

- create-react-app，自带react, babel, webpack等

- 安装tailwindcss相关，参考 <https://www.smashingmagazine.com/2020/02/tailwindcss-react-project/> 
```shell
npm install tailwindcss postcss-cli autoprefixer -D
```

- axios，参考https://www.robinwieruch.de/react-hooks-fetch-data

```shell
npm i axios
```
使用方法参考
```
import React, { useState, useEffect } from 'react';
import axios from 'axios'

const Apitest = () => {
    const url = process.env.REACT_APP_API_DOMAIN + '/api/test'

    const [data, setData] = useState([]);

    const fetchData = async () => {
        const result = await axios(url);
        setData(result.data);
    };

    useEffect(() => {

        fetchData();
    }, []);

    return (
        <ul>
            {data.map(item => (
                <li key={item.objectID}>
                    <a href={item.name} className='text-red-500'>{item.email}</a>
                </li>
            ))}
        </ul>
    );
}

export default Apitest;
```

### 5.各种bug的解决

- npm run start 正常，但是 npm run build后的html显示不正常，见https://stackoverflow.com/questions/46235798/relative-path-in-index-html-after-build 
  解决方法是在 package.json中增加 "homepage": "./",

```json
  "name": "bee_front",
  "version": "0.1.0",
  "homepage": "./",
```

- npm run build后的html能在浏览器独立显示后，在django下面仍然不显示，是因为 STATICFILES_DIRS设成了

```python
os.path.join(BASE_DIR, 'static')
```
​	改为
```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build/static'),
]
```

- django admin css not working,  报错信息为：
  "GET /admin/static/admin/css/dashboard.css HTTP/1.1" 404 
  其中 static 是在settings.py中设置的STATIC_URL = 'static/'，将 settings.py中的  STATIC_URL = '/'  即可。
  https://stackoverflow.com/questions/56352489/what-does-django-staticsettings-static-url-document-root-settings-static-root   这里有个很好的解释。

### 6. 升级方向

- 在django的app里，使用react+tailwind，每个app里的build文件夹是一个app，这样一个django可以联合django template和多个独立开发的app，使用django的router进行不同内容主题的页面跳转。
- 增加login/logout等管理，将app置于django的用户权限管理之下