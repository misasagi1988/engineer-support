import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Form, Input, Button, Card, message } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'
import { login } from '../api/auth'
import { getMe } from '../api/auth'
import { useAuthStore } from '../store/authStore'

const LoginPage: React.FC = () => {
  const navigate = useNavigate()
  const { login: authLogin } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [form] = Form.useForm()

  const onFinish = async (values: any) => {
    setLoading(true)
    try {
      const result = await login(values.username, values.password)
      console.log('login response:', JSON.stringify(result.data, null, 2))
      const token = result.data?.access_token
      console.log('token:', token ? token.slice(0, 20) + '...' : token)
      if (!token) {
        message.error('登录失败: 未收到token')
        return
      }
      localStorage.setItem('token', token)
      const userResult = await getMe()
      console.log('me response:', JSON.stringify(userResult.data, null, 2))
      authLogin(token, userResult.data)
      message.success('登录成功')
      navigate('/')
    } catch (err: any) {
      console.error('login error:', err)
      message.error('登录失败: ' + (err.response?.data?.detail || err.message))
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()
      await onFinish(values)
    } catch {
      // validation failed
    }
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#f0f2f5' }}>
      <Card title="运维辅助系统" style={{ width: 400 }}>
        <Form form={form} initialValues={{ username: '', password: '' }}>
          <Form.Item name="username" rules={[{ required: true, message: '请输入用户名' }]}>
            <Input prefix={<UserOutlined />} placeholder="用户名" size="large" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: '请输入密码' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="密码" size="large" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" onClick={handleSubmit} loading={loading} block size="large">
              {loading ? '登录中...' : '登录'}
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}

export default LoginPage
