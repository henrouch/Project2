# URL Shortener

## Authors
- Henry Rouch  
- Winston Mwindaare  
- Franklin Adu-Baah  

## Language
**Python**

---

## Project Overview

This project is a **command-line URL shortener** built in Python. It allows users to store long URLs and convert them into a shortened version using a **unique ASCII code of fewer than 12 characters**. These shortened codes can later be used to retrieve the original URL.

The program is designed to be simple, beginner-friendly, and to use persistent storage through a `.json` file.

---

## Example

**Original URL**
https://www.google.com/home?userId=12345&profile=abcdef  

**Shortened URL**
https://www.google.com/short123  


In this example, `short123` is the unique identifier used to reference the original URL.

---

## Features

### 1. Add New URLs
- Users can input long URLs through a menu-driven interface.
- The program prompts the user step by step.
- Designed to be quick and easy to use.

---

### 2. URL Shortening
- Users may:
  - Choose their own custom short code, or  
  - Allow the program to randomly generate one.
- All short codes:
  - Are fewer than 12 ASCII characters.
  - Must be unique before being stored.

---

### 3. Search by Short Code
- Users can retrieve the original URL by entering the shortened code.
- Eliminates the need to retype long URLs.
- Ensures fast and efficient lookups.

---

### 4. Input Validation
- The program checks whether a user-entered URL is valid.
- Invalid URLs trigger an error message.
- Valid URLs proceed to the shortening and storage process.

---

### 5. Persistent Storage (JSON)
- URLs and their shortened versions are stored in a `.json` file.
- On program startup:
  - Existing data is loaded.
- On updates or exit:
  - New data is saved.
- The program safely handles cases where the file does not yet exist.

---

### 6. URL Count Feature
- Displays the total number of shortened URLs stored.
- Implemented using Python’s built-in dictionary tools.
- Fast and simple to execute.


