#!/usr/bin/env python3
import json
import os

def test_files_exist():
    """检查必要文件是否存在"""
    files = ['rental_viewer.html', 'vanpeople_rentals.json']
    missing_files = []

    for file in files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return False
    else:
        print("✅ 所有必要文件都存在")
        return True

def test_json_data():
    """测试JSON数据的有效性"""
    try:
        with open('vanpeople_rentals.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✅ JSON数据加载成功，共有 {len(data)} 条记录")

        # 检查数据结构
        if len(data) > 0:
            sample = data[0]
            required_fields = ['title', 'price', 'location', 'publish_time']

            for field in required_fields:
                if field in sample:
                    print(f"✅ 包含字段: {field}")
                else:
                    print(f"⚠️  缺少字段: {field}")

        return True
    except Exception as e:
        print(f"❌ JSON数据验证失败: {e}")
        return False

def test_html_structure():
    """测试HTML文件的基本结构"""
    try:
        with open('rental_viewer.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 检查关键元素
        required_elements = [
            'id="rental-grid"',
            '<script>',
            'loadRentalData',
            'vanpeople_rentals.json'
        ]

        for element in required_elements:
            if element in html_content:
                print(f"✅ HTML包含: {element}")
            else:
                print(f"❌ HTML缺少: {element}")
                return False

        return True
    except Exception as e:
        print(f"❌ HTML文件验证失败: {e}")
        return False

def main():
    print("🔍 正在测试租房信息网页查看器...")
    print("=" * 50)

    success = True

    # 测试文件存在性
    if not test_files_exist():
        success = False

    print()

    # 测试JSON数据
    if not test_json_data():
        success = False

    print()

    # 测试HTML结构
    if not test_html_structure():
        success = False

    print()
    print("=" * 50)

    if success:
        print("🎉 所有测试通过！")
        print("📋 使用说明:")
        print("1. 确保在项目目录中运行: python3 -m http.server 8000")
        print("2. 在浏览器中访问: http://localhost:8000/rental_viewer.html")
        print("3. 使用搜索、筛选和排序功能浏览租房信息")
        print()
        print("✨ 功能特色:")
        print("• 搜索房源标题和地区")
        print("• 按地区、价格范围筛选")
        print("• 按时间、价格、标题、地区排序")
        print("• 响应式设计，支持移动设备")
        print("• 显示房源图片和详细信息")
    else:
        print("❌ 测试失败，请检查错误信息")

if __name__ == "__main__":
    main()