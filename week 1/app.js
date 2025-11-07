let burger_menu = document.querySelector("#mobile_menu");
let menu_list = document.querySelector("#menu_list");
let delete_icon = document.querySelector("#delete_icon");
burger_menu.addEventListener("click", () => {
  open_burger_menu();
});
delete_icon.addEventListener("click", () => {
  close_burger_menu();
});

function open_burger_menu() {
  burger_menu.style.display = "none";
  menu_list.style.display = "block";
  // menu_list.style.height = `${menu_height}px`;
}
function close_burger_menu() {
  burger_menu.style.display = "block";
  menu_list.style.display = "none";
}
//處理漢堡選單在尺寸超過600px之後的隱藏問題
window.addEventListener("resize", () => {
  if (window.innerWidth > 600) {
    menu_list.style.display = "none";
    burger_menu.style.display = "none";
  } else {
    // 回到手機狀態時，顯示漢堡圖示
    burger_menu.style.display = "block";
  }
});
