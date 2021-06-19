# spotify_checkin
A service to notify your friends if you listen to the same song on repeat too much.

This code is designed to run on AWS Lambda. The example user data given in lambda__function.py is currently static, but future versions will receive this information when called by AWS.

To implement, replace the exmaple user data with that for which you would like to check-in on your friends. Then create a lambda function, setting a cloudwatch trigger to run the code periodically.
