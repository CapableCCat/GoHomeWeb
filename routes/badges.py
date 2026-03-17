from flask import Blueprint, render_template, session, jsonify
from routes.auth import login_required
from models.badge import BadgeStorage
from models.user import User
from models.storage import UserStorage

badges_bp = Blueprint('badges', __name__)


@badges_bp.route('/badges')
@login_required
def index():
    """勋章墙页面"""
    user = User(UserStorage.get_by_id(session['user_id']))
    user_badges = BadgeStorage.get_by_user(user.id)
    all_definitions = BadgeStorage.get_all_definitions()

    # 获取用户已获得的勋章 ID 列表
    earned_ids = set(b['badge_id'] for b in user_badges)

    # 按分类组织勋章
    categories = {
        'time': {'name': '时间里程碑', 'badges': []},
        'streak': {'name': '签到连续', 'badges': []},
        'special': {'name': '特殊成就', 'badges': []},
    }

    for badge_id, definition in all_definitions.items():
        category = definition.get('category', 'special')
        categories[category]['badges'].append({
            'id': badge_id,
            'name': definition['name'],
            'description': definition['description'],
            'earned': badge_id in earned_ids,
            'earned_at': next(
                (b['earned_at'] for b in user_badges if b['badge_id'] == badge_id),
                None
            )
        })

    return render_template('badges.html', user=user, categories=categories)


@badges_bp.route('/api/badges')
@login_required
def api_list():
    """API: 获取用户勋章列表"""
    user_badges = BadgeStorage.get_by_user(session['user_id'])
    all_definitions = BadgeStorage.get_all_definitions()

    result = []
    for badge in user_badges:
        definition = all_definitions.get(badge['badge_id'], {})
        result.append({
            'id': badge['badge_id'],
            'name': definition.get('name', ''),
            'description': definition.get('description', ''),
            'category': definition.get('category', ''),
            'earned_at': badge['earned_at']
        })

    return jsonify(result)


@badges_bp.route('/api/badges/definitions')
@login_required
def api_definitions():
    """API: 获取所有勋章定义"""
    all_definitions = BadgeStorage.get_all_definitions()

    # 按分类组织
    categories = {
        'time': {'name': '时间里程碑', 'badges': []},
        'streak': {'name': '签到连续', 'badges': []},
        'special': {'name': '特殊成就', 'badges': []},
    }

    for badge_id, definition in all_definitions.items():
        category = definition.get('category', 'special')
        categories[category]['badges'].append({
            'id': badge_id,
            'name': definition['name'],
            'description': definition['description'],
            'category': category
        })

    return jsonify(categories)
