# User Stories for Patient Enrollment Processing

## User Story 1: Automated Patient Enrollment Intake

*   **As a Patient Enrollment Portal,**
*   **I want the system to automatically receive and process new patient enrollment submissions,**
*   **so that patient data is efficiently and immediately moved into the patient management workflow upon successful submission.**

### Acceptance Criteria:

*   **GIVEN** a new Patient Enrollment Form is successfully submitted through the Patient Enrollment Portal.
*   **WHEN** the submission occurs.
*   **THEN** the exposed REST API endpoint for patient enrollment processing is automatically invoked via HTTPS.
*   **AND** the API validates the incoming request payload against the defined API Specification (e.g., RAML/OpenAPI).
*   **AND** the API validates the JWT token provided for authentication and authorization.
*   **AND** the system logs the initiation of the enrollment process, ensuring any Protected Health Information (PHI) is masked according to logging policies.

---

## User Story 2: Patient Data Mapping and Secure Storage

*   **As a Patient Management System,**
*   **I want to accurately map and securely store new patient enrollment data into the Patients database table,**
*   **so that complete, correct, and protected patient records are maintained.**

### Acceptance Criteria:

*   **GIVEN** a valid, authenticated, and authorized new patient enrollment request payload is received by the API.
*   **WHEN** the system processes the request.
*   **THEN** the system uses a data transformation mechanism (e.g., DataWeave) to correctly map the following fields from the enrollment form to the `Patients` table schema:
    *   Patient Full Name → `patient_name`
    *   Date of Birth → `dob`
    *   Gender → `gender`
    *   Address → `address_line1`
    *   City → `city`
    *   State/Region → `state`
    *   Postal Code → `postal_code`
    *   Phone Number → `contact_phone`
    *   Insurance Policy Number → `insurance_id`
*   **AND** the system generates a unique `patient_id` for the new patient record.
*   **AND** a new record containing all mapped data is successfully inserted into the target Healthcare Patient Database's `Patients` table using secure database credentials.
*   **AND** all Protected Health Information (PHI) is encrypted during transit and at rest, adhering to security and compliance requirements.

---

## User Story 3: Patient Enrollment Processing Failure Notification

*   **As a Healthcare IT Support Group,**
*   **I want to be automatically notified when a new patient enrollment record fails to be saved to the database,**
*   **so that I can promptly investigate, diagnose, and resolve data integrity issues and ensure patient data is not lost.**

### Acceptance Criteria:

*   **GIVEN** an attempt to insert a new patient record into the `Patients` table fails for any reason (e.g., database unavailability, data validation error, duplicate patient ID, network connectivity issue, etc.).
*   **WHEN** the database insertion operation fails.
*   **THEN** the failure event is logged by the global error handler with relevant details, including the error message and context.
*   **AND** all sensitive data (e.g., `insurance_id`, `patient_name`, `dob`) within the logs is masked as per the defined logging policy.
*   **AND** an email notification is automatically sent via the Email Connector to the configured Healthcare IT support group.
*   **AND** the email notification includes sufficient non-PHI details to identify the failed transaction and the reason for failure (e.g., timestamp, error type, a unique transaction ID).