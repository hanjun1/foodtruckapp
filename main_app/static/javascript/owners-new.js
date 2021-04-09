let menuTable = document.querySelector(".menu");
let newMenuBtn = document.querySelector(".new-menu");
newMenuBtn.addEventListener("click", () => {
  let newRow = menuTable.insertRow(-1);
  let cell1 = newRow.insertCell(0);
  let cell2 = newRow.insertCell(1);
  let cell3 = newRow.insertCell(2);
  let cell4 = newRow.insertCell(3);
  cell1.innerHTML = `<input type="text" class="form-control food-name" name="food_name">`;
  cell2.innerHTML = `<input type="text" class="form-control food-description" name="food_description">`;
  cell3.innerHTML = `<input type="number" class="form-control food-price" min="0.00" max="10000.00" step="0.01" name="food_price" placeholder="0.00">`;
  cell4.innerHTML = `<input type="submit" class="btn delete"style="width: 100%; background-color: #BCD5E3;" value="-">`;
  cell4.children[0].addEventListener("click", () => {
    menuTable.deleteRow(cell4.children[0].parentElement.parentElement.rowIndex);
  });
});
let deleteBtns = document.querySelectorAll(".delete");
deleteBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    menuTable.deleteRow(btn.parentElement.parentElement.rowIndex);
  });
});
let openHour = document.querySelectorAll(".open-hour");
let closeHour = document.querySelectorAll(".close-hour");
let foodName = document.querySelectorAll(".food-name");
let foodDescription = document.querySelectorAll(".food-description");
let foodPrice = document.querySelectorAll(".food-price");
validateForm = () => {
  for (i = 0; i < openHour.length; i++) {
    if (openHour[i].value != "" && closeHour[i].value == "") {
      closeHour[i].required = true;
      closeHour[i].style.border = "1px solid red";
      return false;
    }
  }
  for (i = 0; i < foodName.length; i++) {
    if (
      (foodName[i].value != "" && foodDescription[i].value == "") ||
      (foodName[i].value != "" && foodPrice[i].value == "")
    ) {
      foodDescription[i].required = true;
      foodPrice[i].required = true;
      return false;
    }
  }
};

new google.maps.places.Autocomplete(document.getElementById("autocomplete"));

(function () {
  "use strict";
  window.addEventListener(
    "load",
    function () {
      var forms = document.getElementsByClassName("needs-validation");
      var validateGroup = document.getElementsByClassName("validate-me");
      var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener(
          "submit",
          function (event) {
            if (form.checkValidity() === false) {
              event.preventDefault();
              event.stopPropagation();
            }
            for (var i = 0; i < validateGroup.length; i++) {
              validateGroup[i].classList.add("was-validated");
            }
          },
          false
        );
      });
    },
    false
  );
})();
