import requests
from typing import Annotated
from fastapi import FastAPI,Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
app=FastAPI() #產生FastAPI物件
app.add_middleware(SessionMiddleware,secret_key='sychcc')
templates=Jinja2Templates(directory="public")

#動態檔案

    
#verification Endpoint
@app.post('/login')
async def login(request:Request):
    data=await request.json()
    email=data.get('email')
    password=data.get('password')
    if email=='abc@abc.com' and password=='abc':
        #設定logged in狀態為true
        request.session['logged_in']=True
        return JSONResponse(content={"redirect_url": "/member"})
    elif len(email)==0 or len(password)==0:
        request.session['logged_in']=False
        return JSONResponse(content={"redirect_url": "/ohoh?msg=請輸入信箱和密碼"})
    else:
        #設定logged in狀態為false
        request.session['logged_in']=False
        return JSONResponse(content={"redirect_url": "/ohoh?msg=帳號、或密碼輸入錯誤"})
#錯誤頁面 /ohoh
@app.get('/ohoh')
async def show_error(request:Request,msg:str=''):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})

#會員頁面 /member
@app.get('/member')
async def show_member(request:Request):
    if not request.session.get('logged_in'):
        return RedirectResponse('/')
    return templates.TemplateResponse("member.html", {"request": request})

#登出系統 /logout
@app.get('/logout')
async def logout(request:Request):
    request.session['logged_in']=False
    return RedirectResponse('/')

#取得hotel資訊
@app.get('/hotel/{hotel_no}')
async def show_hotel(request:Request,hotel_no:str):
    ch_url='https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch'
    en_url='https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en'
    print(f"=== Debug Info ===")
    print(f"Hotel No: {hotel_no}")
    print(f"CH URL: {ch_url}")
    print(f"EN URL: {en_url}")
    ch_resp=requests.get(ch_url)
    en_resp=requests.get(en_url)
    print(f"CH Status Code: {ch_resp.status_code}")
    print(f"EN Status Code: {en_resp.status_code}")
    if ch_resp.status_code==200 and en_resp.status_code==200:
        ch_data=ch_resp.json()
        en_data=en_resp.json()

        # 從 list 陣列中找出符合的 hotel
        ch_hotel = None
        en_hotel = None
        
        for hotel in ch_data['list']:
            if str(hotel['_id']) == hotel_no:
                ch_hotel = hotel
                break
        
        for hotel in en_data['list']:
            if str(hotel['_id']) == hotel_no:
                en_hotel = hotel
                break
        
        if ch_hotel and en_hotel:
            return templates.TemplateResponse('hotel.html', {
                'request': request,
                'ch_name': ch_hotel['旅宿名稱'],
                'en_name': en_hotel['hotel name'],
                'tel': ch_hotel['電話或手機號碼']
            })
        else:
            return templates.TemplateResponse('hotel.html', {
                'request': request,
                'msg': '查詢不到相關資料'
            })
    else:
        return templates.TemplateResponse('hotel.html', {
            'request': request,
            'msg': '查詢不到相關資料'
        })
        






#靜態檔案放在動態檔案下面
#靜態檔案

app.mount('/',StaticFiles(directory='public',html=True))