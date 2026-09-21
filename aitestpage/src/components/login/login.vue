<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="brand-logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 12l2 2 4-4"/>
            <circle cx="12" cy="12" r="10"/>
          </svg>
        </div>
        <h1 class="brand-title">AI Test Platform</h1>
        <p class="brand-subtitle">Sign in to continue</p>
      </div>

      <el-form :model="form" status-icon :rules="rules" ref="form" class="login-form">
        <el-form-item prop="user">
          <label class="input-label">Username</label>
          <el-input
            v-model="form.user"
            placeholder="Enter your username"
            prefix-icon="el-icon-user"
          ></el-input>
        </el-form-item>

        <el-form-item prop="password">
          <label class="input-label">Password</label>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Enter your password"
            prefix-icon="el-icon-lock"
            show-password
            @keyup.enter.native="login"
          ></el-input>
        </el-form-item>

        <el-form-item class="action-buttons">
          <el-button type="primary" class="btn-login" @click="login" :loading="loading">Sign In</el-button>
          <el-button type="primary" class="btn-signup" @click="signUp">Create Account</el-button>
        </el-form-item>
      </el-form>

      <div class="login-footer">
        <span>Secure login with AES encryption</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      loading: false,
      form: {
        user: '',
        password: ''
      },
      rules: {
        user: [
          { required: true, message: 'Please enter username', trigger: 'blur' },
          { min: 3, max: 20, message: 'Length should be 3-20 characters', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9_]+$/, message: 'Only letters, numbers and underscores', trigger: 'blur' }
        ],
        password: [
          { required: true, message: 'Please enter password', trigger: 'blur' },
          { pattern: /^\S{6,15}$/, message: 'Password must be 6-15 non-space characters', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    login () {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true
          var params = {
            user: this.form.user,
            password: this.form.password
          }
          this.axios.post('/api/login', params).then((res) => {
            const data = res.data || res
            if (data.code === 200) {
              if (data.token) {
                localStorage.setItem('token', data.token)
              }
              this.$message({
                message: 'Login successful',
                type: 'success'
              })
              setTimeout(() => {
                window.location.href = window.location.origin + window.location.pathname + '#/home/prd'
              }, 300)
            } else {
              this.$message({
                message: data.msg || 'Login failed, incorrect credentials',
                type: 'warning'
              })
            }
          }).catch((err) => {
            console.error('Login request failed:', err)
            this.$message({
              message: 'Network error, please check connection',
              type: 'error'
            })
          }).finally(() => {
            this.loading = false
          })
        } else {
          this.$message({
            message: 'Please check your input',
            type: 'warning'
          })
        }
      })
    },
    signUp () {
      this.$refs.form.validate((valid) => {
        if (valid) {
          var params = {
            user: this.form.user,
            password: this.form.password
          }
          this.axios.post('/api/signup', params).then((res) => {
            const data = res.data || res
            const code = data.code
            if (code === 200) {
              this.$message({
                message: 'Registration successful, you can now sign in',
                type: 'success'
              })
            } else {
              this.$message({
                message: data.msg || 'Registration failed, please try again',
                type: 'warning'
              })
            }
          }).catch((err) => {
            console.error('Registration request failed:', err)
            this.$message({
              message: 'Network error, please check connection',
              type: 'error'
            })
          })
        } else {
          this.$message({
            message: 'Please check your input format',
            type: 'warning'
          })
        }
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--bg-base);
  background-image:
    radial-gradient(ellipse at 20% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(139, 92, 246, 0.06) 0%, transparent 50%);
}

.login-card {
  width: 400px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-2xl);
  padding: var(--space-10);
  box-shadow: var(--shadow-lg);
}

.login-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.brand-logo {
  width: 52px;
  height: 52px;
  background: var(--gradient-brand);
  border-radius: var(--radius-xl);
  margin: 0 auto var(--space-4);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.brand-title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.brand-subtitle {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin: 0;
}

.login-form {
  width: 100%;
}

.input-label {
  display: block;
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin-bottom: var(--space-2);
  font-weight: var(--font-normal);
}

.action-buttons {
  margin-top: var(--space-6);
  margin-bottom: 0;
}

.btn-login {
  width: 100%;
  height: 40px;
  font-size: var(--text-md);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-3);
}

.btn-signup {
  width: 100%;
  height: 40px;
  font-size: var(--text-md);
  border-radius: var(--radius-lg);
  background-color: transparent !important;
  border-color: var(--border-subtle) !important;
  color: var(--text-secondary) !important;
}

.btn-signup:hover {
  background-color: var(--bg-elevated) !important;
  border-color: var(--color-primary-500) !important;
  color: var(--color-primary-400) !important;
}

.login-footer {
  text-align: center;
  margin-top: var(--space-6);
  padding-top: var(--space-5);
  border-top: 1px solid var(--border-default);
}

.login-footer span {
  font-size: var(--text-xs);
  color: var(--text-disabled);
}
</style>
