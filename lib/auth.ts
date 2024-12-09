import { betterAuth } from "better-auth";
import { genericOAuth } from "better-auth/plugins";
import { LibsqlDialect } from "@libsql/kysely-libsql";
import { sendEmail } from "./email";
import { username } from "better-auth/plugins";

const dialect = new LibsqlDialect({
  url: process.env.TURSO_DATABASE_URL || "",
  authToken: process.env.TURSO_AUTH_TOKEN || "",
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
  socialProviders: {
    github: {
      clientId: process.env.AUTH_GITHUB_ID || "",
      clientSecret: process.env.AUTH_GITHUB_SECRET || "",
    },
    google: {
      clientId: process.env.AUTH_GOOGLE_ID || "",
      clientSecret: process.env.AUTH_GOOGLE_SECRET || "",
    },
    discord: {
      clientId: process.env.AUTH_DISCORD_ID || "",
      clientSecret: process.env.AUTH_DISCORD_SECRET || "",
    },
    twitch: {
      clientId: process.env.AUTH_TWITCH_ID || "",
      clientSecret: process.env.AUTH_TWITCH_SECRET || "",
    },
    twitter: {
      clientId: process.env.AUTH_TWITTER_ID || "",
      clientSecret: process.env.AUTH_TWITTER_SECRET || "",
    },
  },
  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ["google", "github", "discord", "twitch", "twitter", "yahoo", "spotify"],
    },
  },
  plugins: [
    username(),
    genericOAuth({
      config: [
        {
          providerId: "spotify",
          type: "oauth2",
          clientId: process.env.AUTH_SPOTIFY_ID || "",
          clientSecret: process.env.AUTH_SPOTIFY_SECRET || "",
          authorizationUrl: "https://accounts.spotify.com/authorize",
          tokenUrl: "https://accounts.spotify.com/api/token",
          userInfoUrl: "https://api.spotify.com/v1/me",
          scopes: ["user-read-email", "user-read-private"],
          getUserInfo: async (tokens) => {
            try {
              const response = await fetch("https://api.spotify.com/v1/me", {
                headers: {
                  Authorization: `Bearer ${tokens.accessToken}`,
                  "Content-Type": "application/json",
                },
              });

              if (!response.ok) throw new Error(`Spotify API error: ${response.status}`);

              const data = await response.json();

              return {
                id: data.id,
                email: data.email,
                name: data.display_name || data.id,
                image: data.images?.[0]?.url,
                emailVerified: true,
                createdAt: new Date(),
                updatedAt: new Date(),
              };
            } catch (error) {
              console.error("Error:", error);
              return null;
            }
          },
        },
        {
          providerId: "yahoo",
          type: "oauth2",
          clientId: process.env.AUTH_YAHOO_ID || "",
          clientSecret: process.env.AUTH_YAHOO_SECRET || "",
          authorizationUrl: "https://api.login.yahoo.com/oauth2/request_auth",
          tokenUrl: "https://api.login.yahoo.com/oauth2/get_token",
          userInfoUrl: "https://api.login.yahoo.com/openid/v1/userinfo",
          scopes: ["openid", "email", "profile"],
          getUserInfo: async (tokens) => {
            try {
              const response = await fetch("https://api.login.yahoo.com/openid/v1/userinfo", {
                headers: {
                  Authorization: `Bearer ${tokens.accessToken}`,
                },
              });

              if (!response.ok) throw new Error(`Yahoo API error: ${response.status}`);

              const data = await response.json();

              return {
                id: data.sub,
                email: data.email,
                name: data.name || data.sub,
                image: data.picture,
                emailVerified: data.email_verified,
                createdAt: new Date(),
                updatedAt: new Date(),
              };
            } catch (error) {
              console.error("Error:", error);
              return null;
            }
          },
        },
      ],
    }),
  ],
});
