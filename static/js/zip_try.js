var map
            var geocoder;

            function initMap() {            
               map = new google.maps.Map(document.getElementById('map'), {
                    center: new google.maps.LatLng(-33.863276, 151.207977),
                    zoom: 12
                });
                geocoder = new google.maps.Geocoder();
        var infoWindow = new google.maps.InfoWindow;

                //eigenes
                var summaryPanel = document.getElementById('directions-panel');
                summaryPanel.innerHTML = '';

          // Change this depending on the name of your PHP or XML file
        }               

      function downloadUrl(url, callback) {
        var request = window.ActiveXObject ?
            new ActiveXObject('Microsoft.XMLHTTP') :
            new XMLHttpRequest;

        request.onreadystatechange = function() {
          if (request.readyState == 4) {
            request.onreadystatechange = codeAddress;
            callback(request, request.status);
          }
        };

        request.open('GET', url, true);
        request.send(null);
      }


            function codeAddress() {
            var zipCode = document.getElementById("PLZ").innerHTML;
                    geocoder.geocode({
                            'address': zipCode, "componentRestrictions":{"country":"DE"}
                    }, function (results, status) {
                            if (status == google.maps.GeocoderStatus.OK) {
                                    map.setCenter(results[0].geometry.location);
                                    var marker = new google.maps.Marker({
                                            map: map,
                                            position: results[0].geometry.location
                                    });
                            } else {
                                    alert("Geocode was not successful for the following reason: " + status);
                            }
                    });
            }
