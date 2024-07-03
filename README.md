# DBMS_AE1

# Library Management System

##Overview

This library administration system is made to manage the several aspects of running a library, such as keeping track of patron information, book data, and loan activities. The system can accommodate four separate user categories, each with unique features and attributes: staff, librarians, students, and administrators.

## Components

### 1. User Management

- **Entities**: User, Staff, Librarian, Student, Administrator
- **Attributes**:
  - User: password, email_address, first_name, last_name, phone_number, address, profile_picture
  - Staff: id, email_address (FK to User)
  - Librarian: id, email_address (FK to User)
  - Student: id, email_address (FK to User)
  - Administrator: id, email_address (FK to User)

### 2. Book Management

- **Entities**: Book
- **Attributes**: year_purchased, for_sale, price, author, version, title, secondary_title, publisher, description, available

### 3. Borrowing Management

- **Entities**: Borrows
- **Attributes**: user_email (FK to User), book_title (FK to Book), borrow_date, return_date, condition

## Normalization

Third Normal Form (3NF) normalisation is applied to the database to guarantee data integrity and prevent redundancy. Table relationships are preserved by using primary keys and foreign keys.

## Physical Design

Indexes are created on frequently searched fields to improve performance:
- Index on `email_address` in the User table.
- Index on `title` in the Book table.
- Composite index on `user_email` and `book_title` in the Borrows table.

## How to Use

### Prerequisites

- MySQL or any other relational database management system
- Python 3.x (for running scripts, if any)

### Setup

1. https://github.com/MatipaM/DBMS_AE1/compare/main...Bilal-Idris-patch-1?quick_pull=1