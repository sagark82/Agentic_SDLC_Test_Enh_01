## User Stories for Patient Enrollment Processing

### User Story 1: Triggering Patient Enrollment Processing

*   **As a:** System
*   **I want to:** automatically trigger the patient enrollment data processing
*   **So that:** new patient data is processed efficiently and without manual intervention after successful submission.

**Acceptance Criteria:**

*   **GIVEN** a new Patient enrollment form is successfully submitted through the portal
*   **WHEN** the submission is confirmed
*   **THEN** the process for creating a new patient record in the healthcare database is automatically initiated.

---

### User Story 2: Mapping Patient Enrollment Data

*   **As a:** System
*   **I want to:** accurately map specific fields from a submitted Patient Enrollment Form to the Patients table schema
*   **So that:** the correct information can be stored consistently in the healthcare database.

**Acceptance Criteria:**

*   **GIVEN** a successfully submitted Patient Enrollment Form
*   **WHEN** the data mapping process is executed
*   **THEN** the following fields are correctly mapped:
    *   "Patient Full Name" from the form maps to `patient_name` in the database.
    *   "Patient ID (system-generated)" from the form maps to `patient_id` in the database.
    *   "Date of Birth" from the form maps to `dob` in the database.
    *   "Gender" from the form maps to `gender` in the database.
    *   "Address" from the form maps to `address_line1` in the database.
    *   "City" from the form maps to `city` in the database.
    *   "State/Region" from the form maps to `state` in the database.
    *   "Postal Code" from the form maps to `postal_code` in the database.
    *   "Phone Number" from the form maps to `contact_phone` in the database.
    *   "Insurance Policy Number" from the form maps to `insurance_id` in the database.

---

### User Story 3: Storing New Patient Records

*   **As a:** System
*   **I want to:** insert the mapped patient enrollment data into the Patients table
*   **So that:** a new patient record is successfully created and persisted in the healthcare database.

**Acceptance Criteria:**

*   **GIVEN** valid mapped patient data from a submitted enrollment form
*   **WHEN** the insertion process is executed
*   **THEN** a new record containing all mapped fields (as specified in US2) is successfully inserted into the `Patients` table of the target database.
*   **AND** the newly created patient record is accessible for subsequent healthcare operations and queries.

---

### User Story 4: Handling Patient Record Creation Failures

*   **As a:** System
*   **I want to:** log and notify relevant personnel about any failures during patient record creation
*   **So that:** issues can be promptly identified, diagnosed, and resolved, ensuring data integrity and operational continuity.

**Acceptance Criteria:**

*   **GIVEN** a failure occurs during the insertion of a new patient record into the `Patients` table
*   **WHEN** the insertion attempt fails (e.g., due to database unavailability, data validation error, or duplicate patient ID)
*   **THEN** the system logs the failure details, including:
    *   A timestamp of the failure.
    *   The specific error message or exception.
    *   Relevant contextual data (e.g., the patient ID or form submission identifier that caused the failure).
*   **AND** an email notification is automatically sent to the "Healthcare IT support group".
*   **AND** the email notification includes:
    *   A clear indication of the failure.
    *   The error message and type of failure.
    *   Sufficient context to identify the affected patient enrollment (e.g., form ID, patient name).
    *   A reference to where the detailed log entry can be found.