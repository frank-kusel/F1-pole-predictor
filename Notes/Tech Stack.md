# Tech stacks
The app will use the following tech stack. 
- Django tech stack
- Coding language requirements:
  - Python (backend)
  - JavaScript (frontend)
  - CSS (for styling) 

## Backend
- Django - Python web framework for rapid development with built-in features for handling authentication, database operations, URL routing, and template rendering.
- Django Rest Framework - a toolkit for building Web APIs and simplifies the creation of RESTful APIs by providing serialisers, view sets, authentication classes, and other utilities.

## Frontend
- React / Vue.js - component-based architecture, virtual DOM, reactive data binding making it easier to create complex UIs
- Webpack - module bundler that helps bundle JavaScript, CSS, and other assets. This can help with performance..
- Babel - JS compiler allows backward compatibility
- Axios / Fetch API - library for making HTTP requests from frontend to backend API, asynchronously

## Database
- PostgreSQL - relational database management system that integrates with Django. Support for JSON data types.

## Authentication
- Django Authentication - built-in, ability to integrate third-party authentication

## Deployment
- Heroku / AWS / DigitalOcean - cloud platforms for deploying Django apps.

---

One thing to keep in mind is that the primary output of the app will be to show a leaderboard in the form of tables. This can be done in many simple ways, however, plotting more complex graphs will require graphing libraries. 
There are several graphing options:
- Graphing libraries for the backend on Django, such as Chart.js, Plotly.js, D3.js, or Highcharts.
- Frontend frameworks like Recharts or Victor (React) or VueCharts (Vue.js).
Table libraries
- DataTables (JS)
- Handsontable
- ag-Grid

Data retrieval from the backend to the frontend can be done using Django's ORM to query data into JSON format to be consumed by the frontend tools. 
