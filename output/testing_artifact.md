# Test Strategy and Plan for Patient Enrollment Processing System

## 1. Introduction
This document outlines the test strategy and plan for the new Patient Enrollment Processing System. Its purpose is to ensure that the system meets all specified functional and non-functional requirements, processes patient enrollment data accurately, efficiently, and handles errors gracefully.

## 2. Test Strategy

### 2.1. Scope of Testing
The testing scope encompasses the backend processing flow for patient enrollment, triggered by a successful submission via the Patient Enrollment Portal. This includes:
*   **API Gateway:** Verification of request reception, initial validation, and routing.
*   **Enrollment Submission Service:** Confirmation of message publishing to the Message Queue.
*   **Message Queue:** Validation of message persistence, delivery, retry mechanisms, and Dead-Letter Queue (DLQ) functionality.
*   **Patient Processing Service:** Core functionality testing including data consumption, mapping, validation, database insertion, logging, and notification triggering.
*   **Healthcare Database:** Verification of data storage, schema compliance, and data integrity in the `Patients` table.
*   **Logging Service:** Validation of detailed log capture for all events, especially failures.
*   **Notification Service:** Confirmation of email notifications being sent with correct content to the designated recipients.

**Out of Scope:**
*   The Patient Enrollment Portal's UI/UX and client-side validations.
*   Comprehensive security penetration testing (will be a separate engagement).
*   Performance testing beyond basic load simulation.

### 2.2. Test Objectives
The primary objectives of testing are to:
1.  **Verify Automatic Triggering (US1):** Ensure that successful patient enrollment submissions automatically initiate the backend processing workflow.
2.  **Validate Data Mapping (US2):** Confirm that all specified fields from the enrollment form are accurately mapped to the `Patients` table schema.
3.  **Ensure Record Storage (US3):** Verify that new patient records are successfully inserted and persisted in the Healthcare Database with correct data.
4.  **Confirm Robust Failure Handling (US4):** Validate that the system correctly identifies, logs, and notifies relevant personnel about failures during record creation.
5.  **Assess System Resilience:** Verify the system's ability to handle transient errors through retry mechanisms and manage persistent failures via a Dead-Letter Queue (DLQ).
6.  **Ensure Data Integrity:** Confirm that data stored in the database is accurate, consistent, and adheres to schema constraints.
7.  **Validate Logging and Notifications:** Ensure that all required log details are captured and notifications contain accurate and sufficient information for diagnosis.

### 2.3. Types of Testing

*   **Unit Testing:**
    *   **Focus:** Individual components, functions, and methods (e.g., data mapping logic, database interaction logic, logging utility, notification sender).
    *   **Methodology:** Developer-led testing, typically using frameworks like JUnit, NUnit, Pytest.
*   **Integration Testing:**
    *   **Focus:** Interactions between different services and components (e.g., API Gateway to Enrollment Submission Service, Enrollment Submission Service to Message Queue, Patient Processing Service to Healthcare Database, Patient Processing Service to Logging/Notification Services).
    *   **Methodology:** Automated tests simulating component interactions, using mock services or actual integrated environments.
*   **API Testing:**
    *   **Focus:** Testing the `/api/v1/patient-enrollment` endpoint directly to verify request handling, response codes, and initial data validation.
    *   **Methodology:** Automated tests using tools like Postman, Newman, RestAssured, or custom scripts.
*   **End-to-End Testing:**
    *   **Focus:** Simulating the entire patient enrollment workflow from an API submission to successful database record creation or failure handling (including log and notification verification).
    *   **Methodology:** Automated BDD scenarios (as detailed below) executed against a fully integrated test environment.
*   **Database Testing:**
    *   **Focus:** Directly querying the Healthcare Database to verify data persistence, schema compliance, data integrity, and correctness of mapped values after processing.
    *   **Methodology:** SQL queries, automated scripts, and ORM layer tests.
*   **Negative Testing / Error Handling Testing:**
    *   **Focus:** Testing the system's behavior with invalid inputs, edge cases, missing required data, duplicate entries, and simulated service failures (e.g., database unavailability, network issues).
    *   **Methodology:** Dedicated test cases covering US4, including verification of detailed logging and notification content as per HLD.
*   **Resilience Testing:**
    *   **Focus:** Validating the Message Queue's retry mechanisms for transient errors and the proper routing of messages to a Dead-Letter Queue (DLQ) for persistent or exhausted-retry failures.
    *   **Methodology:** Simulating transient and persistent failures and observing message flow and system recovery.
*   **Performance Testing (Basic):**
    *   **Focus:** Ensuring the API Gateway and the initial message queuing can handle expected load without significant latency.
    *   **Methodology:** Basic load tests on the `/api/v1/patient-enrollment` endpoint to confirm responsiveness.
*   **Security Testing (Basic):**
    *   **Focus:** Verifying basic security aspects like authentication/authorization for API access and data integrity during transmission.
    *   **Methodology:** Checking API endpoint access controls and data sanitization.

## 3. Automation Test Scripts (BDD Feature File)

The following BDD feature file, written in Gherkin, provides a high-level description of the automated test scenarios. These scenarios cover the functional requirements outlined in the User Stories and incorporate feedback regarding detailed logging, notification content, and resilience mechanisms.

Feature: Patient Enrollment Processing

  As a System, I want to process new patient enrollment data efficiently and reliably,
  mapping it to a standardized schema, storing it in the healthcare database,
  and handling any failures gracefully through detailed logging and notifications.

  Background:
    Given the Patient Enrollment Processing System components are operational
    And the Healthcare Database is accessible
    And the Logging Service is configured to receive logs
    And the Notification Service is configured to send emails to "Healthcare IT support group"

  Scenario Outline: Successfully process and store a new patient enrollment
    Given a new Patient enrollment form is submitted through the portal with the following data:
      | Field Name                    | Value                     |
      | Patient Full Name             | <patient_full_name>       |
      | Patient ID (system-generated) | <patient_id_system_generated> |
      | Date of Birth                 | <date_of_birth>           |
      | Gender                        | <gender>                  |
      | Address                       | <address>                 |
      | City                          | <city>                    |
      | State/Region                  | <state_region>            |
      | Postal Code                   | <postal_code>             |
      | Phone Number                  | <phone_number>            |
      | Insurance Policy Number       | <insurance_policy_number> |
    When the submission is confirmed by the API Gateway with a 202 Accepted response
    Then the process for creating a new patient record in the healthcare database is automatically initiated
    And the following fields are correctly mapped and inserted into the `Patients` table:
      | Form Field Name               | DB Column Name    |
      | Patient Full Name             | patient_name      |
      | Patient ID (system-generated) | patient_id        |
      | Date of Birth                 | dob               |
      | Gender                        | gender            |
      | Address                       | address_line1     |
      | City                          | city              |
      | State/Region                  | state             |
      | Postal Code                   | postal_code       |
      | Phone Number                  | contact_phone     |
      | Insurance Policy Number       | insurance_id      |
    And a new record with patient ID "<patient_id_system_generated>" exists in the `Patients` table
    And the `created_at` and `updated_at` fields for patient ID "<patient_id_system_generated>" are system-generated timestamps

    Examples:
      | patient_full_name | patient_id_system_generated | date_of_birth | gender | address       | city      | state_region | postal_code | phone_number   | insurance_policy_number |
      | Jane Doe          | PAT-2023-0002               | 1985-03-20    | Female | 456 Oak Ave   | Sometown  | NY           | 10001       | +12125551234   | INS-XYZ-67890           |
      | Bob Smith         | PAT-2023-0003               | 1970-11-01    | Male   | 789 Pine Ln   | Villaget  | TX           | 75001       | +19725550000   | INS-DEF-11223           |
      | Alice Johnson     | PAT-2023-0004               | 2000-07-25    | Female | 101 Elm St    | Newberry  | MA           | 02108       | +16175559876   | INS-GHI-44556           |


  Scenario: Handle duplicate patient ID failure during record creation
    Given a new Patient enrollment form is submitted with patient ID "PAT-DUPLICATE-001"
    And a patient record with ID "PAT-DUPLICATE-001" already exists in the `Patients` table
    When the Patient Processing Service attempts to insert the new record
    Then a failure occurs during the insertion of the new patient record
    And the system logs the failure details including:
      | Log Field               | Expected Content                                     |
      | error_type              | DATABASE_UNIQUE_CONSTRAINT_VIOLATION                 |
      | error_message           | CONTAINS "duplicate key value violates unique constraint" |
      | submission_id           | NOT NULL                                             |
      | patient_id_attempted    | "PAT-DUPLICATE-001"                                  |
      | affected_form_context   | CONTAINS "PAT-DUPLICATE-001"                         |
      | service_instance_id     | NOT NULL                                             |
      | trace_id                | NOT NULL                                             |
    And an email notification is sent to "Healthcare IT support group" with the following content:
      | Email Part              | Expected Content                                     |
      | Subject                 | CONTAINS "[CRITICAL] Patient Enrollment Processing Failure - Submission ID:" |
      | Body                    | CONTAINS "Dear Healthcare IT Support Group,"         |
      | Body                    | CONTAINS "Failure Type: DATABASE_UNIQUE_CONSTRAINT_VIOLATION" |
      | Body                    | CONTAINS "Error Message: CONTAINS 'Duplicate entry for patient ID \\'PAT-DUPLICATE-001\\''" |
      | Body                    | CONTAINS "Affected Patient Enrollment Details:"      |
      | Body                    | CONTAINS "Patient Name (attempted):"                 |
      | Body                    | CONTAINS "Patient ID (attempted): PAT-DUPLICATE-001" |
      | Body                    | CONTAINS "Log Reference: CONTAINS 'submission_id:' AND CONTAINS 'trace_id:'" |
    And the message for "PAT-DUPLICATE-001" is moved to the Dead-Letter Queue after retries are exhausted


  Scenario: Handle invalid patient data failure during record creation (e.g., missing required field)
    Given a new Patient enrollment form is submitted with patient ID "PAT-INVALID-001" and missing "Date of Birth"
    When the Patient Processing Service attempts to map and validate the new record
    Then a failure occurs due to data validation error
    And the system logs the failure details including:
      | Log Field               | Expected Content                                     |
      | error_type              | DATA_VALIDATION_ERROR                                |
      | error_message           | CONTAINS "Date of Birth cannot be null"              |
      | submission_id           | NOT NULL                                             |
      | patient_id_attempted    | "PAT-INVALID-001"                                    |
      | affected_form_context   | CONTAINS "PAT-INVALID-001"                           |
      | service_instance_id     | NOT NULL                                             |
      | trace_id                | NOT NULL                                             |
    And an email notification is sent to "Healthcare IT support group" with the following content:
      | Email Part              | Expected Content                                     |
      | Subject                 | CONTAINS "[CRITICAL] Patient Enrollment Processing Failure - Submission ID:" |
      | Body                    | CONTAINS "Dear Healthcare IT Support Group,"         |
      | Body                    | CONTAINS "Failure Type: DATA_VALIDATION_ERROR"       |
      | Body                    | CONTAINS "Error Message: CONTAINS 'Date of Birth cannot be null'" |
      | Body                    | CONTAINS "Affected Patient Enrollment Details:"      |
      | Body                    | CONTAINS "Patient Name (attempted):"                 |
      | Body                    | CONTAINS "Patient ID (attempted): PAT-INVALID-001"   |
      | Body                    | CONTAINS "Log Reference: CONTAINS 'submission_id:' AND CONTAINS 'trace_id:'" |
    And the message for "PAT-INVALID-001" is moved to the Dead-Letter Queue after retries are exhausted


  Scenario: Validate retry mechanism for transient database errors
    Given a new Patient enrollment form is submitted with patient ID "PAT-RETRY-001"
    And the Healthcare Database is initially unavailable for 2 attempts
    And the Healthcare Database becomes available on the 3rd attempt
    When the Patient Processing Service attempts to insert the new record
    Then the Patient Processing Service retries the insertion 2 times
    And the Patient Processing Service successfully inserts the record on the 3rd attempt
    And a new record with patient ID "PAT-RETRY-001" exists in the `Patients` table
    And no critical failure email notification is sent for this transient issue
    And the message for "PAT-RETRY-001" is acknowledged and removed from the Message Queue


  Scenario: Validate Dead-Letter Queue for persistent errors after retries
    Given a new Patient enrollment form is submitted with patient ID "PAT-DLQ-001"
    And the Healthcare Database consistently rejects insertion for "PAT-DLQ-001" due to a persistent error (e.g., specific data type mismatch)
    And the Message Queue is configured to retry 3 times before moving to DLQ
    When the Patient Processing Service attempts to insert the new record
    Then the Patient Processing Service attempts to insert the record 3 times
    And after 3 retries, the record insertion still fails
    And the system logs the failure details for each attempt, including `error_type` as a persistent error
    And an email notification is sent to "Healthcare IT support group" for the final failure
    And the message for "PAT-DLQ-001" is moved to the Dead-Letter Queue
    And no record with patient ID "PAT-DLQ-001" exists in the `Patients` table