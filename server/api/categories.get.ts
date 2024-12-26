export default defineEventHandler(async () => {
  const categories = [
    { slug: 'pop', name: 'Pop' },
    { slug: 'rock', name: 'Rock' },
    { slug: 'rap', name: 'Rap' },
    { slug: 'klassik', name: 'Klassik' }
  ]

  return { categories }
})
