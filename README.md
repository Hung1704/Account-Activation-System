# NYCU ADFP Cloud 2.0 Account Activation System

This project provides a secure platform for students and researchers at National Yang Ming Chiao Tung University (NYCU) to activate their ADFP accounts. The system ensures data security through key-based authentication, account credential generation, and file upload functionality, including the binding of VPN and server accounts to individual users.

## Key Features

* **Account Authentication**: Verifies users by checking course or lab keys before allowing account binding.
* **Single Account Binding**: Each account can only be bound to one user. Once bound, the account cannot be re-bound unless manually unbound by removing the lock file.
* **Credential Generation**: Automatically provides users with their ADFP and VPN credentials upon successful account activation.
* **File Uploads**: Users must upload their Proof of Enrollment and NDA during the account activation process.
* **Credential Download**: After activation, users can download their credentials as an Excel file for safekeeping.
* **Session Management**: Securely manages user sessions throughout the activation process.

## Command Line Utilities

The system includes utility scripts to help manage the application:

1. **01\_run\_ADFP\_Account**:

   * Command: `nohup python ADFP_Account.py &`
   * Runs the Flask application in the background. Using `nohup` ensures the process continues even after the terminal is closed.

2. **02\_check**:

   * Command: `ps -aux | grep "python ADFP_Account.py" | grep -v grep`
   * Checks if the `ADFP_Account.py` process is currently running.

3. **03\_kill**:

   * Command: `kill \`ps -aux | grep "python ADFP\_Account.py" | grep -v grep | awk '{print $2}'\`\`
   * Terminates the running `ADFP_Account.py` process.

## How to Use

1. **Start the Application**: Run the application using the command `nohup python ADFP_Account.py &`.

2. **Access the System**: Open a browser and go to `http://localhost:8080/`.

3. **Fill in Your Information**: Complete the account information form and upload the course or lab key to verify your identity.

4. **Upload Documents**: Upload your Proof of Enrollment and the signed NDA as PNG files.

5. **Confirm and Bind**: Review your information, agree to the terms and regulations, and complete the account binding process.

6. **Download Credentials**: After account activation, you can download your ADFP and VPN credentials. Be sure to save them immediately as they are only displayed once.

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


## Folder Structure and File Descriptions

Each course or lab has its own set of files that are essential to the activation process. Below is an example of the `2024_Summer/pmic` folder:

```php-template
└── 2024_Summer
    └── pmic
        ├── 2024_Summer_pmic_ADFP.xlsx
        ├── 2024_Summer_pmic.key
        ├── 2024_Summer_pmic_VPN.xlsx
        ├── INFO/
        │   └── pmic005_info.xlsx
        ├── LOCK/
        │   └── pmic005.lock
        ├── NDA/
        │   └── pmic005_<Name>_NDA.png
        └── STU/
            └── pmic005_<Name>_stu.png
```

### File Descriptions:

* **2024\_Summer\_pmic\_ADFP.xlsx**: Contains ADFP account credentials for students enrolled in the course.
* **2024\_Summer\_pmic.key**: The key file provided by the TA or Lab supervisor for students to verify their enrollment during the account activation process.
* **2024\_Summer\_pmic\_VPN.xlsx**: Stores the VPN credentials for each student, including account names and passwords.
* **INFO/pmic005\_info.xlsx**: Created after account activation, containing student information and their generated credentials.
* **LOCK/pmic005.lock**: A lock file created after successful binding to prevent the account from being re-bound. This lock must be manually deleted if re-binding is required.
* **NDA/pmic005\_<Name>\_NDA.png**: The signed Non-Disclosure Agreement uploaded by the student.
* **STU/pmic005\_<Name>\_stu.png**: The Proof of Enrollment uploaded by the student.

### Account Binding and Lock File

Each account is limited to a **single binding**. Once the account is bound to a user, no further uploads or changes can be made unless the **lock file** is removed. The lock file (`LOCK/pmic005.lock`) ensures that the account is securely bound. If unbinding is required, the lock file must be manually deleted, after which the binding process can be repeated.

## System Requirements

* **Flask**: Web framework for Python
* **Pandas**: Data manipulation library for reading and writing Excel files.
* **Portalocker**: For file locking mechanisms to ensure key file integrity.
* **xlsxwriter**: Used for writing Excel files.

### Installation

To install the required dependencies, run:

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

