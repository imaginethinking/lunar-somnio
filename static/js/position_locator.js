if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {document.getElementById('latitude').value = position.coords.latitude;
        document.getElementById('longitude').value = position.coords.longitude;});}