<template>
  <div class="user-manage-page" :class="{ 'theme-dark': isDarkTheme }">
    <div class="page-header">
      <h2 class="page-title">
        <a-icon type="team" />
        <span>{{ $t('userManage.title') || 'User Management' }}</span>
      </h2>
      <p class="page-desc">{{ $t('userManage.description') || 'Manage system users, roles and permissions' }}</p>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <a-button type="primary" @click="showCreateModal">
        <a-icon type="user-add" />
        {{ $t('userManage.createUser') || 'Create User' }}
      </a-button>
      <a-button @click="loadUsers">
        <a-icon type="reload" />
        {{ $t('common.refresh') || 'Refresh' }}
      </a-button>
    </div>

    <!-- User Table -->
    <a-card :bordered="false" class="user-table-card">
      <a-table
        :columns="columns"
        :dataSource="users"
        :loading="loading"
        :pagination="pagination"
        :rowKey="record => record.id"
        @change="handleTableChange"
      >
        <!-- Status Column -->
        <template slot="status" slot-scope="text">
          <a-tag :color="text === 'active' ? 'green' : 'red'">
            {{ text === 'active' ? ($t('userManage.active') || 'Active') : ($t('userManage.disabled') || 'Disabled') }}
          </a-tag>
        </template>

        <!-- Role Column -->
        <template slot="role" slot-scope="text">
          <a-tag :color="getRoleColor(text)">
            {{ getRoleLabel(text) }}
          </a-tag>
        </template>

        <!-- Last Login Column -->
        <template slot="last_login_at" slot-scope="text">
          <span v-if="text">{{ formatTime(text) }}</span>
          <span v-else class="text-muted">{{ $t('userManage.neverLogin') || 'Never' }}</span>
        </template>

        <!-- Actions Column -->
        <template slot="action" slot-scope="text, record">
          <a-space>
            <a-tooltip :title="$t('common.edit') || 'Edit'">
              <a-button type="link" size="small" @click="showEditModal(record)">
                <a-icon type="edit" />
              </a-button>
            </a-tooltip>
            <a-tooltip :title="$t('userManage.resetPassword') || 'Reset Password'">
              <a-button type="link" size="small" @click="showResetPasswordModal(record)">
                <a-icon type="key" />
              </a-button>
            </a-tooltip>
            <a-tooltip :title="$t('common.delete') || 'Delete'">
              <a-popconfirm
                :title="$t('userManage.confirmDelete') || 'Are you sure to delete this user?'"
                @confirm="handleDelete(record.id)"
              >
                <a-button type="link" size="small" :disabled="record.id === currentUserId">
                  <a-icon type="delete" style="color: #ff4d4f" />
                </a-button>
              </a-popconfirm>
            </a-tooltip>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- Create/Edit User Modal -->
    <a-modal
      v-model="modalVisible"
      :title="isEdit ? ($t('userManage.editUser') || 'Edit User') : ($t('userManage.createUser') || 'Create User')"
      :confirmLoading="modalLoading"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
    >
      <a-form :form="form" layout="vertical">
        <a-form-item :label="$t('userManage.username') || 'Username'">
          <a-input
            v-decorator="['username', {
              rules: [{ required: !isEdit, message: $t('userManage.usernameRequired') || 'Please enter username' }]
            }]"
            :disabled="isEdit"
            :placeholder="$t('userManage.usernamePlaceholder') || 'Enter username'"
          >
            <a-icon slot="prefix" type="user" />
          </a-input>
        </a-form-item>

        <a-form-item v-if="!isEdit" :label="$t('userManage.password') || 'Password'">
          <a-input-password
            v-decorator="['password', {
              rules: [
                { required: true, message: $t('userManage.passwordRequired') || 'Please enter password' },
                { min: 6, message: $t('userManage.passwordMin') || 'Password must be at least 6 characters' }
              ]
            }]"
            :placeholder="$t('userManage.passwordPlaceholder') || 'Enter password (min 6 characters)'"
          >
            <a-icon slot="prefix" type="lock" />
          </a-input-password>
        </a-form-item>

        <a-form-item :label="$t('userManage.nickname') || 'Nickname'">
          <a-input
            v-decorator="['nickname']"
            :placeholder="$t('userManage.nicknamePlaceholder') || 'Enter nickname'"
          >
            <a-icon slot="prefix" type="smile" />
          </a-input>
        </a-form-item>

        <a-form-item :label="$t('userManage.email') || 'Email'">
          <a-input
            v-decorator="['email', {
              rules: [{ type: 'email', message: $t('userManage.emailInvalid') || 'Invalid email format' }]
            }]"
            :placeholder="$t('userManage.emailPlaceholder') || 'Enter email'"
          >
            <a-icon slot="prefix" type="mail" />
          </a-input>
        </a-form-item>

        <a-form-item :label="$t('userManage.role') || 'Role'">
          <a-select
            v-decorator="['role', { initialValue: 'user' }]"
            :placeholder="$t('userManage.rolePlaceholder') || 'Select role'"
          >
            <a-select-option v-for="role in roles" :key="role.id" :value="role.id">
              {{ getRoleLabel(role.id) }}
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item v-if="isEdit" :label="$t('userManage.status') || 'Status'">
          <a-select
            v-decorator="['status', { initialValue: 'active' }]"
            :placeholder="$t('userManage.statusPlaceholder') || 'Select status'"
          >
            <a-select-option value="active">{{ $t('userManage.active') || 'Active' }}</a-select-option>
            <a-select-option value="disabled">{{ $t('userManage.disabled') || 'Disabled' }}</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- Reset Password Modal -->
    <a-modal
      v-model="resetPasswordVisible"
      :title="$t('userManage.resetPassword') || 'Reset Password'"
      :confirmLoading="resetPasswordLoading"
      @ok="handleResetPassword"
    >
      <a-form :form="resetPasswordForm" layout="vertical">
        <a-alert
          :message="$t('userManage.resetPasswordWarning') || 'This will reset the user\'s password'"
          type="warning"
          showIcon
          style="margin-bottom: 16px"
        />
        <a-form-item :label="$t('userManage.newPassword') || 'New Password'">
          <a-input-password
            v-decorator="['new_password', {
              rules: [
                { required: true, message: $t('userManage.passwordRequired') || 'Please enter new password' },
                { min: 6, message: $t('userManage.passwordMin') || 'Password must be at least 6 characters' }
              ]
            }]"
            :placeholder="$t('userManage.newPasswordPlaceholder') || 'Enter new password'"
          >
            <a-icon slot="prefix" type="lock" />
          </a-input-password>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import { getUserList, createUser, updateUser, deleteUser, resetUserPassword, getRoles } from '@/api/user'
import { baseMixin } from '@/store/app-mixin'
import { mapGetters } from 'vuex'

export default {
  name: 'UserManage',
  mixins: [baseMixin],
  data () {
    return {
      loading: false,
      users: [],
      roles: [],
      pagination: {
        current: 1,
        pageSize: 10,
        total: 0
      },
      // Create/Edit Modal
      modalVisible: false,
      modalLoading: false,
      isEdit: false,
      editingUser: null,
      // Reset Password Modal
      resetPasswordVisible: false,
      resetPasswordLoading: false,
      resetPasswordUserId: null
    }
  },
  computed: {
    ...mapGetters(['userInfo']),
    isDarkTheme () {
      return this.navTheme === 'dark' || this.navTheme === 'realdark'
    },
    currentUserId () {
      return this.userInfo?.id
    },
    columns () {
      return [
        {
          title: 'ID',
          dataIndex: 'id',
          width: 60
        },
        {
          title: this.$t('userManage.username') || 'Username',
          dataIndex: 'username',
          width: 120
        },
        {
          title: this.$t('userManage.nickname') || 'Nickname',
          dataIndex: 'nickname',
          width: 120
        },
        {
          title: this.$t('userManage.email') || 'Email',
          dataIndex: 'email',
          width: 180
        },
        {
          title: this.$t('userManage.role') || 'Role',
          dataIndex: 'role',
          width: 100,
          scopedSlots: { customRender: 'role' }
        },
        {
          title: this.$t('userManage.status') || 'Status',
          dataIndex: 'status',
          width: 100,
          scopedSlots: { customRender: 'status' }
        },
        {
          title: this.$t('userManage.lastLogin') || 'Last Login',
          dataIndex: 'last_login_at',
          width: 160,
          scopedSlots: { customRender: 'last_login_at' }
        },
        {
          title: this.$t('common.actions') || 'Actions',
          dataIndex: 'action',
          width: 150,
          scopedSlots: { customRender: 'action' }
        }
      ]
    }
  },
  beforeCreate () {
    this.form = this.$form.createForm(this)
    this.resetPasswordForm = this.$form.createForm(this, { name: 'resetPassword' })
  },
  mounted () {
    this.loadUsers()
    this.loadRoles()
  },
  methods: {
    async loadUsers () {
      this.loading = true
      try {
        const res = await getUserList({
          page: this.pagination.current,
          page_size: this.pagination.pageSize
        })
        if (res.code === 1) {
          this.users = res.data.items || []
          this.pagination.total = res.data.total || 0
        } else {
          this.$message.error(res.msg || 'Failed to load users')
        }
      } catch (error) {
        this.$message.error('Failed to load users')
      } finally {
        this.loading = false
      }
    },

    async loadRoles () {
      try {
        const res = await getRoles()
        if (res.code === 1) {
          this.roles = res.data.roles || []
        }
      } catch (error) {
        console.error('Failed to load roles:', error)
      }
    },

    handleTableChange (pagination) {
      this.pagination.current = pagination.current
      this.pagination.pageSize = pagination.pageSize
      this.loadUsers()
    },

    showCreateModal () {
      this.isEdit = false
      this.editingUser = null
      this.modalVisible = true
      this.$nextTick(() => {
        this.form.resetFields()
      })
    },

    showEditModal (record) {
      this.isEdit = true
      this.editingUser = record
      this.modalVisible = true
      this.$nextTick(() => {
        this.form.setFieldsValue({
          username: record.username,
          nickname: record.nickname,
          email: record.email,
          role: record.role,
          status: record.status
        })
      })
    },

    handleModalCancel () {
      this.modalVisible = false
      this.form.resetFields()
    },

    handleModalOk () {
      this.form.validateFields(async (err, values) => {
        if (err) return

        this.modalLoading = true
        try {
          let res
          if (this.isEdit) {
            res = await updateUser(this.editingUser.id, {
              nickname: values.nickname,
              email: values.email,
              role: values.role,
              status: values.status
            })
          } else {
            res = await createUser(values)
          }

          if (res.code === 1) {
            this.$message.success(res.msg || 'Success')
            this.modalVisible = false
            this.form.resetFields()
            this.loadUsers()
          } else {
            this.$message.error(res.msg || 'Operation failed')
          }
        } catch (error) {
          this.$message.error('Operation failed')
        } finally {
          this.modalLoading = false
        }
      })
    },

    async handleDelete (id) {
      try {
        const res = await deleteUser(id)
        if (res.code === 1) {
          this.$message.success(res.msg || 'User deleted')
          this.loadUsers()
        } else {
          this.$message.error(res.msg || 'Delete failed')
        }
      } catch (error) {
        this.$message.error('Delete failed')
      }
    },

    showResetPasswordModal (record) {
      this.resetPasswordUserId = record.id
      this.resetPasswordVisible = true
      this.$nextTick(() => {
        this.resetPasswordForm.resetFields()
      })
    },

    handleResetPassword () {
      this.resetPasswordForm.validateFields(async (err, values) => {
        if (err) return

        this.resetPasswordLoading = true
        try {
          const res = await resetUserPassword({
            user_id: this.resetPasswordUserId,
            new_password: values.new_password
          })
          if (res.code === 1) {
            this.$message.success(res.msg || 'Password reset successfully')
            this.resetPasswordVisible = false
            this.resetPasswordForm.resetFields()
          } else {
            this.$message.error(res.msg || 'Reset failed')
          }
        } catch (error) {
          this.$message.error('Reset failed')
        } finally {
          this.resetPasswordLoading = false
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

.user-manage-page {
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

  .toolbar {
    margin-bottom: 16px;
    display: flex;
    gap: 12px;
  }

  .user-table-card {
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);

    .text-muted {
      color: #94a3b8;
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

    .user-table-card {
      background: #1e222d;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);

      /deep/ .ant-card-body {
        background: #1e222d;
      }

      /deep/ .ant-table {
        background: #1e222d;
        color: #c9d1d9;

        .ant-table-thead > tr > th {
          background: #252a36;
          color: #e0e6ed;
          border-bottom-color: #30363d;
        }

        .ant-table-tbody > tr > td {
          border-bottom-color: #30363d;
        }

        .ant-table-tbody > tr:hover > td {
          background: #252a36;
        }
      }

      .text-muted {
        color: #6e7681;
      }
    }
  }
}
</style>
