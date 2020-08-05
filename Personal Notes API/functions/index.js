require('dotenv').config()

const bodyParser = require('body-parser');
const functions = require('firebase-functions');
const app = require('express')();

const firebase = require('./config/app-config');
const ref = firebase.database().ref('/');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(require('cors')());

app.use('/notes', require('./routes/notes'));
app.use('/archives', require('./routes/archives'));

// internal error handling
app.use(function(err, req, res, next) {
    console.log(err);
    res.statusCode = 500;
    res.json({ 'status': 'Internal Server Error' });
});

const port = process.env.APP_PORT || 8080;
const host = process.env.APP_HOST || '127.0.0.1';
app.listen(port, host);
console.log(`Server listening at ${host}:${port}`);

exports.app = functions.https.onRequest(app);