import { betterAuth } from "better-auth";
import { LibsqlDialect } from "@libsql/kysely-libsql";

const dialect = new LibsqlDialect({
  url: process.env.NUXT_TURSO_DATABASE_URL || "",
  authToken: process.env.NUXT_TURSO_AUTH_TOKEN || "",
});

interface EmailUser {
  email: string;
}

interface EmailParams {
  user: EmailUser;
  url: string;
  token: string;
}

export const auth = betterAuth({
  database: {
    dialect,
    type: "sqlite",
  },
  emailAndPassword: {
    enabled: true,
    username: {
      enabled: true,
      required: true,
      minLength: 3,
      maxLength: 20,
      validate: (value: string) => {
        if (!value) return 'login.error.required';
        if (value.length < 3) return 'register.error.usernameTooShort';
        if (value.length > 20) return 'register.error.usernameTooLong';
        return true;
      }
    },
    email: {
      validate: (value: string): string | true => {
        if (!value) return 'login.error.required';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'login.error.invalidEmail';
        return true;
      }
    } as any,
    password: {
      validate: (value: string): string | true => {
        if (!value) return 'login.error.required';
        if (value.length < 8) return 'register.error.passwordTooShort';
        return true;
      }
    } as any,
  },
  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ["discord", "github"]
    },
  },
  socialProviders: {
    discord: {
      clientId: process.env.DISCORD_CLIENT_ID as string,
      clientSecret: process.env.DISCORD_CLIENT_SECRET as string,
    },
    github: {
      clientId: process.env.NUXT_GITHUB_CLIENT_ID as string,
      clientSecret: process.env.NUXT_GITHUB_CLIENT_SECRET as string,
    },
  },
});
