// This code was taken and modified from the google maps documentation
// https://developers.google.com/maps/documentation/javascript/adding-a-google-map#maps_add_map-javascript


// Initialize and adding the google map
function initMap() {
    // The coordinates location of St Albans
    const stalbans = {
        lat: 51.753665,
        lng: -0.337222
    };
    // The map, centered at St Albans and zoom set
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: stalbans,
    });
    // The marker, positioned at St Albans town center
    const marker = new google.maps.Marker({
        position: stalbans,
        map: map,
    });
}