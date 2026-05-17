# FamilyFlow
#### Video Demo: <URL HERE>
#### Description:

## What is FamilyFlow?

FamilyFlow is a simple but practical web application built with Flask, Python, SQLite, HTML, CSS, and JavaScript. The idea behind this project came from a real need: modern families have busy daily routines, and keeping track of everyone's events, tasks, and shopping needs can be overwhelming. This application brings everything together in one place, making family organization easier and more fun — especially for children.

## The Idea

The concept is straightforward: one login per family, with different experiences depending on who is logging in. Adults have access to a full dashboard with an interactive calendar, task management, and a shopping list. Children, on the other hand, are redirected to a colorful and simplified interface that shows only their own events and tasks, making it easy and enjoyable for them to stay organized without feeling overwhelmed.

## Challenges

The most challenging part of building this project was dealing with unexpected errors along the way and connecting different technologies together. Integrating Flask with SQLite, Bootstrap, and FullCalendar.js required careful attention to how each piece communicated with the others. Every error was a learning opportunity, and solving them one by one made the final result even more rewarding.

## Features

### Family Login
Each family registers with a unique name and password. When logging in, each member identifies themselves by name, and the system redirects them to the appropriate area based on their role — adult or child.

### Calendar and Events
The dashboard displays a full interactive calendar powered by FullCalendar.js, showing all family events. Adults can add new events with a title, date, time, and assign them to a specific family member.

### Task Management
Adults can create household tasks and assign them to any family member, including children. Each task can have a due date and can be marked as done directly from the dashboard.

### Shopping List
The shopping list allows any adult to add items that need to be purchased. Items can be marked as bought or deleted once no longer needed.

### Child Area
When a child logs in, they are redirected to a special colorful and simplified interface that shows only their own events and tasks, making it easy and fun for them to use independently.

## Files

- **app.py** — Main Flask application with all routes and logic
- **init_db.py** — Script to initialize the SQLite database
- **family.db** — SQLite database storing all family data
- **templates/layout.html** — Base HTML template with navbar
- **templates/login.html** — Login page
- **templates/register.html** — Family registration page
- **templates/dashboard.html** — Main dashboard with calendar and summaries
- **templates/events.html** — Add events page
- **templates/tasks.html** — Add tasks page
- **templates/shopping.html** — Shopping list page
- **templates/child.html** — Special child-friendly interface
- **static/css/styles.css** — Custom CSS styles
- **static/js/main.js** — JavaScript for interactivity

## Design Choices

Flask was chosen because it was taught throughout CS50 and is perfect for small web applications. SQLite was used for its simplicity and portability. Bootstrap made the interface responsive and mobile-friendly. The child area was intentionally designed to be colorful and simple so that young children can use it independently, without needing help from adults.

This project was a true challenge from start to finish, and that is exactly what made it so rewarding to complete.

## How to Run

1. Install dependencies: `pip install flask flask-session cs50`
2. Initialize database: `python init_db.py`
3. Run the app: `flask run`
4. Open `http://127.0.0.1:5000` in your browser