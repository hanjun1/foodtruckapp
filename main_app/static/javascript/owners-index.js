let count = 0;
let savedVals = [];
let ratings = [];
document.querySelectorAll(".rating").forEach((rating) => {
  ratings.push(rating.innerHTML);
});
let trucks = document.querySelectorAll(".truck-container-favourite");
trucks.forEach((truck) => {
  let name = truck.children[1].children[0].children[0].innerHTML;
  let rating = ratings[count++];
  let location = truck.children[1].children[3].children[0].innerHTML;
  let truckId = truck.children[1].children[4].innerHTML;
  savedVals.push([name, rating, location, truckId]);
});

function initMap() {
  const geocoder = new google.maps.Geocoder();
  const toronto = { lat: 43.65107, lng: -79.347015 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: toronto,
  });
  savedVals.forEach((truck) => {
    geocodeAddress(geocoder, map, truck);
  });
}

function geocodeAddress(geocoder, resultsMap, truck) {
  geocoder.geocode({ address: truck[2] }, function (results, status) {
    if (status == "OK") {
      const contentString =
        `<div class="pin">` +
        `<div id="title">${truck[0]}</div>` +
        `<div>Rating: ${truck[1]}</div>` +
        `<div>${truck[2]}</div>` +
        `<div><a id="details" href="/results/${truck[3]}/">Show Details</a></div>` +
        `</div>`;
      const infowindow = new google.maps.InfoWindow({
        content: contentString,
      });
      let marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location,
        title: truck[0],
      });
      marker.addListener("click", () => {
        infowindow.open(map, marker);
      });
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}
initMap();
