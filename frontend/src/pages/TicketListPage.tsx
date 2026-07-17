import React, { useEffect, useState } from 'react'
import { Table, Tag, Select, Button, Space, Input } from 'antd'
import { PlusOutlined, SearchOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { listTickets } from '../api/tickets'
import type { Ticket } from '../types'

const { Option } = Select

const priorityColor: Record<string, string> = {
  p0: 'red',
  p1: 'orange',
  p2: 'blue',
  p3: 'green',
}

const statusLabel: Record<string, string> = {
  pending: '待处理',
  processing: '处理中',
  resolved: '已解决',
  closed: '已关闭',
}

const TicketListPage: React.FC = () => {
  const navigate = useNavigate()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(false)
  const [statusFilter, setStatusFilter] = useState<string | undefined>()
  const [priorityFilter, setPriorityFilter] = useState<string | undefined>()
  const [searchText, setSearchText] = useState('')

  const fetchTickets = async () => {
    setLoading(true)
    try {
      const params: Record<string, any> = {}
      if (statusFilter) params.status = statusFilter
      if (priorityFilter) params.priority = priorityFilter
      if (searchText) params.q = searchText
      const { data } = await listTickets(params)
      setTickets(data)
    } catch (err) {
      console.error('Failed to fetch tickets:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTickets()
  }, [statusFilter, priorityFilter, searchText])

  useEffect(() => {
    const timer = setInterval(fetchTickets, 30000)
    return () => clearInterval(timer)
  }, [statusFilter, priorityFilter, searchText])

  const columns = [
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      width: 80,
      render: (p: string) => (
        <Tag color={priorityColor[p] || 'default'}>{p}</Tag>
      ),
    },
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (s: string) => <Tag>{statusLabel[s] || s}</Tag>,
    },
    {
      title: '模块',
      key: 'module',
      width: 120,
      render: (_: unknown, record: Ticket) => (
        <span>{record.module_id || '—'}</span>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (v: string) => new Date(v).toLocaleString('zh-CN'),
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Space>
          <Input
            placeholder="搜索工单..."
            prefix={<SearchOutlined />}
            style={{ width: 200 }}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            allowClear
          />
          <Select
            placeholder="状态"
            style={{ width: 120 }}
            allowClear
            value={statusFilter}
            onChange={setStatusFilter}
          >
            <Option value="pending">待处理</Option>
            <Option value="processing">处理中</Option>
            <Option value="resolved">已解决</Option>
            <Option value="closed">已关闭</Option>
          </Select>
          <Select
            placeholder="优先级"
            style={{ width: 100 }}
            allowClear
            value={priorityFilter}
            onChange={setPriorityFilter}
          >
            <Option value="p0">P0</Option>
            <Option value="p1">P1</Option>
            <Option value="p2">P2</Option>
            <Option value="p3">P3</Option>
          </Select>
        </Space>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/tickets/new')}>
          新建工单
        </Button>
      </div>
      <Table
        columns={columns}
        dataSource={tickets}
        rowKey="id"
        loading={loading}
        onRow={(record) => ({
          onClick: () => navigate(`/tickets/${record.id}`),
          style: { cursor: 'pointer' },
        })}
      />
    </div>
  )
}

export default TicketListPage
