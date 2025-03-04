export default defineEventHandler((event) => {
  setResponseStatus(event, 200)
  return {
    status: 'healthy',
    timestamp: new Date().toISOString(),
  }
})
