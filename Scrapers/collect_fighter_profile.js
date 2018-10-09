var fs = require('fs');
var jsonfile = require('jsonfile')
var ufc = require('ufc');
var count =0;
var array = fs.readFileSync('data/profile_links/fighter_profile_links0.txt').toString().split("\n");
array.forEach(function(value){
		var url = "http://www.ufc.com"+value
		ufc.getFighter(url, function(data) {
			// console.log(data);
		   var file ='json/'+ value.split("/")[2]+'.json'
		jsonfile.writeFile(file, data, function (err) {
			console.error(err)
		})
		console.log( count);
		console.log(value);
		count+=1;
		  });
});
