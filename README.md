# Group4-Capstone-Project
IMPORTANT
Before you can run the flask app on your machine make sure to have installed pip and the relevant python packages:
 pip install flask,
 pip install flask_socketio,
 pip install secrets,
 pip install werkzeug,
 pip install os,
 pip install random,
 
 Once you have all the necessary packages installed you can start downloading the files/folders.
 1.Make sure everything is inside one main folder
 2.inside the main folder make sure you have a static and templates folder
 3.The static folder holds the css and the javascript make seperate folders inside the static folder for both
 4.The templates folder hols the html, insert the html files into the templates folder
 5.If you have images make an images folder in the templates folder and insert it there if the image is referenced in the html, if the image is referenced in the css make the images folder in the static and add the image there
 5.The uploads folder is for the server to have a place to store the videos you will be uploading
 
 TO RUN:
 You can run the server in one of two ways.
 the first way is to open up the folder in your editor (i.e vs code) go to the flask_app.py file and click run, then in the terminal follow the link it generates.
 the second way is through the command line, cd to the directory in which you have all the code/files, after you reach the destination use:
 python --flask_app.py
 
 Once you get the flask app running, upload the video of your choosing(make sure its an mp4 file) and then click "Create Watch Party". This will load the video into the video player for viewing
