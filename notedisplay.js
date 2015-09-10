var Firebase = require('firebase')
var sys = require('sys')
var exec = require('child_process').exec;
var spawn = require('child_process').spawn;
var config = require('./config');

var last = null;

var db = new Firebase(config().firebase).child('notes');
db.limitToLast(1).on('child_added', function(res) {
	var node = res.val();
	if (last === res.key()) return;
	last = res.key();
	console.log(node);
	var blink = spawn('python2', ['./blink.py', 'blue']);
	blink.stdin.end();
	var child = spawn('python2', ['./display/note.py',node.author]);
	child.stdin.write(node.text); 
	child.stdin.end()
});
