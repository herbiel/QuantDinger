"""
Authentication API Routes

Handles login, logout, and user info retrieval.
Supports both multi-user (database) and single-user (legacy) modes.
"""
import os
from flask import Blueprint, request, jsonify, g
from app.config.settings import Config
from app.utils.auth import generate_token, login_required, authenticate_legacy
from app.utils.logger import get_logger

logger = get_logger(__name__)

auth_bp = Blueprint('auth', __name__)


def _is_single_user_mode() -> bool:
    """Check if system is in single-user (legacy) mode"""
    return os.getenv('SINGLE_USER_MODE', 'false').lower() == 'true'


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint.
    
    Request body:
        username: str
        password: str
    
    Returns:
        token: JWT token
        userinfo: User information
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'msg': 'No data provided', 'data': None}), 400
            
        username = data.get('username') or data.get('account')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'code': 400, 'msg': 'Missing username or password', 'data': None}), 400
        
        is_demo = os.getenv('IS_DEMO_MODE', 'false').lower() == 'true'
        user = None
        
        # Try multi-user authentication first
        if not _is_single_user_mode():
            try:
                from app.services.user_service import get_user_service
                user = get_user_service().authenticate(username, password)
            except Exception as e:
                logger.warning(f"Multi-user auth failed, trying legacy: {e}")
        
        # Fallback to legacy single-user mode
        if not user:
            user = authenticate_legacy(username, password)
        
        if not user:
            return jsonify({'code': 0, 'msg': 'Invalid credentials', 'data': None}), 401
        
        # Generate token
        token = generate_token(
            user_id=user.get('id') or user.get('user_id', 1),
            username=user.get('username', username),
            role=user.get('role', 'admin')
        )
        
        if not token:
            return jsonify({'code': 500, 'msg': 'Token generation error', 'data': None}), 500
        
        # Build user info for frontend
        userinfo = {
            'id': user.get('id') or user.get('user_id', 1),
            'username': user.get('username', username),
            'nickname': user.get('nickname', 'User') + (' (Demo)' if is_demo else ''),
            'avatar': user.get('avatar', '/avatar2.jpg'),
            'is_demo': is_demo,
            'role': {
                'id': user.get('role', 'admin'),
                'permissions': _get_permissions(user.get('role', 'admin'))
            }
        }
        
        return jsonify({
            'code': 1,
            'msg': 'Login successful',
            'data': {
                'token': token,
                'userinfo': userinfo
            }
        })
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'code': 500, 'msg': str(e), 'data': None}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout (client removes token; server is stateless)."""
    return jsonify({'code': 1, 'msg': 'Logout successful', 'data': None})


@auth_bp.route('/info', methods=['GET'])
@login_required
def get_user_info():
    """Get current user info."""
    try:
        is_demo = os.getenv('IS_DEMO_MODE', 'false').lower() == 'true'
        
        user_id = getattr(g, 'user_id', 1)
        username = getattr(g, 'user', Config.ADMIN_USER)
        role = getattr(g, 'user_role', 'admin')
        
        # Try to get full user info from database
        user_data = None
        if not _is_single_user_mode():
            try:
                from app.services.user_service import get_user_service
                user_data = get_user_service().get_user_by_id(user_id)
            except Exception as e:
                logger.warning(f"Failed to get user from database: {e}")
        
        if user_data:
            return jsonify({
                'code': 1,
                'msg': 'Success',
                'data': {
                    'id': user_data.get('id'),
                    'username': user_data.get('username'),
                    'nickname': user_data.get('nickname', 'User') + (' (Demo)' if is_demo else ''),
                    'email': user_data.get('email'),
                    'avatar': user_data.get('avatar', '/avatar2.jpg'),
                    'is_demo': is_demo,
                    'role': {
                        'id': user_data.get('role', 'user'),
                        'permissions': _get_permissions(user_data.get('role', 'user'))
                    }
                }
            })
        
        # Fallback for legacy mode
        return jsonify({
            'code': 1,
            'msg': 'Success',
            'data': {
                'id': user_id,
                'username': username,
                'nickname': 'Admin' + (' (Demo)' if is_demo else ''),
                'avatar': '/avatar2.jpg',
                'is_demo': is_demo,
                'role': {
                    'id': role,
                    'permissions': _get_permissions(role)
                }
            }
        })
    except Exception as e:
        logger.error(f"get_user_info error: {e}")
        return jsonify({'code': 500, 'msg': str(e), 'data': None}), 500


def _get_permissions(role: str) -> list:
    """Get permissions list for a role"""
    try:
        from app.services.user_service import get_user_service
        return get_user_service().get_user_permissions(role)
    except Exception:
        # Default permissions for admin
        if role == 'admin':
            return ['dashboard', 'view', 'indicator', 'backtest', 'strategy', 
                    'portfolio', 'settings', 'user_manage', 'credentials']
        return ['dashboard', 'view', 'indicator', 'backtest', 'strategy', 'portfolio']
