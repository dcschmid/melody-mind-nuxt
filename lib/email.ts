import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export const sendEmail = async ({
  to,
  subject,
  text,
  html
}: {
  to: string;
  subject: string;
  text: string;
  html?: string;
}) => {
  try {
    const data = await resend.emails.send({
      from: 'noreply@deine-domain.de',
      to,
      subject,
      text,
      html
    });
    return { data, error: null };
  } catch (error) {
    return { data: null, error };
  }
};
