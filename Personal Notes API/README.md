# Personal Notes RESTful API

**1. How to run application**<br/>
step 1: Clone repository from https://github.com/jwcn97/personal-notes<br/>
step 2: Install npm packages
   ```sh
   npm install
   ```
step 3: Download Firebase Service Account json file and put this at project root<br/>
step 4: In .env file, change the database url value with relevant Firebase project databaseURL (located on Firebase Console)<br/>
step 5: Start the server
   ```sh
   npm start
   ```
<br/>

**2. How to deploy application**<br/>
step 1: login into Firebase<br/>
step 2: initialise "realtime-database" and "functions"<br/>
step 3: deploy
   ```sh
   firebase login
   firebase init
   firebase deploy
   ```
<br/>

**3. Instructions to the UX team**<br/>

{app-url} = https://personal-notes-2aa0a.firebaseapp.com

Action | Method | URL | JSON body parameters
--- | --- | --- | ---
Show list of notes | GET | '{app-url}/notes/' |
View a note | GET | '{app-url}/notes/:id' |
Save a new note | POST | '{app-url}/notes/' | "title" & "content" in string
Update a note | PATCH | '{app-url}/notes/:id' | "title" & "content" in string
Delete a note | DELETE | '{app-url}/notes/:id' |
Archive a note | PUT | '{app-url}/notes/:id' |
Show list of archived notes | GET | '{app-url}/archives/' |
View an archived note | GET | '{app-url}/archives/:id' |
Delete an archived note | DELETE | '{app-url}/archives/:id' |
Unarchive a note | PUT | '{app-url}/archives/:id' |
<br/>

**4. Choice of technology and the reasons for using them (with alternatives)**<br/>
- Firebase realtime database<br/>
  easy-to-follow online documentation on implementing REST API for mobile applications<br/>
- NodeJS<br/>
  familiar with this programming language since it has been used in my previous internship<br/>
- Alternative: MongoDB<br/>
  not familiar with SQL databases being used in MongoDB but would love to explore more if time permits
<br/>

**5. If more time were given, what are some changes or extra features that could be implemented?**<br/>
- more properties of the notes such as tags/priorities<br/>
- arranging notes in order of time-created/time-updated/tags/priorities<br/>
- enable sharing and downloading of notes to friends on social media<br/>
- emable push notifications
