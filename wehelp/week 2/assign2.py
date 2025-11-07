#task1
def func1(name):
    coordinate = {
      '悟空': [0, 0, "L"],
      '辛巴': [-3, 3, "L"],
      '貝吉塔': [-4, -1, "L"],
      '特南克斯': [1, -2, "L"],
      '丁滿': [-1, 4, "R"],
      '弗利沙': [4, -1, "R"],
  }
    x = coordinate[name][0];
    y = coordinate[name][1];
    diff_array = []
    max_val = -float('inf')
    farthest = []
    closest = []
    min_val = float('inf')
    for key,value in coordinate.items():
       
        diff=abs(value[0]-x)+abs(value[1]-y)
        if key!= name:
            if value[2]!=coordinate[name][2]:
                diff=diff+2
            diff_array.append({ 'name': key, 'diff': diff })
    # print(diff_array)

    for key,value in enumerate(diff_array):
        if value['diff']>max_val:
            max_val=value['diff']
            farthest=[]
            farthest.append(value['name'])
        elif value['diff']==max_val:
            farthest.append(value['name'])
        if value['diff']<min_val:
            min_val=value['diff']
            closest=[]
            closest.append(value['name'])
        elif value['diff']==min_val:
            closest.append(value['name'])
    # print(min_val,max_val)
    print("最遠",farthest,'最近',closest)


#測試
func1("辛巴");
func1("悟空");
func1("弗利沙");
func1("特南克斯");


#task2
services = [
  {"name":"S1", "r":4.5,"c": 1000},
  {"name":"S2", "r":3,"c": 1200},
  {"name":"S3", "r":3.8,"c": 800}
]

# 建立一個字典 services_dict：
# key 是 (r, c, name) 這三個值組成的 tuple
# value 是一個空的 list，用來記錄這個服務被預約的時段
services_dict = { (service["r"], service["c"], service["name"]) : [] for service in services }

# 定義一個函式：檢查時段是否有重疊
# st, ed 是新的預約起訖時間；slot 是已存在的時段 [start, end]
def check_slot(st, ed, slot):
  # 只要新時段的起點或終點落在已有時段內，就算衝突
  if slot[0] <= st <slot[1] or slot[0] < ed <= slot[1]:
    return True
  return False

# 從字串條件 (例如 "r>=3.5") 中取出右邊的數字
# 只處理 >=, <=, >, < 這四種符號
def extract_diff(criteria):
  for op in [">=", "<=", ">", "<"]:
    if op in criteria:
      # 用 split(op) 切開，取右邊的數字部分
      return float(criteria.split(op)[1])
  return None

# 根據條件字串 (criteria) 來比較某個值 (value)
# 回傳 True 或 False，代表是否符合條件
def my_eval(value, criteria):
  if ">=" in criteria:
    return value >= float(criteria.split(">=")[1])
  elif ">" in criteria:
    return value > float(criteria.split(">")[1])
  elif "<=" in criteria:
    return value <= float(criteria.split("<=")[1])
  elif "<" in criteria:
    return value < float(criteria.split("<")[1])

# 主函式 func2
# ss: 服務清單 (其實沒用到)
# start, end: 預約起訖時間
# criteria: 選擇條件，例如 "c>=800"、"r<=4"、"name=S3"
def func2(ss, start, end, criteria):

  # 情況一：條件是跟 c 或 r 有關（例如價格或評分）
  if "c" in criteria or "r" in criteria:
    # 決定要比對 tuple 的哪個欄位
    # c 是 index=1，r 是 index=0
    key_index = 1 if "c" in criteria else 0
    diff = extract_diff(criteria)  # 取出右邊數值

    # 選出符合條件的服務 (例如 r<=4.0)
    valid = [k for k in services_dict if my_eval(k[key_index], criteria)]

    # 依照與條件值的距離排序，越接近的排前面
    valid.sort(key=lambda k: abs(k[key_index] - diff))

    # 如果沒有任何符合的服務
    if not valid:
      print("Sorry")
      return

    # 依序嘗試每個符合條件的服務
    for k in valid:
      # 如果這個服務之前有被預約
      if services_dict[k]:
        # 檢查是否與已有時段衝突
        conflict = False
        for slot in services_dict[k]:
          if check_slot(start, end, slot):
            conflict = True  # 有衝突，不能預約
            break
        if conflict:
          continue
  
      # 沒衝突 -> 加入新的時段
      services_dict[k].append([start, end])
      print(k[2])  # 印出服務名稱（tuple 第三個元素 name）
      return
    # 如果所有候選服務都衝突或沒有可用，才印 Sorry
    print("Sorry")
    return  

  # 情況二：條件是用名稱篩選（例如 "name=S3"）
  else:
    for k in services_dict:
      if k[2] in criteria:  # tuple 的第三個元素是 name
        # 同樣檢查是否有時段衝突
        if services_dict[k]:
          for slot in services_dict[k]:
            if check_slot(start, end, slot):
              print("Sorry")
              return
        # 沒衝突就加入
        services_dict[k].append([start, end])
        print(k[2])
        return


#測試
func2(services, 15, 17, "c>=800");  
func2(services, 11, 13, "r<=4");    
func2(services, 10, 12, "name=S3"); 
func2(services, 15, 18, "r>=4.5");  
func2(services, 16, 18, "r>=4"); 
func2(services, 13, 17, "name=S1"); 
func2(services, 8, 9, "c<=1500");   
func2(services, 8, 9, "c<=1500");   

#task3
def func3(index):
    if index==0:
        return 25
    if index==1:
        return 23
    #偶數項
    if index%2==0:
        k=index/2 #第k個偶數項
        #k是奇數要加-5
        if k % 2 != 0 :
          return func3(index - 2) + -5
        elif (k % 2 == 0) :
        #k是偶數加3
          return func3(index - 2) + 3
    elif index % 2 != 0:
       k=(index-1)/2
       if k%2!=0:
          return func3(index - 2) + -2
       elif k%2==0:
          return func3(index - 2) + 0
       
#task4
def func4(sp,stat,n):
    fitted_car=[]
    for index, bit_n in enumerate(stat):
        if bit_n=="1":
            continue
        value=sp[index]-n
        fitted_car.append({'index': index, 'value': value})
    # print(fitted_car)
    min_val=1000000000
    min_index=-1
    for item in fitted_car:
        if abs(item['value'])<=min_val:
            min_val = abs(item["value"])
            min_index = (item["index"])
    print(min_index)
#測試
func4([3, 1, 5, 4, 3, 2], "101000", 2);
func4([1, 0, 5, 1, 3], "10100", 4);
func4([4, 6, 5, 8], "1000", 4);