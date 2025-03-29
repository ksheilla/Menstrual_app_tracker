The Menstrual Cycle Tracker is a web application designed to help users track their menstrual cycles and receive personalized food recommendations based on their current phase (e.g., menstruation, ovulation). The app integrates with the Spoonacular API to fetch nutritionally relevant recipes, ensuring users have access to healthy and balanced meal suggestions.

This README provides instructions for setting up, deploying, and testing the application.

video demo link:https://youtu.be/5tXrSrRoaYQ?si=Ev0zZcWgL4Y4YTZJ

Features
Cycle Tracking : Users can log their menstrual cycle data.

Phase-Based Recommendations : Food recommendations tailored to the user's current phase (e.g., iron-rich foods for menstruation).

API Integration : Fetches recipes from the Spoonacular API.

Scalable Deployment : Configured with a load balancer to handle high traffic efficiently.

Responsive Design : User-friendly interface optimized for both desktop and mobile devices.

Technologies Used

Backend : Flask (Python)

Frontend : HTML, CSS, JavaScript

Database : JSON file for simplicity (can be extended to a database like SQLite or PostgreSQL)

API : Spoonacular API for food recommendations

Web Server : Nginx or HAProxy as the load balancer

Deployment : Ubuntu-based servers (Web01, Web02) with SSH key-based authentication

Styling : Custom CSS for a clean and modern design

How it is used:

you input the two last dates you got your periods(if you input only one date a message will be displayed saying that there isn't enoug data for a prediction),the two dates or more will be stored in the cycle history.In case you want to remove one date on the cycle history,you simply click on it.After inputing the dates;the app will then give you an accurate predictions.
