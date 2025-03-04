export default defineEventHandler(() => {
  return {
    message: 'API is working!',
    timestamp: new Date().toISOString(),
    status: 'success',
  }
})
