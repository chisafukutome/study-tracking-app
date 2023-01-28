let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 29.6436, lng: -82.3549 },
    zoom: 14,
  });

  map.addListener('click', function(e) {
    console.log(e);
    addMarker(e.latLng);
  });

}

function addMarker(latLng) {
    let marker = new google.maps.Marker({
        map: map,
        position: latLng,
        draggable: true
    });
}

window.initMap = initMap;