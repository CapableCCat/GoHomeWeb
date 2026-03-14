"""
AI 思乡话语生成器
支持多种大模型 API：Anthropic Claude、阿里云百炼、OpenAI 等
"""

import requests
from typing import Optional, List
from enum import Enum
import json


class ModelProvider(Enum):
    """模型提供商"""
    ANTHROPIC = "anthropic"
    ALIYUN = "aliyun"
    OPENAI = "openai"
    CUSTOM = "custom"


class AIHometownGenerator:
    """AI 思乡话语生成器"""

    # 内置提示词模板
    PROMPT_TEMPLATES = {
        'diet': {
            'name': '饮食关怀',
            'template': '请用{dialect}方言风格，写一句关于家乡美食的关怀话语，要温馨朴实，体现家乡味道。家乡地点：{location}。要求：口语化，接地气，20 字以内。'
        },
        'weather': {
            'name': '天气问候',
            'template': '请用{dialect}方言风格，写一句结合家乡天气的问候语，体现对家人的牵挂。家乡地点：{location}。要求：温暖贴心，口语化，25 字以内。'
        },
        'festival': {
            'name': '节日思念',
            'template': '请用{dialect}方言风格，写一句节日思乡的话语，表达想家的心情。家乡地点：{location}。要求：情感真挚，有地方特色，30 字以内。'
        },
        'daily': {
            'name': '日常问候',
            'template': '请用{dialect}方言风格，写一句日常思乡问候语。家乡地点：{location}。要求：朴实自然，像家人之间的对话，20 字以内。'
        },
        'poem': {
            'name': '思乡诗句',
            'template': '请用{dialect}方言风格，创作一句简短的思乡诗句或顺口溜。家乡地点：{location}。要求：押韵，有地方特色，20 字以内。'
        },
        'childhood': {
            'name': '童年回忆',
            'template': '请用{dialect}方言风格，写一句唤起童年家乡回忆的话语。家乡地点：{location}。要求：温馨怀旧，有画面感，25 字以内。'
        }
    }

    # 常见地区方言映射
    DIALECT_MAP = {
        '北京': '北京话',
        '上海': '上海话',
        '广东': '粤语',
        '广州': '粤语',
        '深圳': '粤语',
        '四川': '四川话',
        '成都': '四川话',
        '重庆': '重庆话',
        '湖南': '湖南话',
        '长沙': '长沙话',
        '湖北': '湖北话',
        '武汉': '武汉话',
        '河南': '河南话',
        '河北': '河北话',
        '山东': '山东话',
        '陕西': '陕西话',
        '西安': '陕西话',
        '江苏': '江苏话',
        '浙江': '浙江话',
        '杭州': '杭州话',
        '福建': '福建话',
        '厦门': '闽南话',
        '台湾': '闽南话',
        '东北': '东北话',
        '哈尔滨': '东北话',
        '辽宁': '东北话',
        '吉林': '东北话',
        '黑龙江': '东北话',
        '江西': '江西话',
        '安徽': '安徽话',
        '山西': '山西话',
        '天津': '天津话',
        '云南': '云南话',
        '贵州': '贵州话',
        '广西': '广西话',
        '海南': '海南话',
        '甘肃': '甘肃话',
        '青海': '青海话',
        '宁夏': '宁夏话',
        '新疆': '新疆话',
        '西藏': '藏语风格',
        '内蒙古': '蒙古语风格',
    }

    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        model: str = None,
        provider: str = None
    ):
        """
        初始化生成器

        Args:
            api_key: API 密钥
            base_url: API 基础 URL
            model: 模型名称
            provider: 模型提供商 (anthropic/aliyun/openai/custom)
        """
        self.api_key = api_key
        self.base_url = base_url or ''
        self.model = model or ''
        self.provider = self._detect_provider(provider, base_url)

    def _detect_provider(self, provider: str = None, base_url: str = None) -> ModelProvider:
        """根据配置检测模型提供商"""
        if provider:
            try:
                return ModelProvider(provider.lower())
            except ValueError:
                pass

        # 根据 base_url 自动检测
        if base_url:
            if 'anthropic' in base_url.lower():
                return ModelProvider.ANTHROPIC
            elif 'aliyuncs' in base_url.lower() or 'dashscope' in base_url.lower():
                return ModelProvider.ALIYUN
            elif 'openai' in base_url.lower():
                return ModelProvider.OPENAI

        # 默认使用 Anthropic 格式
        return ModelProvider.CUSTOM

    def _get_dialect(self, location: str) -> str:
        """根据地点获取方言"""
        for key, dialect in self.DIALECT_MAP.items():
            if key in location:
                return dialect
        return '普通话'

    def _build_prompt(self, location: str, dialect: str, category: str = 'daily', custom_prompt: str = None) -> str:
        """构建提示词"""
        if custom_prompt:
            return custom_prompt.format(dialect=dialect, location=location)

        if category in self.PROMPT_TEMPLATES:
            template = self.PROMPT_TEMPLATES[category]
            return template['template'].format(dialect=dialect, location=location)

        return f'请用{dialect}方言风格，写一句关于思乡的话语。家乡地点：{location}。要求：温馨感人，口语化。'

    def _call_anthropic_api(self, prompt: str) -> Optional[str]:
        """调用 Anthropic Claude API"""
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01'
        }

        data = {
            'model': self.model or 'claude-sonnet-4-20250514',
            'max_tokens': 100,
            'messages': [{'role': 'user', 'content': prompt}]
        }

        url = f'{self.base_url}/messages' if self.base_url else 'https://api.anthropic.com/v1/messages'

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get('content', [{}])[0].get('text', '')

    def _call_aliyun_api(self, prompt: str) -> Optional[str]:
        """调用阿里云百炼 API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': self.model or 'qwen-plus',
            'input': {'message': prompt},
            'parameters': {'max_tokens': 100}
        }

        url = f'{self.base_url}/compatible-mode/v1/chat/completions' if self.base_url else 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content', '')

    def _call_openai_api(self, prompt: str) -> Optional[str]:
        """调用 OpenAI 兼容 API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': self.model or 'gpt-3.5-turbo',
            'max_tokens': 100,
            'messages': [{'role': 'user', 'content': prompt}]
        }

        url = f'{self.base_url}/chat/completions' if self.base_url else 'https://api.openai.com/v1/chat/completions'

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content', '')

    def _call_custom_api(self, prompt: str) -> Optional[str]:
        """调用自定义 API（默认使用 OpenAI 兼容格式）"""
        return self._call_openai_api(prompt)

    def _call_api(self, prompt: str) -> Optional[str]:
        """
        调用大模型 API（根据提供商自动选择）

        Args:
            prompt: 提示词

        Returns:
            生成的文本，失败返回 None
        """
        try:
            if self.provider == ModelProvider.ANTHROPIC:
                return self._call_anthropic_api(prompt)
            elif self.provider == ModelProvider.ALIYUN:
                return self._call_aliyun_api(prompt)
            elif self.provider == ModelProvider.OPENAI:
                return self._call_openai_api(prompt)
            else:
                return self._call_custom_api(prompt)
        except requests.exceptions.RequestException as e:
            print(f"API 调用失败：{e}")
            return None
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"解析响应失败：{e}")
            return None

    def generate(
        self,
        location: str,
        category: str = 'daily',
        custom_prompt: str = None
    ) -> Optional[dict]:
        """
        生成思乡话语

        Args:
            location: 家乡地点
            category: 分类 (diet/weather/festival/daily/poem/childhood)
            custom_prompt: 自定义提示词（可选）

        Returns:
            包含生成结果和元数据的字典
        """
        dialect = self._get_dialect(location)
        prompt = self._build_prompt(location, dialect, category, custom_prompt)
        result = self._call_api(prompt)

        if result:
            result = result.strip().strip('"\'""')
            return {
                'content': result,
                'category': self.PROMPT_TEMPLATES.get(category, {}).get('name', category),
                'dialect': dialect,
                'location': location,
                'category_key': category
            }
        return None

    def generate_for_checkin(
        self,
        user_info: dict
    ) -> Optional[dict]:
        """
        为签到打卡生成思乡话语（根据用户信息自动生成）

        Args:
            user_info: 用户信息，包含 hometown, current_city 等

        Returns:
            生成结果
        """
        hometown = user_info.get('hometown', '')
        current_city = user_info.get('current_city', '')

        if not hometown:
            return None

        dialect = self._get_dialect(hometown)

        # 构建综合提示词，结合用户信息
        prompt = f'''请用{dialect}方言风格，写一句温馨的日常问候语。
家乡：{hometown}
当前所在城市：{current_city or '外地'}

要求：
- 口语化，像家人之间的对话
- 体现对游子的关怀
- 20 字以内'''

        result = self._call_api(prompt)

        if result:
            result = result.strip().strip('"\'""')
            return {
                'content': result,
                'category': 'AI 生成',
                'dialect': dialect,
                'location': hometown
            }
        return None

    def generate_batch(self, location: str, categories: List[str] = None) -> List[dict]:
        """
        批量生成多个分类的思乡话语

        Args:
            location: 家乡地点
            categories: 分类列表

        Returns:
            生成结果列表
        """
        if categories is None:
            categories = ['daily', 'diet', 'weather', 'poem']

        results = []
        for category in categories:
            result = self.generate(location, category)
            if result:
                results.append(result)
        return results

    def get_available_categories(self) -> List[dict]:
        """获取所有可用的分类"""
        return [
            {'key': key, 'name': value['name']}
            for key, value in self.PROMPT_TEMPLATES.items()
        ]
