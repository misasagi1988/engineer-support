import React, { useState } from 'react'
import { Card, Input, Button, Select, List, Tag, Checkbox, message, Row, Col, Divider } from 'antd'
import { SearchOutlined } from '@ant-design/icons'
import { locate } from '../api/ai'
import type { AILocateResult } from '../types'

const { TextArea } = Input

const AILocatePage: React.FC = () => {
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AILocateResult | null>(null)
  const [checkedSteps, setCheckedSteps] = useState<string[]>([])

  const handleLocate = async () => {
    if (!description.trim()) { message.warning('请输入问题描述'); return }
    setLoading(true)
    try {
      const { data } = await locate(description)
      setResult(data)
      setCheckedSteps([])
    } catch {
      message.error('定位失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const deployModeLabel: Record<string, string> = {
    standalone: '单机', ha: 'HA', cluster: '集群', hierarchical: '上下级',
  }

  return (
    <div>
      <h2>智能定位</h2>
      {/* Section 1: Input */}
      <Card title="输入问题描述" style={{ marginBottom: 16 }}>
        <TextArea rows={4} value={description} onChange={e => setDescription(e.target.value)} placeholder="请描述客户遇到的问题..." />
        <div style={{ marginTop: 12 }}>
          <Button type="primary" icon={<SearchOutlined />} loading={loading} onClick={handleLocate}>
            开始定位
          </Button>
        </div>
      </Card>

      {result && (
        <>
          {/* Section 2: Results */}
          <Card title="识别结果" style={{ marginBottom: 16 }}>
            <Row gutter={16}>
              <Col span={8}>
                <strong>识别模块:</strong>{' '}
                {result.module_candidates[0]?.module || '未识别'}
              </Col>
              <Col span={8}>
                <strong>识别版本:</strong>{' '}
                {result.version_candidates[0]?.version || '未识别'}
              </Col>
              <Col span={8}>
                <strong>部署模式:</strong>{' '}
                {result.deploy_mode_hints ? deployModeLabel[result.deploy_mode_hints] || result.deploy_mode_hints : '未识别'}
              </Col>
            </Row>
            {result.root_cause_candidates.length > 0 && (
              <div style={{ marginTop: 12 }}>
                <strong>根因候选:</strong>
                <List
                  size="small"
                  dataSource={result.root_cause_candidates}
                  renderItem={(item, idx) => (
                    <List.Item>
                      <Tag color="blue">#{idx + 1}</Tag> {item.description}
                    </List.Item>
                  )}
                />
              </div>
            )}
          </Card>

          {/* Section 3: Recommendations */}
          <Card title="推荐方案" style={{ marginBottom: 16 }}>
            {result.similar_cases.length > 0 ? (
              <List
                size="small"
                dataSource={result.similar_cases}
                renderItem={item => (
                  <List.Item>
                    <List.Item.Meta
                      title={
                        <>
                          {item.title}{' '}
                          {item.deploy_mode && <Tag>{deployModeLabel[item.deploy_mode] || item.deploy_mode}</Tag>}
                          <Tag color="green">{Math.round(item.confidence_score * 100)}%</Tag>
                        </>
                      }
                      description={item.root_cause}
                    />
                  </List.Item>
                )}
              />
            ) : (
              <p style={{ color: '#999' }}>暂无匹配案例，请在知识库中手动搜索</p>
            )}
          </Card>

          {/* Troubleshooting Path */}
          <Card title="排查路径">
            {result.troubleshooting_path.length > 0 ? (
              <Checkbox.Group value={checkedSteps} onChange={v => setCheckedSteps(v as string[])}>
                <List
                  size="small"
                  dataSource={result.troubleshooting_path}
                  renderItem={step => (
                    <List.Item>
                      <Checkbox value={step.title}>{step.title}: {step.description}</Checkbox>
                    </List.Item>
                  )}
                />
              </Checkbox.Group>
            ) : (
              <p style={{ color: '#999' }}>暂无排查路径</p>
            )}
          </Card>
        </>
      )}
    </div>
  )
}

export default AILocatePage
