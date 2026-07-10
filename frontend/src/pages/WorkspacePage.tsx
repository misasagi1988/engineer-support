import React, { useEffect, useState } from 'react'
import { Row, Col, Card, Statistic, List, Tag, Button } from 'antd'
import { useNavigate } from 'react-router-dom'
import { getDashboardStats } from '../api/stats'
import { listTickets } from '../api/tickets'

const priorityColor: Record<string, string> = { p0: 'red', p1: 'orange', p2: 'blue', p3: 'green' }

const WorkspacePage: React.FC = () => {
  const navigate = useNavigate()
  const [stats, setStats] = useState<Record<string, number> | null>(null)
  const [todos, setTodos] = useState<any[]>([])

  useEffect(() => {
    getDashboardStats().then(r => setStats(r.data)).catch(() => {})
    listTickets({ status: 'pending', limit: 5 }).then(r => setTodos(r.data)).catch(() => {})
  }, [])

  return (
    <div>
      <h2>工作台</h2>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}><Card><Statistic title="待处理" value={stats?.pending ?? 0} /></Card></Col>
        <Col span={6}><Card><Statistic title="处理中" value={stats?.processing ?? 0} /></Card></Col>
        <Col span={6}><Card><Statistic title="已解决" value={stats?.resolved ?? 0} /></Card></Col>
        <Col span={6}><Card><Statistic title="总计" value={stats?.total ?? 0} /></Card></Col>
      </Row>
      <Card title="我的待办" extra={<Button type="link" onClick={() => navigate('/tickets')}>查看全部</Button>}>
        <List
          size="small"
          dataSource={todos}
          renderItem={(item: any) => (
            <List.Item onClick={() => navigate(`/tickets/${item.id}`)} style={{ cursor: 'pointer' }}>
              <List.Item.Meta
                title={<><Tag color={priorityColor[item.priority]}>{item.priority?.toUpperCase()}</Tag> {item.title}</>}
                description={item.created_at?.slice(0, 10)}
              />
            </List.Item>
          )}
        />
      </Card>
      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={8}><Card hoverable onClick={() => navigate('/tickets/new')}>📝 新建工单</Card></Col>
        <Col span={8}><Card hoverable onClick={() => navigate('/ai-locate')}>🔍 智能定位</Card></Col>
        <Col span={8}><Card hoverable onClick={() => navigate('/knowledge')}>📚 知识库</Card></Col>
      </Row>
    </div>
  )
}

export default WorkspacePage
