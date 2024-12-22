import { betterAuth } from "better-auth";
import { LibsqlDialect } from "@libsql/kysely-libsql";
import { sendEmail } from "./email";
import { username } from "better-auth/plugins";

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
      validate: (value: string) => {
        if (!value) return 'login.error.required';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'login.error.invalidEmail';
        return true;
      }
    },
    password: {
      validate: (value: string) => {
        if (!value) return 'login.error.required';
        if (value.length < 8) return 'register.error.passwordTooShort';
        return true;
      }
    }
  },
  account: {
    accountLinking: {
      enabled: true,
    },
  },
  plugins: [
    username(),
  ],
  sendResetPassword: async ({ user, url, token }: EmailParams) => {
    await sendEmail({
      to: user.email,
      subject: "Passwort zurücksetzen",
      text: `Klicken Sie auf diesen Link, um Ihr Passwort zurückzusetzen: ${url}`,
      html: `
        <h1>Passwort zurücksetzen</h1>
        <p>Klicken Sie auf den folgenden Link, um Ihr Passwort zurückzusetzen:</p>
        <p><a href="${url}">Passwort zurücksetzen</a></p>
      `,
    });
  },
  sendVerificationEmail: async ({ user, url, token }: EmailParams) => {
    await sendEmail({
      to: user.email,
      subject: "E-Mail-Adresse bestätigen",
      text: `Klicken Sie auf diesen Link, um Ihre E-Mail-Adresse zu bestätigen: ${url}`,
      html: `
        <h1>E-Mail-Adresse bestätigen</h1>
        <p>Klicken Sie auf den folgenden Link, um Ihre E-Mail-Adresse zu bestätigen:</p>
        <p><a href="${url}">E-Mail bestätigen</a></p>
      `,
    });
  },
});
