function changeToArray(item) {
    for (var property in item) {
        // checks if object properties have array format
        if (typeof(item[property]) === 'object') {
            var arr = [];
            for (var subProperty in item[property]) {
                item[property][subProperty]['key'] = subProperty;
                arr.push(item[property][subProperty]);
            }
            item[property] = arr;
        }
    }
    return item;
}

module.exports = function(snapshot) {
    if (snapshot.key === 'notes' || snapshot.key === 'archives') {
        var arr = [];
        snapshot.forEach(function(childSnapshot) {
            var item = childSnapshot.val();
            item.key = childSnapshot.key;   
    
            arr.push(changeToArray(item));
        });
    }
    return arr;
}