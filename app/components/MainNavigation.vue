<template>
  <!-- Andere Navigation-Elemente -->
  <div class="navigation-links">
    <!-- Hier können Probleme auftreten -->
    <NuxtLink 
      v-for="(link, index) in navigationLinks" 
      :key="index"
      :to="localePath(link.to)"
      class="nav-link"
      :class="{ 'active': isActive(link.to) }"
      :aria-current="isActive(link.to) ? 'page' : null"
    >
      {{ $t(link.title) }}
    </NuxtLink>
    
    <!-- Entfernen Sie die href-Attribute bei allen NuxtLinks -->
    <!-- Falsche Version:
    <NuxtLink 
      to="/rules" 
      href="/rules"
      class="nav-link"
    >
      {{ $t('navigation.rules') }}
    </NuxtLink>
    -->
  </div>
  <!-- Weitere Navigation-Elemente -->
</template>

<!-- ... rest of the component ... -->
