interface Category {
  slug: string;
  name: string;
}

export default defineEventHandler<{ categories: Category[] }>(async () => {
  const categories: Category[] = [
    { slug: 'pop', name: 'Pop' },
    { slug: 'rock', name: 'Rock' },
    { slug: 'rap', name: 'Rap' },
    { slug: 'klassik', name: 'Klassik' }
  ]

  return { categories }
})
