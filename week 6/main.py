import requests
from typing import Annotated
from fastapi import FastAPI,Request,Body
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import os
from dotenv import load_dotenv
app=FastAPI() #產生FastAPI物件
#準備sessionmiddleware管理使用者狀態
app.add_middleware(SessionMiddleware,secret_key=os.getenv('SECRET_KEY'))
templates=Jinja2Templates(directory="templates")
# 載入環境變數
load_dotenv()
#準備資料庫連線
import mysql.connector
def get_db_connection():
    return mysql.connector.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_DATABASE')
    )

#動態檔案

    
#verification Endpoint

#註冊帳號 signup
@app.post('/signup')
def signup(body=Body(None)):
    body=json.loads(body)
    name=body['name']
    email=body['email']
    password=body['password']
    
    # 檢查欄位
    if name=="" or email=="" or password=="":
        return JSONResponse({'ok':False,'msg':'請輸入完整欄位'})
    
    # 檢查資料庫
    con=get_db_connection()
    cursor=con.cursor()
    cursor.execute('SELECT * FROM member WHERE email=%s',[email])
    result=cursor.fetchone()
    
    if result==None:  # 沒有重複
        cursor.execute('INSERT INTO member(name,email,password) VALUES(%s,%s,%s)',[name,email,password])
        con.commit()
        return JSONResponse({'ok': True})
    else:  # 重複
        return JSONResponse({'ok':False,'msg':'重複的電子郵件'})



#登入
@app.post('/login')
def signin(request:Request,body=Body(None)):
    body=json.loads(body)
    email=body['email']
    password=body['password']

     # 檢查欄位
    if email=="" or password=="":
        return JSONResponse({'ok':False,'msg':'請輸入完整欄位'})
    #根據前端輸入的信箱密碼從資料庫取得資料
    con=get_db_connection()
    cursor=con.cursor()
    cursor.execute('SELECT * FROM member WHERE email=%s AND password=%s',[email,password])
    result=cursor.fetchone()

    if result==None: #資料庫沒有對應資料
        request.session['member']=None
        return {'ok':False,'msg':'電子郵件或密碼錯誤'}
    else: #登入成功
        request.session['member']={
            'id': result[0],
            'name':result[1],
            'email':result[2]
        }
        return{'ok':True}
#錯誤頁面 /ohoh
@app.get('/ohoh')
async def show_error(request:Request,msg:str=''):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})

# #會員頁面 /member
# @app.get('/member')
# async def show_member(request:Request):
#     member = request.session.get('member')
#     if not member:
#         return RedirectResponse('/')
#     else:
#         return templates.TemplateResponse("member.html", {"request": request,"name":member['name']})

# 取得當前登入會員資訊的 API
@app.get('/api/member')
def get_member_info(request: Request):
    member = request.session.get('member')
    if member:
        return {'ok': True, 'name': member['name'], 'email': member['email'],'id': member['id']}
    else:
        return {'ok': False}

# 會員頁面
@app.get('/member')
async def show_member(request: Request):
    member=request.session.get('member')
    if not member:
        return RedirectResponse('/')
    # 取得所有留言
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute('''
        SELECT message.id, message.content, message.member_id, member.name
        FROM message 
        JOIN member ON message.member_id = member.id
        ORDER BY message.time DESC
    ''')
    messages = cursor.fetchall()
    cursor.close()
    con.close()
    return templates.TemplateResponse("member.html",  {
        "request": request,
        "name": member['name'],
        "member_id": member['id'],
        "messages": messages
    })
    




#登出系統 /logout
@app.get('/logout')
async def logout(request:Request):
    request.session['member']=None
    return RedirectResponse('/')

#留言板
# create message 新增訊息
@app.post('/createMessage')
def createMessage(request: Request,body=Body(None)):
    #預期會收到的請求文本內容{'name':'姓名‘,'message':'內容'}
    data = json.loads(body)
    member = request.session.get('member')
    
    if not member:
        return {'ok': False}
    
    member_id = member['id']
    content = data.get('content', '')
    #連線到資料庫，將資料新增到資料表中
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute('INSERT INTO message(member_id, content) VALUES(%s, %s)', [member_id, content])
    con.commit()
    # return RedirectResponse('/member')
    return {'ok': True}
#2.取得留言ＡＰＩ
@app.get('/message')
def getMessage():
#連線到資料庫
    con = get_db_connection()
    #字典=TRUE因為要用字典形式把資料抓出來
    cursor = con.cursor(dictionary=True)
    cursor.execute('''
        SELECT message.id, message.content, message.member_id, member.name
        FROM message
        JOIN member ON message.member_id = member.id
        ORDER BY message.time DESC
    ''')
    data = cursor.fetchall()
    cursor.close()
    con.close()
    return data 

#３.根據編號，刪除留言ＡＰＩ
#３.根據編號，刪除留言ＡＰＩ
@app.post('/deleteMessage')
def deleteMessage(request: Request, body=Body(None)):
    # 檢查 body 是否已經是 dict（FastAPI 自動解析）或需要手動解析
    if isinstance(body, dict):
        data = body
    else:
        data = json.loads(body)
    
    member = request.session.get('member')
    
    if not member:
        return JSONResponse({'ok': False, "msg": "未登入"})
    
    message_id = data.get('id')
    
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute('DELETE FROM message WHERE id = %s AND member_id = %s', [message_id, member['id']])
    con.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    con.close()
    
    if affected_rows > 0:
        return JSONResponse({"ok": True})
    else:
        return JSONResponse({"ok": False, "msg": "只能刪自己的留言"})



#靜態檔案放在動態檔案下面
#靜態檔案

app.mount('/',StaticFiles(directory='public',html=True))


