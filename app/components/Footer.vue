<template>
  <footer class="bg-surface py-medium">
    <div class="container mx-auto px-small">
      <div class="flex flex-wrap justify-between">
        <!-- Andere Footer-Inhalte -->
        <div class="footer-links">
          <!-- Korrekte Implementierung für interne Links -->
          <NuxtLink 
            v-for="(link, index) in footerLinks" 
            :key="index"
            :to="localePath(link.to)"
            class="text-text-secondary hover:text-text transition-colors duration-normal mr-4 mb-2"
          >
            {{ $t(link.title) }}
          </NuxtLink>
          
          <!-- Externe Links sollten nur href verwenden -->
          <a 
            v-for="(externalLink, index) in externalLinks"
            :key="`ext-${index}`"
            :href="externalLink.url"
            target="_blank" 
            rel="noopener noreferrer"
            class="text-text-secondary hover:text-text transition-colors duration-normal mr-4 mb-2"
          >
            {{ $t(externalLink.title) }}
          </a>
          
          <!-- Falsche Implementierung (entfernen):
          <NuxtLink 
            to="/privacy"
            href="/privacy"
            class="text-text-secondary hover:text-text transition-colors duration-normal mr-4"
          >
            {{ $t('footer.privacy') }}
          </NuxtLink>
          -->
        </div>
      </div>
    </div>
  </footer>
</template>

<!-- ... rest of the component ... -->
