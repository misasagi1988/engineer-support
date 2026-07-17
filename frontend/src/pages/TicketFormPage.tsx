import React, { useEffect, useState } from 'react'
import { Form, Input, Select, Button, Card, message, Space } from 'antd'
import { useNavigate } from 'react-router-dom'
import { createTicket } from '../api/tickets'
import { listCustomers } from '../api/customers'
import { listModules } from '../api/modules'
import { listVersions } from '../api/versions'
import type { Customer, Module, Version } from '../types'

const { TextArea } = Input
const { Option } = Select

const TicketFormPage: React.FC = () => {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [loading, setLoading] = React.useState(false)
  const [customers, setCustomers] = useState<Customer[]>([])
  const [modules, setModules] = useState<Module[]>([])
  const [versions, setVersions] = useState<Version[]>([])

  useEffect(() => {
    listCustomers().then(r => setCustomers(Array.isArray(r.data) ? r.data : [])).catch(() => {})
    listModules().then(r => setModules(Array.isArray(r.data) ? r.data : [])).catch(() => {})
    listVersions().then(r => setVersions(Array.isArray(r.data) ? r.data : [])).catch(() => {})
  }, [])

  const handleSubmit = async (values: Record<string, any>) => {
    setLoading(true)
    try {
      await createTicket(values)
      message.success('工单创建成功')
      navigate('/tickets')
    } catch (err) {
      console.error('Failed to create ticket:', err)
      message.error('创建工单失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card title="新建工单">
      <Form form={form} layout="vertical" onFinish={handleSubmit}>
        <Form.Item name="title" label="标题" rules={[{ required: true, message: '请输入标题' }]}>
          <Input placeholder="请输入工单标题" />
        </Form.Item>
        <Form.Item name="description" label="描述" rules={[{ required: true, message: '请输入描述' }]}>
          <TextArea rows={4} placeholder="请详细描述问题" />
        </Form.Item>
        <Form.Item name="customer_id" label="客户">
          <Select placeholder="请选择客户" allowClear showSearch optionFilterProp="label"
            options={customers.map(c => ({ label: c.name, value: c.id }))}
          />
        </Form.Item>
        <Form.Item name="deployment_id" label="部署">
          <Select placeholder="请先选择客户后选择部署" allowClear disabled>
            <Option value="">请先选择客户</Option>
          </Select>
        </Form.Item>
        <Form.Item name="module_id" label="模块">
          <Select placeholder="请选择模块" allowClear showSearch optionFilterProp="label"
            options={modules.map(m => ({ label: m.name, value: m.id }))}
          />
        </Form.Item>
        <Form.Item name="version_id" label="版本">
          <Select placeholder="请选择版本" allowClear
            options={versions.filter(v => v.is_active).map(v => ({ label: v.name, value: v.id }))}
          />
        </Form.Item>
        <Form.Item name="deploy_mode" label="部署模式">
          <Select placeholder="请选择部署模式">
            <Option value="standalone">单机</Option>
            <Option value="ha">HA</Option>
            <Option value="cluster">集群</Option>
            <Option value="hierarchical">上下级</Option>
          </Select>
        </Form.Item>
        <Form.Item name="priority" label="优先级" rules={[{ required: true, message: '请选择优先级' }]}>
          <Select placeholder="请选择优先级">
            <Option value="p0">P0</Option>
            <Option value="p1">P1</Option>
            <Option value="p2">P2</Option>
            <Option value="p3">P3</Option>
          </Select>
        </Form.Item>
        <Form.Item name="source" label="来源">
          <Select placeholder="请选择来源">
            <Option value="jira">Jira</Option>
            <Option value="wechat">企微</Option>
            <Option value="manual">手动</Option>
          </Select>
        </Form.Item>
        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" loading={loading}>
              提交
            </Button>
            <Button onClick={() => navigate('/tickets')}>取消</Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  )
}

export default TicketFormPage
