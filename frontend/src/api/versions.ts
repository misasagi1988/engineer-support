import client from './client'
export const listVersions = () => client.get('/versions')
export const createVersion = (data: any) => client.post('/versions', data)
