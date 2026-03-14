from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
from routes.auth import login_required
from utils.ai_hometown_generator import AIHometownGenerator
from config import AI_API_KEY, AI_API_BASE_URL, AI_MODEL
from models.storage import QuoteStorage

ai_hometown_bp = Blueprint('ai_hometown', __name__)


def get_generator():
    """获取 AI 生成器实例"""
    if not AI_API_KEY:
        return None
    return AIHometownGenerator(
        api_key=AI_API_KEY,
        base_url=AI_API_BASE_URL,
        model=AI_MODEL
    )


@ai_hometown_bp.route('/ai-hometown')
@login_required
def index():
    """AI 思乡话语生成主页"""
    generator = get_generator()
    categories = []
    if generator:
        categories = generator.get_available_categories()

    return render_template('ai_hometown/index.html', categories=categories, has_api_key=bool(AI_API_KEY))


@ai_hometown_bp.route('/ai-hometown/generate', methods=['POST'])
@login_required
def generate():
    """生成思乡话语"""
    generator = get_generator()

    if not generator:
        return jsonify({
            'success': False,
            'error': '请先配置 API Key'
        })

    location = request.form.get('location', '').strip()
    category = request.form.get('category', 'daily')
    custom_prompt = request.form.get('custom_prompt', '').strip()

    if not location:
        return jsonify({
            'success': False,
            'error': '请输入家乡地点'
        })

    # 生成话语
    result = generator.generate(location, category, custom_prompt if custom_prompt else None)

    if result:
        return jsonify({
            'success': True,
            'data': result
        })
    else:
        return jsonify({
            'success': False,
            'error': '生成失败，请稍后重试'
        })


@ai_hometown_bp.route('/ai-hometown/generate-batch', methods=['POST'])
@login_required
def generate_batch():
    """批量生成思乡话语"""
    generator = get_generator()

    if not generator:
        return jsonify({
            'success': False,
            'error': '请先配置 API Key'
        })

    location = request.form.get('location', '').strip()

    if not location:
        return jsonify({
            'success': False,
            'error': '请输入家乡地点'
        })

    # 批量生成
    results = generator.generate_batch(location)

    if results:
        return jsonify({
            'success': True,
            'data': results
        })
    else:
        return jsonify({
            'success': False,
            'error': '生成失败，请稍后重试'
        })


@ai_hometown_bp.route('/ai-hometown/save', methods=['POST'])
@login_required
def save_quote():
    """保存生成的话语到收藏"""
    content = request.form.get('content', '').strip()
    category = request.form.get('category', 'AI 生成').strip()

    if not content:
        return jsonify({
            'success': False,
            'error': '话语内容不能为空'
        })

    user_id = session['user_id']
    QuoteStorage.add_custom(user_id, content, category)

    return jsonify({
        'success': True,
        'message': '已保存到收藏'
    })


@ai_hometown_bp.route('/ai-hometown/history')
@login_required
def history():
    """生成历史"""
    user_id = session['user_id']
    # 从 storage 获取 AI 生成的话语
    all_quotes = QuoteStorage.get_all_quotes(user_id)
    ai_quotes = [q for q in all_quotes if q.get('category', '').startswith('AI') or q.get('category', '') in ['饮食关怀', '天气问候', '节日思念', '日常问候', '思乡诗句', '童年回忆']]

    return render_template('ai_hometown/history.html', quotes=ai_quotes)
