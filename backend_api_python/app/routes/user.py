"""
User Management API Routes

Provides endpoints for user CRUD operations, role management, etc.
Only accessible by admin users.
"""
from flask import Blueprint, request, jsonify, g
from app.services.user_service import get_user_service
from app.utils.auth import login_required, admin_required
from app.utils.logger import get_logger

logger = get_logger(__name__)

user_bp = Blueprint('user_manage', __name__)


@user_bp.route('/list', methods=['GET'])
@login_required
@admin_required
def list_users():
    """
    List all users (admin only).
    
    Query params:
        page: int (default 1)
        page_size: int (default 20, max 100)
    """
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        page_size = min(100, max(1, page_size))
        
        result = get_user_service().list_users(page=page, page_size=page_size)
        
        return jsonify({
            'code': 1,
            'msg': 'success',
            'data': result
        })
    except Exception as e:
        logger.error(f"list_users failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500


@user_bp.route('/detail', methods=['GET'])
@login_required
@admin_required
def get_user_detail():
    """Get user detail by ID (admin only)"""
    try:
        user_id = request.args.get('id', type=int)
        if not user_id:
            return jsonify({'code': 0, 'msg': 'Missing user id', 'data': None}), 400
        
        user = get_user_service().get_user_by_id(user_id)
        if not user:
            return jsonify({'code': 0, 'msg': 'User not found', 'data': None}), 404
        
        return jsonify({
            'code': 1,
            'msg': 'success',
            'data': user
        })
    except Exception as e:
        logger.error(f"get_user_detail failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500


@user_bp.route('/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    """
    Create a new user (admin only).
    
    Request body:
        username: str (required)
        password: str (required)
        email: str (optional)
        nickname: str (optional)
        role: str (optional, default 'user')
    """
    try:
        data = request.get_json() or {}
        
        user_id = get_user_service().create_user(data)
        
        return jsonify({
            'code': 1,
            'msg': 'User created successfully',
            'data': {'id': user_id}
        })
    except ValueError as e:
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 400
    except Exception as e:
        logger.error(f"create_user failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500


@user_bp.route('/update', methods=['PUT'])
@login_required
@admin_required
def update_user():
    """
    Update user information (admin only).
    
    Query params:
        id: int (required)
    
    Request body:
        email: str (optional)
        nickname: str (optional)
        role: str (optional)
        status: str (optional)
    """
    try:
        user_id = request.args.get('id', type=int)
        if not user_id:
            return jsonify({'code': 0, 'msg': 'Missing user id', 'data': None}), 400
        
        data = request.get_json() or {}
        
        success = get_user_service().update_user(user_id, data)
        
        if success:
            return jsonify({'code': 1, 'msg': 'User updated successfully', 'data': None})
        else:
            return jsonify({'code': 0, 'msg': 'Update failed', 'data': None}), 400
    except Exception as e:
        logger.error(f"update_user failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500


@user_bp.route('/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_user():
    """Delete a user (admin only)"""
    try:
        user_id = request.args.get('id', type=int)
        if not user_id:
            return jsonify({'code': 0, 'msg': 'Missing user id', 'data': None}), 400
        
        # Prevent deleting self
        if hasattr(g, 'user_id') and g.user_id == user_id:
            return jsonify({'code': 0, 'msg': 'Cannot delete yourself', 'data': None}), 400
        
        success = get_user_service().delete_user(user_id)
        
        if success:
            return jsonify({'code': 1, 'msg': 'User deleted successfully', 'data': None})
        else:
            return jsonify({'code': 0, 'msg': 'Delete failed', 'data': None}), 400
    except Exception as e:
        logger.error(f"delete_user failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500


@user_bp.route('/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_user_password():
    """
    Reset a user's password (admin only).
    
    Request body:
        user_id: int (required)
        new_password: str (required)
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        new_password = data.get('new_password', '')
        
        if not user_id:
            return jsonify({'code': 0, 'msg': 'Missing user_id', 'data': None}), 400
        
        if len(new_password) < 6:
            return jsonify({'code': 0, 'msg': 'Password must be at least 6 characters', 'data': None}), 400
        
        success = get_user_service().reset_password(user_id, new_password)
        
        if success:
            return jsonify({'code': 1, 'msg': 'Password reset successfully', 'data': None})
        else:
            return jsonify({'code': 0, 'msg': 'Reset failed', 'data': None}), 400
    except ValueError as e:
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 400
    except Exception as e:
        logger.error(f"reset_user_password failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500


@user_bp.route('/roles', methods=['GET'])
@login_required
@admin_required
def get_roles():
    """Get available roles and their permissions"""
    service = get_user_service()
    
    roles = []
    for role in service.ROLES:
        roles.append({
            'id': role,
            'name': role.capitalize(),
            'permissions': service.get_user_permissions(role)
        })
    
    return jsonify({
        'code': 1,
        'msg': 'success',
        'data': {'roles': roles}
    })


# Self-service endpoints (accessible by any logged-in user)

@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user's profile"""
    try:
        user_id = getattr(g, 'user_id', None)
        if not user_id:
            return jsonify({'code': 0, 'msg': 'Not authenticated', 'data': None}), 401
        
        user = get_user_service().get_user_by_id(user_id)
        if not user:
            return jsonify({'code': 0, 'msg': 'User not found', 'data': None}), 404
        
        # Add permissions
        user['permissions'] = get_user_service().get_user_permissions(user.get('role', 'user'))
        
        return jsonify({
            'code': 1,
            'msg': 'success',
            'data': user
        })
    except Exception as e:
        logger.error(f"get_profile failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500


@user_bp.route('/profile/update', methods=['PUT'])
@login_required
def update_profile():
    """
    Update current user's profile (limited fields).
    
    Request body:
        nickname: str (optional)
        email: str (optional)
        avatar: str (optional)
    """
    try:
        user_id = getattr(g, 'user_id', None)
        if not user_id:
            return jsonify({'code': 0, 'msg': 'Not authenticated', 'data': None}), 401
        
        data = request.get_json() or {}
        
        # Only allow updating certain fields for self-service
        allowed = {}
        for field in ['nickname', 'email', 'avatar']:
            if field in data:
                allowed[field] = data[field]
        
        if not allowed:
            return jsonify({'code': 0, 'msg': 'No valid fields to update', 'data': None}), 400
        
        success = get_user_service().update_user(user_id, allowed)
        
        if success:
            return jsonify({'code': 1, 'msg': 'Profile updated successfully', 'data': None})
        else:
            return jsonify({'code': 0, 'msg': 'Update failed', 'data': None}), 400
    except Exception as e:
        logger.error(f"update_profile failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500


@user_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """
    Change current user's password.
    
    Request body:
        old_password: str (required)
        new_password: str (required)
    """
    try:
        user_id = getattr(g, 'user_id', None)
        if not user_id:
            return jsonify({'code': 0, 'msg': 'Not authenticated', 'data': None}), 401
        
        data = request.get_json() or {}
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        
        if not old_password or not new_password:
            return jsonify({'code': 0, 'msg': 'Both old and new password required', 'data': None}), 400
        
        if len(new_password) < 6:
            return jsonify({'code': 0, 'msg': 'New password must be at least 6 characters', 'data': None}), 400
        
        success = get_user_service().change_password(user_id, old_password, new_password)
        
        if success:
            return jsonify({'code': 1, 'msg': 'Password changed successfully', 'data': None})
        else:
            return jsonify({'code': 0, 'msg': 'Old password incorrect', 'data': None}), 400
    except ValueError as e:
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 400
    except Exception as e:
        logger.error(f"change_password failed: {e}")
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 500
