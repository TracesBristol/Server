var fs = require('fs');
var MongoClient = require('mongodb').MongoClient,
    f = require('util').format,
    assert = require('assert');

// Connection URL
var url = 'mongodb://<USERNAME>:<PASSWORD>@127.0.0.1:3000/meteor';

// Use connect method to connect to the Server
MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    insertDocuments(db, function() {
        db.close();
    });
    removeUnsupported(db, function() {
        db.close();
    });
    removeUntagged(db, function() {
        db.close();
    });
});

var insertDocuments = function(db, callback) {
    var files = fs.readdirSync("./tweets");
    var fileslength = files.length;
    var numOfFiles = fileslength;
    var json;

    while (fileslength > 0) {
        var file = fs.readFileSync("./tweets/" + files[fileslength - 1]);
        try {
            var json = JSON.parse(file);
        } catch (err) {
            json = [{
                unsupportedfile: 1
            }];
        }
        var collection = db.collection('tweets');
        collection.insertMany(json, function(err, r) {
            assert.equal(err, null);
            callback();
        });
        fs.unlinkSync("./tweets/" + files[fileslength - 1]);
        fileslength -= 1;
    }
};

var removeUnsupported = function(db, callback) {
    var remove = 0;
    var collection = db.collection('tweets');
    collection.remove({'unsupportedfile':1} , function(err, r) {
        remove = 0;
        callback();
    });

}

var removeUntagged = function(db, callback) {
    var collection = db.collection('tweets');
    collection.remove({"tag" : {"$exists" : false} } , function(err, r) {
        assert.equal(null, err);
        callback();
    });
}
