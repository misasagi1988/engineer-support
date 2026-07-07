import React, { useEffect, useState } from 'react'
import { Tabs, Table, Button, Modal, Form, Input, Select, Space, Tag, message } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import * as customers from '../api/customers'
import * as deployments from '../api/deployments'
import * as modules from '../api/modules'
import * as versions from '../api/versions'
import * as paths from '../api/troubleshootingPaths'

const AdminPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('customers')

  const items = [
    { key: 'customers', label: '客户管理', children: <CustomersTab /> },
    { key: 'deployments', label: '部署实例', children: <DeploymentsTab /> },
    { key: 'modules', label: '模块管理', children: <ModulesTab /> },
    { key: 'versions', label: '版本管理', children: <VersionsTab /> },
    { key: 'troubleshooting', label: '排查路径', children: <TroubleshootingTab /> },
    { key: 'users', label: '用户管理', children: <UsersTab /> },
  ]

  return <Tabs activeKey={activeTab} onChange={setActiveTab} items={items} />
}

// ---------- Customers Tab ----------
const CustomersTab: React.FC = () => {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try {
      const res = await customers.listCustomers()
      setData(Array.isArray(res.data) ? res.data : res.data?.data ?? [])
    } catch { /* ignore */ } finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async () => {
    const values = await form.validateFields()
    await customers.createCustomer(values)
    message.success('客户创建成功')
    setModalOpen(false)
    form.resetFields()
    fetchData()
  }

  const columns: ColumnsType<any> = [
    { title: '名称', dataIndex: 'name', key: 'name' },
    {
      title: '合同级别',
      dataIndex: 'contract_level',
      key: 'contract_level',
      render: (v: string) => <Tag color="blue">{v}</Tag>,
    },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  ]

  return (
    <>
      <Button type="primary" onClick={() => setModalOpen(true)} style={{ marginBottom: 16 }}>新增</Button>
      <Table columns={columns} dataSource={data} loading={loading} rowKey="id" />
      <Modal title="新增客户" open={modalOpen} onCancel={() => setModalOpen(false)} onOk={handleSubmit}>
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="客户名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="contract_level" label="合同级别" rules={[{ required: true }]}>
            <Select options={[
              { label: '基础', value: 'basic' },
              { label: '标准', value: 'standard' },
              { label: '高级', value: 'premium' },
            ]} />
          </Form.Item>
          <Form.Item name="contact_info" label="联系方式">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}

// ---------- Deployments Tab ----------
const DeploymentsTab: React.FC = () => {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try {
      const res = await deployments.listDeployments()
      setData(Array.isArray(res.data) ? res.data : res.data?.data ?? [])
    } catch { /* ignore */ } finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async () => {
    const values = await form.validateFields()
    await deployments.createDeployment(values)
    message.success('部署创建成功')
    setModalOpen(false)
    form.resetFields()
    fetchData()
  }

  const columns: ColumnsType<any> = [
    { title: '名称', dataIndex: 'name', key: 'name' },
    { title: '部署模式', dataIndex: 'deploy_mode', key: 'deploy_mode' },
    { title: '环境', dataIndex: 'environment', key: 'environment' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  ]

  return (
    <>
      <Button type="primary" onClick={() => setModalOpen(true)} style={{ marginBottom: 16 }}>新增</Button>
      <Table columns={columns} dataSource={data} loading={loading} rowKey="id" />
      <Modal title="新增部署" open={modalOpen} onCancel={() => setModalOpen(false)} onOk={handleSubmit}>
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="部署名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="deploy_mode" label="部署模式" rules={[{ required: true }]}>
            <Select options={[
              { label: '云部署', value: 'cloud' },
              { label: '本地部署', value: 'on-premise' },
              { label: '混合部署', value: 'hybrid' },
            ]} />
          </Form.Item>
          <Form.Item name="environment" label="环境" rules={[{ required: true }]}>
            <Select options={[
              { label: '开发', value: 'development' },
              { label: '测试', value: 'staging' },
              { label: '生产', value: 'production' },
            ]} />
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}

// ---------- Modules Tab ----------
const ModulesTab: React.FC = () => {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try {
      const res = await modules.listModules()
      setData(Array.isArray(res.data) ? res.data : res.data?.data ?? [])
    } catch { /* ignore */ } finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async () => {
    const values = await form.validateFields()
    await modules.createModule(values)
    message.success('模块创建成功')
    setModalOpen(false)
    form.resetFields()
    fetchData()
  }

  const columns: ColumnsType<any> = [
    { title: '模块名称', dataIndex: 'name', key: 'name' },
    { title: '描述', dataIndex: 'description', key: 'description' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  ]

  return (
    <>
      <Button type="primary" onClick={() => setModalOpen(true)} style={{ marginBottom: 16 }}>新增</Button>
      <Table columns={columns} dataSource={data} loading={loading} rowKey="id" />
      <Modal title="新增模块" open={modalOpen} onCancel={() => setModalOpen(false)} onOk={handleSubmit}>
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="模块名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}

// ---------- Versions Tab ----------
const VersionsTab: React.FC = () => {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try {
      const res = await versions.listVersions()
      setData(Array.isArray(res.data) ? res.data : res.data?.data ?? [])
    } catch { /* ignore */ } finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async () => {
    const values = await form.validateFields()
    await versions.createVersion(values)
    message.success('版本创建成功')
    setModalOpen(false)
    form.resetFields()
    fetchData()
  }

  const columns: ColumnsType<any> = [
    { title: '版本号', dataIndex: 'name', key: 'name' },
    { title: '发布日期', dataIndex: 'release_date', key: 'release_date' },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (v: boolean) => v ? <Tag color="green">活跃</Tag> : <Tag>非活跃</Tag>,
    },
  ]

  return (
    <>
      <Button type="primary" onClick={() => setModalOpen(true)} style={{ marginBottom: 16 }}>新增</Button>
      <Table columns={columns} dataSource={data} loading={loading} rowKey="id" />
      <Modal title="新增版本" open={modalOpen} onCancel={() => setModalOpen(false)} onOk={handleSubmit}>
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="版本号" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="release_date" label="发布日期">
            <Input type="date" />
          </Form.Item>
          <Form.Item name="is_active" label="是否活跃" valuePropName="checked">
            <Select options={[
              { label: '是', value: true },
              { label: '否', value: false },
            ]} />
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}

// ---------- Troubleshooting Paths Tab ----------
const TroubleshootingTab: React.FC = () => {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try {
      const res = await paths.listPaths()
      setData(Array.isArray(res.data) ? res.data : res.data?.data ?? [])
    } catch { /* ignore */ } finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async () => {
    const values = await form.validateFields()
    await paths.createPath(values)
    message.success('排查路径创建成功')
    setModalOpen(false)
    form.resetFields()
    fetchData()
  }

  const columns: ColumnsType<any> = [
    { title: '模块ID', dataIndex: 'module_id', key: 'module_id' },
    { title: '部署模式', dataIndex: 'deploy_mode', key: 'deploy_mode' },
    { title: '版本', dataIndex: 'version', key: 'version' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  ]

  return (
    <>
      <Button type="primary" onClick={() => setModalOpen(true)} style={{ marginBottom: 16 }}>新增</Button>
      <Table columns={columns} dataSource={data} loading={loading} rowKey="id" />
      <Modal title="新增排查路径" open={modalOpen} onCancel={() => setModalOpen(false)} onOk={handleSubmit}>
        <Form form={form} layout="vertical">
          <Form.Item name="module_id" label="模块ID" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="deploy_mode" label="部署模式" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="version" label="版本" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}

// ---------- Users Tab ----------
const UsersTab: React.FC = () => {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try {
      const res = await customers.listCustomers() // reuse until user endpoint exists
      setData([])
    } catch { /* ignore */ } finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const columns: ColumnsType<any> = [
    { title: '用户名', dataIndex: 'username', key: 'username' },
    { title: '邮箱', dataIndex: 'email', key: 'email' },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      render: (v: string, record: any) => (
        <Select
          size="small"
          style={{ width: 120 }}
          value={v}
          options={[
            { label: '管理员', value: 'admin' },
            { label: '运营', value: 'operator' },
            { label: '普通用户', value: 'user' },
          ]}
          onChange={async (value) => {
            // TODO: call user update API
            message.info(`角色已更新为: ${value}`)
          }}
        />
      ),
    },
  ]

  return (
    <>
      <Button type="primary" onClick={() => setModalOpen(true)} style={{ marginBottom: 16 }}>新增</Button>
      <Table columns={columns} dataSource={data} loading={loading} rowKey="id" />
      <Modal title="新增用户" open={modalOpen} onCancel={() => setModalOpen(false)} onOk={() => setModalOpen(false)}>
        <Form form={form} layout="vertical">
          <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="email" label="邮箱" rules={[{ required: true, type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="role" label="角色">
            <Select options={[
              { label: '管理员', value: 'admin' },
              { label: '运营', value: 'operator' },
              { label: '普通用户', value: 'user' },
            ]} />
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}

export default AdminPage
