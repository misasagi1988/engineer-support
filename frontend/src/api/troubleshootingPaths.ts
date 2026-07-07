import client from './client'
export const listPaths = () => client.get('/troubleshooting-paths')
export const createPath = (data: any) => client.post('/troubleshooting-paths', data)
export const updatePath = (id: string, data: any) => client.put(`/troubleshooting-paths/${id}`, data)
