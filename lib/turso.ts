import { createClient } from "@libsql/client";

export function useTurso(/* event: H3Event */) {
  const { turso } = useRuntimeConfig(/* event */);

  return createClient({
    url: turso.databaseUrl,
    authToken: turso.authToken,
  });
}
