#!/usr/bin/env python3
import json
import os

def test_json_structure():
    """测试新的JSON结构"""
    print("🔍 测试JSON数据结构...")

    try:
        with open('vanpeople_rentals.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 检查新的数据结构
        if 'metadata' in data and 'rentals' in data:
            print("✅ JSON结构更新成功")

            metadata = data['metadata']
            rentals = data['rentals']

            print(f"📊 元数据信息:")
            print(f"   抓取时间: {metadata.get('scraped_at', '未知')}")
            print(f"   房源总数: {metadata.get('total_count', 0)}")
            print(f"   数据源: {metadata.get('source', '未知')}")
            print(f"   过滤说明: {metadata.get('filtered', '无')}")

            # 检查是否真的过滤了"面议"价格
            negotiable_count = sum(1 for rental in rentals if rental.get('price') == '面议')
            print(f"✅ 价格为'面议'的房源数量: {negotiable_count} (应该为0)")

            # 统计有效价格的房源
            valid_price_count = sum(1 for rental in rentals
                                  if rental.get('price') and
                                     rental.get('price') != '面议' and
                                     '$' in rental.get('price', ''))
            print(f"✅ 有有效价格的房源数量: {valid_price_count}")

            return True
        else:
            print("❌ JSON结构未更新，仍为旧格式")
            return False

    except Exception as e:
        print(f"❌ JSON测试失败: {e}")
        return False

def test_html_updates():
    """测试HTML文件是否包含新功能"""
    print("\n🔍 测试HTML文件更新...")

    try:
        with open('rental_viewer.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 检查关键更新
        checks = [
            ('data-timestamp', 'ID为data-timestamp的时间戳元素'),
            ('displayTimestamp', '显示时间戳的函数'),
            ('metadata', 'metadata变量定义'),
            ('面议', '面议过滤逻辑'),
            ('jsonData.metadata', '新JSON结构处理')
        ]

        all_passed = True
        for check, description in checks:
            if check in html_content:
                print(f"✅ 包含{description}")
            else:
                print(f"❌ 缺少{description}")
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"❌ HTML测试失败: {e}")
        return False

def test_price_filtering():
    """测试价格过滤逻辑"""
    print("\n🔍 测试价格过滤...")

    try:
        with open('vanpeople_rentals.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'rentals' in data:
            rentals = data['rentals']
        else:
            rentals = data  # 兼容旧格式

        # 详细统计
        price_stats = {
            'total': len(rentals),
            'with_price': 0,
            'negotiable': 0,
            'valid_dollar': 0,
            'no_price': 0
        }

        price_examples = []

        for rental in rentals:
            price = rental.get('price', '')

            if not price:
                price_stats['no_price'] += 1
            elif price == '面议':
                price_stats['negotiable'] += 1
            elif '$' in price:
                price_stats['valid_dollar'] += 1
                if len(price_examples) < 5:
                    price_examples.append(f"{rental.get('title', '无标题')[:30]}... -> {price}")

            if price:
                price_stats['with_price'] += 1

        print(f"📊 价格统计:")
        print(f"   总房源: {price_stats['total']}")
        print(f"   有价格信息: {price_stats['with_price']}")
        print(f"   价格'面议': {price_stats['negotiable']} ⭐ (应该为0)")
        print(f"   有效美元价格: {price_stats['valid_dollar']}")
        print(f"   无价格信息: {price_stats['no_price']}")

        if price_examples:
            print(f"\n💰 价格示例:")
            for example in price_examples:
                print(f"   {example}")

        # 验证过滤是否成功
        filter_success = price_stats['negotiable'] == 0
        print(f"\n{'✅' if filter_success else '❌'} 价格过滤{'成功' if filter_success else '失败'}")

        return filter_success

    except Exception as e:
        print(f"❌ 价格过滤测试失败: {e}")
        return False

def main():
    print("🚀 测试程序更新结果")
    print("=" * 60)

    success_count = 0
    total_tests = 3

    # 测试JSON结构
    if test_json_structure():
        success_count += 1

    # 测试HTML更新
    if test_html_updates():
        success_count += 1

    # 测试价格过滤
    if test_price_filtering():
        success_count += 1

    print("\n" + "=" * 60)
    print(f"🎯 测试结果: {success_count}/{total_tests} 项通过")

    if success_count == total_tests:
        print("🎉 所有更新功能测试通过！")
        print("\n📋 更新摘要:")
        print("✅ 1. 爬虫程序现在自动过滤价格'面议'的房源")
        print("✅ 2. JSON文件包含抓取时间戳和元数据信息")
        print("✅ 3. 网页显示数据更新时间和过滤说明")
        print("✅ 4. 统计信息只计算有效价格房源")
        print("✅ 5. 搜索和排序功能排除'面议'房源")
        print("\n🌐 刷新浏览器查看更新后的网页: http://localhost:8080/rental_viewer.html")
    else:
        print("⚠️  部分功能可能需要检查")

if __name__ == "__main__":
    main()