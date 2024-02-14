# Ice-Cream Distribution System

This project entails creating a robust ice-cream distribution system designed as a web service/API to handle user authentication, ice-cream order processing, payment transactions, and statistical data collection on ice-cream sales. Aimed to support tens of thousands of concurrent users and accommodate slow payment gateway processing.

# Features

- User Authentication.
- Order Processing.
- Payment Transactions.
- Statistical Data Collection.
- Caching.
- Queuing.
- Logging.
- Automated Testing.

# Chaching with redis

This project utilizes [Redis](https://redis.io/) for caching, significantly enhancing performance and scalability. By configuring Django to use Redis as the caching backend, the system can store session data, cache frequently accessed data, and reduce database queries. This setup ensures a swift response for users and a streamlined experience, particularly beneficial for high-traffic environments. Redis, known for its speed and efficiency, serves as an integral component in optimizing the application's overall performance.

# Queuing with Python-RQ

The project leverages [Django-RQ](https://github.com/rq/django-rq) for efficient task queuing and asynchronous execution, utilizing Redis as the backend. Configured with RQ_QUEUES, it specifies Redis settings, enabling seamless integration for background job processing. This setup enhances performance by offloading tasks such as payment processing ensuring a responsive user experience by minimizing wait times for foreground processes.

# Prerequisites

Ensure you have the following installed to work with the betting-api:

- Python 3.11: Needed for running the application.
- Docker: If you plan to use Docker for building and running the application.
  Download from Docker's official site.

## Run Project

1. Clone the repository:

```bash
  git clone git@github.com:EmbeddedCodes/distribution_service.git
```

2. Navigate to the project directory:

```bash
  cd distribution_service
```

3. The project is containerised. on the root of the project: run

```bash
  docker-compose up --biuld
```

# Access Admin Panel

- Create admin user:

```
docker-compose exec web python manage.py createsuperuser

```

- Navigate to admin panel url:

```
  /admin/
```

- Login using your credintials

# Admin Panel

- Add new products:

  Navigate to **Ice creams** and click **ADD ICE CREAM** button then fill the form and save.

- View Apps data:

  You can view, edit and delete data in the admin panel by navigating to the target app.

# Authentication using API endpoint

- Post your credintials using API login endpoint:

```
/api/auth/login/
```

- Body :

```
{
  "username": "username",
  "password": "********"
}
```

# Basic Shopping Experience Overview

The project offers an intuitive shopping interface, enabling customers to explore Ice-Cream products easily. Shoppers have the convenience of browsing, adding desired items to their cart, and placing orders.

# API Documentation And Endppoints

- You can view API Documentation nad endpoints using swagger:

```
  /api/docs/swagger/
```

- Or redoc:

```
  /api/docs/redoc/
```

# Running Tests

To run tests, run the following command.

```bash
  docker-compose exec web python manage.py test
```

# Optimizations

- Logging:
  consider integrating an external logging service. This service can aggregate logs from different parts of your application, making it easier to monitor, search through, and analyze logs. Services like [Loggly](https://www.loggly.com/use-cases/django-apps-logging-with-loggly/) or [Splunk](https://splunkbase.splunk.com/) stack provide powerful tools for real-time monitoring and alerting.

- Statistics:
  For more robust insights into application performance and user interactions, enhancing the existing statistics collection and saving these metrics to the database can provide deeper analytical capabilities
- Reactjs Demo:
  Creating a demo using [ReactJS](https://react.dev/) to interact with API endpoints and show case API functionalities.

- Using Corseheaders:
  Integrating [django-cors-headers](https://pypi.org/project/django-cors-headers/) is a key optimization for projects requiring communication between a Django backend and a frontend framework like ReactJS, especially when they are hosted on different domains. This package manages Cross-Origin Resource Sharing (CORS) issues, allowing or restricting frontend requests based on defined policies. Properly configuring CORS is crucial for the security and functionality of web applications, ensuring smooth interaction between client-side and server-side components without compromising security standards.

# Author

- Author: Ayser Shuhaib
- Date: 13/2/2024
