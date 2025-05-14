# A - Setting up login flow with firebase authentication

For the following example I will only show how to login with google

## Creating a project
Navigate to the firebase console and create a new project
Follow the setup flow

Open the "Authentication" tab and navigate to the "sign-in method" page.

Add google as a provider


## Attaching a firebase application
Go to your project settings and press the "Add app" button.
This should provide you with the setup settings necessarry for your login integration


## Setting up web application
Since you cannot use modular syntax for importing node modules when hosting with http-server, we'll be using vite for this example
Open a terminal and create a new vite project.

$ npm create vite@latest <your-project-name> -- --template vanilla

Navigate to the created project in the terminal and install the firebase node module with:
$ npm install firebase

Create index.html and main.js

I recommend the following structure:
```
├── index.html
├── package.json
├── package-lock.json
├── public
│   └── vite.svg
└── src
    ├── counter.js
    ├── javascript.svg
    ├── main.js
    └── style.css
```

Remember to import your main.js as a module in index.html:
```
<script type="module" src="src/main.js"></script>
```
At this point it may be a good idea to check if the attribute "type" in package.json is set to "module".

## Setting up authentication flow
After creating the application there should now be a copy-pastable javascript setup on your project settings page under the tab "Your apps"

Paste this into your main.js.

It should look something like this:
```
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "<YOUR_API_KEY>",
    authDomain: "<YOUR_AUTH_DOMAIN>.firebaseapp.com",
    projectId: "<YOUR_PROJECT_ID>",
    storageBucket: "<YOUR_STORAGE_BUCKET>.firebasestorage.app",
    messagingSenderId: "<YOUR_MESSAGING_SENDER_ID>",
    appId: "<YOUR_APP_ID>",
    measurementId: "G-K0X3L0T9KE"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
```


We then need to initialize the auth and provider objects
Add the following at the bottom of your main.js:
```
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
```
For the following example we'll trigger a google login popup:
```
signInWithPopup(auth, provider)
    .then((result) => {
        // This gives you a Google Access Token. You can use it to access the Google API.
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const token = credential.accessToken;
        // The signed-in user info.
        const user = result.user;
        // IdP data available using getAdditionalUserInfo(result)
        // ...
    }).catch((error) => {
        // Handle Errors here.
        const errorCode = error.code;
        const errorMessage = error.message;
        // The email of the user's account used.
        const email = error.customData.email;
        // The AuthCredential type that was used.
        const credential = GoogleAuthProvider.credentialFromError(error);
        // ...
    });
```

The above code will trigger a login prompt with google. You could eventually trigger this code by wrapping it in a function triggered by an event listener