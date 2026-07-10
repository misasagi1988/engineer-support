import client from './client'
import type { Ticket } from '../types'

export const listTickets = (params?: Record<string, any>) =>
  client.get<Ticket[]>('/tickets', { params })

export const getTicket = (id: string) =>
  client.get<Ticket>(`/tickets/${id}`)

export const createTicket = (data: Record<string, any>) =>
  client.post<Ticket>('/tickets/', data)

export const updateTicket = (id: string, data: Record<string, any>) =>
  client.put<Ticket>(`/tickets/${id}`, data)

export const updateTicketStatus = (id: string, status: string) =>
  client.put(`/tickets/${id}/status`, { status })

export const generateCase = (id: string) =>
  client.post(`/tickets/${id}/generate-case`)
