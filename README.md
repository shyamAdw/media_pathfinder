# Media Pathfinder

Media Pathfinder is a visualization tool that helps Google Ads users understand their account structure and performance through an interactive, hierarchical chart.

## Project Structure
media_pathfinder/
├── backend/          # Flask backend application
│   ├── app.py

│   ├── utils.py

│   └── google_ads_service.py
├── frontend/         # React frontend application
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js

│       ├── components/
│       │   ├── WaterfallChart.js
│       │   └── Filters.js

│       ├── services/
│       │   └── api.js

│       └── App.css

├── requirements.txt   # Backend dependencies
└── package.json       # Frontend dependencies


## Prerequisites

*   Python 3.8 or higher
*   Node.js 16 or higher
*   npm 8 or higher
*   A Google Cloud Project with the Google Ads API enabled
*   Google Ads API credentials (`developer_token`, `client_id`, `client_secret`, `refresh_token`)

## Backend Setup

1.  **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   **macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

    *   **Windows:**

        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Create `googleads.yaml`:**

    *   Create a file named `googleads.yaml` in the `backend` directory.
    *   Add your Google Ads API credentials in the following format:

    ```yaml
    adwords:
      developer_token: YOUR_DEVELOPER_TOKEN
      client_id: YOUR_CLIENT_ID
      client_secret: YOUR_CLIENT_SECRET
      refresh_token: YOUR_REFRESH_TOKEN
    ```

    **Note:** You can obtain these credentials by creating a project in the Google Cloud Console, enabling the Google Ads API, and setting up OAuth 2.0.

## Frontend Setup

1.  **Navigate to the frontend directory:**

    ```bash
    cd ../frontend
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    ```

3.  **Create `.env` file:**

    *   Create a file named `.env` in the `frontend` directory.
    *   Add your Google Client ID, which is used for Google Sign-In:

    ```
    REACT_APP_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
    ```

    **Note:** The Client ID should be for a web application created in your Google Cloud Project.

## Running the Application

1.  **Start the backend server:**

    *   Make sure you are in the `backend` directory and your virtual environment is activated.
    *   Run:

    ```bash
    python app.py
    ```

    The backend server will start on `http://localhost:5000`.

2.  **Start the frontend development server:**

    *   Open a new terminal window/tab.
    *   Navigate to the `frontend` directory:

    ```bash
    cd ../frontend
    ```

    *   Run:

    ```bash
    npm start
    ```

    The frontend will start on `http://localhost:3000`, and it will automatically proxy API requests to the backend.

3.  **Access the application:**

    Open your web browser and go to `http://localhost:3000`.

## Usage

1.  **Sign in with Google:**
    *   Click the "Sign in with Google" button.
    *   Choose a Google account that has access to a Google Ads account.
    *   Grant the necessary permissions.

2.  **Enter Customer ID and Select Campaign Status:**

    *   Enter a valid Google Ads customer ID in the "Customer ID" field.
    *   Select the desired campaign status from the dropdown menu (e.g., "ENABLED", "PAUSED").

3.  **Fetch Data:**
    *   Click the "Fetch Data" button.

4.  **Interact with the Waterfall Chart:**

    *   The chart will display the revenue-weighted data for the specified customer ID.
    *   Click on the bars in the chart to drill down into different levels of the account hierarchy (Campaigns -> Match Types).

## Troubleshooting

*   **Authentication Errors:**
    *   Make sure your `googleads.yaml` file is correctly configured with valid credentials.
    *   Ensure that the Google account you are using for authentication has access to the specified Google Ads customer ID.
*   **API Errors:**
    *   Verify that the Google Ads API is enabled for your Google Cloud Project.
    *   Check the backend server logs for any error messages related to API requests.
*   **Frontend Errors:**
    *   Use your browser's developer tools (console and network tab) to diagnose any issues with the frontend application.

If you encounter any problems, please check the logs and error messages for clues. You can also refer to the Google Ads API documentation for more information.