describe("Join Activity flow - Unhappy Paths", () => {
  it("shows an error modal when max participants is reached (409 Conflict)", () => {
    // 1. Intercepts για να φορτώσει η σελίδα (Home Page)
    
    // Pinned activities → κενή λίστα
    cy.intercept("GET", "**/activities/pinned", {
      statusCode: 200,
      body: [], // Το Home.jsx περιμένει array απευθείας ή {data: []} ανάλογα το axios setup, εδώ βάζουμε array βάσει του κώδικα fetchPinned
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

    // 🔴 Join request → ΑΠΟΤΥΧΙΑ (Max Participants)
    // Επιστρέφουμε status 409 Conflict και το μήνυμα σφάλματος στο body
    cy.intercept(
      "POST",
      "**/users/*/activities/*/joinRequests",
      {
        statusCode: 409,
        body: {
          success: false,
          message: "Activity is already full.", // Αυτό το message διαβάζει το Home.jsx (e.response.data.message)
        },
      }
    ).as("joinRequestFull");

    // 2. Επισκέπτουμε την αρχική ΚΑΙ "σετάρουμε" τον user
    cy.visit("/", {
      onBeforeLoad(win) {
        win.localStorage.setItem("userId", "123");
      },
    });

    // 3. Περιμένουμε να φορτώσουν οι λίστες
    cy.wait("@getPinned"); 
    cy.wait("@getUpcoming");

    // 4. Πατάμε το JOIN κουμπί στην κάρτα δραστηριότητας
    cy.contains("button", "Join").click();

    // 5. Ελέγχουμε ότι έγινε η POST κλήση και επέστρεψε 409
    cy.wait("@joinRequestFull")
      .its("response.statusCode")
      .should("eq", 409);

    // 6. 🟢 ΕΛΕΓΧΟΣ: Εμφανίζεται το StatusModal με το μήνυμα σφάλματος
    // Το Home.jsx χρησιμοποιεί το StatusModal για να δείξει το e.response.data.message
    cy.contains("Activity is already full.").should("be.visible");
    
    // Προαιρετικά: Ελέγχουμε ότι είναι error modal (αν υπάρχει τρόπος διάκρισης, π.χ. χρώμα ή εικονίδιο)
    // Αλλά το περιεχόμενο κειμένου αρκεί για το acceptance test.
  });
});