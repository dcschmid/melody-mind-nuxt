<template>
  <div class="album-cover-game">
    <h1>Album Cover Erraten</h1>
    <p>
      Teste dein Wissen über Album-Cover! Erkenne den Künstler, bevor das Cover vollständig enthüllt
      wird.
    </p>

    <div class="category-selection">
      <h2>Wähle eine Kategorie:</h2>
      <div class="category-buttons">
        <NuxtLink
          v-for="category in categories"
          :key="category.id"
          :to="`/albumcoverguess/${category.id}`"
          class="category-button"
        >
          {{ category.name }}
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categories: [
        { id: '1980s', name: '80er Jahre' },
        { id: '1990s', name: '90er Jahre' },
        { id: '2000s', name: '2000er Jahre' },
        { id: '2010s', name: '2010er Jahre' },
      ],
    }
  },
  head() {
    return {
      title: 'Album Cover Erraten - Melody Mind',
    }
  },
}
</script>

<style scoped>
.album-cover-game {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.category-selection {
  margin-top: 40px;
}

.category-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.category-button {
  display: block;
  padding: 20px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.category-button:hover {
  background-color: #0056b3;
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
