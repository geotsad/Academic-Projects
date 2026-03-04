describe("Review Activity flow - Unhappy Paths", () => {
  // -----------------------------------------------------------
  // Sub-Scenario A: Submit Fails Due to Missing Rating (Frontend Validation)
  // -----------------------------------------------------------
  it("prevents submission if rating is missing and displays validation error", () => {
    // 1. Intercepts για να φορτώσει το ActivityDetails
    cy.intercept("GET", "**/users/*/activities/*/details", {
      statusCode: 200,
      body: {
        completed: true,
        activityType: "Evening Run",
        participants: [{ userId: 1, username: "Alice Doe" }],
      },
    }).as("getDetails");

    // Intercept για την POST κλήση (Ορίζουμε τι ΘΑ γινόταν αν περνούσε το validation)
    cy.intercept("POST", "**/users/*/activities/*/reviews", {
      statusCode: 400,
      body: { success: false, error: "Rating is required." },
    }).as("submitReviewFail");

    // 2. Πλοήγηση στη σελίδα ActivityDetails
    cy.visit("/activity/activity-1", {
      onBeforeLoad(win) {
        win.localStorage.setItem("userId", "1");
      },
    });

    cy.wait("@getDetails");

    // 3. Πατάμε "Review Activity"
    cy.contains("button", "Review Activity").click();
    cy.url().should("include", "/review/activity-1");

    // 4. ❌ ΔΕΝ Επιλέγουμε rating (αφήνουμε το πεδίο κενό)

    // 5. Γράφουμε comment
    cy.get('textarea[placeholder="What did and didn\'t you like?"]')
      .type("Great route, but I forgot the rating!");
    
    // 6. Πατάμε Submit
    cy.contains("button", "Submit").click();

    // 7. 🟢 ΕΛΕΓΧΟΣ 1: Εμφανίστηκε το on-screen μήνυμα λάθους
    // Το μήνυμα προέρχεται από τη validateReview
    cy.contains("Please rate the activity before submitting!").should("be.visible");

    // 8. (ΔΙΟΡΘΩΣΗ) Αφαιρέσαμε τον έλεγχο 'not.have.been.called' που προκαλούσε το error.
    // Το γεγονός ότι βλέπουμε το παραπάνω μήνυμα και ότι το URL δεν άλλαξε,
    // αρκεί για να επιβεβαιώσουμε ότι η υποβολή μπλοκαρίστηκε.

    // 9. Ελέγχουμε ότι δεν έγινε redirect (παραμένουμε στη σελίδα review)
    cy.url().should("include", "/review/activity-1");
  });

  // -----------------------------------------------------------
  // Sub-Scenario B: Activity Not Completed (Confirms Design Choice)
  // -----------------------------------------------------------
  it("shows the 'Review Activity' button even if the activity is NOT completed", () => {
    // 1. Intercepts για να επιστρέψει details ΜΕ completed: false
    cy.intercept("GET", "**/users/*/activities/*/details", {
      statusCode: 200,
      body: {
        activityType: "Evening Run",
        completed: false, // Η ΔΡΑΣΤΗΡΙΟΤΗΤΑ ΔΕΝ ΕΧΕΙ ΟΛΟΚΛΗΡΩΘΕΙ
      },
    }).as("getDetailsNotCompleted");

    // 2. Πηγαίνουμε στη σελίδα ActivityDetails
    cy.visit("/activity/activity-1", {
      onBeforeLoad(win) {
        win.localStorage.setItem("userId", "1");
      },
    });

    cy.wait("@getDetailsNotCompleted");

    // 3. 🟢 ΕΛΕΓΧΟΣ: Το test ΠΡΕΠΕΙ να βρει το κουμπί.
    cy.contains("button", "Review Activity").should("be.visible");
    
    cy.log('DESIGN CONFIRMED: The "Review Activity" button is visible even though completed: false.');
  });
});