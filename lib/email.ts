// Email sending functionality has been removed
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
  // Email functionality has been removed
  console.log('Email sending has been disabled');
  return { data: null, error: 'Email sending functionality has been removed' };
};
