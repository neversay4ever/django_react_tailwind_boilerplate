从 react_tailwind_boilerplate 库 和 https://github.com/nicholaskajoh/React-Django   改装，tailwindcss版本改为1.4.0 以上。
react_tailwind_boilerplate 直接从create-react-app 开始

# 背景
本库的目的是解决在django中使用react的问题，基本思路是：
1. react可以独立开发，热启动，能用tailwindcss的自定义功能。这些在simpleDjangoReact库里是做不到的。参考  https://github.com/nicholaskajoh/React-Django    这个库的做法，在react app里放django，而不是django app里放react，可以最大化发挥create-react-app的强大功能。
2. 利用django的注册系统，所以选择通过django的view访问react的html的方式。hmtl来自react的build文件夹下的index.html，因此django的template文件夹定义为
```python
        'DIRS': [
            os.path.join(BASE_DIR, 'build')
        ],
```
3. 通过django-rest-framework的API传数据到react。
react build成的html被当作是django的一个正常的html template，因此react访问的域名按道理只需要相对域名，即http://127.0.0.1:8000/api/lead/  后面的api/lead部分；
但在react dev阶段，因为我们都是通过http://127.0.0.1:3000/   来热启动react，因此需要在react里显式指定http://127.0.0.1:8000   部分，并且在django的dev模式下需要安装django-cors-headers允许跨域请求。

4. dev下的API域名处理，参考 https://medium.com/@tacomanator/environments-with-create-react-app-7b645312c09d ， 将package.json里的
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


5. 实际的操作流程是：
5.1 首先npm run build，以创建一个build文件夹，作为django项目的template目录，见上一步。
5.2 在项目根目录下，python manage.py runserver, 进行django开发，包括api设计和admin中的数据录入
5.3 在项目根目录下，npm run dev ， 进行前端开发。在有django提供API数据的情况下，npm run dev足以开发前端的一切。
5.4 进入部署阶段，npm run build, django将build文件夹下的index.html作为一个页面。

6. python的环境设置，在shell中，项目根目录下
```
virtualenv -p python3 venv
source venv/bin/activate
```
退出虚拟环境使用
```
deactivate
```

7. 需要安装的django包，可以加上 -i https://pypi.tuna.tsinghua.edu.cn/simple 加速
7.1 使用Django2.2 LTS版本，使用django-rest-framwork， 附带安装markdown和django-filter
```
pip install Django==2.2
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```

7.2. 安装 whitenoise，可以在production阶段对static文件server，不需要通过nginx。whitenoises使用方法见http://whitenoise.evans.io/en/stable/，注意版本的差异。本库使用5.0.1版
```
pip install whitenoise==5.0.1

```

7.3 django的admin部分，引入djangoql和django-import-export，分别是admin下复杂检索和导入excel用的，在admin.py中的代码为
```
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

```
pip install djangoql===0.13.1
pip install django-import-export===2.1.0
```
7.4 如上第3步所述，安装django-cors-headers允许dev形式下的跨域请求。
```
```

8. npm需要装的包
8.1 axios，参考https://www.robinwieruch.de/react-hooks-fetch-data
```
npm i axios
```
```
import React, { useState, useEffect } from 'react';
import axios from 'axios';
 
function App() {
  const [data, setData] = useState({ hits: [] });
 
  const fetchData = async () => {
    const result = await axios(
      'https://hn.algolia.com/api/v1/search?query=redux',
    );
    setData(result.data);
  };

  useEffect(() => {
    fetchData();
  }, []);
 
  return (
    <ul>
      {data.hits.map(item => (
        <li key={item.objectID}>
          <a href={item.url}>{item.title}</a>
        </li>
      ))}
    </ul>
  );
}
 
export default App;
```

8.2 useFetch这个hook，有点复杂


9.bug 问题
9.1 npm run start 正常，但是 npm run build后的html显示不正常，见https://stackoverflow.com/questions/46235798/relative-path-in-index-html-after-build 
9.2 上述9.1解决后，django下面仍然不显示，是因为 STATICFILES_DIRS设成了
```
os.path.join(BASE_DIR, 'static')
```
改为
```
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build/static'),
]
```
9.3 django admin 突然css not working, 报错信息为：
[08/May/2020 21:35:08] "GET /admin/static/admin/css/dashboard.css HTTP/1.1" 404 4161
其中 static 是在settings.py中设置的STATIC_URL = 'static/'
将 settings.py中的  STATIC_URL = '/'  即可


10. 注意事项
从github上拉下来后
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
因为staticfiles没有同步到github，因此需要
```
python manage.py collectstatic
```

11. 需要尝试的
11.1 在django的app里，使用react+tailwind，每个app里的build文件夹是一个app，这样一个django可以联合django template和多个独立开发的app，使用django的router进行不同内容主题的页面跳转。
11.2 增加login/logout等管理，将app置于django的用户权限管理之下