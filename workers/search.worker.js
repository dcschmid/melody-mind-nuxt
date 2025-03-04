self.onmessage = function (e) {
  const { categories, query } = e.data
  const filtered = categories.filter(
    (category) =>
      category.headline.toLowerCase().includes(query) ||
      category.introSubline.toLowerCase().includes(query)
  )
  self.postMessage(filtered)
}
