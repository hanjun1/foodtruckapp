let closeNavEl = document.querySelector(".closebtn");
let openNavEl = document.querySelector(".openbtn");

openNavEl.addEventListener("click", openNav);
closeNavEl.addEventListener("click", closeNav);

function openNav() {
  document.getElementById("mySidebar").style.width = "300px";
  document.querySelector(".sub-main").addEventListener("click", closeNav);
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.querySelector(".sub-main").removeEventListener("click", closeNav);
}
