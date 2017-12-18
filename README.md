# PersonalizedWeatherAssistant
CMSC389L Final Project. 

This project utilizes AWS services on the backend in order to create a static website
that offers suggestions for the number of layers of clothing a user should wear for
the current day. 

Following the link to go to the site!
http://pwa-final-project-website.s3-website-us-east-1.amazonaws.com

Recreating this applicatiion is quite simple.  You need to zip and upload the deployment packages 
(deployment.zip and deployment2.zip) as their own lambda functions. You then need to create two
dynamodb databases in order to hold the user login and preferences information.  After performing
those two steps, the site will be fully functional.  In this case, the site is also hosted
from the S3 bucket will global read permissions.

Below is the Architecture diagram for this project
![PWA Architecture](https://raw.githubusercontent.com/BDanielCS/PersonalizedWeatherAssistant/master/archi.png)

As you can see above, lambda plays a crucial role in the integration of the other aws services which is why it is
of utmost important that the deployment environments be uploaded.
