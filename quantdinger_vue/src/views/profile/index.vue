<template>
  <div class="profile-page" :class="{ 'theme-dark': isDarkTheme }">
    <div class="page-header">
      <h2 class="page-title">
        <a-icon type="user" />
        <span>{{ $t('profile.title') || 'My Profile' }}</span>
      </h2>
      <p class="page-desc">{{ $t('profile.description') || 'Manage your account settings and preferences' }}</p>
    </div>

    <a-row :gutter="24">
      <!-- Profile Card -->
      <a-col :xs="24" :md="8">
        <a-card :bordered="false" class="profile-card">
          <div class="avatar-section">
            <a-avatar :size="100" :src="profile.avatar || '/avatar2.jpg'" />
            <h3 class="username">{{ profile.nickname || profile.username }}</h3>
            <p class="user-role">
              <a-tag :color="getRoleColor(profile.role)">
                {{ getRoleLabel(profile.role) }}
              </a-tag>
            </p>
          </div>
          <a-divider />
          <div class="profile-info">
            <div class="info-item">
              <a-icon type="user" />
              <span class="label">{{ $t('profile.username') || 'Username' }}:</span>
              <span class="value">{{ profile.username }}</span>
            </div>
            <div class="info-item">
              <a-icon type="mail" />
              <span class="label">{{ $t('profile.email') || 'Email' }}:</span>
              <span class="value">{{ profile.email || '-' }}</span>
            </div>
            <div class="info-item">
              <a-icon type="calendar" />
              <span class="label">{{ $t('profile.lastLogin') || 'Last Login' }}:</span>
              <span class="value">{{ formatTime(profile.last_login_at) || '-' }}</span>
            </div>
          </div>
        </a-card>
      </a-col>

      <!-- Edit Profile -->
      <a-col :xs="24" :md="16">
        <a-card :bordered="false" class="edit-card">
          <a-tabs v-model="activeTab">
            <!-- Basic Info Tab -->
            <a-tab-pane key="basic" :tab="$t('profile.basicInfo') || 'Basic Info'">
              <a-form :form="profileForm" layout="vertical" class="profile-form">
                <a-form-item :label="$t('profile.nickname') || 'Nickname'">
                  <a-input
                    v-decorator="['nickname', { initialValue: profile.nickname }]"
                    :placeholder="$t('profile.nicknamePlaceholder') || 'Enter your nickname'"
                  >
                    <a-icon slot="prefix" type="smile" />
                  </a-input>
                </a-form-item>

                <a-form-item :label="$t('profile.email') || 'Email'">
                  <a-input
                    v-decorator="['email', {
                      initialValue: profile.email,
                      rules: [{ type: 'email', message: $t('profile.emailInvalid') || 'Invalid email format' }]
                    }]"
                    :placeholder="$t('profile.emailPlaceholder') || 'Enter your email'"
                  >
                    <a-icon slot="prefix" type="mail" />
                  </a-input>
                </a-form-item>

                <a-form-item>
                  <a-button type="primary" :loading="saving" @click="handleSaveProfile">
                    <a-icon type="save" />
                    {{ $t('common.save') || 'Save' }}
                  </a-button>
                </a-form-item>
              </a-form>
            </a-tab-pane>

            <!-- Change Password Tab -->
            <a-tab-pane key="password" :tab="$t('profile.changePassword') || 'Change Password'">
              <a-form :form="passwordForm" layout="vertical" class="password-form">
                <a-alert
                  :message="$t('profile.passwordHint') || 'Password must be at least 6 characters'"
                  type="info"
                  showIcon
                  style="margin-bottom: 24px"
                />

                <a-form-item :label="$t('profile.oldPassword') || 'Current Password'">
                  <a-input-password
                    v-decorator="['old_password', {
                      rules: [{ required: true, message: $t('profile.oldPasswordRequired') || 'Please enter current password' }]
                    }]"
                    :placeholder="$t('profile.oldPasswordPlaceholder') || 'Enter current password'"
                  >
                    <a-icon slot="prefix" type="lock" />
                  </a-input-password>
                </a-form-item>

                <a-form-item :label="$t('profile.newPassword') || 'New Password'">
                  <a-input-password
                    v-decorator="['new_password', {
                      rules: [
                        { required: true, message: $t('profile.newPasswordRequired') || 'Please enter new password' },
                        { min: 6, message: $t('profile.passwordMin') || 'Password must be at least 6 characters' }
                      ]
                    }]"
                    :placeholder="$t('profile.newPasswordPlaceholder') || 'Enter new password'"
                  >
                    <a-icon slot="prefix" type="lock" />
                  </a-input-password>
                </a-form-item>

                <a-form-item :label="$t('profile.confirmPassword') || 'Confirm Password'">
                  <a-input-password
                    v-decorator="['confirm_password', {
                      rules: [
                        { required: true, message: $t('profile.confirmPasswordRequired') || 'Please confirm password' },
                        { validator: validateConfirmPassword }
                      ]
                    }]"
                    :placeholder="$t('profile.confirmPasswordPlaceholder') || 'Confirm new password'"
                  >
                    <a-icon slot="prefix" type="lock" />
                  </a-input-password>
                </a-form-item>

                <a-form-item>
                  <a-button type="primary" :loading="changingPassword" @click="handleChangePassword">
                    <a-icon type="key" />
                    {{ $t('profile.changePassword') || 'Change Password' }}
                  </a-button>
                </a-form-item>
              </a-form>
            </a-tab-pane>
          </a-tabs>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { getProfile, updateProfile, changePassword } from '@/api/user'
import { baseMixin } from '@/store/app-mixin'

export default {
  name: 'Profile',
  mixins: [baseMixin],
  data () {
    return {
      loading: false,
      saving: false,
      changingPassword: false,
      activeTab: 'basic',
      profile: {
        id: null,
        username: '',
        nickname: '',
        email: '',
        avatar: '',
        role: 'user',
        last_login_at: null
      }
    }
  },
  computed: {
    isDarkTheme () {
      return this.navTheme === 'dark' || this.navTheme === 'realdark'
    }
  },
  beforeCreate () {
    this.profileForm = this.$form.createForm(this, { name: 'profile' })
    this.passwordForm = this.$form.createForm(this, { name: 'password' })
  },
  mounted () {
    this.loadProfile()
  },
  methods: {
    async loadProfile () {
      this.loading = true
      try {
        const res = await getProfile()
        if (res.code === 1) {
          this.profile = res.data
          this.$nextTick(() => {
            this.profileForm.setFieldsValue({
              nickname: this.profile.nickname,
              email: this.profile.email
            })
          })
        } else {
          this.$message.error(res.msg || 'Failed to load profile')
        }
      } catch (error) {
        this.$message.error('Failed to load profile')
      } finally {
        this.loading = false
      }
    },

    handleSaveProfile () {
      this.profileForm.validateFields(async (err, values) => {
        if (err) return

        this.saving = true
        try {
          const res = await updateProfile(values)
          if (res.code === 1) {
            this.$message.success(res.msg || 'Profile updated successfully')
            this.loadProfile()
          } else {
            this.$message.error(res.msg || 'Update failed')
          }
        } catch (error) {
          this.$message.error('Update failed')
        } finally {
          this.saving = false
        }
      })
    },

    validateConfirmPassword (rule, value, callback) {
      const newPassword = this.passwordForm.getFieldValue('new_password')
      if (value && value !== newPassword) {
        callback(this.$t('profile.passwordMismatch') || 'Passwords do not match')
      } else {
        callback()
      }
    },

    handleChangePassword () {
      this.passwordForm.validateFields(async (err, values) => {
        if (err) return

        this.changingPassword = true
        try {
          const res = await changePassword({
            old_password: values.old_password,
            new_password: values.new_password
          })
          if (res.code === 1) {
            this.$message.success(res.msg || 'Password changed successfully')
            this.passwordForm.resetFields()
          } else {
            this.$message.error(res.msg || 'Change password failed')
          }
        } catch (error) {
          this.$message.error('Change password failed')
        } finally {
          this.changingPassword = false
        }
      })
    },

    getRoleColor (role) {
      const colors = {
        admin: 'red',
        manager: 'orange',
        user: 'blue',
        viewer: 'default'
      }
      return colors[role] || 'default'
    },

    getRoleLabel (role) {
      const labels = {
        admin: this.$t('userManage.roleAdmin') || 'Admin',
        manager: this.$t('userManage.roleManager') || 'Manager',
        user: this.$t('userManage.roleUser') || 'User',
        viewer: this.$t('userManage.roleViewer') || 'Viewer'
      }
      return labels[role] || role
    },

    formatTime (timestamp) {
      if (!timestamp) return ''
      const date = new Date(typeof timestamp === 'number' ? timestamp * 1000 : timestamp)
      return date.toLocaleString()
    }
  }
}
</script>

<style lang="less" scoped>
@primary-color: #1890ff;

.profile-page {
  padding: 24px;
  min-height: calc(100vh - 120px);
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);

  .page-header {
    margin-bottom: 24px;

    .page-title {
      font-size: 24px;
      font-weight: 700;
      margin: 0 0 8px 0;
      color: #1e3a5f;
      display: flex;
      align-items: center;
      gap: 12px;

      .anticon {
        font-size: 28px;
        color: @primary-color;
      }
    }

    .page-desc {
      color: #64748b;
      font-size: 14px;
      margin: 0;
    }
  }

  .profile-card {
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    text-align: center;

    .avatar-section {
      padding: 20px 0;

      .ant-avatar {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      }

      .username {
        margin: 16px 0 8px;
        font-size: 20px;
        font-weight: 600;
        color: #1e3a5f;
      }

      .user-role {
        margin: 0;
      }
    }

    .profile-info {
      text-align: left;

      .info-item {
        display: flex;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #f0f0f0;

        &:last-child {
          border-bottom: none;
        }

        .anticon {
          font-size: 16px;
          color: @primary-color;
          margin-right: 12px;
        }

        .label {
          color: #64748b;
          margin-right: 8px;
        }

        .value {
          color: #1e3a5f;
          font-weight: 500;
        }
      }
    }
  }

  .edit-card {
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);

    .profile-form,
    .password-form {
      max-width: 500px;

      /deep/ .ant-input,
      /deep/ .ant-input-password {
        border-radius: 8px;
      }
    }
  }

  // Dark theme
  &.theme-dark {
    background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);

    .page-header {
      .page-title {
        color: #e0e6ed;
      }
      .page-desc {
        color: #8b949e;
      }
    }

    .profile-card,
    .edit-card {
      background: #1e222d;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);

      /deep/ .ant-card-body {
        background: #1e222d;
      }
    }

    .profile-card {
      .avatar-section {
        .username {
          color: #e0e6ed;
        }
      }

      .profile-info {
        .info-item {
          border-bottom-color: #30363d;

          .label {
            color: #8b949e;
          }

          .value {
            color: #e0e6ed;
          }
        }
      }
    }

    .edit-card {
      /deep/ .ant-tabs-bar {
        border-bottom-color: #30363d;
      }

      /deep/ .ant-tabs-tab {
        color: #8b949e;

        &:hover {
          color: #e0e6ed;
        }
      }

      /deep/ .ant-tabs-tab-active {
        color: @primary-color;
      }

      /deep/ .ant-form-item-label label {
        color: #c9d1d9;
      }

      /deep/ .ant-input,
      /deep/ .ant-input-password {
        background: #0d1117;
        border-color: #30363d;
        color: #c9d1d9;

        &:hover,
        &:focus {
          border-color: @primary-color;
        }
      }
    }
  }
}
</style>
