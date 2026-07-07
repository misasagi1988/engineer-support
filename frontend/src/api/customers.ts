import client from './client'
export const listCustomers = () => client.get('/customers')
export const createCustomer = (data: any) => client.post('/customers', data)
export const updateCustomer = (id: string, data: any) => client.put(`/customers/${id}`, data)
