import React from 'react'
import { Outlet, useNavigate } from 'react-router-dom'
import { Layout, Menu, Avatar, Dropdown, Space } from 'antd'
import {
  DesktopOutlined,
  FileTextOutlined,
  SearchOutlined,
  BookOutlined,
  SettingOutlined,
  LogoutOutlined,
} from '@ant-design/icons'
import { useAuthStore } from '../store/authStore'

const { Header, Content, Sider } = Layout

const LayoutComponent: React.FC = () => {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const userMenu = {
    items: [
      { key: 'logout', icon: <LogoutOutlined />, label: '退出登录' },
    ],
    onClick: handleLogout,
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider breakpoint="lg" collapsible>
        <div style={{ padding: '16px', color: '#fff', fontSize: '16px', fontWeight: 'bold', textAlign: 'center' }}>
          运维辅助系统
        </div>
        <Menu theme="dark" defaultSelectedKeys={['workspace']} mode="inline" onClick={({ key }) => navigate(key)}>
          <Menu.Item key="/" icon={<DesktopOutlined />}>工作台</Menu.Item>
          <Menu.Item key="/tickets" icon={<FileTextOutlined />}>工单管理</Menu.Item>
          <Menu.Item key="/ai-locate" icon={<SearchOutlined />}>智能定位</Menu.Item>
          <Menu.Item key="/knowledge" icon={<BookOutlined />}>知识库</Menu.Item>
          <Menu.Item key="/admin" icon={<SettingOutlined />}>管理后台</Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
          <Dropdown menu={userMenu}>
            <Space>
              <Avatar>{user?.username?.[0]?.toUpperCase()}</Avatar>
              <span>{user?.username}</span>
            </Space>
          </Dropdown>
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}

export default LayoutComponent
