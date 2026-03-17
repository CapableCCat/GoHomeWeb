# 思乡签到 - HomeSignin

在中国文化中，**“落叶归根，魂归故里”** 是一种根深蒂固的情感。无论一个人走得多远、在外漂泊多少年，家乡始终是心里最柔软的地方。家乡不仅仅是一个地理坐标，更是一段童年的记忆、一种熟悉的味道、一份难以割舍的情感连接。

对很多在外求学、工作、生活的人来说，离开家乡往往意味着新的机会与成长，但同时也伴随着思念与牵挂。时间一天天过去，人们在城市中奔波忙碌，却常常会在某个瞬间想起家乡的街道、熟悉的方言、家人的笑脸，以及那些再普通不过却无比温暖的日常。

**“思乡签到（HomeSignin）”** 正是基于这样的情感而诞生的一个小应用。它为离开家乡的人提供一个简单而温暖的方式，记录自己离家生活的每一天。通过每日签到，用户可以看到自己离开家乡的时间、坚持打卡的记录，以及最近一段时间的生活轨迹。

在签到的同时，系统会随机生成一句“思乡话语”，或是用户自己写下的一句心情，让每一次签到都不仅仅是一次简单的记录，而是一种情绪的表达与释放。随着时间的累积，这些记录会逐渐成为一段属于自己的“离乡日记”。

## 功能特性

- **用户系统**: 注册/登录、个人资料管理（家乡、当前城市、离家日期）
- **签到打卡**: 每日签到、记录签到时间
- **数据统计**: 离家天数、累计签到、连续签到、最长连续签到
- **周日历视图**: 直观展示最近 7 天签到情况
- **思乡话语**: 内置 20 条思乡话语，打卡后自动生成
- **自定义话语**: 用户可添加自己的思乡话语
- **AI 思乡话语生成**: 支持多模型（Claude/通义千问/OpenAI 等），签到时根据用户家乡自动生成方言风格思乡话语
- **徽章系统**: 14 种徽章（时间徽章、连续徽章、特殊徽章），记录签到成就
- **家庭问候**: 配置家庭成员称呼，签到时生成家庭问候语
- **Vue 3 前端**: 现代化 SPA 应用，响应式设计，支持移动端

## 技术栈

- **后端**: Python + Flask
- **前端**: Vue 3 + Vite + Pinia + Vue Router + Axios + TailwindCSS
- **数据存储**: JSON 文件（轻量级，无需数据库）
- **包管理**: pixi (Python), npm (Node.js)

## 快速开始

### 1. 安装依赖

```bash
cd HomeSignin
pixi install
```

### 2. 配置环境变量（可选）

如果需要使用 AI 生成功能，请复制 `.env.example` 文件并配置 API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 配置。支持多种模型提供商：

**Anthropic Claude:**
```
AI_API_KEY=sk-ant-xxxxx
AI_API_BASE_URL=https://api.anthropic.com/v1
AI_MODEL=claude-sonnet-4-20250514
```

**阿里云百炼（通义千问）:**
```
AI_API_KEY=sk-xxxxx
AI_API_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_MODEL=qwen-plus
```

**OpenAI:**
```
AI_API_KEY=sk-xxxxx
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

### 3. 启动应用

本项目包含前后端，需要分别启动：

**启动后端（Flask）：**
```bash
pixi run dev
```

**启动前端（Vite + Vue 3）：**
```bash
cd frontend
npm install
npm run dev
```

启动完成后，访问 **http://localhost:3000** 使用应用。

> 前端开发服务器（port 3000）会自动代理 API 请求到后端（port 5001）

## 测试账号

项目包含预配置的测试账号，可用于快速体验：

| 用户名 | 密码 | 说明 |
|--------|------|------|
| `demo` | `demo123` | 默认测试账号（家乡：湖南长沙，当前城市：北京） |

你也可以在登录页面注册新账号。

## 项目结构

```
HomeSignin/
├── app.py                  # Flask 应用入口
├── config.py               # 配置文件
├── pixi.toml               # Pixi 配置
├── requirements.txt        # Python 依赖
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── main.js         # 应用入口
│   │   ├── App.vue         # 根组件
│   │   ├── views/          # 页面组件
│   │   │   ├── Dashboard.vue   # 仪表盘
│   │   │   ├── Checkin.vue     # 签到页
│   │   │   ├── Badges.vue      # 徽章墙
│   │   │   └── Profile.vue     # 个人资料
│   │   ├── components/     # 可复用组件
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── router/         # 路由配置
│   │   └── api/            # API 客户端
│   ├── package.json        # 前端依赖
│   ├── vite.config.js      # Vite 配置
│   └── tailwind.config.js  # TailwindCSS 配置
├── data/
│   ├── users.json          # 用户数据
│   ├── checkins.json       # 签到记录
│   ├── badges.json         # 徽章数据
│   ├── ai_quotes.json      # AI 生成语录
│   └── quotes.json         # 思乡话语（20 条内置）
├── models/
│   ├── __init__.py
│   ├── storage.py          # JSON 数据存储
│   └── user.py             # 用户模型
├── routes/
│   ├── __init__.py
│   ├── auth.py             # 认证路由
│   ├── checkin.py          # 签到路由
│   ├── dashboard.py        # 仪表盘路由
│   ├── quotes.py           # 话语管理路由
│   ├── ai_hometown.py      # AI 思乡话语生成路由
│   ├── badges.py           # 徽章路由
│   └── api.py              # JSON API 路由（供前端调用）
├── templates/              # HTML 模板
│   └── ai_hometown/        # AI 生成模板
├── static/
│   ├── css/
│   │   └── style.css       # 样式文件
│   └── js/
│   │   └── main.js         # 前端脚本
└── utils/
    ├── __init__.py
    ├── quote_generator.py  # 话语生成器
    └── ai_hometown_generator.py  # AI 思乡话语生成器
```

## 内置思乡话语分类

- **古诗**: 经典思乡诗词
- **现代**: 现代思乡散文
- **亲情**: 关于父母家人的牵挂
- **感悟**: 游子心得感悟

## 使用说明

1. 注册账号，填写家乡、当前城市、离家日期
2. 登录后可在首页查看离家天数和签到统计
3. 点击"签到"进行每日打卡
4. 签到后自动生成一句思乡话语
5. 可在"话语"页面查看和添加自定义话语
6. 可在"AI 生成"页面使用 AI 生成方言风格思乡话语

## AI 思乡话语生成

### 多模型支持

AI 生成功能支持多种大模型 API，可通过配置切换：

| 提供商 | 模型示例 | 配置方式 |
|--------|----------|----------|
| Anthropic | claude-sonnet-4-20250514 | 原生支持 |
| 阿里云百炼 | qwen-plus | 兼容模式 |
| OpenAI | gpt-4o-mini | 原生支持 |
| 其他 | 任意 OpenAI 兼容 API | 自定义配置 |

### 签到自动集成

每次签到时，系统会：
1. 读取用户的家乡信息
2. 自动匹配方言风格（如四川话、粤语等）
3. 调用 AI 生成具有地方特色的思乡话语
4. 如果没有配置 API，则使用内置话语

### 生成分类

手动生成功能支持以下分类：
- **饮食关怀**: 用家乡方言风格生成关于美食的关怀话语
- **天气问候**: 结合家乡天气的问候语
- **节日思念**: 节日思乡话语
- **日常问候**: 日常思乡问候（如"娃吃饭了吗"）
- **思乡诗句**: 创作思乡诗句或顺口溜
- **童年回忆**: 唤起童年家乡回忆的话语

系统会根据你输入的家乡地点自动匹配对应的方言风格（如四川话、粤语、北京话等）。

## TODO

- [ ] 添加地图模块，显示当前位置离家的距离
- [ ] 添加用户头像上传功能
- [ ] 实现多语言支持
- [ ] 增加移动端推送提醒
- [ ] 开发桌面端应用
- [ ] 签到分享功能（生成海报图片）
- [ ] 家庭群组成员管理（添加多个家庭成员）
- [ ] 签到历史记录页面

## 部署指南

### 方案一：GitHub Pages + Render（推荐）

将前端部署到 GitHub Pages，后端部署到 Render 云平台（免费额度）。

#### 1. 部署后端到 Render

**步骤：**

1. 访问 [render.com](https://render.com) 并注册账号

2. 点击 "New +" → "Web Service"

3. 连接你的 GitHub 仓库，选择 `GoHome` 项目

4. 配置如下：
   - **Name**: `homesignin-api`
   - **Branch**: `main`
   - **Root Directory**: 留空
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt -r requirements-prod.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

5. 设置环境变量（在 Render 控制台）：
   ```
   PORT=5001
   SECRET_KEY=<生成一个随机密钥>
   AI_API_KEY=<你的 AI API 密钥>（可选）
   AI_API_BASE_URL=<你的 AI API 地址>（可选）
   AI_MODEL=<你使用的模型>（可选）
   ```

6. 点击 "Create Web Service"，等待部署完成

7. 部署完成后，你会得到一个类似 `https://homesignin-api.onrender.com` 的 URL

#### 2. 配置前端并部署到 GitHub Pages

**步骤：**

1. 在 `frontend/.env` 文件中配置后端 API 地址：
   ```
   VITE_API_BASE_URL=https://homesignin-api.onrender.com
   ```

2. 构建前端：
   ```bash
   cd frontend
   npm install
   npm run build
   ```

3. 在 GitHub 仓库页面，进入 **Settings** → **Pages**

4. 在 **Source** 下拉框选择 **GitHub Actions**

5. 提交代码到 `main` 分支，GitHub Actions 会自动构建并部署

6. 部署完成后，访问 `https://<你的用户名>.github.io/GoHome/` 即可使用

#### 3. 配置 CORS（重要）

由于前端和后端分离，需要在后端添加 CORS 支持。编辑 `app.py`：

```python
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # ...
    CORS(app, supports_credentials=True)
    # ...
```

### 方案二：Docker 一键部署

如果你有支持 Docker 的服务器，可以使用 Docker 部署。

**构建镜像：**

```bash
docker build -t homesignin .
```

**运行容器：**

```bash
docker run -d -p 5001:5001 -v $(pwd)/data:/app/data -e SECRET_KEY=your-secret-key homesignin
```

### 方案三：单机部署（开发环境）

适合本地开发或内网使用。

**启动后端：**
```bash
pixi run dev
```

**启动前端（新终端）：**
```bash
cd frontend
npm run dev
```

访问 http://localhost:3000


## License

MIT License