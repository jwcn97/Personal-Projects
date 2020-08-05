const express = require('express');
const router = express.Router();

const firebase = require('../config/app-config');
const ref = firebase.database().ref('/archives/');

const handleSnapshot = require('../helper/handle-snapshot');

// get list of notes in archives
router.get("/", function(req, res) {
    ref.once('value')
    .then(function(snapshot) {
        if (snapshot.exists()) {
            res.statusCode = 200;
            res.json({ 'status': 200, 'data': handleSnapshot(snapshot) });
        } else {
            res.statusCode = 404;
            res.json({ 'status': 'Notes not found' });
        }
    })
});

// get a note in archives
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
});

// update a note in archives
router.patch("/:id", function(req, res) {
    ref.child(`${req.params.id}`).once('value')
    .then(function(snapshot) {
        if (snapshot.exists()) {
            res.statusCode = 403;
            res.json({ 'status': 'Not allowed to edit in archives' });
        } else {
            res.statusCode = 404;
            res.json({ 'status': 'Note not found' });
        }
    })
});

// delete a note in archives
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

// unarchive a note
router.put("/:id", function(req, res) {
    ref.child(`${req.params.id}`).once('value')
    .then(function(snapshot) {
        if (snapshot.exists()) {
            // add to notes section
            firebase.database().ref('/notes/').push(snapshot.val())
            .then(() => {
                // remove from archives section
                ref.child(`${req.params.id}`).remove()
                .then(() => res.json({ 'status': 'Note unarchived' }))
                .catch(() => {
                    res.statusCode = 400;
                    res.json({ 'status': 'Note could not be removed from archives section' });
                })
            })
            .catch(() => {
                res.statusCode = 400;
                res.json({ 'status': 'Note could not be unarchived' });
            })
        } else {
            res.statusCode = 404;
            res.json({ 'status': 'Note not found' });
        }
    });
});

module.exports = router;