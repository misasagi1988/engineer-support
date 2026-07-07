import client from './client'

export const getDashboardStats = () =>
  client.get('/stats/dashboard')
