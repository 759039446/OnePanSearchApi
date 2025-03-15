# 一盘搜索API

网盘聚合搜索，基于FastAPI和aiohttp 对接各种网盘资源搜索接口，通过一个接口请求聚合搜索网盘资源

## 使用方法
启动`main.py`

### v1版本

打开网址：
http://127.0.0.1:21123/search/xxxx

如：http://127.0.0.1:21123/search/庆余年2

### v2版本
http://127.0.0.1:21123/search/庆余年2

### 搜索接口
```json
{
  "success": true,
  "data": [
    {
      "id": 70036,
      "question": "[**年 第二季][2024][全36集][国产剧]",
      "answer": "链接：https://pan.baidu.com/s/1blKG5Rj8fndOPDkgpJdtqA?pwd=8888 提取码：8888\n链接：https://pan.xunlei.com/s/VOEEoqsn0avO395RBrC1dZYvA1\n链接：https://pan.quark.cn/s/4c5cabb9c7b9",
      "isTop": 0
    },
    {
      "question": "**年（迅雷）",
      "answer": "**年（迅雷）链接：https://pan.xunlei.com/s/VOEt71t9cc8KeUBBCn-j4rOLA1?pwd=94ck&origin=lilizj# 提取码：94ck"
    },
    {
      "question": "**年2",
      "answer": "**年2链接：https://pan.baidu.com/s/1JxOH-syPQUgAGnOoY-h8rQ?pwd=9lrd 提取码：9lrd"
    },
    {
      "question": " **年",
      "answer": "**年1-2链接: https://pan.baidu.com/s/1NJIa8t2Iy5pfQg753KPzuA?pwd=43n6 提取码: 43n6"
    }
  ],
  "message": "搜索成功",
  "code": 200
}
```

## 目前支持：
http://p.kkkob.com/

其他接口等更新

##  开发环境：

python 3.12


## 安装pip依赖

```
pip install -r requirement.txt
```

## 编译成exe命令：

```
pip install nuitka 
python -m nuitka --standalone --onefile  --remove-output main.py
```
## 更新计划
1. 添加更多接口
2. 检测是否失效
3. 性能优化、代码优化

# 交流群

