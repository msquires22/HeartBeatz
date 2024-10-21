# HeartBeatz
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



