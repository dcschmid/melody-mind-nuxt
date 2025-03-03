import prettierPlugin from 'eslint-plugin-prettier'
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt(
  // Ignores configuration
  {
    ignores: [
      // Nuxt build output
      '.nuxt',
      '.output',
      'dist',

      // Node modules
      'node_modules',

      // Logs
      '*.log',

      // Cache
      '.cache',

      // Generated files
      'public/thumbhash',

      // Package manager lock files
      'yarn.lock',
      'package-lock.json',
      'pnpm-lock.yaml',

      // Other
      '.DS_Store',

      // Large JSON files
      'app/json/genres/**/*.json',

      // Markdown files
      '**/*.md',
      'content/**/*.md',
    ],
  },
  // Custom ESLint configuration
  {
    files: ['**/*.vue', '**/*.js', '**/*.ts'],
    rules: {
      // Customize rules for your project
      'vue/multi-word-component-names': 'off',
      'vue/no-multiple-template-root': 'off',
      'no-console': ['warn', { allow: ['warn', 'error', 'info'] }],
      'no-debugger': 'warn',
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-empty-object-type': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',
      '@stylistic/brace-style': 'off',
      '@stylistic/operator-linebreak': 'off',
      '@stylistic/comma-dangle': 'off',
      '@stylistic/arrow-parens': 'off',
      '@stylistic/member-delimiter-style': 'off',
      '@stylistic/quote-props': 'off',
      'vue/first-attribute-linebreak': 'off',
      'vue/html-indent': 'off',
      'vue/max-attributes-per-line': 'off',
      'vue/html-closing-bracket-newline': 'off',
      'vue/html-self-closing': 'off',
      'vue/attributes-order': 'off',
      'import/order': 'off',
    },
  },
  // Integration with Prettier
  {
    files: ['**/*.vue', '**/*.js', '**/*.ts', '**/*.json'],
    plugins: {
      prettier: prettierPlugin,
    },
    rules: {
      'prettier/prettier': 'off',
    },
  },
)
