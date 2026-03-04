const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:3000",
    watchForFileChanges: true,

    setupNodeEvents(on, config) {
      // Μπορείς να προσθέσεις event listeners εδώ στο μέλλον (π.χ. tasks)
    },
  },
});
