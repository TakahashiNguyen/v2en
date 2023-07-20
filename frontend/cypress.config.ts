import { defineConfig } from 'cypress';

export default defineConfig({
  video: false,
  e2e: {
    // setupNodeEvents(on, config) {}
    screenshotOnRunFailure: false,
    baseUrl: 'http://localhost:9000/',
    supportFile: 'test/cypress/support/e2e.ts',
    specPattern: 'test/cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
  },
});
