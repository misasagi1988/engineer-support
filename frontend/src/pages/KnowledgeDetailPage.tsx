import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Spin, Card, Tag, Button, Space, Descriptions, Typography, Divider, List } from 'antd'
import { ArrowLeftOutlined, CheckCircleOutlined, ArchiveOutlined, LinkOutlined } from '@ant-design/icons'
import { getCase, reviewCase } from '../api/cases'
import type { Case } from '../types'

const { Title, Paragraph, Text } = Typography

const DEPLOY_MODE_LABELS: Record<string, string> = {
  standalone: '单机',
  HA: 'HA',
  cluster: '集群',
  hierarchy: '上下级',
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

const KnowledgeDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [data, setData] = useState<Case | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    getCase(id)
      .then((res) => setData(res.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false))
  }, [id])

  const handleReview = async (status: string) => {
    if (!id) return
    try {
      await reviewCase(id, status)
      const res = await getCase(id)
      setData(res.data)
    } catch {
      // ignore
    }
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 80 }}>
        <Spin size="large" />
      </div>
    )
  }

  if (!data) {
    return (
      <div style={{ padding: 24 }}>
        <Paragraph>未找到该知识条目</Paragraph>
        <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/knowledge')}>
          返回列表
        </Button>
      </div>
    )
  }

  const troubleshootingSteps = data.troubleshooting_path ?? []
  const user = JSON.parse(localStorage.getItem('user') ?? '{}')

  return (
    <div>
      <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/knowledge')} style={{ marginBottom: 16 }}>
        返回列表
      </Button>

      <Card>
        <Space style={{ marginBottom: 8 }} wrap>
          <Title level={3} style={{ margin: 0 }}>{data.title}</Title>
          <Tag color={STATUS_COLORS[data.review_status] ?? 'default'}>
            {STATUS_LABELS[data.review_status] ?? data.review_status}
          </Tag>
        </Space>

        {data.tags && data.tags.length > 0 && (
          <Space style={{ marginBottom: 16 }} wrap>
            {data.tags.map((t) => <Tag key={t}>{t}</Tag>)}
          </Space>
        )}

        <Descriptions column={2} bordered style={{ marginBottom: 24 }}>
          <Descriptions.Item label="模块">{data.module_id}</Descriptions.Item>
          <Descriptions.Item label="部署模式">
            {data.deploy_mode ? DEPLOY_MODE_LABELS[data.deploy_mode] ?? data.deploy_mode : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="创建时间">{new Date(data.created_at).toLocaleString()}</Descriptions.Item>
          <Descriptions.Item label="更新时间">{new Date(data.updated_at).toLocaleString()}</Descriptions.Item>
          {data.ticket_id && (
            <Descriptions.Item label="关联工单" span={2}>
              <LinkOutlined />{' '}
              <Button type="link" style={{ padding: 0 }} onClick={() => navigate(`/tickets/${data.ticket_id}`)}>
                {data.ticket_id}
              </Button>
            </Descriptions.Item>
          )}
          {data.customer_id && (
            <Descriptions.Item label="客户">{data.customer_id}</Descriptions.Item>
          )}
          {data.confidence_score != null && (
            <Descriptions.Item label="置信度">{(data.confidence_score * 100).toFixed(1)}%</Descriptions.Item>
          )}
        </Descriptions>

        <Divider orientation="left">根因分析</Divider>
        <Paragraph>{data.root_cause || '暂无'}</Paragraph>

        <Divider orientation="left">解决方案</Divider>
        <Paragraph>{data.solution || '暂无'}</Paragraph>

        {troubleshootingSteps.length > 0 && (
          <>
            <Divider orientation="left">排查路径</Divider>
            <List
              dataSource={troubleshootingSteps}
              renderItem={(step, idx) => (
                <List.Item>
                  <List.Item.Meta
                    title={`步骤 ${idx + 1}: ${step.title ?? ''}`}
                    description={step.description ?? ''}
                  />
                </List.Item>
              )}
            />
          </>
        )}

        {user.role === 'admin' && (
          <>
            <Divider orientation="left">审核操作</Divider>
            <Space>
              {data.review_status !== 'reviewed' && (
                <Button
                  type="primary"
                  icon={<CheckCircleOutlined />}
                  onClick={() => handleReview('reviewed')}
                >
                  审核通过
                </Button>
              )}
              {data.review_status !== 'archived' && (
                <Button
                  icon={<ArchiveOutlined />}
                  onClick={() => handleReview('archived')}
                >
                  归档
                </Button>
              )}
            </Space>
          </>
        )}
      </Card>
    </div>
  )
}

export default KnowledgeDetailPage
