import { usernameClient } from "better-auth/client/plugins";
import { genericOAuthClient } from "better-auth/client/plugins";
import { createAuthClient } from "better-auth/vue";

export const authClient = createAuthClient({
  plugins: [
    usernameClient(),
    genericOAuthClient()
  ],
});
