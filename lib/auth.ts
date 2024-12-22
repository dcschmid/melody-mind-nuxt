import { betterAuth } from "better-auth";
import { LibsqlDialect } from "@libsql/kysely-libsql";
import { sendEmail } from "./email";
import { username } from "better-auth/plugins";

const dialect = new LibsqlDialect({
  url: process.env.NUXT_TURSO_DATABASE_URL || "",
  authToken: process.env.NUXT_TURSO_AUTH_TOKEN || "",
});

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
    },
    sendResetPassword: async ({ user, url, token }) => {
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
    sendVerificationEmail: async ({ user, url, token }) => {
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
  },
  account: {
    accountLinking: {
      enabled: true,
    },
  },
  plugins: [
    username(),
  ],
});
