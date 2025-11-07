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

//抓檔案1的名字還有序號
//用序號去找檔案2圖片的網址
//名稱對應區塊 class=pro_text
//圖片對應區塊class='pro_pic' img src
let attraction_list = [];
let pic_list = [];
fetch("https://cwpeng.github.io/test/assignment-3-1")
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    console.log(data);
    for (let i = 0; i < data.rows.length; i++) {
      attraction_list.push({
        sname: data.rows[i]["sname"],
        serial: data.rows[i]["serial"],
        used: true,
      });
      if (i == 12) {
        break;
      }
    }

    // console.log(attraction_list);

    let pros = document.querySelectorAll(".pro");

    for (let i = 0; i < 3; i++) {
      let pro_text = document.createElement("div");
      pro_text.className = "pro_text";
      let newContent = document.createTextNode(attraction_list[i]["sname"]);
      pro_text.appendChild(newContent);
      pros[i].appendChild(pro_text);
    }

    let pics = document.querySelectorAll(".pic");
    for (let i = 3; i < attraction_list.length; i++) {
      let pic_title = document.createElement("div");
      pic_title.className = "pic_title";
      let new_content2 = document.createTextNode(attraction_list[i]["sname"]);
      pic_title.appendChild(new_content2);
      pics[i - 3].appendChild(pic_title);
    }

    //讓attraction_list繼續push剩下的資料
    for (let i = 13; i < data.rows.length; i++) {
      attraction_list.push({
        sname: data.rows[i]["sname"],
        serial: data.rows[i]["serial"],
        used: false,
      });
    }
    console.log(attraction_list);
  });

//抓圖片
fetch("https://cwpeng.github.io/test/assignment-3-2")
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    attraction_list.forEach((attraction) => {
      for (let i = 0; i < data.rows.length; i++) {
        if (attraction["serial"] == data.rows[i].serial) {
          let pics = data.rows[i].pics.match(/\/d_upload_ttn\/[^ ]+?\.jpg/g);
          if (pics.length > 0) {
            pic_list.push({
              sname: attraction["sname"],
              serial: data.rows[i].serial,
              pic: "https://www.travel.taipei" + pics[0],
            });
            // console.log(pics);
          }
        }
      }
    });
    console.log(pic_list); //有圖片網址

    let pro_pic = document.querySelectorAll(".pro_pic");
    let pic = document.querySelectorAll(".pic");
    console.log(pic);
    for (let i = 0; i < 3; i++) {
      let attraction_img = document.createElement("img");
      attraction_img.src = pic_list[i]["pic"];
      attraction_img.alt = "attraction picture";
      pro_pic[i].appendChild(attraction_img);
    }
    for (let i = 3; i < 13 && i < pic_list.length; i++) {
      let attraction_img = document.createElement("img");
      attraction_img.src = pic_list[i]["pic"];
      attraction_img.alt = "attraction picture";
      attraction_img.className = "attraction";
      pic[i - 3].appendChild(attraction_img);
    }
    //整理資料
    let finalData = [];
    for (let i = 0; i < attraction_list.length; i++) {
      if (attraction_list[i]["used"] == false) {
        let matchedPic = pic_list.find(
          (pic) => pic.serial == attraction_list[i]["serial"]
        );
        if (matchedPic) {
          finalData.push({
            sname: attraction_list[i]["sname"],
            serial: attraction_list[i]["serial"],
            pic: matchedPic.pic,
          });
        }
      }
    }
    console.log(finalData);
    //按下按鈕之後觸發事件;
    let load_button = document.querySelector("#load_button");
    let pic_box = document.querySelector(".pic_box");
    let current_index = 0;
    let picId = 0;
    load_button.addEventListener("click", () => {
      //每次載入10個
      let endIndex = Math.min(current_index + 10, finalData.length);

      for (let i = current_index; i < endIndex; i++) {
        picId += 1;
        let new_pic = document.createElement("div");
        new_pic.className = "pic";
        new_pic.innerHTML = `<img class="star" src="star.png" alt="star icon" />
    <img class='attraction'src=${finalData[i]["pic"]} alt="attraction picture" >
    <div class='pic_title'>${finalData[i]["sname"]}</div>`;
        if (picId == 1 || picId == 6) {
          new_pic.id = `pic${picId}`;
        }

        if (picId == 10) {
          picId = 0;
        }
        pic_box.appendChild(new_pic);
      }
      //記住現在的index到哪裡了
      current_index = endIndex;
      if (current_index >= finalData.length) {
        load_button.style.display = "none";
      }
    });
  });

//   container.appendChild(new_block);
