🧾 dbms-project-vset

This is a fun little budget tracker I made for my Database Management Systems lab!

💻 Technologies Used

Flask

SQLite3

Jinja2

⚙️ Flask
Flask is a lightweight and flexible web framework in Python that enables the creation of functional and dynamic web applications. It’s highly extensible and handles routing, requests, and responses efficiently—making it a powerful tool for web development.

🎨 Bootstrap 5
Bootstrap provides responsive layouts, styled buttons, forms, and tables without the need for custom CSS. This ensures the app looks clean and professional with minimal effort.

🏪 SQLite
SQLite is a lightweight database used to define, store, and manage data. It doesn’t require a separate server and integrates directly with the application, making it ideal for smaller web apps.

😎 Jinja2
Jinja2 is a templating engine for Flask. It lets you insert Python logic into HTML, making it easy to display data, use loops, and apply conditions in your web pages. This makes your front-end both dynamic and reusable.

💻 OS Module
The os library in Python helps interact with the operating system—for example, to handle file paths or check if the database already exists.

🗂️ Database Schema Design
![db](https://github.com/user-attachments/assets/3dc4d3f8-b7fc-4ec4-bfe3-820f38f15215)

1. AUTO INCREMENT is used for the id columns in both months and items tables to ensure unique, sequential identifiers.
2. NOT NULL constraints ensure essential fields like budget, month, and item are always filled.
3. Foreign Keys maintain relational integrity, making sure every item is tied to a valid month and preventing orphan records.

🎉 Functioning
This project is a simple monthly expense tracker built with Flask, SQLite, Jinja2, and Bootstrap.

Users can:

🤑 Add a new month with a defined budget
🤑 Log individual expense items under that month
🤑 Automatically track total spent and budget left
🤑 Edit or delete any item as needed
🤑 Receive a warning when less than 10% of the budget remains

All information is shown in a clean, responsive interface. This app helps you stay on top of your finances with minimal hassle!
