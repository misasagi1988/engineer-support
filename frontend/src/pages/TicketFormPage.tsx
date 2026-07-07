import React from 'react'
import { Form, Input, Select, Button, Card, message, Space } from 'antd'
import { useNavigate } from 'react-router-dom'
import { createTicket } from '../api/tickets'

const { TextArea } = Input
const { Option } = Select

const TicketFormPage: React.FC = () => {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [loading, setLoading] = React.useState(false)

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
          <Select placeholder="请选择客户（待接入）" allowClear>
            <Option value="">待接入客户数据</Option>
          </Select>
        </Form.Item>
        <Form.Item name="deployment_id" label="部署">
          <Select placeholder="请选择部署（待接入）" allowClear>
            <Option value="">待接入部署数据</Option>
          </Select>
        </Form.Item>
        <Form.Item name="module_id" label="模块">
          <Select placeholder="请选择模块（待接入）" allowClear>
            <Option value="">待接入模块数据</Option>
          </Select>
        </Form.Item>
        <Form.Item name="version_id" label="版本">
          <Select placeholder="请选择版本（待接入）" allowClear>
            <Option value="">待接入版本数据</Option>
          </Select>
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
            <Option value="P0">P0</Option>
            <Option value="P1">P1</Option>
            <Option value="P2">P2</Option>
            <Option value="P3">P3</Option>
          </Select>
        </Form.Item>
        <Form.Item name="source" label="来源">
          <Select placeholder="请选择来源">
            <Option value="jira">Jira</Option>
            <Option value="wecom">企微</Option>
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
