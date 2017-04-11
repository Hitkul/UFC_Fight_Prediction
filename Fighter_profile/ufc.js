var fs = require('fs');
var jsonfile = require('jsonfile')
var ufc = require('ufc');
var count =0;
var array = fs.readFileSync('name_files/name_ufc_part_1.txt').toString().split("\n");
array.forEach(function(value){
		var url = "http://www.ufc.com/fighter/"+value
		ufc.getFighter(url, function(data) {
			// console.log(data);
		   var file ='json/'+ value+'.json'
		jsonfile.writeFile(file, data, function (err) {
			console.error(err)
		})
		console.log( count);
		console.log(value);
		count+=1;
		  });
});
