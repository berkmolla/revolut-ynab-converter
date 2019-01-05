var args = process.argv.slice(2);

var spawn = require("child_process").spawn;
console.log(args)
var spawned_process = spawn('python',["convert.py", ...args]);

spawned_process.stdout.on('data', function (data){
    console.log(data)
});
