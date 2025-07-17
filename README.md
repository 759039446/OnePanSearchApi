# 一盘搜索API

网盘聚合搜索，基于FastAPI和aiohttp 对接各种网盘资源搜索接口，通过一个接口请求聚合搜索网盘资源

## 使用方法
启动`main.py`



### v2版本
http://127.0.0.1:21123/search?keyword=诛仙&type=夸克网盘&fromSite=kk大厅&page=1&pageSize=10

**请求方式**

> GET

**请求Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述                                                                     |
| --- | --- | ---- | ---- |--------------------------------------------------------------------------|
| keyword | 诛仙 | String | 是 | -                                                                        |
| type | 夸克网盘 | String | 是 | -                                                                        |
| fromSite | kk大厅 | String | 是 | 不传则搜全部 可选项：kk大厅、kk短剧、kk橘子资源、kk小宇、kk小悠、kk天天追剧<br/>【速度自行判断】趣盘搜、酷乐—百度、酷乐—夸克 |
| page | 1 | String | 是 | -                                                                        |
| pageSize | 10 | String | 是 | -                                                                        |

### 搜索接口
```json
{
	"success": true,
	"data": [{
		"id": 61642,
		"name": "[诛仙][2022][更新至52集][动画]",
		"url": "https://pan.baidu.com/s/1E8EQr6xyqF3-KHPXacKC9Q?pwd=8888",
		"type": "百度网盘",
		"pwd": "8888",
		"fromSite": "kk大厅"
	}, {
		"id": 36050,
		"name": "[诛仙青云志 1~2季][2016][完结][国剧]",
		"url": "https://pan.baidu.com/s/1tllrmYTTLvr0yN0lSrKiNw?pwd=8888",
		"type": "百度网盘",
		"pwd": "8888",
		"fromSite": "kk大厅"
	}, {
		"id": 50114,
		"name": "[诛仙 Ⅰ][2019][爱情/奇幻][中国]",
		"url": "https://pan.baidu.com/s/11CUDRJI7efHgTTMvdozB9Q?pwd=8888",
		"type": "百度网盘",
		"pwd": "8888",
		"fromSite": "kk大厅"
	}, {
		"id": 51289,
		"name": "[诛仙番外之铃心剑魄][2016][奇幻 / 武侠][中国]",
		"url": "https://pan.baidu.com/s/14QkigYCFIguYq-aI3r5IPg?pwd=8888",
		"type": "百度网盘",
		"pwd": "8888",
		"fromSite": "kk大厅"
	}, {
		"id": "",
		"name": " 诛仙青云志2",
		"url": "https://pan.baidu.com/s/1Tt8VqAmrmgBKfmgxLqmueQ",
		"type": "百度网盘",
		"pwd": "",
		"fromSite": "kk小宇"
	}, {
		"id": "",
		"name": " 诛仙青云志1",
		"url": "https://pan.baidu.com/s/1cvqmncZfrNz8FU52uQpwfg",
		"type": "百度网盘",
		"pwd": "",
		"fromSite": "kk小宇"
	}, {
		"id": "",
		"name": "我在养老院里学诛仙（99集）",
		"url": "https://pan.baidu.com/s/18z5_fuSch7bp9CCs2Et-rQ?pwd=mokc",
		"type": "百度网盘",
		"pwd": "",
		"fromSite": "酷乐—百度"
	}, {
		"id": "",
		"name": "诛仙殿主开局女帝上门求婚（79集）李子峰 远霞",
		"url": "https://pan.baidu.com/s/1ebVYEQFeTLbn2jNq57sF1w?pwd=hpzr",
		"type": "百度网盘",
		"pwd": "",
		"fromSite": "酷乐—百度"
	}, {
		"id": "",
		"name": "剑弑诸神（剑来诛仙）（混沌剑神）（剑荡九天）（75集）",
		"url": "https://pan.baidu.com/s/1y27I6rMLEfsxOVNAcKhsWw?pwd=qwwb",
		"type": "百度网盘",
		"pwd": "",
		"fromSite": "酷乐—百度"
	}, {
		"id": "",
		"name": "诛天大主宰（83集）仙侠剧",
		"url": "https://pan.baidu.com/s/1Z8usqyPO2u_egpA2J-wDWg?pwd=npri",
		"type": "百度网盘",
		"pwd": "",
		"fromSite": "酷乐—百度"
	}],
	"total": 10,
	"message": "搜索成功",
	"code": 200
}
```
## 接口用时
![接口用时](/docs/微信图片_20250403153222.png)

## 目前支持：

看源码,啥也不知道


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
## 已知问题
1. 因为kkkob站点关掉了，暂时更换成差不多的站点，速度较慢没有以前快，质量也没有很高，有对接需求的可以提issue
2. kk大厅为类似站点的用户资源，资源参差不齐，自行决定排序内容
3. kk大厅的链接、提取码 正则可能会匹配不到，需要修改正则匹配规则，如果有匹配不到的可以提issue

## 更新计划
1. 添加更多接口
2. 检测是否失效
3. 性能优化、代码优化

# 交流群
[【派派圈短剧】qq群： 956740061](https://qm.qq.com/q/9yOkycLpIs) 
<br><br>
禁止广告
