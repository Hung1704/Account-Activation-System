# NYCU ADFP Cloud 2.0 Account Activation System

This project is designed to facilitate the management and activation of ADFP accounts for students and researchers at National Yang Ming Chiao Tung University (NYCU). The system handles account activation by verifying course/research keys, uploading necessary documents (such as Proof of Enrollment and NDA), and generating credentials for both ADFP and VPN access. Developed with Flask, this web-based solution ensures security by utilizing key-based authentication and session management.

## Key Features

* **Account Authentication**: Securely validates user information against pre-uploaded course or research keys.
* **Credential Management**: Automatically generates and provides ADFP and VPN account details to users, ensuring they are bound securely to their respective owners.
* **File Uploads**: Users are required to upload a proof of enrollment and a signed NDA to complete the activation process.
* **Session Management**: User data is stored securely in sessions to prevent unauthorized access.
* **Credential Download**: Once an account is activated, users can download their account credentials in an Excel file for safekeeping.
* **User Responsibility and Regulation**: The system enforces strict usage rules and responsibilities through a checkbox agreement section, ensuring compliance.

## How to Use

1. **Run the Application**: Launch the Flask application with `python ADFP_Account.py`.
2. **Access the System**: Open your browser and navigate to `http://localhost:8080/`.
3. **Fill in Information**: Complete the account and personal details form on the homepage, and upload the key file provided by the TA or Lab supervisor.
4. **Upload Documents**: After key validation, upload the required documents: a PNG file of the proof of enrollment and the signed NDA.
5. **Confirm and Bind Account**: Agree to the terms and regulations by checking the boxes and confirm the binding of your account.
6. **Download Credentials**: After account activation, download your ADFP and VPN credentials. The credentials will only be displayed once.

## Folder Structure

```php
ADFP_Account_Register_System
├── ADFP_Account.py                # Main Flask application file
├── COURSE/                        # Folder for course-related data
├── LAB/                           # Folder for lab-related data
├── static/
│   ├── NDA.pdf                    # Downloadable NDA file
│   └── styles.css                 # CSS styles for the web pages
├── templates/
│   ├── home.html                  # Homepage template
│   ├── success.html               # Success page template
│   └── upload_documents.html      # Document upload page template
└── uploads/                       # Temporary storage for uploaded files
```

## System Requirements

* **Flask**: Web framework for Python
* **Pandas**: Used for processing Excel files
* **Portalocker**: Provides file locking mechanisms
* **xlsxwriter**: For writing Excel files

To install the necessary dependencies, use:

```bash
pip install flask pandas portalocker xlsxwriter
```

## HTML File Overview

1. **home.html**:

   * The homepage where users fill out the form to activate their account.
   * Fields include Account Type, Account Name, Student ID, Semester/Course Code (for course accounts), or Lab Code (for lab accounts).
   * Users upload the course or research key for validation.
   * Session management is used to store user information for the next steps.

2. **upload\_documents.html**:

   * Displays a form for users to upload two PNG files: proof of enrollment and the signed NDA.
   * Uses JavaScript to preview uploaded images and verify that the filenames are correct.
   * Checkbox sections for users to agree to terms and conditions before proceeding.

3. **success.html**:

   * Displays the ADFP and VPN credentials upon successful account activation.
   * Credentials are hidden by default and can be revealed by the user via a 'Show Password' button.
   * Users can download their credentials as an Excel file.

## Security Features

* **Session-Based Authentication**: User data is temporarily stored in the session to prevent unauthorized access during the account activation process.
* **File Locking**: The system ensures that key files are not overwritten by using file locks, guaranteeing the integrity of uploaded keys.
* **Single Use Credentials**: Once displayed, the ADFP and VPN credentials are not shown again, and users are encouraged to change passwords immediately.


