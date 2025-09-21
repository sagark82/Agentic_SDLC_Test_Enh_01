```markdown
## User Stories for Patient Enrollment Process

### User Story 1: Secure Patient Enrollment API Endpoint

*   **As the Patient Enrollment Portal,**
*   **I want to securely submit new patient enrollment forms,**
*   **so that the patient registration process can be initiated reliably and confidentially.**

**Acceptance Criteria:**

*   **GIVEN** a new patient enrollment form is successfully submitted through the Patient Enrollment Portal (web/mobile).
*   **WHEN** the form data is sent to the system.
*   **THEN** the system automatically triggers the patient registration process via an exposed HTTPS REST API endpoint.
*   **AND** the API endpoint is deployed on CloudHub (or the hospital's private cloud).
*   **AND** the API validates the incoming request using a JSON Web Token (JWT) for authentication.
*   **AND** the API decrypts any Protected Health Information (PHI) within the payload using configured encryption before further processing.
*   **AND** the API validates the incoming JSON payload against its predefined API specification (e.g., RAML/OpenAPI schema) to ensure data structure and type compliance.

---

### User Story 2: Patient Data Mapping and Transformation

*   **As the system,**
*   **I want to accurately map submitted patient enrollment data to the healthcare database schema,**
*   **so that patient information is correctly structured for storage.**

**Acceptance Criteria:**

*   **GIVEN** a valid, authenticated, and decrypted patient enrollment payload is received by the API.
*   **WHEN** the system processes the payload.
*   **THEN** the system transforms the incoming data using DataWeave (or equivalent data transformation tool).
*   **AND** the `Patient Full Name` field from the enrollment form is mapped to the `patient_name` column in the Patients table.
*   **AND** a unique system-generated `Patient ID` is created and mapped to the `patient_id` column.
*   **AND** the `Date of Birth` field is mapped to the `dob` column.
*   **AND** the `Gender` field is mapped to the `gender` column.
*   **AND** the `Address` field is mapped to the `address_line1` column.
*   **AND** the `City` field is mapped to the `city` column.
*   **AND** the `State/Region` field is mapped to the `state` column.
*   **AND** the `Postal Code` field is mapped to the `postal_code` column.
*   **AND** the `Phone Number` field is mapped to the `contact_phone` column.
*   **AND** the `Insurance Policy Number` field is mapped to the `insurance_id` column.

---

### User Story 3: New Patient Record Insertion

*   **As the system,**
*   **I want to insert the transformed patient data as a new record into the Patients table,**
*   **so that new patients are successfully registered in the healthcare database.**

**Acceptance Criteria:**

*   **GIVEN** patient data has been successfully mapped and transformed according to the healthcare database schema.
*   **WHEN** the system attempts to store the data.
*   **THEN** a new record containing the mapped data is inserted into the `Patients` table in the target Healthcare Patient DB (PostgreSQL / Oracle Healthcare instance).
*   **AND** the database connection uses securely stored credentials.
*   **AND** the insertion operation is performed via a dedicated database connector (e.g., MuleSoft Database Connector).
*   **AND** upon successful insertion, the process completes without triggering an error notification.

---

### User Story 4: Database Insertion Failure Notification & Logging

*   **As the Healthcare IT Support Group,**
*   **I want to be automatically notified when a patient record insertion fails,**
*   **so that I can quickly investigate and resolve data integrity issues.**

**Acceptance Criteria:**

*   **GIVEN** an attempt to insert a new patient record into the `Patients` table fails (e.g., due to database unavailability, data validation error, duplicate patient ID, network issue, or other system errors).
*   **WHEN** the insertion failure occurs.
*   **THEN** the system's global error handler catches the exception.
*   **AND** the system logs the failure details, including the error message, timestamp, and relevant contextual information (e.g., patient ID if generated, error type).
*   **AND** all sensitive data (e.g., `Insurance ID`, `SSN` if present in the original payload) is masked in the logs to comply with security requirements.
*   **AND** an email notification is automatically sent to the configured Healthcare IT support group.
*   **AND** the email contains sufficient details about the failure (e.g., error type, timestamp, patient identifier if available and safe to include, brief context) without exposing raw Protected Health Information (PHI).