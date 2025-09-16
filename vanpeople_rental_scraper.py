#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

class VanpeopleRentalScraper:
    def __init__(self):
        self.base_url = "https://c.vanpeople.com/zufang/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.rentals = []

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_rental_info(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        rental_items = soup.find_all('li', class_='list')
        print(f"找到{len(rental_items)}个租房项目")

        for i, item in enumerate(rental_items):
            try:
                rental_info = {}

                title_link = item.find('a', class_='c-list-title')
                if title_link:
                    rental_info['title'] = title_link.get_text(strip=True)
                    rental_info['link'] = title_link.get('href', '')
                    if rental_info['link'] and not rental_info['link'].startswith('http'):
                        rental_info['link'] = 'https://c.vanpeople.com' + rental_info['link']

                money_span = item.find('span', class_='money')
                if money_span:
                    rental_info['price'] = money_span.get_text(strip=True)

                mark_span = item.find('span', class_='mark')
                if mark_span:
                    rental_info['price_unit'] = mark_span.get_text(strip=True)

                tags_span = item.find('span', class_='tags')
                if tags_span:
                    rental_info['included'] = tags_span.get_text(strip=True)

                # 扩展的地区识别 - 支持中英文地名
                location_mapping = {
                    # 中文地名
                    '温哥华': '温哥华',
                    '列治文': '列治文',
                    '本拿比': '本拿比',
                    '素里': '素里',
                    '高贵林': '高贵林',
                    '新西敏': '新西敏',
                    '北温': '北温',
                    '西温': '西温',
                    '兰里': '兰里',
                    '枫树岭': '枫树岭',
                    '白石': '白石',
                    '三角洲': '三角洲',
                    '阿伯茨福德': '阿伯茨福德',
                    '维多利亚': '维多利亚',
                    '惠斯勒': '惠斯勒',
                    # 英文地名
                    'Vancouver': '温哥华',
                    'Richmond': '列治文',
                    'Burnaby': '本拿比',
                    'Surrey': '素里',
                    'Coquitlam': '高贵林',
                    'New Westminster': '新西敏',
                    'North Vancouver': '北温',
                    'West Vancouver': '西温',
                    'Langley': '兰里',
                    'Maple Ridge': '枫树岭',
                    'White Rock': '白石',
                    'Delta': '三角洲',
                    'Abbotsford': '阿伯茨福德',
                    'Port Coquitlam': '高贵林港',
                    'Port Moody': '满地宝',
                    'Victoria': '维多利亚',
                    'Whistler': '惠斯勒',
                    'Nanaimo': '纳奈莫',
                    'Pitt Meadows': '匹特草原',
                    'Sunshine Coast': '阳光海岸'
                }

                # 检查所有span元素中的地区信息
                found_location = False
                for span in item.find_all('span'):
                    text = span.get_text(strip=True)
                    for location_key, location_value in location_mapping.items():
                        if location_key.lower() in text.lower():
                            rental_info['location'] = location_value
                            found_location = True
                            break
                    if found_location:
                        break

                # 如果在span中没找到，再在整个item的文本中搜索
                if not found_location:
                    item_text = item.get_text()
                    for location_key, location_value in location_mapping.items():
                        if location_key.lower() in item_text.lower():
                            rental_info['location'] = location_value
                            break

                tips_div = item.find('div', class_='c-list-tips')
                if tips_div:
                    tip_texts = [span.get_text(strip=True) for span in tips_div.find_all('span')]
                    rental_info['property_details'] = tip_texts

                img_tag = item.find('img')
                if img_tag:
                    # 优先检查懒加载图片的data-original属性
                    img_src = img_tag.get('data-original', '') or img_tag.get('src', '')

                    if img_src:
                        rental_info['image_url'] = img_src

                        # 标记是否为真实图片
                        if 'nopic' in img_src:
                            rental_info['has_real_image'] = False
                        else:
                            rental_info['has_real_image'] = True

                        # 如果是懒加载图片，添加标记
                        if img_tag.get('data-original'):
                            rental_info['is_lazy_loaded'] = True

                contact_h2 = item.find('h2', class_='c-list-uname')
                if contact_h2:
                    rental_info['contact'] = contact_h2.get_text(strip=True)

                date_span = item.find('span', class_='c-list-date')
                if date_span:
                    rental_info['publish_time'] = date_span.get_text(strip=True)

                languages_div = item.find('div', class_='c-list-lan')
                if languages_div:
                    rental_info['languages'] = languages_div.get_text(strip=True)

                rental_info['scraped_at'] = datetime.now().isoformat()

                # 过滤掉价格为"面议"的房源
                if rental_info.get('title') and rental_info.get('price') != '面议':
                    self.rentals.append(rental_info)
                elif i < 3:
                    if rental_info.get('price') == '面议':
                        print(f"项目{i+1}价格为面议，已跳过")
                    else:
                        print(f"项目{i+1}未找到标题，内容: {item.get_text()[:100]}...")

            except Exception as e:
                print(f"Error parsing rental item {i+1}: {e}")
                continue

    def scrape_rentals(self, pages=1):
        print(f"开始抓取vanpeople租房信息，共{pages}页...")

        for page in range(1, pages + 1):
            if page == 1:
                url = self.base_url
            else:
                url = f"{self.base_url}?page={page}"

            print(f"正在抓取第{page}页: {url}")
            html_content = self.fetch_page(url)

            if html_content:
                if page == 1:
                    with open('debug_page1.html', 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print("第1页HTML已保存到debug_page1.html用于调试")

                self.parse_rental_info(html_content)
                time.sleep(1)
            else:
                print(f"无法获取第{page}页内容")

        print(f"抓取完成，共获取{len(self.rentals)}条租房信息")
        return self.rentals

    def save_to_json(self, filename='vanpeople_rentals.json'):
        # 创建包含元数据的数据结构
        data_with_metadata = {
            "metadata": {
                "scraped_at": datetime.now().isoformat(),
                "total_count": len(self.rentals),
                "source": "vanpeople.com",
                "filtered": "排除价格为'面议'的房源"
            },
            "rentals": self.rentals
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_with_metadata, f, ensure_ascii=False, indent=2)
        print(f"租房信息已保存到 {filename}")
        print(f"数据抓取时间: {data_with_metadata['metadata']['scraped_at']}")
        print(f"有效房源数量: {len(self.rentals)} (已排除价格'面议'的房源)")

    def print_summary(self):
        if not self.rentals:
            print("未找到租房信息")
            return

        print(f"\n=== 租房信息汇总 ===")
        print(f"总数: {len(self.rentals)}条")

        locations = {}
        for rental in self.rentals:
            location = rental.get('location', '未知')
            locations[location] = locations.get(location, 0) + 1

        print("\n按地区分布:")
        for location, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
            print(f"  {location}: {count}条")

        print(f"\n=== 最新租房信息 ===")
        for i, rental in enumerate(self.rentals[:5], 1):
            print(f"\n{i}. {rental.get('title', '无标题')}")
            if rental.get('price'):
                print(f"   价格: {rental['price']}")
            if rental.get('location'):
                print(f"   地区: {rental['location']}")
            if rental.get('publish_time'):
                print(f"   发布时间: {rental['publish_time']}")
            if rental.get('link'):
                print(f"   链接: {rental['link']}")

def main():
    scraper = VanpeopleRentalScraper()

    try:
        rentals = scraper.scrape_rentals(pages=3)

        if rentals:
            scraper.save_to_json()
            scraper.print_summary()
        else:
            print("未获取到任何租房信息")

    except KeyboardInterrupt:
        print("\n用户中断了程序")
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()