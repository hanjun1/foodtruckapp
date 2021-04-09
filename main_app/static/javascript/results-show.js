let hoursModal = document.getElementById("modal-hours");
let menuModal = document.getElementById("modal-menu");
let showHoursBtn = document.querySelector(".show-hours");
let showMenuBtn = document.querySelector(".show-menu");
let spanClose = document.querySelector(".close-hours");
let spanMenuClose = document.querySelector(".close-menu");

showMenuBtn.onclick = function () {
  menuModal.style.display = "block";
};

showHoursBtn.onclick = function () {
  hoursModal.style.display = "block";
};

spanClose.onclick = function () {
  hoursModal.style.display = "none";
};

spanMenuClose.onclick = function () {
  menuModal.style.display = "none";
};

window.onclick = function (e) {
  if (e.target == hoursModal) {
    hoursModal.style.display = "none";
  } else if (e.target == menuModal) {
    menuModal.style.display = "none";
  }
};

function initMap() {
  const geocoder = new google.maps.Geocoder();
  const toronto = { lat: 43.65107, lng: -79.347015 };
  const map = new google.maps.Map(document.getElementById("show-map"), {
    zoom: 11,
    center: toronto,
  });
  let location = document.querySelector(".show-truck-location");
  geocodeAddress(geocoder, map, location);
}

function geocodeAddress(geocoder, resultsMap, location) {
  geocoder.geocode({ address: location.innerHTML }, function (results, status) {
    if (status == "OK") {
      let marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location,
      });
      resultsMap.panTo(results[0].geometry.location);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}

initMap();
