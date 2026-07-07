import client from './client'
export const listModules = () => client.get('/modules')
export const createModule = (data: any) => client.post('/modules', data)
export const updateModule = (id: string, data: any) => client.put(`/modules/${id}`, data)
