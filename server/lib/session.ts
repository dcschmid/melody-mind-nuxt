import { H3Event } from 'h3'
import { authClient } from '~/lib/auth-client'

export async function requireUserSession(event: H3Event) {
  const authHeader = getHeader(event, 'cookie')
  if (!authHeader) {
    throw createError({ statusCode: 401, message: 'No session cookie' })
  }

  const session = await authClient.getSession()
  if (!session?.data?.user) {
    throw createError({ statusCode: 401, message: 'Invalid session' })
  }

  return session.data
}
