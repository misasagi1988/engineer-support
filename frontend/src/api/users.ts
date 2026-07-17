import client from './client'

export const listUsers = () => client.get('/users')
export const createUser = (data: { username: string; email: string; password: string; role: string }) =>
  client.post('/users', data)
export const updateUserRole = (id: string, role: string) => client.put(`/users/${id}/role`, { role })
