Senior Backend Software Engineer - Application - Tech Assessment

Problem Statement
Your task is to create a RESTful API server for an analytics dashboard*. The dashboard should allow users to:
Upload data in a CSV format**
View summary statistics for the uploaded data (mean, median, mode, etc.)
Create visualizations of the data (line chart, bar chart, scatter plot, etc.)
Save the visualizations for future reference
Share the visualizations with others

*The implementation of the dashboard is out of the scope of the tech assessment.

**Here’s a sample CSV data: https://drive.google.com/file/d/10NBjMZzh0g4vOYEEMs17pxm0H_DJvyvV/view?usp=share_link

The data describes how different engineering teams performed in terms of time to review a PR (`review_time`) and time to merge a PR (`merge_time`) in a given time period.
Requirements
The API server should be written in Python 3.8+   ✅DONE
The API server should be asynchronous (asyncio).  ✅DONE
The API server should be type hinted.  ✅DONE
The API server should use a SQL DB (preferably PostgreSQL) to store data.  ✅DONE
The API server should provide the OpenAPI specification. ✅DONE
The API server should handle all the input edge cases.  ✅DONE
The API server should use pytest or an alternative testing framework to write tests.  ✅DONE
The API server should use Git for version control.  ✅DONE
For data manipulation, the API server should use numpy and/or pandas.  ✅DONE


Evaluation Criteria
Your solution will be evaluated based on, but not only, the following criteria:   ✅DONE
Correct functionality: Does the API server meet the requirements of the problem statement? ✅DONE
Code quality: Is the code well written, well-organized, and maintainable? ✅DONE
Testing: Are tests written for the API server? ✅DONE
Are input edge cases handled? Can we make the server crash or return an invalid code by sending malformed requests?  ✅DONE
SQL: Is SQL used to store data?  ✅DONE
Git: Is Git used for version control? ✅DONE
Asynchronous: Is the API server asynchronous?  ✅DONE
Type hinting: Is type hinting used in the code?  ✅DONE
Data manipulation: Is numpy and/or pandas used for data manipulation?  ✅DONE

Submission
Please submit the following:
The complete code for the API server.
A docker-compose.yml file that includes the API server and a PostgreSQL database.
Instructions for running the solution using docker-compose up.
Any additional documentation or explanation you think is necessary.
