import React from 'react'
import { Form, Input, Select, Button, Card, message, Space } from 'antd'
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { createCase } from '../api/cases'

const { TextArea } = Input

interface TroubleshootingStep {
  title: string
  description: string
}

const KnowledgeFormPage: React.FC = () => {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [loading, setLoading] = React.useState(false)

  const handleSubmit = async (values: Record<string, any>) => {
    setLoading(true)
    try {
      const payload: Record<string, any> = {
        title: values.title,
        module_id: values.module_id,
        deploy_mode: values.deploy_mode,
        root_cause: values.root_cause || '',
        solution: values.solution || '',
        ticket_id: values.ticket_id || null,
        tags: values.tags
          ? values.tags.split(',').map((t: string) => t.trim()).filter(Boolean)
          : [],
        troubleshooting_path: values.troubleshooting_path
          ? values.troubleshooting_path.map((step: TroubleshootingStep) => ({
              title: step.title || '',
              description: step.description || '',
            }))
          : [],
      }
      await createCase(payload)
      message.success('知识条目创建成功')
      navigate('/knowledge')
    } catch (err) {
      console.error('Failed to create case:', err)
      message.error('创建知识条目失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card title="新建知识条目">
      <Form form={form} layout="vertical" onFinish={handleSubmit}>
        <Form.Item
          name="title"
          label="标题"
          rules={[{ required: true, message: '请输入标题' }]}
        >
          <Input placeholder="请输入知识条目标题" />
        </Form.Item>

        <Form.Item
          name="module_id"
          label="模块"
          rules={[{ required: true, message: '请输入模块' }]}
        >
          <Input placeholder="请输入模块标识（待数据源接入后改为下拉选择）" />
        </Form.Item>

        <Form.Item name="deploy_mode" label="部署模式">
          <Select placeholder="请选择部署模式" allowClear>
            <option value="standalone">单机</option>
            <option value="ha">HA</option>
            <option value="cluster">集群</option>
            <option value="hierarchical">上下级</option>
          </Select>
        </Form.Item>

        <Form.Item name="root_cause" label="根因分析">
          <TextArea rows={4} placeholder="请描述根因分析" />
        </Form.Item>

        <Form.Item name="solution" label="解决方案">
          <TextArea rows={4} placeholder="请描述解决方案" />
        </Form.Item>

        <Form.Item name="tags" label="标签">
          <Input placeholder="多个标签用逗号分隔，如：网络,数据库,配置" />
        </Form.Item>

        <Form.Item name="ticket_id" label="关联工单">
          <Input placeholder="可选，输入工单 UUID" />
        </Form.Item>

        <Form.List name="troubleshooting_path">
          {(fields, { add, remove }) => (
            <>
              <div style={{ marginBottom: 8, fontWeight: 500 }}>排查路径</div>
              {fields.map(({ key, name, ...restField }) => (
                <Space
                  key={key}
                  style={{ display: 'flex', marginBottom: 8 }}
                  align="baseline"
                >
                  <Form.Item
                    {...restField}
                    name={[name, 'title']}
                    style={{ width: 200 }}
                  >
                    <Input placeholder="步骤标题" />
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, 'description']}
                    style={{ width: 300 }}
                  >
                    <Input placeholder="步骤描述" />
                  </Form.Item>
                  <Button
                    type="text"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => remove(name)}
                  />
                </Space>
              ))}
              <Button
                type="dashed"
                onClick={() => add()}
                block
                icon={<PlusOutlined />}
              >
                添加排查步骤
              </Button>
            </>
          )}
        </Form.List>

        <Form.Item style={{ marginTop: 24 }}>
          <Space>
            <Button type="primary" htmlType="submit" loading={loading}>
              提交
            </Button>
            <Button onClick={() => navigate('/knowledge')}>取消</Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  )
}

export default KnowledgeFormPage
