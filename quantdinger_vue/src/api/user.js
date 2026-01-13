/**
 * User Management API
 */
import request from '@/utils/request'

// ==================== Admin APIs ====================

/**
 * Get user list (admin only)
 * @param {Object} params - { page, page_size }
 */
export function getUserList (params) {
  return request({
    url: '/api/users/list',
    method: 'get',
    params
  })
}

/**
 * Get user detail (admin only)
 * @param {Number} id - User ID
 */
export function getUserDetail (id) {
  return request({
    url: '/api/users/detail',
    method: 'get',
    params: { id }
  })
}

/**
 * Create new user (admin only)
 * @param {Object} data - { username, password, email, nickname, role }
 */
export function createUser (data) {
  return request({
    url: '/api/users/create',
    method: 'post',
    data
  })
}

/**
 * Update user (admin only)
 * @param {Number} id - User ID
 * @param {Object} data - { email, nickname, role, status }
 */
export function updateUser (id, data) {
  return request({
    url: '/api/users/update',
    method: 'put',
    params: { id },
    data
  })
}

/**
 * Delete user (admin only)
 * @param {Number} id - User ID
 */
export function deleteUser (id) {
  return request({
    url: '/api/users/delete',
    method: 'delete',
    params: { id }
  })
}

/**
 * Reset user password (admin only)
 * @param {Object} data - { user_id, new_password }
 */
export function resetUserPassword (data) {
  return request({
    url: '/api/users/reset-password',
    method: 'post',
    data
  })
}

/**
 * Get available roles
 */
export function getRoles () {
  return request({
    url: '/api/users/roles',
    method: 'get'
  })
}

// ==================== Self-Service APIs ====================

/**
 * Get current user profile
 */
export function getProfile () {
  return request({
    url: '/api/users/profile',
    method: 'get'
  })
}

/**
 * Update current user profile
 * @param {Object} data - { nickname, email, avatar }
 */
export function updateProfile (data) {
  return request({
    url: '/api/users/profile/update',
    method: 'put',
    data
  })
}

/**
 * Change current user password
 * @param {Object} data - { old_password, new_password }
 */
export function changePassword (data) {
  return request({
    url: '/api/users/change-password',
    method: 'post',
    data
  })
}
