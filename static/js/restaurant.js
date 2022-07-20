const geocoder = new google.maps.Geocoder();

function initMap() {
  var map = new google.maps.Map(document.querySelector('#map'), {
      center: { lat: 34.397, lng: 150.644 },
      scrollwheel: false,
      zoom: 2
  });
  const center = { lat: 50.064192, lng: -130.605469 };
// Create a bounding box with sides ~10km away from the center point
const defaultBounds = {
  north: center.lat + 0.1,
  south: center.lat - 0.1,
  east: center.lng + 0.1,
  west: center.lng - 0.1,
};
const input = document.getElementById("pac-input");
const options = {
  bounds: defaultBounds,
  componentRestrictions: { country: "us" },
  fields: ["address_components", "geometry", "icon", "name"],
  strictBounds: false,
};
const autocomplete = new google.maps.places.Autocomplete(input, options);

const infowindow = new google.maps.InfoWindow();

const marker = new  google.maps.Marker({
  map: map,
  anchorPoint: new google.maps.Point(0, -29)
});
autocomplete.addListener('place_changed', function() {
    infowindow.close();
    marker.setVisible(false);
    var place = autocomplete.getPlace();
    if(!place.geometry) {
      window.alert("No such place");
      return;
    }

  if (place.geometry.viewport){
    map.fitBounds(place.geometry.viewport);
  }else{
    map.setCenter(place.geometry.location);
    map.setZoom(12);
  }
  marker.setPosition(place.geometry.location);
  marker.setVisible(true);

  let address = '';
  if (place.address_components) {
    address = [
      (place.address_components[0] && place.address_components[0].short_name || ''),
      (place.address_components[1] && place.address_components[1].short_name || ''),
      (place.address_components[2] && place.address_components[2].short_name || ''),
    ].join(' ');
  }infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
  infowindow.open(map, marker);

  // Location details
  for (var i = 0; i < place.address_components.length; i++) {
      if(place.address_components[i].types[0] == 'postal_code'){
          document.getElementById('postal_code').innerHTML = place.address_components[i].long_name;
      }
      if(place.address_components[i].types[0] == 'country'){
          document.getElementById('country').innerHTML = place.address_components[i].long_name;
      }
  }
  document.getElementById('location').innerHTML = place.street_address;
  document.getElementById('lat').innerHTML = place.geometry.location.lat();
  document.getElementById('lon').innerHTML = place.geometry.location.lng();
  
  var locations = [];
  //Using fetch to process the ajax call 
  // if you use fetch, besure to include the source below this line in your template
  //<script src="https://cdnjs.cloudflare.com/ajax/libs/fetch/2.0.3/fetch.js"></script>
  // fetch('/restaurants')
  // .then(function(response) {
  //  return response.text();
  //  }).then(function(body) {
  //  var obj = JSON.parse(body);
  //  var myAdd = {};
  //  var addresses = obj.cordinates;
  //  var l = addresses.length;
  //  for (i = 0; i < l; i++) {
  //  myAdd = {
  //       position: {
  //           lat: parseFloat(obj.cordinates[i].lat),
  //           lng: parseFloat(obj.cordinates[i].lng)
  //                 },
  //           title: obj.cordinates[i].title,
  //            };
  //  locations.push(myAdd);
  // }
  // locations.forEach(function(feature) {
  //           var marker = new google.maps.Marker({
  //             position: feature.position,
  //             title: feature.title,
  //             map: map
  //           });
  //         });
});

}