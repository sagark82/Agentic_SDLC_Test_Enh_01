# Test Strategy & Plan: Patient Enrollment Application

**Document Version:** 1.0  
**Date:** October 26, 2023  
**Author:** QA Automation Engineer

---

## 1. Test Strategy

### 1.1 Introduction
This document outlines the comprehensive testing strategy for the Patient Enrollment Application. Its purpose is to define the scope, objectives, methodologies, and resources required to ensure the application meets the functional and non-functional requirements specified in the SRS and HLD. This strategy will guide all testing activities throughout the software development lifecycle (SDLC).

### 1.2 Scope of Testing

#### 1.2.1 In Scope
-   **Functional Testing:** End-to-end validation of all user stories (US1-US9) across the three epics:
    -   **Patient Onboarding & Account Management:** Patient registration (email/phone), verification, multi-step form logic, data persistence, document uploads, and digital consent.
    -   **Patient Experience & Support:** Patient dashboard, application status tracking, notifications, informational pages (FAQ, Privacy), site search, and support contact form.
    -   **Provider & Admin Portal:** Secure login, dashboard functionality (sorting, filtering), application review workflow (approve, reject, request info), and Role-Based Access Control (RBAC) verification.
-   **API Testing:** Validation of all RESTful API endpoints defined in the HLD for functionality, security, and performance. This includes testing authentication (JWT), data validation, error handling, and response codes.
-   **Security Testing:**
    -   Verification of security controls defined in US10, including RBAC, data encryption (in-transit and at-rest), input validation (to prevent XSS, SQLi), and secure headers (CSP).
    -   Testing for session management vulnerabilities and access control flaws.
-   **Performance Testing:**
    -   Validating performance benchmarks from US11 (LCP < 2.5s, API response < 500ms).
    -   Basic load testing to ensure the system performs under expected user load.
-   **Accessibility Testing:**
    -   Ensuring compliance with WCAG 2.2 Level AA standards as per US12, including keyboard-only navigation, screen reader compatibility, and color contrast ratios.
-   **Compatibility Testing:**
    -   **Cross-Browser:** Latest versions of Chrome, Firefox, Safari, and Edge.
    -   **Cross-Device:** Validating responsiveness on Desktop, Tablet, and Mobile viewports.
-   **Database Testing:** Verifying data integrity, encryption of sensitive PHI fields, and correctness of data mapping between the application and the PostgreSQL database.
-   **BDD Generation Tool Testing:** Validating the functionality of the developer tool described in US13 to ensure it generates syntactically correct Gherkin feature files.

#### 1.2.2 Out of Scope
-   Testing of third-party services themselves (e.g., AWS SES, Twilio), beyond verifying the integration points.
-   Underlying cloud infrastructure performance and security testing.
-   Exhaustive penetration testing (this will be conducted by a specialized third-party security team but will be based on findings from our internal security tests).
-   Usability testing with real end-users (this is a separate activity owned by the product/UX team).

### 1.3 Testing Objectives
-   To validate that all functional requirements specified in the user stories are implemented correctly.
-   To ensure the application is secure and compliant with HIPAA regulations, protecting all Patient Health Information (PHI).
-   To verify that the application meets the defined non-functional requirements for performance, accessibility, and reliability.
-   To identify, document, and track defects to resolution in a timely manner.
-   To provide a high degree of confidence to stakeholders for a successful production release.
-   To build a robust and maintainable regression suite to support future development and CI/CD.

### 1.4 Testing Types & Levels
-   **Unit Testing:** Performed by developers to test individual functions and components in isolation.
-   **Integration Testing:** Testing the interfaces and interactions between modules, such as API-to-database communication and frontend-to-API calls.
-   **System (End-to-End) Testing:** Performed by the QA team on the fully integrated application to validate the complete user workflows. This includes:
    -   **Functional & Regression Testing:** Validating new features and ensuring existing functionality is not broken.
    -   **UI/UX Testing:** Manual and automated checks for visual consistency and responsiveness.
    -   **Security Testing:** Verifying authentication, authorization, and data protection mechanisms.
    -   **Performance Testing:** Measuring response times and stability under load.
    -   **Accessibility Testing:** Automated and manual checks against WCAG 2.2 AA standards.
-   **User Acceptance Testing (UAT):** Conducted by product owners and business stakeholders to confirm the application meets business requirements before release.

### 1.5 Test Automation Strategy
A Behavior-Driven Development (BDD) approach will be central to our strategy. Gherkin feature files will serve as executable specifications.

-   **Automation Pyramid:**
    -   **UI/E2E Tests (10%):** Focus on critical user journeys (e.g., full patient registration and submission).
    -   **API/Service Tests (30%):** Test business logic, security, and integration points at the API layer for speed and stability.
    -   **Unit Tests (60%):** A strong foundation of unit tests written by developers.

-   **Tools and Frameworks:**
    -   **Test Management:** Jira for tracking user stories, test cases, and defects.
    -   **BDD Framework:** `pytest-bdd` (Python) to bind Gherkin feature files to test code, aligning with the backend tech stack.
    -   **UI Automation:** **Playwright** with Python for its robust cross-browser capabilities, auto-waits, and speed.
    -   **API Automation:** **`pytest`** with the **`httpx`** library for making asynchronous API requests, mirroring the FastAPI backend.
    -   **Performance Testing:** **k6** or **JMeter** for load testing API endpoints. **Google Lighthouse** for frontend performance metrics.
    -   **Accessibility Testing:** **Axe-core** integrated into the Playwright test suite for automated checks.
    -   **CI/CD:** **GitHub Actions** to trigger automated test suites (API, UI regression) on every pull request and deployment.
    -   **Reporting:** **Allure Report** integrated with `pytest` for detailed and interactive test execution reports.

### 1.6 Test Environments
-   **Development:** Local developer environments for coding and unit testing.
-   **QA/Testing:** A stable, dedicated environment that is a close replica of production. All system, integration, and regression testing will be performed here.
-   **Staging/Pre-Production:** An environment for UAT and final validation before deploying to production. Performance tests may also be run here.
-   **Production:** The live environment. Smoke tests will be executed post-deployment.

### 1.7 Roles & Responsibilities
-   **Developers:** Write unit tests, perform code reviews, fix bugs, and support QA in debugging.
-   **QA Automation Engineer:** Design and execute the test strategy, create and maintain Gherkin feature files, develop and maintain automated test scripts (UI, API), report and track defects, and manage the test automation framework.
-   **Product Owner:** Define acceptance criteria, participate in UAT, and prioritize defects.
-   **DevOps Engineer:** Maintain the CI/CD pipeline and manage the test environments.

### 1.8 Defect Management
-   **Tool:** Jira
-   **Workflow:** Defects will follow a standard lifecycle: `New` -> `In Analysis` -> `Ready for Development` -> `In Progress` -> `Ready for QA` -> `Done` / `Reopened`.
-   **Severity Levels:**
    -   **P1 - Blocker:** Prevents major functionality; no workaround exists.
    -   **P2 - Critical:** A major feature is broken or fails frequently; a difficult workaround may exist.
    -   **P3 - Major:** A feature is not working as expected but does not impact the entire system.
    -   **P4 - Minor:** UI/cosmetic issue or a defect with an easy workaround.

### 1.9 Entry & Exit Criteria

#### 1.9.1 Entry Criteria (for System Testing)
-   The build has been successfully deployed to the QA environment.
-   All unit and integration tests have passed in the CI pipeline.
-   The development team has provided release notes detailing the changes in the build.
-   A smoke test on critical functionalities has passed.

#### 1.9.2 Exit Criteria (for Release)
-   All planned test cases have been executed.
-   The automated regression suite has a pass rate of 100%.
-   There are no open P1 (Blocker) or P2 (Critical) defects.
-   All high-priority P3 defects are addressed or have a clear mitigation plan.
-   UAT has been completed and signed off by the Product Owner.
-   All testing documentation and reports are complete.

---

## 2. BDD Feature Files

# User Story 1: Secure Patient Registration
Feature: Patient Account Registration
  As a prospective patient, I want to create a secure account so that I can begin the enrollment process.

  Scenario: Successful registration using an email address
    Given I am on the registration page
    When I fill in the registration form with my name, a unique email, and a strong password
    And I submit the form
    Then I should see a message "Verification link sent to your email."
    And the system should send a verification email to my address
    When I follow the verification link from the email
    Then my account should be verified
    And I should be able to log in with my email and password

  Scenario: Successful registration using a phone number
    Given I am on the registration page
    When I fill in the registration form with my name, a unique phone number, and a strong password
    And I submit the form
    Then I should see a message "Verification code sent to your phone."
    And the system should send a verification code via SMS to my phone number
    When I enter the received SMS code on the verification page
    Then my account should be verified
    And I should be able to log in with my phone number and password

  Scenario Outline: Registration fails with invalid or weak data
    Given I am on the registration page
    When I attempt to register with the following details:
      | Field         | Value                 |
      | Name          | <name>                |
      | Email         | <email>               |
      | Phone Number  | <phone>               |
      | Password      | <password>            |
      | Confirm Password | <confirm_password> |
    Then I should see the error message "<error_message>"

    Examples:
      | name      | email               | phone      | password    | confirm_password | error_message                                   |
      | "Jane Doe"| "invalid-email"     | "1234567890" | "StrongPass1!" | "StrongPass1!"   | "Please enter a valid email address."           |
      | "Jane Doe"| "jane@example.com"  | "1234567890" | "weak"      | "weak"           | "Password must be at least 8 characters long."    |
      | "Jane Doe"| "jane@example.com"  | "1234567890" | "StrongPass1!" | "WrongPass1!"    | "Passwords do not match."                       |

  Scenario: Attempt to register with an existing email
    Given a patient with the email "existing.user@example.com" already exists
    When I try to register with the email "existing.user@example.com"
    Then I should see an error message "An account with this email already exists."

  Scenario: Rate limiting is applied after multiple failed registration attempts
    Given I am on the registration page
    When I submit the registration form with invalid data 6 times within one minute from the same IP address
    Then I should see a message "Too many registration attempts. Please try again later."
    And my IP address should be temporarily blocked from making further registration attempts

# User Story 2 & 3: Multi-Step Enrollment and Document Upload
Feature: Multi-Step Enrollment Application and Document Upload
  As a registered patient, I want to complete a multi-step form and upload documents to provide my information.

  Scenario: A new patient completes the multi-step enrollment form successfully
    Given I am a registered and logged-in patient
    And I am on the first step of the enrollment form "Personal Details"
    When I fill in the "Personal Details" with valid information
    And I click "Save and Continue"
    Then I should be on the "Medical History" step
    And the progress indicator should show step 2 of 3 is active
    When I fill in the "Medical History" with valid information
    And I click "Save and Continue"
    Then I should be on the "Insurance Information" step
    When I fill in the "Insurance Information" with valid information
    And I click "Save and Continue"
    Then I should be on the "Document Upload" step

  Scenario: A patient saves progress and returns later
    Given I am a registered and logged-in patient
    And I have completed the "Personal Details" step of the enrollment form
    When I log out and log back in later
    Then I should be taken to the "Medical History" step of the form
    And my previously entered "Personal Details" should be saved

  Scenario: A patient uploads required documents
    Given I am on the "Document Upload" step
    And I see a list of required documents: "ID proof", "Insurance card"
    When I upload a valid "ID_Proof.pdf" file for "ID proof"
    Then I should see a progress bar during the upload
    And I should see "ID_Proof.pdf" listed as uploaded with an option to delete it
    When I upload a valid "Insurance_Card.jpg" file for "Insurance card"
    Then I should see "Insurance_Card.jpg" listed as uploaded

  Scenario Outline: Attempt to upload an invalid document
    Given I am on the "Document Upload" step
    When I attempt to upload the file "<file_name>"
    Then I should see the error message "<error_message>"

    Examples:
      | file_name              | error_message                                 |
      | "large_file.pdf"       | "File size exceeds the 10MB limit."           |
      | "unsupported_file.txt" | "File type not supported. Please use PDF, JPG, or PNG." |
      | "infected_file.pdf"    | "A virus was detected in the file. Upload failed." |

# User Story 4: Digital Consent Capture
Feature: Digital Consent Capture
  As a registered patient, I want to provide digital consent to finalize my application.

  Scenario: Patient provides consent via checkbox and submits the application
    Given I have completed all enrollment form steps and document uploads
    And I am on the "Consent" page
    When I review the "Privacy Policy" and "Terms of Service"
    And I check the box "I have read and agree to the terms."
    And I click "Submit Application"
    Then my application should be submitted successfully
    And a non-editable, timestamped copy of the consent should be stored with my application

  Scenario: Patient provides consent via digital signature
    Given I am on the "Consent" page
    When I draw my signature in the digital signature pad
    And I click "Submit Application"
    Then my application should be submitted successfully
    And the system should log my consent with the date, time, and IP address

  Scenario: Attempt to submit application without providing consent
    Given I have completed all enrollment form steps and document uploads
    And I am on the "Consent" page
    When I click "Submit Application" without providing consent
    Then the submission should fail
    And I should see a message "You must provide consent to continue."

# User Story 5: Patient Dashboard and Status Tracking
Feature: Patient Dashboard and Application Status Tracking
  As a patient, I want to view my application status and receive notifications.

  Scenario Outline: Patient dashboard displays the correct application status
    Given I am a logged-in patient who has submitted an application
    And my application status is "<current_status>"
    When I navigate to my dashboard
    Then I should see my application status displayed as "<current_status>"
    And I should see a read-only summary of my submitted information

    Examples:
      | current_status      |
      | "Submitted"         |
      | "In Review"         |
      | "Approved"          |
      | "Rejected"          |

  Scenario: Patient dashboard displays a message when action is required
    Given I am a logged-in patient
    And my application status is "Action Required" with the reason "Please upload a clearer copy of your ID"
    When I navigate to my dashboard
    Then I should see my application status as "Action Required"
    And I should see a message "Please upload a clearer copy of your ID"

  Scenario: Patient receives an email notification on status change
    Given I am a patient with an application "In Review"
    When an admin changes my application status to "Approved"
    Then an email notification should be sent to my registered email address with the subject "Your Application Status has been Updated"
    And the email body should state that my application has been approved

# User Story 6 & 7: Informational Pages and Support
Feature: Informational Pages, Search, and Support
  As a user, I want to find information and contact support easily.

  Scenario: A user searches the FAQ page
    Given I am on the "FAQ" page
    When I enter "insurance" into the search bar
    Then I should see a list of relevant FAQ titles containing the word "insurance"
    When I search for "insurnce" with a typo
    Then I should still see relevant results for "insurance"

  Scenario: A logged-in patient submits a support request
    Given I am a logged-in patient with the name "John Doe" and email "john.doe@example.com"
    When I navigate to the "Contact Us" page
    Then the "Name" field should be pre-populated with "John Doe"
    And the "Email Address" field should be pre-populated with "john.doe@example.com"
    When I fill in the "Subject" and "Message" fields
    And I submit the contact form
    Then I should see a confirmation message on the screen
    And I should receive a confirmation email with a ticket number

# User Story 8 & 9: Provider and Admin Portal
Feature: Provider and Admin Application Management
  As a provider or admin, I want to manage patient enrollment applications efficiently.

  Scenario: An admin logs in and filters the application list
    Given I am an admin user
    When I log in to the admin portal
    And I navigate to the dashboard
    Then I should see a table of patient applications
    When I filter the list by status "Submitted"
    Then I should only see applications with the "Submitted" status
    When I sort the list by "Submission Date" in descending order
    Then the most recent applications should appear at the top

  Scenario: An admin user has access to settings not visible to a provider
    Given I am logged in as an admin user
    When I view the navigation menu
    Then I should see a link to "System Settings"
    When I log out and log in as a provider user
    And I view the navigation menu
    Then I should not see a link to "System Settings"

  Scenario Outline: A provider makes a decision on an application
    Given I am a provider logged into the portal
    And I am viewing a patient application with status "In Review"
    When I click the "<action>" button
    And I provide the reason "<reason>"
    And I confirm the action
    Then the application status should be updated to "<new_status>"
    And a notification should be sent to the patient with the reason
    And an entry should be created in the audit log for this action

    Examples:
      | action                    | reason                                | new_status        |
      | "Approve"                 | "All documents are verified."         | "Approved"        |
      | "Reject"                  | "Does not meet eligibility criteria." | "Rejected"        |
      | "Request More Information"| "The uploaded ID is not legible."     | "Action Required" |

# User Story 10: System Security and Compliance
Feature: System Security and Role-Based Access Control
  As a system stakeholder, I want to ensure the application is secure and compliant.

  Scenario: A patient cannot access another patient's data
    Given patient "A" is logged in
    And patient "B" has an application with ID "app-b-123"
    When patient "A" attempts to access the API endpoint "/api/v1/enrollment/applications/app-b-123"
    Then the request should be denied with a "403 Forbidden" status code

  Scenario: An admin action on PHI is recorded in the audit log
    Given an admin is logged in
    And a patient application with ID "app-c-456" exists
    When the admin views the details of application "app-c-456"
    Then an audit log entry should be created with the following data:
      | Field              | Value                         |
      | user_id            | The admin's user ID           |
      | action             | "VIEWED_PATIENT_APPLICATION"  |
      | target_entity_type | "enrollment_application"      |
      | target_entity_id   | "app-c-456"                   |

# User Story 11 & 12: Performance and Accessibility
Feature: Application Performance and Accessibility
  As a user, I want a fast and accessible application experience.

  Scenario: Key pages load within performance targets
    Given I am a user with typical network conditions
    When I navigate to the "Home" page
    Then the Largest Contentful Paint (LCP) should be less than 2.5 seconds
    When I log in as a patient and navigate to my "Dashboard"
    Then the Largest Contentful Paint (LCP) should be less than 2.5 seconds

  Scenario: A user can navigate the registration form using only the keyboard
    Given I am on the registration page
    When I press the "Tab" key
    Then the focus should move to the "Name" input field
    When I press the "Tab" key again
    Then the focus should move to the "Email" input field
    When I am focused on the "Submit" button and press "Enter"
    Then the form should be submitted

# User Story 13: BDD Feature File Generation
Feature: BDD Feature File Generation Tool
  As a QA Engineer or Developer, I want to generate BDD feature files from use cases.

  Scenario: Generate a feature file for the patient registration use case
    Given I am a developer in the project's command line interface
    When I run the command "python manage.py generate_feature patient_registration"
    Then a file named "patient_registration.feature" should be created
    And the file should contain valid Gherkin syntax
    And the file should include a scenario for "Successful registration using an email address"
    And the file should include a scenario for "Attempt to register with an existing email"