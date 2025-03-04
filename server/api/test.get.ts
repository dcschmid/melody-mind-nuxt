export default defineEventHandler((event) => {
  return {
    message: 'API is working!',
    timestamp: new Date().toISOString(),
    status: 'success',
  }
})
