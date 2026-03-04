describe("Join Activity flow", () => {
  it("sends a join request successfully", () => {
    // 1. Κάνουμε intercept ΟΛΑ τα calls ΠΡΙΝ φορτώσει η εφαρμογή

    // Pinned activities → κενή λίστα
    cy.intercept("GET", "**/activities/pinned", {
      statusCode: 200,
      body: { data: [] },
    }).as("getPinned");

    // Upcoming activities → μία fake δραστηριότητα
    cy.intercept("GET", "**/users/*/activities*", {
      statusCode: 200,
      body: {
        data: [
          {
            activityId: "activity-1",
            isPinned: false,
            details: {
              activityType: "Hiking",
              date: "2025-05-10",
              time: "10:00",
              location: "Athens",
            },
          },
        ],
      },
    }).as("getUpcoming");

    // Join request → επιτυχία
    cy.intercept(
      "POST",
      "**/users/*/activities/*/joinRequests",
      {
        statusCode: 200,
        body: {
          success: true,
          data: { message: "ok" },
        },
      }
    ).as("joinRequest");

    // 2. Επισκέπτουμε την αρχική ΚΑΙ "σετάρουμε" τον user πριν φορτώσει η React
    cy.visit("/", {
      onBeforeLoad(win) {
        // Προσαρμόζεις τα keys για το AuthContext σου αν χρειάζεται
        win.localStorage.setItem("userId", "123");
      },
    });

    // 3. Περιμένουμε να φορτώσει η fake λίστα
    cy.wait("@getUpcoming");

    // 4. Πατάμε το JOIN κουμπί
    cy.contains("button", "Join").click();

    // 5. Ελέγχουμε ότι έγινε η POST κλήση
    cy.wait("@joinRequest")
      .its("response.statusCode")
      .should("eq", 200);

    // 6. Ελέγχουμε ότι εμφανίζεται το success μήνυμα από το Home.jsx
    cy.contains("Request sent!").should("be.visible");
  });
});
