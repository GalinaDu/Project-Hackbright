// const geocoder = new google.maps.Geocoder();

function initMap() {
  var map = new google.maps.Map(document.querySelector('#map'), {
      center: { lat: 37.773972, lng: -122.431297},
      scrollwheel: false,
      zoom: 10
  });
  const center = { lat: 50.064192, lng: -130.605469 };
const defaultBounds = {
  north: center.lat + 0.01,
  south: center.lat - 0.01,
  east: center.lng + 0.01,
  west: center.lng - 0.01,
};
const input = document.getElementById("pac-input");
const options = {
  bounds: defaultBounds,
  componentRestrictions: { country: "us"},
  fields: ["address_components", "geometry", "icon", "name"],
  strictBounds: false,
  // types: ["establishment"],
};
const autocomplete = new google.maps.places.Autocomplete(input, options);

const infowindow = new google.maps.InfoWindow();
const marker = new  google.maps.Marker({
  map: map,
  anchorPoint: new google.maps.Point(0, -29)
});
var city = null
autocomplete.addListener('place_changed', function() {
    infowindow.close();
    marker.setVisible(false);
    var place = autocomplete.getPlace();
    if(!place.geometry) {
      window.alert("No place with address exists");
      return;
    }

  if (place.geometry.viewport){
    map.fitBounds(place.geometry.viewport);
  }else{
    map.setCenter(place.geometry.location);
    map.setZoom(15);
  }
  marker.setIcon(({
    url: place.icon,
    size: new google.maps.Size(51, 51),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(17, 34),
    scaledSize: new google.maps.Size(35, 35)
  }));
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
    if(place.address_components[i].types[0] == 'locality'){
      document.getElementById('city').innerHTML = place.address_components[i].long_name;
      city = place.address_components[i].long_name; 
  }
}
// document.getElementById('location').innerHTML = place.street_address;
document.getElementById('lat').innerHTML = place.geometry.location.lat();
document.getElementById('lon').innerHTML = place.geometry.location.lng();
// console.log("Lat val", )
// console.log("Lng val", place.geometry.location.lng())
// console.log("City", city)
var payload = {
  city: city,
  lat: place.geometry.location.lat(),
  lng: place.geometry.location.lng()
}
fetch('/mapdata', {
  method: 'POST',
  body: JSON.stringify(payload),
  headers: {"Content-Type": "application/json"},
})
.then((response) => console.log(response))
.catch((err) => console.log("err", err))
});

 
          
     
}



 

 