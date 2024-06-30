function findNearbyVeterinarians() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;

            // Redirect to Flask route to handle fetching veterinarians
            fetch(`/find_veterinarians?lat=${lat}&lng=${lng}`)
                .then(response => response.json())
                .then(data => {
                    if (data.veterinarians && data.veterinarians.length > 0) {
                        // Display veterinarians or update map
                        console.log('Veterinarians near you:', data.veterinarians);
                    } else {
                        console.log('No veterinarians found near your location.');
                    }
                })
                .catch(error => {
                    console.error('Error fetching veterinarians:', error);
                    alert('Error fetching veterinarians. Please try again.');
                });
        }, function(error) {
            console.error('Error getting user location:', error);
            alert('Error getting your location. Please try again.');
        });
    } else {
        alert('Geolocation is not supported by this browser.');
    }
}
