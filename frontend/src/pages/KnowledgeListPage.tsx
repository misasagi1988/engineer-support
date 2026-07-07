import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Tag, Table, Input, Select, Space, Spin, Typography } from 'antd'
import { SearchOutlined } from '@ant-design/icons'
import { listCases } from '../api/cases'
import type { Case } from '../types'
import type { ColumnsType } from 'antd/es/table'

const { Title } = Typography

const DEPLOY_MODE_LABELS: Record<string, string> = {
  standalone: '单机',
  HA: 'HA',
  cluster: '集群',
  'hierarchy': '上下级',
}

const STATUS_COLORS: Record<string, string> = {
  draft: 'orange',
  reviewed: 'green',
  archived: 'blue',
}

const STATUS_LABELS: Record<string, string> = {
  draft: '草稿',
  reviewed: '已审核',
  archived: '已归档',
}

const KnowledgeListPage: React.FC = () => {
  const navigate = useNavigate()
  const [data, setData] = useState<Case[]>([])
  const [loading, setLoading] = useState(false)
  const [searchText, setSearchText] = useState('')
  const [filterModule, setFilterModule] = useState<string | undefined>(undefined)
  const [filterDeployMode, setFilterDeployMode] = useState<string | undefined>(undefined)
  const [filterStatus, setFilterStatus] = useState<string | undefined>(undefined)

  useEffect(() => {
    setLoading(true)
    const params: Record<string, any> = {}
    if (filterModule) params.module_id = filterModule
    if (filterDeployMode) params.deploy_mode = filterDeployMode
    if (filterStatus) params.review_status = filterStatus
    listCases(params)
      .then((res) => setData(res.data))
      .catch(() => setData([]))
      .finally(() => setLoading(false))
  }, [filterModule, filterDeployMode, filterStatus])

  const uniqueModules = Array.from(new Set(data.map((c) => c.module_id).filter(Boolean)))
  const uniqueDeployModes = Array.from(new Set(data.map((c) => c.deploy_mode).filter(Boolean)))

  const columns: ColumnsType<Case> = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
    },
    {
      title: '模块',
      dataIndex: 'module_id',
      key: 'module_id',
      width: 120,
      render: (v: string) => <span>{v || '-'}</span>,
    },
    {
      title: '部署模式',
      dataIndex: 'deploy_mode',
      key: 'deploy_mode',
      width: 100,
      render: (v: string) => (v ? <Tag>{DEPLOY_MODE_LABELS[v] ?? v}</Tag> : '-'),
    },
    {
      title: '标签',
      dataIndex: 'tags',
      key: 'tags',
      width: 180,
      render: (tags: string[]) => (
        <Space wrap>
          {(tags ?? []).map((t) => (
            <Tag key={t}>{t}</Tag>
          ))}
        </Space>
      ),
    },
    {
      title: '审核状态',
      dataIndex: 'review_status',
      key: 'review_status',
      width: 120,
      render: (v: string) => (
        <Tag color={STATUS_COLORS[v] ?? 'default'}>{STATUS_LABELS[v] ?? v}</Tag>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (v: string) => new Date(v).toLocaleString(),
    },
  ]

  return (
    <div>
      <Title level={4}>知识库</Title>

      <Space style={{ marginBottom: 16 }} wrap>
        <Input
          placeholder="搜索标题或内容..."
          prefix={<SearchOutlined />}
          style={{ width: 260 }}
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        />
        <Select
          allowClear
          placeholder="模块"
          style={{ width: 160 }}
          value={filterModule}
          onChange={setFilterModule}
          options={uniqueModules.map((m) => ({ label: m, value: m }))}
        />
        <Select
          allowClear
          placeholder="部署模式"
          style={{ width: 140 }}
          value={filterDeployMode}
          onChange={setFilterDeployMode}
          options={uniqueDeployModes.map((m) => ({ label: DEPLOY_MODE_LABELS[m] ?? m, value: m }))}
        />
        <Select
          allowClear
          placeholder="审核状态"
          style={{ width: 140 }}
          value={filterStatus}
          onChange={setFilterStatus}
          options={Object.entries(STATUS_LABELS).map(([k, v]) => ({ label: v, value: k }))}
        />
      </Space>

      <Spin spinning={loading}>
        <Table<Case>
          columns={columns}
          dataSource={data.filter((c) =>
            !searchText || c.title.toLowerCase().includes(searchText.toLowerCase())
          )}
          rowKey="id"
          onRow={(record) => ({
            onClick: () => navigate(`/knowledge/${record.id}`),
            style: { cursor: 'pointer' },
          })}
          pagination={{ pageSize: 15 }}
        />
      </Spin>
    </div>
  )
}

export default KnowledgeListPage
