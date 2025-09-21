# Patient Enrollment System Integration - Testing Document

## 1. Test Strategy

### 1.1 Introduction

This document outlines the testing strategy for the Patient Enrollment System Integration project. The primary goal is to ensure that the Patient Enrollment API securely and reliably processes patient enrollment data, transforms it, and stores it in the Healthcare Patient Database, while adhering to security, data integrity, and error handling requirements.

### 1.2 Scope of Testing

**In Scope:**

*   **Patient Enrollment API (MuleSoft Application):**
    *   API endpoint availability and accessibility (HTTPS/TLS).
    *   Request validation (structure, data types).
    *   JWT token validation and authorization.
    *   Data transformation logic (DataWeave mapping from source payload to target DB schema).
    *   Database insertion functionality and data integrity.
    *   Error handling mechanisms (logging, email notifications for failures).
    *   Sensitive data masking in system logs.
    *   Secure database connectivity.
*   **Integration with Healthcare Patient DB:**
    *   Successful record creation.
    *   Accuracy of mapped data in the database.
    *   Handling of database-specific constraints (e.g., duplicate `patient_id`).
*   **Security Aspects:**
    *   HTTPS/TLS encryption in transit.
    *   JWT token-based authentication.
    *   PHI masking in logs.

**Out of Scope:**

*   The Patient Enrollment Portal UI/UX (front-end testing).
*   Performance testing beyond basic load checks (dedicated performance testing phase would follow).
*   Detailed infrastructure testing of CloudHub or the Healthcare Patient DB itself.
*   Security penetration testing (will be a separate security assessment).

### 1.3 Testing Objectives

*   **Functionality:** Verify that all patient enrollment data is submitted, transformed, and stored accurately according to user stories and acceptance criteria.
*   **Data Integrity:** Ensure that data mapping is correct, and patient records are accurately populated in the target database.
*   **Security:** Validate that sensitive patient information (PHI) is protected in transit, at rest (within the API and logs), and that only authorized systems can access the API.
*   **Reliability & Resilience:** Confirm that the system gracefully handles various error conditions (e.g., invalid input, database failures, duplicate IDs) and provides appropriate logging and notifications.
*   **Performance:** Ensure the API can handle expected load efficiently without significant degradation (basic checks within this phase).
*   **Compliance:** Validate adherence to data privacy regulations through PHI encryption and masking.

### 1.4 Types of Testing

1.  **Unit Testing:**
    *   **Purpose:** To test individual components (e.g., DataWeave transformations, custom Mule flows, sub-flows) in isolation.
    *   **Focus:** Verify logic correctness, data transformations, and error paths within specific modules.
    *   **Tools:** MUnit (for MuleSoft applications).

2.  **API Testing (Functional):**
    *   **Purpose:** To validate the functionality of the RESTful Patient Enrollment API endpoint.
    *   **Focus:**
        *   Verify correct HTTP methods, endpoints, request/response formats.
        *   Validate request payload against RAML/OpenAPI schema.
        *   Test all acceptance criteria related to API interaction (e.g., valid input, invalid input, successful responses, error responses).
        *   Verify `201 Created` for successful enrollments and appropriate error codes (`400`, `401`, `500`).
    *   **Tools:** Postman, Newman, ReadyAPI, Karate DSL.

3.  **Integration Testing:**
    *   **Purpose:** To verify the end-to-end flow of the system, including the interaction between the Patient Enrollment API, DataWeave transformation, and the Healthcare Patient DB.
    *   **Focus:**
        *   Successful data flow from API call to database insertion.
        *   Verification of data mapping and persistence accuracy in the database.
        *   Testing of error handling and notification mechanisms across component boundaries.
    *   **Tools:** MUnit (for simulating external systems), Postman/Newman, direct database queries.

4.  **Data Integrity Testing:**
    *   **Purpose:** To ensure that data is transformed and stored accurately and consistently.
    *   **Focus:**
        *   Confirm all source fields are correctly mapped to target database fields.
        *   Verify data types, constraints, and uniqueness (e.g., `patient_id`).
        *   Validate system-generated fields (e.g., `patient_id`, `created_at`).
    *   **Tools:** SQL queries, automated scripts comparing source and target data.

5.  **Security Testing:**
    *   **Purpose:** To validate the security mechanisms implemented.
    *   **Focus:**
        *   **Authentication:** Verify JWT token validation (valid, invalid, missing tokens).
        *   **Authorization:** Ensure only authorized systems can access the API.
        *   **Encryption in Transit:** Confirm HTTPS/TLS is enforced for all API communication (manual verification and network traffic analysis).
        *   **Secure Credential Storage:** Verify database credentials are not exposed (manual review of configuration).
        *   **PHI Protection:** Validate sensitive data masking in logs.
    *   **Tools:** Postman, OWASP ZAP (for basic vulnerability scanning), manual inspection.

6.  **Error Handling & Resilience Testing:**
    *   **Purpose:** To verify how the system reacts to expected and unexpected error conditions.
    *   **Focus:**
        *   **Invalid Input:** Test various malformed or incomplete payloads.
        *   **Database Failures:** Simulate database unavailability, connection errors, or constraint violations (e.g., duplicate `patient_id`).
        *   **External Service Failures:** (If applicable, though DB is the primary external dependency here).
        *   **Logging:** Verify error messages, stack traces, and relevant context are logged.
        *   **Notifications:** Confirm email notifications are sent to IT support for critical failures.
        *   **Global Error Handler:** Ensure consistent error responses and processing.
    *   **Tools:** MUnit (for mocking failures), Postman, database manipulation, email client for verification.

7.  **Logging & Auditing Testing:**
    *   **Purpose:** To ensure that system logs are generated correctly and comply with privacy requirements.
    *   **Focus:**
        *   Verify log formats, levels, and content for both success and failure scenarios.
        *   Crucially, validate that `insurance_id` and any other identified PHI are correctly masked in all log entries.
        *   Ensure masked data is not easily reversible.
    *   **Tools:** Log file analysis, automated log parsers.

8.  **Regression Testing:**
    *   **Purpose:** To ensure that new changes or bug fixes do not negatively impact existing functionality.
    *   **Focus:** Re-execute a subset of critical functional and integration tests after each new deployment or significant code change.
    *   **Tools:** Automated test suites (e.g., Postman collections integrated with Newman in CI/CD).

9.  **User Acceptance Testing (UAT):**
    *   **Purpose:** To obtain formal sign-off from business stakeholders that the system meets their requirements.
    *   **Focus:** End-to-end business scenarios, data accuracy, and overall system usability from a business perspective.
    *   **Tools:** Business users, manual testing.

### 1.5 Test Environment

*   Dedicated QA environment mirroring production setup (CloudHub deployment, Healthcare Patient DB).
*   Access to log management tools.
*   Access to email client for notification verification.

### 1.6 Roles and Responsibilities

*   **QA Automation Engineer:** Develop and execute test plans, create automation scripts, report defects, manage test environments.
*   **Developers:** Conduct unit testing, fix defects, support QA activities.
*   **Scrum Master/Project Manager:** Oversee testing progress, facilitate communication.
*   **Business Analyst/Product Owner:** Define acceptance criteria, participate in UAT.

---

## 2. Automation Test Scripts (BDD Feature File)

Feature: Patient Enrollment System Integration

  As a Patient Enrollment Portal
  I want to securely enroll new patients into the healthcare system
  So that patient records are created, processed, and maintained with integrity and privacy.

  Background:
    Given the Patient Enrollment API endpoint is available and secured with HTTPS/TLS
    And a secure connection to the Healthcare Patient Database is established

  Scenario Outline: Successfully enroll a new patient with valid data

    Given a valid JWT token for authentication
    And the following patient enrollment data is prepared:
      | Field                 | Value                                  |
      |-----------------------|----------------------------------------|
      | patientFullName       | <patientFullName>                      |
      | dateOfBirth           | <dateOfBirth>                          |
      | gender                | <gender>                               |
      | address               | <address>                              |
      | city                  | <city>                                 |
      | stateRegion           | <stateRegion>                          |
      | postalCode            | <postalCode>                           |
      | phoneNumber           | <phoneNumber>                          |
      | insurancePolicyNumber | <insurancePolicyNumber>                |
    When the Patient Enrollment Portal submits the enrollment data to the API
    Then the API should return a 201 Created response
    And the response body should contain a success message and a unique patient ID
    And a new patient record should be successfully inserted into the Healthcare Patient Database
    And the inserted record in the database should match the submitted data, including the generated patient ID
    And system logs should record the successful enrollment with 'insurance_id' masked

    Examples:
      | patientFullName | dateOfBirth | gender | address       | city        | stateRegion | postalCode | phoneNumber   | insurancePolicyNumber |
      | John Doe        | 1980-01-15  | Male   | 123 Main St   | Anytown     | CA          | 90210      | 555-123-4567  | INS-789012345         |
      | Jane Smith      | 1992-07-22  | Female | 456 Oak Ave   | Springfield | IL          | 62704      | 555-987-6543  | INS-11223344          |
      | Alex Johnson    | 11995-03-01 | Other  | 789 Pine Rd   | Metropolis  | NY          | 10001      | 555-444-5555  | INS-99887766          |

  Scenario: Validate Data Mapping and Transformation Logic

    Given an incoming patient enrollment payload with the following structure:
      | Source Field            | Example Value             |
      |-------------------------|---------------------------|
      | patientFullName         | Test Patient              |
      | dateOfBirth             | 2000-01-01                |
      | gender                  | Male                      |
      | address                 | 100 Test St               |
      | city                    | Testville                 |
      | stateRegion             | TX                        |
      | postalCode              | 75001                     |
      | phoneNumber             | 111-222-3333              |
      | insurancePolicyNumber   | TEST-INS-1234             |
    When the Patient Enrollment API processes this data for database insertion
    Then the transformed data for the database should have the following mappings:
      | Target DB Field     | Source Field Name (or Logic)      | Expected Target Value (or Format) |
      |---------------------|-----------------------------------|-----------------------------------|
      | patient_id          | System Generated                  | Unique UUID (e.g., PAT-UUID-...)  |
      | patient_name        | patientFullName                   | Test Patient                      |
      | dob                 | dateOfBirth                       | 2000-01-01                        |
      | gender              | gender                            | Male                              |
      | address_line1       | address                           | 100 Test St                       |
      | city                | city                              | Testville                         |
      | state               | stateRegion                       | TX                                |
      | postal_code         | postalCode                        | 75001                             |
      | contact_phone       | phoneNumber                       | 111-222-3333                      |
      | insurance_id        | insurancePolicyNumber             | TEST-INS-1234                     |
      | created_at          | System Generated                  | Current Timestamp                 |
      | updated_at          | System Generated                  | Current Timestamp                 |

  Scenario Outline: Handle unauthorized API access

    Given a patient enrollment payload is prepared
    When an API request is made with <Authentication_Type>
    Then the API should return a <Status_Code> response
    And the response body should contain an error message indicating <Error_Reason>
    And system logs should record the unauthorized access attempt

    Examples:
      | Authentication_Type | Status_Code | Error_Reason                       |
      | no JWT token        | 401         | Unauthorized: Missing JWT token    |
      | an invalid JWT token| 401         | Unauthorized: Invalid JWT token    |
      | an expired JWT token| 401         | Unauthorized: JWT token expired    |

  Scenario: Handle database insertion failure - Duplicate Patient ID

    Given a valid JWT token for authentication
    And a new patient enrollment payload is prepared
    And the system attempts to generate a 'patient_id'
    And a patient record with the same generated 'patient_id' already exists in the Healthcare Patient Database
    When the Patient Enrollment Portal submits the enrollment data to the API
    Then the API should return a 500 Internal Server Error
    And a failure must be logged with sufficient detail, masking sensitive PHI
    And an email notification must be sent to the designated Healthcare IT support group

  Scenario: Handle database insertion failure - Database Unavailable

    Given a valid JWT token for authentication
    And a new patient enrollment payload is prepared
    And the Healthcare Patient Database is unavailable or inaccessible
    When the Patient Enrollment Portal submits the enrollment data to the API
    Then the API should return a 500 Internal Server Error
    And a failure must be logged with sufficient detail, masking sensitive PHI
    And an email notification must be sent to the designated Healthcare IT support group

  Scenario: Verify sensitive data masking in system logs

    Given a patient enrollment request containing the 'insurancePolicyNumber' field
    When the system processes the request and generates log entries
    Then the 'insurance_id' value in the log entries should be masked (e.g., showing only last 4 digits)
    And any other identified Protected Health Information (PHI) in the log entries should also be masked
    And the masked data should not be easily reversible to its original form