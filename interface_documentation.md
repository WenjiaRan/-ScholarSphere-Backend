

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