# BearChat
UC-specific chatbot.

## Inspiration
We were inspired by the lack of personal voice assistant/chatbot for the students of the University of Cincinnati. Something that is UC student-specific would be greatly beneficial.

 For example, it could help students navigate the campus, find the locations of classrooms, labs, and offices, provide information about course schedules, grades, assignments, and exams, and answer frequently asked questions about campus life and services.

Additionally, a voice assistant could provide **personalized support** and guidance to students, helping them stay on track with their academic and personal goals. It could offer reminders for deadlines and appointments, suggest study resources and techniques, provide feedback on assignments and projects, and connect students with academic advisors and support services.

## What it does

The BearChat has several features, some of which are:

Campus Navigation: BearChat helps students navigate the campus by providing directions to buildings, classrooms, and offices. It can also suggest the best route to take based on the student's location.

Campus Services: The voice assistant could provide information about various campus services such as the library, counseling center, health center, and career center. It could also help students schedule appointments or connect with the appropriate staff.

Campus Events: BearChat can keep students informed about upcoming campus events such as concerts, lectures, and workshops. It could also suggest events that may be of interest to the student based on their preferences.

Therapy Suggestions: During stressful times, BearChat can suggest resources for mental health and well-being. For example, it could recommend therapy sessions or mindfulness exercises.

Weather Information: BearChat can provide students with up-to-date weather information such as the temperature, humidity, and precipitation forecast for the day.

Music Streaming: BearChat can play music for students, either by suggesting a playlist or artist, or by playing the student's preferred genre or style of music.

Personalized Recommendations: Over time, BearChat learn the student's preferences and suggest personalized recommendations for campus services, events, and activities.


## How we built it

BearChat uses NLTK on Python using Tensorflow and Pytorch and is converted to a python web browser using Flask. Along with this, the instances in the Python program use various Google APIs like the text-to-speech API and the weather API. The front-end was created using Flask(Python), HTML, CSS and JavaScript.


## Challenges we ran into

We ran into challenges while trying to convert thePython file using Flask as Tensorflow did not seem to be compatible with the pip version we were using. Upon various attempts, we realised that Tensorflow alone wouldn't work so we moved on to using both Tensorflow and Pytorch. 

While running the code, the audio created by the voice assistant does not seem to be sent back to the main HTML. This is a problem we haven't been able to resolve.

## Accomplishments that we're proud of

We are proud that we were successfully able to make a chatbot on the back-end side. It was able to run with 99% accuracy. Our front-end looks wonderful too!

## What we learned

We learned how to use Flask and Pytorch  and also understood back-end to front-end attachment.

## What's next for BearChat

We plan on adding more features to BearChat and providing it with Google Cloud connectivity which will allow it to be personalised based on any UC student. We also want to be able to add more buildings/parking spots on the location services and also name the UC buses that run on the shuttle services. Overall, we want to improve the student experience in relation to our website.

## Front-end

<img width="1440" alt="Screenshot 2023-02-26 at 10 17 42 AM" src="https://user-images.githubusercontent.com/111902870/221419548-8ae0d51e-ad72-409c-b2bf-1d1eff75825a.png">
