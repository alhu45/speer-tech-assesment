# speer-tech-assesment

For this assesment, I was tasked to build a secure and scalable RESTful API allowing logged in users to create, read, update, and delete notes. The application should also allow users to share their notes with other users and search for notes based on keywords.

For the framework, I decided to use Flask. The reason I used Flask is because a lightweight framework that provides the basic tools needed to build a web applicaitions without enforcing any specfic structures or dependencies. This makes it easier to set up and cutstomize the API accoding to the notes app requiements. The libraries within Flask also support a wide range of extension that helped me manage user authentication, data integration, etc. For example, Flask-JWT helped me handle JWT authentication, while SQLAlchemy was used for database operations. 

Some third party tools I used was postman. Using postman, I was able to develop and debug my API. It provides a interface that allowed me to see what went wrong during various methods such as POST for creating and logging in users. If something went wrong, postman would give me an error code which allowed me to debug the error. Other methods such as GET, PUT, and DELETE were also tested for the notes. Overall, postman was essential for me to test my RESTful API as it allows easy input of headers, parameters, and body data, making it straightforward to configure requests precisely.

Within this file, there are 3 text files.

The first textfile is the requirements for the code to allow anyone to run this code within the environment I created. 

There are also two text files that cover the testcases that can be ran within the testing files. To run the test files, replace the any of the test files with the test desired to be tested. Copy and paste the testcase below the following code to ensure the test files are ran correctly:

'''
import requests

BASE = "http://127.0.0.1:5000/"
'''

Overall, I learned a lot about APIs and how user authorization and authentication mechanisms work. This knowledge deepened my understanding of secure web application development, emphasizing the importance of implementing security practices to protect user data and systems. By exploring different authentication methods, such as JWT (JSON Web Tokens), I understood how tokens can be used to maintain user sessions and restrict access to certain API endpoints based on user roles and permissions.
