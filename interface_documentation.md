

# 1. 注册接口

请求URL：/api/scholarsphere/user/register

请求方式：POST

请求参数：

| 参数名    | 必选 | 类型   | 说明     |
| --------- | ---- | ------ | -------- |
| email     | 是   | string | 用户邮箱 |
| password1 | 是   | string | 用户密码 |
| password2 | 是   | string | 重复密码 |

返回示例：

成功：

```json
{
    "result": 1,
    "message": "注册成功!"
}
```

失败：

```json
{
    "result": 0,
    "message": "用户名, 邮箱, 与密码不允许为空!"
}
```

```json
{
    "result": 0,
    "message": "该邮箱已被注册"
}
```

```json
{
    "result": 0,
    "message": "两次密码不一致!"
}
```

# 2. 邮箱注册状态检查接口

请求URL：/api/scholarsphere/user/checkmailregistered

请求方式：POST

请求参数：

| 参数名 | 必选 | 类型   | 说明     |
| ------ | ---- | ------ | -------- |
| email  | 是   | string | 用户邮箱 |

返回示例：

该邮箱已被注册：

```json
{
    "result": 0,
    "message": "该邮箱已被注册!"
}
```

新邮箱可以注册：

```json
{
    "result": 1,
    "message": "新邮箱,可以注册!"
}
```

请求失败：

```json
{
    "result": 0,
    "message": "请求方式错误！"
}
```

# 3.登录接口

请求URL：/api/scholarsphere/user/login

请求方式：POST

请求参数：

| 参数名    | 必选 | 类型   | 说明     |
| --------- | ---- | ------ | -------- |
| email     | 是   | string | 用户邮箱 |
| password | 是   | string | 用户密码 |

返回示例：

成功：

```json
{
    "result": 1,
    "message": "登录成功!"
}
```

失败：

```json
{
    "result": 0,
    "message": "邮箱不允许为空!"
}
```

```json
{
    "result": 0,
    "message": "用户不存在!"
}
```

```json
{
    "result": 0,
    "message": "密码不能为空!"
}
```

```json
{
    "result": 0,
    "message": "密码错误!"
}
```

```json
{
    "result": 0,
    "message": "现在禁止登录!"
}
```

```json
{
    "result": 0,
    "message": "请求方式错误!"
}
```

# 4.设置七天自动登录接口

请求URL：/api/scholarsphere/user/autologin

请求方式：POST

请求参数：

| 参数名    | 必选 | 类型   | 说明     |
| --------- | ---- | ------ | -------- |
| email     | 是   | string | 用户邮箱 |

返回示例：

成功：

```json
{
    "result": 1,
    "message": "设置成功!"
}
```

失败：

```json
{
    "result": 0,
    "message": "请求方式错误！"
}
```

# 5.高级搜索

### 接口说明

- 该接口用于高级搜索功能，根据给定的搜索条件进行搜索。
- 只接受POST请求。

### 请求URL

- `/api/scholarsphere/search/advancesearch`

### 请求方法

- POST

### 请求参数

| 参数名                    | 必选 | 类型 | 说明                                                         |
| :------------------------ | :--- | :--- | :----------------------------------------------------------- |
| searchDatefrom            | 否   | int  | 搜索起始时间戳                                               |
| searchDateto              | 否   | int  | 搜索结束时间戳                                               |
| searchType                | 否   | str  | 搜索类型，可选值为：`author`、`work_name`、`category`、`content` |
| searchContent             | 否   | str  | 搜索内容                                                     |
| additionalSearchCondition | 否   | list | 额外的搜索条件，格式见下表                                   |

`additionalSearchCondition` 参数格式说明：

| 参数名        | 必选 | 类型 | 说明                                                         |
| :------------ | :--- | :--- | :----------------------------------------------------------- |
| bool          | 是   | str  | 操作符，可选值为：`AND`、`OR`、`NOT`                         |
| searchType    | 是   | str  | 搜索类型，可选值为：`author`、`work_name`、`category`、`content` |
| searchContent | 是   | str  | 搜索内容                                                     |

### 响应参数

| 参数名  | 类型 | 说明                                                         |
| :------ | :--- | :----------------------------------------------------------- |
| results | list | 查询结果列表，每个元素都是一个字典，包含以下键值：`id`、`work_name`、`author_id`、`url`、`has_pdf`、`content`、`send_time`、`author`、`category` |

### 响应示例

请求：

http



```
POST /api/scholarsphere/search/advancesearch HTTP/1.1
Content-Type: application/json

{
    "searchDatefrom": 1630108800,
    "searchDateto": 1630112400,
    "searchType": "content",
    "searchContent": "machine learning",
    "additionalSearchCondition": [
        {
            "bool": "AND",
            "searchType": "author",
            "searchContent": "Li"
        },
        {
            "bool": "AND",
            "searchType": "author",
            "searchContent": "Li"
        }
    ]
}
```

响应：

http



```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "results": [
        {
            "id": "123",
            "work_name": "Machine Learning",
            "author_id": "456",
            "url": "http://example.com",
            "has_pdf": 1,
            "content": "This paper is about machine learning.",
            "send_time": "2021-08-28 12:00:00",
            "author": "Tom Li",
            "category": "Computer Science"
        }
    ]
}
```

# 6.添加作品接口

请求URL：/api/scholarsphere/search/add-work/

请求方式：POST

请求参数：

| 参数名       | 必选 | 类型   | 说明                                        |
| ------------ | ---- | ------ | ------------------------------------------- |
| open_alex_id | 是   | string | 对应作品的open_alex_id                      |
| work_name    | 是   | string | 论文的名字                                  |
| author_id    | 是   | string | 上传pdf的作者的open_alex_id                 |
| url          | 否   | string | 论文的访问路由                              |
| pdf          | 是   | file   | 文章pdf                                     |
| has_pdf      | 否   | int    | 是否有pdf (-1:没有pdf, 0:正在审核, 1:有pdf) |
| content      | 否   | string | 内容                                        |
| send_time    | 是   | string | 上传时间                                    |
| author       | 是   | string | 上传pdf的作者                               |
| category     | 否   | string | 论文分类                                    |

返回示例：

成功：

```json
code{
    "message": "Work added successfully."
}
```

失败：

```json
code{
    "error": "Invalid request method."
}
```

# 7. 获取作品PDF接口

请求URL：/api/scholarsphere/search/get-work-pdf/<work_id>/

请求方式：GET

请求参数：无

返回示例：

成功：

返回PDF文件作为下载响应

失败：

```json
code{
    "error": "Work not found."
}
code{
    "error": "PDF not found."
}
```

# 8.普通搜索

### 接口说明

- 该接口用于普通搜索功能，根据传入的搜索类型进行搜索。
- 只接受POST请求。

### 请求URL

- `/api/scholarsphere/search/normalsearch`

### 请求方法

- POST

### 请求参数

| 参数名                    | 必选 | 类型 | 说明                                                         |
| :------------------------ | :--- | :--- | :----------------------------------------------------------- |
| search_method          | 否   | String  | 选择搜索作者还是文章。`enum=["scholar","article"]` |
| search_key             | 否   | String  | 搜索内容。对于作者的搜索只提供名字检索，对文章的搜索提供作者名、文章编号、文章名  |
| search_type               | 否   | String  | 搜索类型。对于`search_method ="article"`,`enum=["article_name","article_id","author_name"]` |


### 响应参数

| 参数名  | 类型 | 说明                                                         |
| :------ | :--- | :----------------------------------------------------------- |
| results | list | 查询结果列表，每个元素都是一个字典。当`search_method ="article"`时，包含以下键值：`id`、`work_name`、`author_id`、`url`、`has_pdf`、`content`、`send_time`、`author`、`category` ;当`search_method ="scholar`时，包含以下键值：`id`、`name`、`email`、`url`|

### 响应示例

请求：
http



```
POST /api/scholarsphere/search/advancesearch HTTP/1.1
Content-Type: application/json

{
    "search_method" : "scholar",
    "search_key" : "qymiy"
}
```


响应：

http



```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "results": [
        {
            "id": "1",
            "name": "qymiy",
            "email": "2718106017",
            "url": "http://example.com"
        }
    ]
}
```


# 9. 实名绑定


### 接口说明

- 该接口用于为账号进行实名绑定。
- 只接受POST请求。


请求URL：/api/scholarsphere/user/realinfoset

请求方式：POST

请求参数：

| 参数名    | 必选 | 类型   | 说明     |
| --------- | ---- | ------ | -------- |
| name     | 是   | string | 姓名|
| phone | 是   | string | 电话 |
| id_num | 是   | string | 身份证号|
| email | 是   | string | 邮箱|
返回示例：

成功：

```json
{
    "result": 1,
    "message": "实名成功！"
}
```

失败返回例：

```json
{
    "result": 0,
    "message": "此信息已被实名！"
}
```

# 10. 修改个人信息


### 接口说明

- 该接口用于对账号进行信息修改。
- 只接受POST请求。


请求URL：/api/scholarsphere/user/changeinfo

请求方式：POST

请求参数：

| 参数名    | 必选 | 类型   | 说明     |
| --------- | ---- | ------ | -------- |
| keys     | 是   | string | 需要修改项目。可在`enum=["password","description"]`中选择多项，不修改则不传递对应项|
| vals | 是   | string | 修改项目的对应的修改值。！顺序必须和keys一一对应。通过""分割开修改值|
| used_password | 是   | string | 是否修改密码，需要则传入旧密码参数|
| email | 是   | string | 邮箱|
返回示例：

成功：

```json
{
    "result": 1,
    "message": "修改成功"
}
```

失败返回例：

```json
{
    "result": 0,
    "message": "未收到修改内容！"
}
```

请求：
http



```
POST /api/scholarsphere/search/changeinfo HTTP/1.1
Content-Type: application/json

{
    "keys" : ""password","description"",
    "vals" : ""123456","new introduction,by qy"",
    "used_password" : "123456qy",
    "email" : "2718106017"
}
```


