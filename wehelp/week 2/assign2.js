//task1
function func1(name) {
  let coordinate = {
    悟空: [0, 0, "L"],
    辛巴: [-3, 3, "L"],
    貝吉塔: [-4, -1, "L"],
    特南克斯: [1, -2, "L"],
    丁滿: [-1, 4, "R"],
    弗利沙: [4, -1, "R"],
  };
  let x = coordinate[name][0];
  let y = coordinate[name][1];
  let diff_array = [];
  let max = -Infinity;
  let farthest = []; //因為可能會放超過一個變數所以使用array
  let closest = []; //因為可能會放超過一個變數所以使用array
  let min = Infinity;
  for (let key in coordinate) {
    //key表示人名...
    let diff =
      Math.abs(coordinate[key][0] - x) + Math.abs(coordinate[key][1] - y);
    // //求key
    // console.log(key);
    // //求key的值
    // console.log(coordinate[key]);

    // 跳過自己的角色距離
    if (key !== name) {
      //過線+2
      if (coordinate[key][2] !== coordinate[name][2]) {
        diff = diff + 2;
      }
      diff_array.push({ name: key, diff: diff });
    }
  }
  // console.log(diff_array);

  //判斷最遠,最近
  for (let key in diff_array) {
    if (diff_array[key]["diff"] > max) {
      max = diff_array[key]["diff"];
      //刪除前面的最大值
      farthest = [];
      //將最大值的角色加入
      farthest.push(diff_array[key]["name"]);
    } else if (diff_array[key]["diff"] == max) {
      farthest.push(diff_array[key]["name"]);
    }
    if (diff_array[key]["diff"] < min) {
      min = diff_array[key]["diff"];

      //刪除前面的最小值
      closest = [];

      //將最小值的角色加入
      closest.push(diff_array[key]["name"]);
    } else if (diff_array[key]["diff"] == min) {
      closest.push(diff_array[key]["name"]);
    }
  }

  // console.log(min, max);
  console.log(`最遠${farthest},最近${closest}`);
}
//測試
func1("辛巴");
func1("悟空");
func1("弗利沙");
func1("特南克斯");

//task2
// 服務清單
const services = [
  { name: "S1", r: 4.5, c: 1000 },
  { name: "S2", r: 3, c: 1200 },
  { name: "S3", r: 3.8, c: 800 },
];

// 建立字典，用字串 "r,c,name" 當 key，value 存放預約時段陣列
const servicesDict = {};
for (let i = 0; i < services.length; i++) {
  const s = services[i];
  const key = s.r + "," + s.c + "," + s.name;
  servicesDict[key] = [];
}

// 檢查時段是否重疊
function checkSlot(st, ed, slot) {
  if ((slot[0] <= st && st < slot[1]) || (slot[0] < ed && ed <= slot[1])) {
    return true;
  }
  return false;
}

// 從條件字串取右邊數字
function extractDiff(criteria) {
  const ops = [">=", "<=", ">", "<"];
  for (let i = 0; i < ops.length; i++) {
    const op = ops[i];
    if (criteria.indexOf(op) !== -1) {
      return parseFloat(criteria.split(op)[1].trim());
    }
  }
  return null;
}

// 判斷某個值是否符合條件
function myEval(value, criteria) {
  if (criteria.indexOf(">=") !== -1) {
    return value >= parseFloat(criteria.split(">=")[1]);
  } else if (criteria.indexOf(">") !== -1) {
    return value > parseFloat(criteria.split(">")[1]);
  } else if (criteria.indexOf("<=") !== -1) {
    return value <= parseFloat(criteria.split("<=")[1]);
  } else if (criteria.indexOf("<") !== -1) {
    return value < parseFloat(criteria.split("<")[1]);
  }
  return false;
}

// 主函式
function func2(ss, start, end, criteria) {
  if (criteria.indexOf("c") !== -1 || criteria.indexOf("r") !== -1) {
    const keyIndex = criteria.indexOf("c") !== -1 ? 1 : 0;
    const diff = extractDiff(criteria);

    // 找出符合條件的服務
    const valid = [];
    for (const k in servicesDict) {
      const parts = k.split(",");
      const val = parseFloat(parts[keyIndex]);
      if (myEval(val, criteria)) {
        valid.push(k);
      }
    }

    // 排序：距離條件值越接近越前
    valid.sort(function (a, b) {
      const valA = parseFloat(a.split(",")[keyIndex]);
      const valB = parseFloat(b.split(",")[keyIndex]);
      return Math.abs(valA - diff) - Math.abs(valB - diff);
    });

    if (valid.length === 0) {
      console.log("Sorry");
      return;
    }

    // 依序嘗試分配時段
    for (let i = 0; i < valid.length; i++) {
      const k = valid[i];
      const slots = servicesDict[k];
      // 如果該服務已有預約，檢查是否跟新時段衝突
      if (slots && slots.length > 0) {
        let conflict = false;
        for (let j = 0; j < slots.length; j++) {
          if (checkSlot(start, end, slots[j])) {
            conflict = true;
            break;
          }
        }
        if (conflict) {
          // 跳過這個服務，繼續下個 candidate
          continue;
        }
      }
      // 沒衝突 -> 加入並回傳
      servicesDict[k].push([start, end]);
      console.log(k.split(",")[2]); // 印出 name
      return;
    }

    // 所有 candidate 都衝突或不可用
    console.log("Sorry");
    return;
  } else if (criteria.indexOf("name") !== -1) {
    const name = criteria.split("=")[1].trim();
    for (const k in servicesDict) {
      if (k.split(",")[2] === name) {
        const slots = servicesDict[k];
        let conflict = false;
        for (let j = 0; j < slots.length; j++) {
          if (checkSlot(start, end, slots[j])) {
            conflict = true;
            break;
          }
        }
        if (!conflict) {
          slots.push([start, end]);
          console.log(k.split(",")[2]);
          return;
        } else {
          console.log("Sorry");
          return;
        }
      }
    }
    console.log("Sorry");
    return;
  } else {
    console.log("不支援的 criteria");
  }
}

// 測試
func2(services, 15, 17, "c>=800"); // S3
func2(services, 11, 13, "r<=4"); // S3
func2(services, 10, 12, "name=S3"); // Sorry
func2(services, 15, 18, "r>=4.5"); // S1
func2(services, 16, 18, "r>=4"); // Sorry
func2(services, 13, 17, "name=S1"); // Sorry
func2(services, 8, 9, "c<=1500"); // S2
func2(services, 8, 9, "c<=1500"); // S1

//task3

function func3(index) {
  if (index == 0) {
    return 25;
  }
  if (index == 1) {
    return 23;
  }
  //偶數項
  if (index % 2 === 0) {
    let k = index / 2; //第k個偶數項
    //k是奇數要加-5
    if (k % 2 !== 0) {
      return func3(index - 2) + -5;
    } else if (k % 2 == 0) {
      //k是偶數加3
      return func3(index - 2) + 3;
    }
  } else if (index % 2 !== 0) {
    //奇數項
    let k = (index - 1) / 2;
    if (k % 2 !== 0) {
      return func3(index - 2) + -2;
    } else if (k % 2 == 0) {
      return func3(index - 2) + 0;
    }
  }
}

//task4

function func4(sp, stat, n) {
  let fitted_car = [];

  for (let i = 0; i < stat.length; i++) {
    //如果車廂bit number是１就跳到下個車廂
    if (stat[i] == 1) {
      continue;
    }
    // //如果車廂可載客，但是車廂space不夠就跳到下個車廂
    // if (sp[i] < n) {
    //   continue;
    // }
    //如果人數足夠，計算出相差人數，差額最小就是最適合車廂
    // if (sp[i] >= n) {
    //   found = true;}

    //只要bit number不是1就要計算差額
    let value = sp[i] - n;
    fitted_car.push({ index: i, value: value });
  }
  // //沒有適合的車廂
  // if (found !== true) {
  //   return -1;
  // }
  // console.log(fitted_car);
  //判斷fitted_car誰的差值最少
  let min = Infinity;
  let min_index = -1;

  for (let i = 0; i < fitted_car.length; i++) {
    if (Math.abs(fitted_car[i]["value"]) <= min) {
      min = Math.abs(fitted_car[i]["value"]);
      min_index = fitted_car[i]["index"];
    }
  }

  console.log(`${min_index}`);
}
//測試
func4([3, 1, 5, 4, 3, 2], "101000", 2);
func4([1, 0, 5, 1, 3], "10100", 4);
func4([4, 6, 5, 8], "1000", 4);
