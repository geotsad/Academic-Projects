describe("Review Activity flow", () => {
  it("submits a review successfully", () => {
    // 1. Intercepts ΠΡΙΝ το visit

    // ActivityDetails data
    cy.intercept("GET", "**/users/*/activities/*/details", {
      statusCode: 200,
      body: {
        activityType: "Evening Run",
        date: "2025-05-10",
        time: "18:00",
        location: "Athens",
        difficultyLevel: "Medium",
        maxParticipants: 10,
        currentParticipants: 3,
        completed: true,
        participants: [
          { userId: 1, username: "Alice Doe" },
          { userId: 2, username: "Bob Smith" },
        ],
      },
    }).as("getDetails");

    // POST /reviews → επιτυχία
    cy.intercept("POST", "**/users/*/activities/*/reviews", {
      statusCode: 200,
      body: { success: true },
    }).as("submitReview");

    // Για /my-activities μετά το navigate
    cy.intercept("GET", "**/users/*/participatingActivities", {
      statusCode: 200,
      body: { data: [] },
    }).as("getMyUpcoming");

    cy.intercept("GET", "**/users/*/participatedActivities", {
      statusCode: 200,
      body: { data: [] },
    }).as("getMyCompleted");

    // 2. Πηγαίνουμε στη σελίδα ActivityDetails
    cy.visit("/activity/activity-1", {
      onBeforeLoad(win) {
        win.localStorage.setItem("userId", "1"); // AuthContext
      },
    });

    cy.wait("@getDetails");

    // 3. Πατάμε "Review Activity"
    cy.contains("button", "Review Activity").click();
    cy.url().should("include", "/review/activity-1");

    // 4. Επιλέγουμε rating (κλικάρουμε το 4ο αστέρι)
    cy.contains("How do you rate this activity?")
      .parent()          // div που περιέχει και το StarRating
      .find("svg")       // τα 5 <Star> icons είναι svg
      .eq(3)             // 0,1,2,3,4 → το 4ο αστέρι
      .click();

    // 5. Γράφουμε comment (μέσα στο word limit του validateReview)
    cy.get('textarea[placeholder="What did and didn\'t you like?"]')
      .type("Great route and atmosphere, really enjoyed the run!");

    // 6. Stub του window.alert για να ελέγξουμε το μήνυμα
    cy.window().then((win) => {
      cy.stub(win, "alert").as("alert");
    });

    // 7. Πατάμε Submit
    cy.contains("button", "Submit").click();

    // POST /reviews να έχει επιστρέψει 200
    cy.wait("@submitReview")
      .its("response.statusCode")
      .should("eq", 200);

    // Alert με το σωστό μήνυμα
    cy.get("@alert").should(
      "have.been.calledWith",
      "Thank you for your feedback!"
    );

    // Redirect στο /my-activities
    cy.url().should("include", "/my-activities");

    cy.wait("@getMyUpcoming");
    cy.wait("@getMyCompleted");
  });
});
