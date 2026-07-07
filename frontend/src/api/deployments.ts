import client from './client'
export const listDeployments = (params?: any) => client.get('/deployments', { params })
export const createDeployment = (data: any) => client.post('/deployments', data)
export const updateDeployment = (id: string, data: any) => client.put(`/deployments/${id}`, data)
