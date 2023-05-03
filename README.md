# polleve-bot

Prerequisites
[THIS WEBFLOW IS ONLY APPLICABLE FOR CORNELL STUDENTS]
Before running this script, please ensure that you have a webdriver located in your PATH. Firefox webdrivers can be found in the webdrivers folder.

All instructions moving forward should be done in the project's directory.
Installation

To install the required dependencies, run:

    pip install -r requirements.txt

Running

Running this script requires a file called credentials.txt. To create a credentials.txt file, run:

    python main.py

You will be prompted to enter information such as the name of the polleve, your student email, student password, and more.

Here's a brief summary of each attribute:

    poll name: the name of the polleve
    email: Cornell student email
    netid: Cornell student netid
    password: Cornell student password
    default timeout: the amount of time the script should wait before throwing an exception if no multiple choice is found (in ms)
    interval: the interval at which to check for a multiple choice (in sec)

Notes:

    interval should be relatively large to decrease the likelihood of web exceptions.
