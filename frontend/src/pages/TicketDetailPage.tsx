import React, { useEffect, useState } from 'react'
import { Row, Col, Card, Tag, Descriptions, Button, Input, Checkbox, message, Space } from 'antd'
import { useParams } from 'react-router-dom'
import { getTicket, updateTicketStatus, generateCase } from '../api/tickets'
import type { Ticket } from '../types'

const { TextArea } = Input

const priorityColor: Record<string, string> = {
  P0: 'red',
  P1: 'orange',
  P2: 'blue',
  P3: 'green',
}

const statusLabel: Record<string, string> = {
  pending: '待处理',
  in_progress: '处理中',
  resolved: '已解决',
  closed: '已关闭',
}

const TicketDetailPage: React.FC = () => {
  const { id } = useParams()
  
  const [ticket, setTicket] = useState<Ticket | null>(null)
  const [loading, setLoading] = useState(false)
  const [solution, setSolution] = useState('')
  const [updating, setUpdating] = useState(false)

  useEffect(() => {
    if (!id) return
    const fetchTicket = async () => {
      setLoading(true)
      try {
        const { data } = await getTicket(id)
        setTicket(data)
        setSolution(data.solution || '')
      } catch (err) {
        console.error('Failed to fetch ticket:', err)
        message.error('获取工单详情失败')
      } finally {
        setLoading(false)
      }
    }
    fetchTicket()
  }, [id])

  const handleStatusUpdate = async (status: string) => {
    if (!id) return
    setUpdating(true)
    try {
      await updateTicketStatus(id, status)
      message.success(`状态已更新为: ${statusLabel[status] || status}`)
      const { data } = await getTicket(id)
      setTicket(data)
    } catch (err) {
      console.error('Failed to update status:', err)
      message.error('更新状态失败')
    } finally {
      setUpdating(false)
    }
  }

  const handleGenerateCase = async () => {
    if (!id) return
    setUpdating(true)
    try {
      await generateCase(id)
      message.success('案例生成成功')
    } catch (err) {
      console.error('Failed to generate case:', err)
      message.error('案例生成失败')
    } finally {
      setUpdating(false)
    }
  }

  if (loading || !ticket) {
    return <div style={{ padding: 24 }}>加载中...</div>
  }

  return (
    <Row gutter={[16, 16]}>
      <Col span={12}>
        <Card title={ticket.title} loading={loading}>
          <Descriptions column={1} bordered size="small">
            <Descriptions.Item label="描述">{ticket.description || '—'}</Descriptions.Item>
            <Descriptions.Item label="客户">{ticket.customer_id || '—'}</Descriptions.Item>
            <Descriptions.Item label="模块">{ticket.module_id || '—'}</Descriptions.Item>
            <Descriptions.Item label="版本">{ticket.version_id || '—'}</Descriptions.Item>
            <Descriptions.Item label="部署模式">{ticket.deploy_mode || '—'}</Descriptions.Item>
            <Descriptions.Item label="优先级">
              <Tag color={priorityColor[ticket.priority]}>{ticket.priority}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="状态">
              <Tag>{statusLabel[ticket.status] || ticket.status}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="创建时间">
              {new Date(ticket.created_at).toLocaleString('zh-CN')}
            </Descriptions.Item>
            <Descriptions.Item label="来源">{ticket.source || '—'}</Descriptions.Item>
          </Descriptions>
        </Card>
      </Col>

      <Col span={12}>
        <Card title="故障排查清单" style={{ marginBottom: 16 }}>
          <Checkbox.Group style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <Checkbox value="1">确认问题可复现</Checkbox>
            <Checkbox value="2">检查日志异常</Checkbox>
            <Checkbox value="3">确认部署模式配置</Checkbox>
            <Checkbox value="4">核对版本兼容性</Checkbox>
            <Checkbox value="5">定位问题模块</Checkbox>
          </Checkbox.Group>
        </Card>

        <Card title="解决方案" style={{ marginBottom: 16 }}>
          <TextArea
            rows={6}
            value={solution}
            onChange={(e) => setSolution(e.target.value)}
            placeholder="请输入解决方案..."
          />
        </Card>

        <Card title="状态操作" style={{ marginBottom: 16 }}>
          <Space wrap>
            <Button
              type="primary"
              onClick={() => handleStatusUpdate('in_progress')}
              loading={updating}
              disabled={ticket.status === 'in_progress'}
            >
              处理中
            </Button>
            <Button
              onClick={() => handleStatusUpdate('resolved')}
              loading={updating}
              disabled={ticket.status === 'resolved'}
            >
              已解决
            </Button>
            <Button
              danger
              onClick={() => handleStatusUpdate('closed')}
              loading={updating}
              disabled={ticket.status === 'closed'}
            >
              已关闭
            </Button>
          </Space>
        </Card>

        <Card title="附件" style={{ marginBottom: 16 }}>
          <p style={{ color: '#999' }}>附件功能待接入</p>
        </Card>

        <Button type="default" onClick={handleGenerateCase} loading={updating}>
          生成案例
        </Button>
      </Col>
    </Row>
  )
}

export default TicketDetailPage
