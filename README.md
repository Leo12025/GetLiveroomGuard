# B站直播间舰长列表获取工具

这个Python脚本用于获取B站指定直播间的舰长列表信息，包括用户名、UID、舰长等级、勋章等级、排名、陪伴时长和头像URL。

## 功能特点
- 支持通过命令行指定直播间ID
- 自动处理分页数据，获取完整舰长列表
- 输出格式化的舰长信息到控制台（包含用户名、UID、舰长等级、勋章等级、排名、陪伴时长）
- 支持将舰长信息保存到JSON或Excel文件
- 新增测试功能，可使用本地示例数据(exp.json)进行测试

## 环境要求
- Python 3.6+ 
- 所需依赖包: `requests`, `openpyxl` (用于Excel导出)

## 安装依赖
```bash
pip install requests openpyxl
```

## 使用方法

### 1. 获取B站Cookie
使用该工具需要提供B站的Cookie信息，因为获取舰长列表需要登录状态。

获取方法:
1. 打开浏览器，登录B站
2. 按下F12打开开发者工具
3. 切换到Network标签
4. 访问任意B站页面，找到一个请求
5. 在请求头中找到Cookie字段，复制其值

### 2. 配置脚本
打开`get_liveroom_guard.py`文件，将第12行的Cookie值替换为你自己的Cookie:
```python
'Cookie': 'SESSDATA=your_sessdata_here; bili_jct=your_bili_jct_here'  # 需要替换为实际的Cookie
```

### 3. 运行脚本
基本用法:
```bash
python3 get_liveroom_guard.py 直播间ID
```

将结果保存到JSON文件:
```bash
python3 get_liveroom_guard.py 直播间ID -o 输出文件名.json
```

将结果保存到Excel文件:
```bash
python3 get_liveroom_guard.py 直播间ID -e
```

指定Excel文件名:
```bash
python3 get_liveroom_guard.py 直播间ID -o 输出文件名.xlsx -e
```

使用示例数据进行测试:
```bash
python3 get_liveroom_guard.py -t
```

## 输出说明
控制台输出格式:
```
直播间 123456 的舰长列表 (10人):
----------------------------------------------------------------------------------------------------
用户名                UID             舰长等级    勋章等级    排名    陪伴时长(分钟)    头像URL
----------------------------------------------------------------------------------------------------
张三                  123456789      总督        30         1       1200             https://i0.hdslb.com/bfs/face/xxx.jpg
李四                  987654321      提督        25         2       900              https://i0.hdslb.com/bfs/face/yyy.jpg
...
```

JSON文件格式示例:
```json
[
  {
    "用户名": "张三",
    "uid": 123456789,
    "舰长等级": "总督",
    "勋章等级": 30,
    "排名": 1,
    "陪伴时长": 1200,
    "头像URL": "https://i0.hdslb.com/bfs/face/xxx.jpg"
  },
  ...
]
```

Excel文件格式:
- 自动创建工作表"舰长列表"
- 包含表头: 用户名、UID、舰长等级、勋章等级、排名、陪伴时长、头像URL
- 自动调整列宽以适应内容
- 表头加粗并居中显示

## 注意事项
1. 请妥善保管你的Cookie信息，不要分享给他人
2. Cookie有效期有限，过期后需要重新获取
3. 频繁请求可能会被B站限制，请合理使用工具
4. 本工具仅用于学习和研究目的，请勿用于商业用途

## 更新日志
- v1.1: 更新API接口适配，新增排名、陪伴时长和头像URL字段，添加测试功能
- v1.0: 初始版本，支持获取舰长列表并输出到控制台和文件