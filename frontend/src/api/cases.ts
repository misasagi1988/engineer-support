import client from './client'
import type { Case } from '../types'

export const listCases = (params?: Record<string, any>) =>
  client.get<Case[]>('/cases', { params })

export const getCase = (id: string) =>
  client.get<Case>(`/cases/${id}`)

export const createCase = (data: Record<string, any>) =>
  client.post<Case>('/cases', data)

export const updateCase = (id: string, data: Record<string, any>) =>
  client.put<Case>(`/cases/${id}`, data)

export const reviewCase = (id: string, review_status: string) =>
  client.put(`/cases/${id}/review`, { review_status })

export const searchCases = (query: string) =>
  client.post('/cases/search', null, { params: { query } })
