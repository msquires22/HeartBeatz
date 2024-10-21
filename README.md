# HeartBeatz
Notes: I got a working tempo adjuster now from stack overflow, now we need to modify it so it can intake new songs, and have the changes come from HR, not user input

If you add any song files, they need to be .wav. There are online converters to switch from mp3 to wav, then add it to the music folder. We can organzie the music folder by genre once we have a working system, I say keep it small for now for just a few test files


------------

Instructions for setting up/running virtual enviornment (on Mac):

$ = terminal command within the HeartBeatz directory

1. Clone the Repo

2. Install Python 3.9 (works best for our dependencies)
-this uses homebrew, so make sure you also have that installed

$brew install python@3.9

3. Create the virtual enviornment
$python3.9 -m venv venv

4. Activate the virtual enviornment
$source venv/bin/activate

5. Install dependecies 
$pip install -r requirements.txt

6. Update the dependencies if you add code that requires new ones, so we can all access it on our systems
$pip freeze > requirements.txt

7. Deactivate the virtual enviornment when done
$deactivate

8. Add the name of your virtual enviorment folder to the .gitiignore file

9. Run this command to make sure you don't push your virtual envirornemnt before pushing
$git rm -r --cached <folder-name>

Note: Don't create a new virtual enviorment everytime, just once, and then run the one you have starting at step 4

-----------
Sources:

Mikey's ChatGPT coder helper - didn't end up directly using any code from this (yet), but have been using it to answer lots of questions:
https://chatgpt.com/share/6716a487-0f8c-800f-9f7d-aaaa9ef7cbb5

Tempo Changer: 
https://stackoverflow.com/questions/75504433/changing-speed-of-song-while-its-playing-and-have-the-changed-effects-in-the-son



