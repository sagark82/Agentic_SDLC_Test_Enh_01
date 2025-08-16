# High-Level Design: Pharma Inc. Corporate Website

## 1. Architecture
A simple client-server architecture will be used. A Python Flask backend will serve static HTML/CSS/JS files and provide a single API endpoint for the contact form. This lightweight approach is suitable for a low-traffic corporate website.

## 2. Components

### Frontend
-   **index.html:** The main landing page.
-   **about.html:** Company information page.
-   **products.html:** Product listing page.
-   **contact.html:** Contact form and details page.
-   **css/style.css:** Shared stylesheet for a consistent look and feel.
-   **js/main.js:** JavaScript for handling the contact form submission.

### Backend (`app.py`)
-   A Python Flask application.
-   Serves the static HTML pages from the root and static assets from their respective folders.
-   Provides a single API endpoint: `POST /api/contact`.

## 3. API Specification

### `POST /api/contact`
-   **Description:** Receives user inquiries from the contact form.
-   **Request Body (JSON):**
    ```json
    {
      "name": "string",
      "email": "string (email format)",
      "message": "string"
    }
    ```
-   **Success Response (200 OK):**
    ```json
    {
      "message": "Your inquiry has been sent!"
    }
    ```
-   **Error Response (400 Bad Request):**
    ```json
    {
      "error": "Invalid data provided."
    }
    ```
-   **Internal Logic:** The endpoint will receive the form data and send it to the hardcoded email address: `contact@pharma-inc.com`.

## 4. Technology Stack
-   **Frontend:** HTML5, CSS3, Vanilla JavaScript
-   **Backend:** Python 3, Flask
