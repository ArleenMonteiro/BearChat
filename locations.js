// //Parse location_hall.json

// var fs=require("fs");
// const { json } = require("stream/consumers");

// console.log("\n *STARTING* \n");

// var contents=fs.readFileSync("location_hall.json");

contents = {"locs":
    {
    "uc_residential_halls":[
        { "loc":"Bellevue Gardens", "lat":39.1239709, "long":-84.5166 },
        { "loc":"Calhoun Hall", "lat":39.1286478, "long":-84.5170178 },
        { "loc":"Campus Recreation Center Hall", "lat":39.162, "long":-84.45689, "alias":["CRC Hall", "Campus Recreation Hall"] },
        { "loc":"CP Cincy", "lat":39.1264554, "long":-84.5045131},
        { "loc":"Dabney Hall", "lat":39.1316722, "long":-84.5131367 },
        { "loc":"Daniels Hall", "lat":39.1314062, "long":-84.511784 },
        { "loc":"Marian Spencer Hall", "lat":39.1336309, "long":-84.5121906 },
        { "loc":"Morgens Hall", "lat":39.1349757, "long":-84.5119818 },
        { "loc":"Schneider Hall", "lat":39.1322768, "long":-84.5122133 },
        { "loc":"Scioto Hall", "lat":39.1343086, "long":-84.5119974 },
        { "loc":"Siddall Hall", "lat":39.162, "long":-84.45689 },
        { "loc":"Stratford Heights", "lat":39.1313558, "long":-84.5220724 },
        { "loc":"The Deacon", "lat":39.1303605, "long":-84.522991 },
        { "loc":"The Eden", "lat":39.1329805, "long":-84.5050224 },
        { "loc":"Turner Hall", "lat":39.132477, "long":-84.511563 },
        { "loc":"University Edge", "lat":39.1397246, "long":-84.5125798, "alias":"U Edge" },
        { "loc":"University Park Apartments", "lat":39.1291004, "long":-84.5139121, "alias":"UPA" },
        { "loc":"University Square Aparments", "lat":39.1280409, "long":-84.5158603,"alias":"U Square" },
        { "loc":"101 East Corry", "lat":39.1285746, "long":-84.5069421 },
        { "loc":"Jefferson House", "lat":39.1307305, "long":-84.510575 }   
    ],
    "uc_academic_buildings": [
        { "loc":"Aronoff Center - College of Design, Architecture, Art and Planning", "lat":39.1344674, "long":-84.5193474,"alias":"DAAP building" },
        { "loc":"Crosley Tower", "lat":39.1345446, "long":-84.5167187 },
        { "loc":"Rieveschl Hall", "lat":39.1329805, "long":-84.5168032 },
        { "loc":"2925 Campus Green Drive", "lat":39.1355098, "long":-84.5130461, "alias":"New College of Law" },
        { "loc":"Lindner College of Business", "lat":39.1347315, "long":-84.5138938 },
        { "loc":"Geology Physics Building", "lat":39.1334614, "long":-84.5184695 },
        { "loc":"Old Chemistry Building", "lat":39.13314 , "long":-84.517552},
        { "loc":"Engineering Research Center", "lat":39.133255, "long":-84.515569,"alias":"Mantei Center"},
        { "loc":"Rhodes Hall", "lat":39.132863, "long":-84.5161},
        { "loc":"Baldwin Hall", "lat":39.132861, "long":-84.516696},
        { "loc":"College Of Arts and Sciences", "lat":39.131866, "long":-84.519147},
        { "loc":"French Hall West", "lat":39.132357, "long":-84.512919},
        { "loc":"College of Law", "lat":39.129055, "long":-84.520034},
        { "loc":"College of Education, Criminal Justice, and Human Services", "lat":39.130442, "long":-84.519367,"alias":["CECH Building","Teachers-Dyer","Teachers Hall","Dyer Hall"]},
        { "loc":"Corbett Center of Performing Arts", "lat":39.129846, "long":-84.518099,"alias":["College-Conservatory of Music","CCM"]},
        { "loc":"Mary Emery Hall", "lat":39.130632, "long":-84.517905,"alias":"Bearcast Media"},
        { "loc":"Edwards Center", "lat":39.129197, "long":-84.512506},
        { "loc":"60 West Charlton", "lat":39.131013, "long":39.131013,"alias":["AACRC building","ELS Language Centers"]}


    ]}
}

//console.log(contents['locs']);

//var jsonData=JSON.parse(contents);
var jsonData=contents;
// Parse the JSON file into a JavaScript object
// const data = JSON.parse(contents);
const data = contents;

// Access the "uc_residential_halls" array
const ucResidentialHalls = data.locs.uc_residential_halls;

  
  // Initialize and add the map
function initMap() {
  // The location of UC

  const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
      center: {lat:39.1345446,lng:-84.5167187},
      });


      for (let i = 0; i < ucResidentialHalls.length; i++) {
        const hall = ucResidentialHalls[i];

        const marker = new google.maps.Marker({
          position: {lat:hall['lat'], lng:hall['long']},
          map: map,
          title : hall['loc'],
        });
      }


 }

//initMap()
//window.initMap = initMap;

//jsonData['locs.uc_residential_halls];
