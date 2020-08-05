const express = require('express');
const router = express.Router();

const firebase = require('../config/app-config');
const ref = firebase.database().ref('/notes/');

const handleSnapshot = require('../helper/handle-snapshot');

// get list of notes
router.get("/", function(req, res) {
    ref.once('value')
    .then(function(snapshot) {
        if (snapshot.exists()) {
            res.statusCode = 200;
            res.json({ 'status': 200, 'data': handleSnapshot(snapshot) });
        } else {
            res.statusCode = 404;
            res.json({ 'status': 'Note(s) not found' });
        }
    })
    .catch(() => {
        res.statusCode = 400;
        res.json({ 'status': 'Notes could not be obtained' });
    })
});

// save a new note
// "title" and "content" in string format
router.post("/", function(req, res) {
    ref.push({
        title: req.body.title,
        content: req.body.content,
        timestamp: firebase.database.ServerValue.TIMESTAMP
    })
    .then(() => res.json({ 'status': 'Note Added' }))
    .catch(() => {
        res.statusCode = 400;
        res.json({ 'status': 'Note could not be saved' })
    })
});

// get a note
router.get("/:id", function(req, res) {
    ref.child(`${req.params.id}`).once('value')
    .then(function(snapshot) {
        if (snapshot.exists()) {
            res.statusCode = 200;
            res.json({ 'status': 200, 'data': snapshot.val() });
        } else {
            res.statusCode = 404;
            res.json({ 'status': 'Note not found' });
        }
    })
    .catch(() => {
        res.statusCode = 400;
        res.json({ 'status': 'Note could not be obtained' });
    })
});

// update note
// "title" and "content" in string format
router.patch("/:id", function(req, res) {
    ref.child(`${req.params.id}`).once('value')
    .then(function(snapshot) {
        if (snapshot.exists()) {
            ref.child(`${req.params.id}`).update({
                title: req.body.title,
                content: req.body.content,
                timestamp: firebase.database.ServerValue.TIMESTAMP
            })
            .then(() => res.json({ 'status': 'Note Updated' }))
            .catch(() => {
                res.statusCode = 400;
                res.json({ 'status': 'Note could not be updated' })
            })
        } else {
            res.statusCode = 404;
            res.json({ 'status': 'Note not found' });
        }
    })
});

// delete note
router.delete("/:id", function(req, res) {
    ref.child(`${req.params.id}`).once('value')
    .then(function(snapshot) {
        if (snapshot.exists()) {
            ref.child(`${req.params.id}`).remove()
            .then(() => res.json({ 'status': 'Note deleted' }))
            .catch(() => {
                res.statusCode = 400;
                res.json({ 'status': 'Note could not be deleted' });
            })
        } else {
            res.statusCode = 404;
            res.json({ 'status': 'Note not found' });
        }
    })
});

// archive a note
router.put("/:id", function(req, res) {
    ref.child(`${req.params.id}`).once('value')
    .then(function(snapshot) {
        if (snapshot.exists()) {
            // add to archives section
            firebase.database().ref('/archives/').push(snapshot.val())
            .then(() => {
                // remove from notes section
                ref.child(`${req.params.id}`).remove()
                .then(() => res.json({ 'status': 'Note archived' }))
                .catch(() => {
                    res.statusCode = 400;
                    res.json({ 'status': 'Note could not be removed from notes section' });
                })
            })
            .catch(() => {
                res.statusCode = 400;
                res.json({ 'status': 'Note could not be archived' });
            })
        } else {
            res.statusCode = 404;
            res.json({ 'status': 'Note not found' });
        }
    });
});

module.exports = router;