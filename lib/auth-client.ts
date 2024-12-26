import { usernameClient } from "better-auth/client/plugins";
import { createAuthClient } from "better-auth/vue";

export const authClient = createAuthClient();

export const signInWithDiscord = async () => {
  return await authClient.signIn.social({
    provider: "discord"
  });
};
