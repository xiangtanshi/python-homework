import requests
import base64

#image feature获取函数
def img_detect(img_path):
    
    # 将图片以base64编码方式打开
    img_path = str(img_path)
    with open(img_path, 'rb') as f:
        img = str(base64.b64encode(f.read()), 'utf-8')
        
    # 参数与URL的设置
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {"image": img, "image_type": "BASE64", "face_field": "gender,age,beauty","max_face_num":10}
    #face_field参数用于指定需要获取的人脸特性,max_face_num为最多处理的人脸数目，本程序只探测含有一张人脸的图片
    access_token = "24.9d9aa138f819619b09f31d611aac24ef.2592000.1556014990.282335-15832197"
    #access_token为使用api接口必须的密匙，与我的百度云上的某个应用相对应
    request_url = request_url + "?access_token=" + access_token
    
    # 获取数据
    response = requests.post(request_url, data=params)
    content = response.json()
    age = content['result']['face_list'][0]['age']
    beauty = content['result']['face_list'][0]['beauty']
    gender = content['result']['face_list'][0]['gender']
    face_num = content["result"]["face_num"]
    return gender,age,beauty,face_num

#根据图片识别人脸进行签到的函数
def img_search(img_path):
    
    #所用的api接口变为search
    img_path = str(img_path)
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    params = {"image": img, "image_type": "BASE64", "group_id_list": "harry_potter", "quality_control": "LOW",
              "liveness_control": "NONE","max_user_num":15}
    #liveness_control为活体检测，主要用于判断是否为二次翻拍，需要限制用户为当场拍照获取图片，
    # 参考阈值0.393241，超过此分值以上则可认为是活体。
    # group_id_list为我的百度云账号中与access_token对应应用中的人脸库
    #max_user_num为最多返回的库成员数目,这里取15，即我的Harry-potter人脸库中人脸总数量，每张脸都可能会返回一个匹配概率
    
    access_token = "24.9d9aa138f819619b09f31d611aac24ef.2592000.1556014990.282335-15832197"
    request_url = request_url + "?access_token=" + access_token
    pic_info = img_detect(img_path)
    face_num = pic_info[3]        #先判断图片中人脸数目
    
    try:
        response = requests.post(request_url, data=params)
        test = response.json()
        num = len(test["result"]["user_list"])      #返回的可能匹配的库人脸数
        name_list = []                              #用来放最终的结果
        for i in range(num):
            score = test["result"]["user_list"][i]["score"]
            #只有score超过50才认为匹配有效
            if score < 50:
                pass
            else:
                name_list.append(test['result']['user_list'][i]["user_id"])
        #从得到的name_list中筛选出正确的人脸
        if len(name_list) == 0:
            result = "you do not belong to harry potter series"
        else:
            j=0
            result = ""
            while j<face_num and j<len(name_list):     #返回的人脸数目不超过照片中人脸数目且为概率最大的几个
                result = name_list[j] + " " + result
                j += 1
    except Exception as e:
        print(e)
        result = "I can hardly recognize you"

    #异常处理
    return result
