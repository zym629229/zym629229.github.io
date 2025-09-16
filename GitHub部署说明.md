# VanPeople 租房信息系统 - GitHub Pages 部署说明

## 项目概述

这是一个自动抓取温哥华地区 VanPeople 网站租房信息的系统，包含数据抓取脚本和网页展示界面。

## 文件结构

```
.
├── docs/
│   └── index.html          # 主页面（从 rental_viewer.html 复制）
├── data/
│   └── vanpeople_rentals.json  # 租房数据文件
├── assets/
│   └── vanpeople_rental_scraper.py  # 数据抓取脚本
├── .github/
│   └── workflows/
│       └── update-data.yml # 自动更新数据的GitHub Action
├── _config.yml            # GitHub Pages 配置
└── GitHub部署说明.md      # 本文档
```

## 部署步骤

### 1. 创建 GitHub 仓库

1. 在 GitHub 上创建新仓库
2. 将所有文件推送到仓库

```bash
git init
git add .
git commit -m "Initial commit: VanPeople rental scraper with GitHub Pages"
git branch -M main
git remote add origin https://github.com/用户名/仓库名.git
git push -u origin main
```

### 2. 启用 GitHub Pages

1. 进入仓库设置 (Settings)
2. 找到 "Pages" 选项
3. 在 "Source" 下选择 "Deploy from a branch"
4. 选择 "main" 分支，文件夹选择 "/docs"
5. 点击 "Save"

### 3. 配置自动数据更新

GitHub Action 已配置为：
- 每天早上6点和晚上6点自动运行
- 可手动触发更新
- 自动提交新的数据文件

#### 手动触发更新：
1. 进入仓库的 "Actions" 标签
2. 选择 "Update Rental Data" workflow
3. 点击 "Run workflow"

## 功能特性

### 数据抓取
- 自动抓取 VanPeople 租房信息
- 过滤掉价格为"面议"的房源
- 支持中英文地区名称识别
- 提取图片URL（包括懒加载图片）
- 生成带时间戳的JSON数据

### 网页展示
- 响应式设计，支持手机和电脑
- 实时搜索和过滤功能
- 按价格、时间、地区排序
- 显示房源图片和详细信息
- 显示数据更新时间

### 地区支持
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
- 等更多地区...

## 本地开发

### 运行数据抓取
```bash
cd assets
python3 vanpeople_rental_scraper.py
```

### 本地预览网页
```bash
# 使用无缓存服务器
python3 nocache_server.py
# 然后访问 http://localhost:8081
```

## 自定义设置

### 修改抓取频率
编辑 `.github/workflows/update-data.yml` 中的 cron 表达式：
```yaml
schedule:
  - cron: '0 6,18 * * *'  # 每天6点和18点
```

### 修改抓取页数
编辑 `assets/vanpeople_rental_scraper.py` 中的 `main()` 函数：
```python
rentals = scraper.scrape_rentals(pages=3)  # 修改页数
```

## 故障排除

### 数据未更新
1. 检查 GitHub Actions 是否运行成功
2. 查看 Actions 日志中的错误信息
3. 手动触发 workflow 测试

### 网页显示问题
1. 确认 `docs/index.html` 存在
2. 检查 GitHub Pages 设置正确
3. 等待几分钟让 GitHub Pages 更新

### 权限问题
确保 GitHub Action 有写入权限：
1. Settings → Actions → General
2. Workflow permissions → Read and write permissions

## 维护说明

- 数据每天自动更新两次
- 监控 GitHub Actions 运行状态
- 定期检查抓取脚本是否需要更新（网站结构变化）
- 根据需要调整过滤条件和地区映射

## 联系方式

如有问题请查看 GitHub Issues 或联系项目维护者。