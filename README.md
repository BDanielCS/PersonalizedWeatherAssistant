# PersonalizedWeatherAssistant
CMSC389L Final Project. 

![home](https://raw.githubusercontent.com/BDanielCS/PersonalizedWeatherAssistant/master/home_screen.png)

This project utilizes AWS services on the backend  (and some frontend) in order to create a static website
that offers suggestions for the number of layers of clothing a user should wear for
the current day. The AWS Machine Learning serivce allows for accurate (92% level of accuracy) 
predictions for users.  All preferences will be stored in various dynamo tables and fed back to the
user through a lambda callback.

Following the link to go to the site!
http://pwa-final-project-website.s3-website-us-east-1.amazonaws.com

Recreating this applicatiion is quite simple.  You need to zip and upload the deployment packages 
(deployment.zip and deployment2.zip) as their own lambda functions. You then need to create two
dynamodb databases in order to hold the user login and preferences information.  After performing
those two steps, the site will be fully functional.  In this case, the site is also hosted
from the S3 bucket will global read permissions.

When visiting the site, lambda will invoke the proper functions in order to log you in to the
appropriate account.  Once in this account, you can obtain prediction for various weather conditions
with the click of a button. Below is the main screen you may see.
![main](https://raw.githubusercontent.com/BDanielCS/PersonalizedWeatherAssistant/master/main_screen.png)

Finally, to understand the aws services at play, please consult the architecture diagram below as well
as the code within the repo.
Below is the Architecture diagram for this project
![PWA Architecture](https://raw.githubusercontent.com/BDanielCS/Personalized_Weather_Assistant/master/archi.png)

As you can see above, lambda plays a crucial role in the integration of the other aws services which is why it is
of utmost important that the deployment environments be uploaded.
