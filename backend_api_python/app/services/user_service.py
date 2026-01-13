"""
User Service - Multi-user management

Handles user CRUD operations, password hashing, and role management.
"""
import hashlib
import time
import os
from typing import Optional, Dict, Any, List
from app.utils.db import get_db_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Try to import bcrypt for secure password hashing
try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False
    logger.warning("bcrypt not installed. Using SHA256 for password hashing (less secure).")


class UserService:
    """User management service"""
    
    # Available roles (ordered by privilege level)
    ROLES = ['viewer', 'user', 'manager', 'admin']
    
    # Role permissions mapping
    ROLE_PERMISSIONS = {
        'viewer': ['dashboard', 'view'],
        'user': ['dashboard', 'view', 'indicator', 'backtest', 'strategy', 'portfolio'],
        'manager': ['dashboard', 'view', 'indicator', 'backtest', 'strategy', 'portfolio', 'settings'],
        'admin': ['dashboard', 'view', 'indicator', 'backtest', 'strategy', 'portfolio', 'settings', 'user_manage', 'credentials'],
    }
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt (preferred) or SHA256 (fallback)"""
        if HAS_BCRYPT:
            salt = bcrypt.gensalt(rounds=12)
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        else:
            # Fallback to SHA256 with salt
            salt = os.urandom(16).hex()
            hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            return f"sha256${salt}${hashed}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        if password_hash.startswith('$2b$') or password_hash.startswith('$2a$'):
            # bcrypt hash
            if HAS_BCRYPT:
                try:
                    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
                except Exception:
                    return False
            return False
        elif password_hash.startswith('sha256$'):
            # SHA256 fallback hash
            parts = password_hash.split('$')
            if len(parts) != 3:
                return False
            salt = parts[1]
            stored_hash = parts[2]
            computed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            return computed == stored_hash
        return False
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                cur.execute(
                    """
                    SELECT id, username, email, nickname, avatar, status, role, 
                           last_login_at, created_at, updated_at
                    FROM qd_users WHERE id = ?
                    """,
                    (user_id,)
                )
                row = cur.fetchone()
                cur.close()
                return row
        except Exception as e:
            logger.error(f"get_user_by_id failed: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username (includes password_hash for auth)"""
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                cur.execute(
                    """
                    SELECT id, username, password_hash, email, nickname, avatar, 
                           status, role, last_login_at, created_at, updated_at
                    FROM qd_users WHERE username = ?
                    """,
                    (username,)
                )
                row = cur.fetchone()
                cur.close()
                return row
        except Exception as e:
            logger.error(f"get_user_by_username failed: {e}")
            return None
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with username and password.
        Returns user info (without password_hash) if successful, None otherwise.
        """
        user = self.get_user_by_username(username)
        if not user:
            return None
        
        if user.get('status') != 'active':
            logger.warning(f"Login attempt for disabled user: {username}")
            return None
        
        if not self.verify_password(password, user.get('password_hash', '')):
            return None
        
        # Update last login time
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                cur.execute(
                    "UPDATE qd_users SET last_login_at = NOW() WHERE id = ?",
                    (user['id'],)
                )
                db.commit()
                cur.close()
        except Exception as e:
            logger.warning(f"Failed to update last_login_at: {e}")
        
        # Remove password_hash from return value
        user.pop('password_hash', None)
        return user
    
    def create_user(self, data: Dict[str, Any]) -> Optional[int]:
        """
        Create a new user.
        
        Args:
            data: {
                username: str (required),
                password: str (required),
                email: str (optional),
                nickname: str (optional),
                role: str (optional, default 'user'),
                status: str (optional, default 'active')
            }
        
        Returns:
            New user ID or None if failed
        """
        username = (data.get('username') or '').strip()
        password = data.get('password') or ''
        
        if not username or not password:
            raise ValueError("Username and password are required")
        
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be 3-50 characters")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        # Check if username already exists
        existing = self.get_user_by_username(username)
        if existing:
            raise ValueError("Username already exists")
        
        password_hash = self.hash_password(password)
        email = (data.get('email') or '').strip() or None
        nickname = (data.get('nickname') or '').strip() or username
        role = data.get('role', 'user')
        status = data.get('status', 'active')
        
        if role not in self.ROLES:
            role = 'user'
        
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                cur.execute(
                    """
                    INSERT INTO qd_users 
                    (username, password_hash, email, nickname, role, status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, NOW(), NOW())
                    """,
                    (username, password_hash, email, nickname, role, status)
                )
                db.commit()
                user_id = cur.lastrowid
                cur.close()
                
                # For PostgreSQL, get the ID differently
                if user_id is None:
                    cur = db.cursor()
                    cur.execute("SELECT id FROM qd_users WHERE username = ?", (username,))
                    row = cur.fetchone()
                    user_id = row['id'] if row else None
                    cur.close()
                
                logger.info(f"Created user: {username} (id={user_id})")
                return user_id
        except Exception as e:
            logger.error(f"create_user failed: {e}")
            raise
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> bool:
        """
        Update user information.
        
        Args:
            user_id: User ID
            data: Fields to update (email, nickname, avatar, role, status)
        """
        allowed_fields = ['email', 'nickname', 'avatar', 'role', 'status']
        updates = []
        values = []
        
        for field in allowed_fields:
            if field in data:
                value = data[field]
                if field == 'role' and value not in self.ROLES:
                    continue
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        values.append(user_id)
        
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                sql = f"UPDATE qd_users SET {', '.join(updates)} WHERE id = ?"
                cur.execute(sql, tuple(values))
                db.commit()
                cur.close()
                return True
        except Exception as e:
            logger.error(f"update_user failed: {e}")
            return False
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password (requires old password verification)"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Get full user with password_hash
        with get_db_connection() as db:
            cur = db.cursor()
            cur.execute("SELECT password_hash FROM qd_users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            cur.close()
            
            if not row:
                return False
            
            if not self.verify_password(old_password, row['password_hash']):
                return False
        
        return self.reset_password(user_id, new_password)
    
    def reset_password(self, user_id: int, new_password: str) -> bool:
        """Reset user password (admin operation, no old password required)"""
        if len(new_password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        password_hash = self.hash_password(new_password)
        
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                cur.execute(
                    "UPDATE qd_users SET password_hash = ?, updated_at = NOW() WHERE id = ?",
                    (password_hash, user_id)
                )
                db.commit()
                cur.close()
                return True
        except Exception as e:
            logger.error(f"reset_password failed: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                cur.execute("DELETE FROM qd_users WHERE id = ?", (user_id,))
                db.commit()
                cur.close()
                return True
        except Exception as e:
            logger.error(f"delete_user failed: {e}")
            return False
    
    def list_users(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """List all users with pagination"""
        offset = (page - 1) * page_size
        
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                
                # Get total count
                cur.execute("SELECT COUNT(*) as count FROM qd_users")
                total = cur.fetchone()['count']
                
                # Get users
                cur.execute(
                    """
                    SELECT id, username, email, nickname, avatar, status, role,
                           last_login_at, created_at, updated_at
                    FROM qd_users
                    ORDER BY id DESC
                    LIMIT ? OFFSET ?
                    """,
                    (page_size, offset)
                )
                users = cur.fetchall()
                cur.close()
                
                return {
                    'items': users,
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': (total + page_size - 1) // page_size
                }
        except Exception as e:
            logger.error(f"list_users failed: {e}")
            return {'items': [], 'total': 0, 'page': 1, 'page_size': page_size, 'total_pages': 0}
    
    def get_user_permissions(self, role: str) -> List[str]:
        """Get permissions for a role"""
        return self.ROLE_PERMISSIONS.get(role, self.ROLE_PERMISSIONS['viewer'])
    
    def ensure_admin_exists(self):
        """
        Ensure at least one admin user exists.
        Creates admin using ADMIN_USER/ADMIN_PASSWORD from env if no users exist.
        """
        try:
            with get_db_connection() as db:
                cur = db.cursor()
                cur.execute("SELECT COUNT(*) as count FROM qd_users")
                count = cur.fetchone()['count']
                cur.close()
                
                if count == 0:
                    # Create admin using env credentials
                    admin_user = os.getenv('ADMIN_USER', 'admin')
                    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
                    
                    self.create_user({
                        'username': admin_user,
                        'password': admin_password,
                        'nickname': 'Administrator',
                        'role': 'admin',
                        'status': 'active'
                    })
                    logger.info(f"Created admin user: {admin_user}")
        except Exception as e:
            logger.error(f"ensure_admin_exists failed: {e}")


# Global singleton
_user_service = None

def get_user_service() -> UserService:
    """Get UserService singleton"""
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service
