import client from './client'

export const listUsers = () => client.get('/users')
export const updateUserRole = (id: string, role: string) => client.put(`/users/${id}/role`, { role })
