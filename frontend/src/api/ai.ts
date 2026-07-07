import client from './client'
import type { AILocateResult } from '../types'

export const locate = (description: string, module_id?: string, deploy_mode?: string) =>
  client.post<AILocateResult>('/ai/locate', { description, module_id, deploy_mode })

export const getTroubleshootingPath = (module_id: string, deploy_mode?: string) =>
  client.get(`/ai/troubleshooting-path/${module_id}`, { params: { deploy_mode } })

export const searchCases = (query: string) =>
  client.post('/cases/search', null, { params: { query } })
