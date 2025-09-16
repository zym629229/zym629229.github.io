# VanPeople租房信息抓取程序

## 功能简介
这个程序可以自动抓取VanPeople网站(vanpeople.com)上最新发布的租房信息，包括：

- 房源标题
- 租金价格和单位
- 包含的设施/服务（水电网等）
- 所在地区
- 房屋类型详情
- 发布时间
- 联系人信息
- 支持的语言
- 房源图片链接

## 安装要求
确保你的系统安装了Python 3.7+，然后安装所需的依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用
直接运行程序，默认抓取前3页的租房信息：

```bash
python3 vanpeople_rental_scraper.py
```

### 自定义页数
你也可以修改程序中的参数来抓取更多页面的信息。

## 输出文件
程序运行后会生成以下文件：

1. `vanpeople_rentals.json` - 包含所有抓取到的租房信息的JSON文件
2. `debug_page1.html` - 第一页的原始HTML文件（用于调试）

## 输出格式示例
```json
{
  "title": "列治文好区house单房出租",
  "link": "https://c.vanpeople.com/zufang/item-3396000.html",
  "price": "$1,100",
  "price_unit": "加币/月",
  "included": "包水, 电, 网, 天然气",
  "location": "列治文",
  "property_details": ["列治文", "分租", "独立屋", "独立卫浴"],
  "contact": "孙女士",
  "publish_time": "1天前",
  "languages": "国语",
  "scraped_at": "2025-09-14T03:49:42.200483"
}
```

## 注意事项
- 程序会在请求之间自动延迟1秒，以避免对服务器造成过大负担
- 请遵守网站的使用条款和robots.txt规则
- 建议不要频繁运行程序，以免被网站限制访问

## 地区支持
程序可以识别以下地区的租房信息：
- 温哥华 (Vancouver)
- 列治文 (Richmond)
- 本拿比 (Burnaby)
- 素里 (Surrey)
- 高贵林 (Coquitlam)
- 新西敏 (New Westminster)
- 北温 (North Vancouver)
- 西温 (West Vancouver)
- 兰里 (Langley)
- 枫树岭 (Maple Ridge)
- 白石 (White Rock)
- 三角洲 (Delta)
- 阿伯茨福德 (Abbotsford)