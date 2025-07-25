import os.path
from flask import Flask
from dotenv import load_dotenv
from datetime import *
from pathlib import Path
import pyautogui
import hashlib
import base64
import json
import requests
import cv2
import time
import os

# 加载环境变量
load_dotenv(dotenv_path=".env")

# 创建Flask应用实例
app = Flask(__name__)

def sendQdWechatPng(path):
    try:
        image_data = Path(path).read_bytes()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        md5_hash = hashlib.md5(image_data).hexdigest()

        message = {
            "msgtype": "image",
            "image": {
                "base64": base64_data,
                "md5": md5_hash
            }
        }

        json_data = json.dumps(message).encode('utf-8')

        headers = {"Content-Type": "application/json"}
        webhook_url = os.getenv('webhook_url')

        response = requests.post(
            webhook_url,
            headers=headers,
            data=json_data
        )
        response.raise_for_status()

        return response

    except Exception as e:
        print(f"[通知发送失败] {e}")
        # 不再 raise，避免中断主流程
        return None



def click_pic(te, ta, resName):
    template = cv2.imread(te, 0)  # 模板图
    target = cv2.imread(ta, 0)  # 目标图

    # 获取模板图的宽高
    h, w = template.shape

    # 模板匹配
    res = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 设置匹配阈值
    threshold = 0.73

    # 检查最佳匹配值是否满足阈值
    if max_val >= threshold:
        # 获取最佳匹配区域左上角坐标
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # 输出坐标
        print("模板图在目标图中的左上角坐标:", top_left)

        # 可视化匹配区域
        cv2.rectangle(target, top_left, bottom_right, (0, 0, 255), 2)
        cv2.imwrite(resName + ".jpg", target)
        return top_left
    else:
        print("未找到满足阈值的匹配区域")
        return False


def qd():
    print("打开模拟器")
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d")

    MuMu_PATH = os.getenv('MuMu_PATH')

    os.startfile(MuMu_PATH)

    time.sleep(15)



    # 截图
    abc = pyautogui.screenshot()
    abc.save("main.png")
    time.sleep(8)


    print("打开米游社")
    # time.sleep(5)
    MY_STEAM_COORDINATES = os.getenv('MY_STEAM_COORDINATES')
    MY_STEAM_COORDINATES_x_str, MY_STEAM_COORDINATES_y_str = MY_STEAM_COORDINATES.split(",")
    MY_STEAM_COORDINATES_x = int(MY_STEAM_COORDINATES_x_str.strip())  # .strip() 移除可能的空白字符
    MY_STEAM_COORDINATES_y = int(MY_STEAM_COORDINATES_y_str.strip())
    pyautogui.moveTo(x=MY_STEAM_COORDINATES_x, y=MY_STEAM_COORDINATES_y)
    time.sleep(5)
    pyautogui.click(button="LEFT",duration=0.1)


    time.sleep(8)
    print("判断是否有青少年模式")
    try:
        p=pyautogui.locateCenterOnScreen("teenager.png", grayscale=False, confidence=0.5)
        time.sleep(1)
        pyautogui.moveTo(x=p.x,y=p.y)
        time.sleep(1)
        pyautogui.click(button="LEFT")
        print("青少年模式")
    except Exception as e:
        print("没有青少年模式")

    time.sleep(5)
    print("点击我知道了")
    pyautogui.moveTo(x=958, y=758)
    time.sleep(5)
    pyautogui.click(button="LEFT",duration=0.1)
    time.sleep(5)

    print("点击返回")
    pyautogui.press('esc')
    time.sleep(3)

    print("打开签到福利")
    Sign_in_benefits = os.getenv('SIGN_IN_BENEFITS')
    x_str, y_str = Sign_in_benefits.split(",")
    x = int(x_str.strip())  # .strip() 移除可能的空白字符
    y = int(y_str.strip())
    pyautogui.moveTo(x=x, y=y)
    time.sleep(1)
    pyautogui.click(button="LEFT")
    time.sleep(5)

    try:
        abc = pyautogui.screenshot()
        abc.save("abc.png")
        time.sleep(3)
        res = click_pic("777.png", "abc.png", "matched_result2")
        time.sleep(1)
        pyautogui.moveTo(res[0] - 10, res[1] + 60)
        time.sleep(1)
        pyautogui.click(button="LEFT")
    except Exception as e:
        print("未找到签到")

    time.sleep(10)
    #发送结果
    pyautogui.screenshot('qd_screenshot.png')
    time.sleep(10)
    sendQdWechatPng("qd_screenshot.png")
    time.sleep(5)
    # 判断签到是否成功
    try:
        qdis = click_pic("qdcg.png", "qd_screenshot.png", "qdres")
        print(qdis)
        print("签到成功")
        with open('qdLog.txt', 'a', encoding='utf-8') as f:
            f.write(formatted_time + '：签到成功。\n')
    except Exception as e:
        print("签到失败")

    time.sleep(5)
    print("回到主页")
    pyautogui.press('esc')
    time.sleep(3)

    Rolling_Coordinates = os.getenv('Rolling_Coordinates')
    Rolling_x_str, Rolling_y_str = Rolling_Coordinates.split(",")
    Rolling_x = int(Rolling_x_str.strip())  # .strip() 移除可能的空白字符
    Rolling_y = int(Rolling_y_str.strip())

    Like_Coordinates = os.getenv('Like_Coordinates')
    Like_x_str, Like_y_str = Like_Coordinates.split(",")
    Like_x = int(Like_x_str.strip())  # .strip() 移除可能的空白字符
    Like_y = int(Like_y_str.strip())

    for i in range(7):
        i = i + 1
        print("第" + str(i) + "篇帖子")
        pyautogui.moveTo(x=Rolling_x, y=Rolling_y)
        time.sleep(1)
        print("看帖子")
        pyautogui.scroll(-155)  # 滚轮向上滚动10格
        time.sleep(1)
        pyautogui.click(button="LEFT")
        time.sleep(5)
        print("点赞")
        pyautogui.moveTo(x=Like_x, y=Like_y)
        time.sleep(1)
        pyautogui.click(button="LEFT")
        time.sleep(2)

        print("返回")
        pyautogui.press('esc')
        time.sleep(3)
        print("下一篇")

    Refresh_Coordinates = os.getenv('Refresh_Coordinates')
    Refresh_x_str, Refresh_y_str = Refresh_Coordinates.split(",")
    Refresh_x = int(Refresh_x_str.strip())  # .strip() 移除可能的空白字符
    Refresh_y = int(Refresh_y_str.strip())
    print("刷新")
    pyautogui.moveTo(x=Refresh_x, y=Refresh_y)
    time.sleep(1)
    pyautogui.click(button="LEFT")
    time.sleep(2)

    Pub_Coordinates = os.getenv('Pub_Coordinates')
    Pub_x_str, Pub_y_str = Pub_Coordinates.split(",")
    Pub_x = int(Pub_x_str.strip())  # .strip() 移除可能的空白字符
    Pub_y = int(Pub_y_str.strip())
    print("点击酒馆")
    time.sleep(2)
    pyautogui.moveTo(x=Pub_x, y=Pub_y)
    time.sleep(2)
    pyautogui.click(button="LEFT")
    time.sleep(2)


    Clock_Coordinates = os.getenv('Clock_Coordinates')
    Clock_x_str, Clock_y_str = Clock_Coordinates.split(",")
    Clock_x = int(Clock_x_str.strip())  # .strip() 移除可能的空白字符
    Clock_y = int(Clock_y_str.strip())
    print("打卡")
    pyautogui.moveTo(x=Clock_x, y=Clock_y)
    time.sleep(1)
    pyautogui.click(button="LEFT")
    time.sleep(1)

    time.sleep(5)
    print("返回")
    pyautogui.press('esc')
    time.sleep(3)

    print("开始分享")
    Share_Coordinates = os.getenv('Share_Coordinates')
    Share_x_str, Share_y_str = Share_Coordinates.split(",")
    Share_x = int(Share_x_str.strip())  # .strip() 移除可能的空白字符
    Share_y = int(Share_y_str.strip())

    for  i in range(3):
        print("刷新")
        pyautogui.moveTo(x=Refresh_x, y=Refresh_y)
        time.sleep(1)
        pyautogui.click(button="LEFT")
        time.sleep(1)

        print("分享")

        pyautogui.moveTo(x=Rolling_x, y=Rolling_y)
        time.sleep(1)
        pyautogui.click(button="LEFT")
        time.sleep(1)
        try:
            p = pyautogui.locateCenterOnScreen("fx.png", grayscale=False, confidence=0.5)
            print("=======", p.x, p.y)
            time.sleep(1)
            pyautogui.moveTo(x=p.x, y=p.y)
            time.sleep(1)
            pyautogui.click(button="LEFT")
            print("找的分享按钮")
            time.sleep(1)
            pyautogui.moveTo(x=Share_x, y=Share_y)
            time.sleep(1)
            pyautogui.click(button="LEFT")
            print("分享成功")

            break
        except Exception as e:
            print("没有分享")
            pyautogui.moveTo(x=960, y=42)
            time.sleep(1)
            pyautogui.click(button="LEFT")
            time.sleep(1)

    time.sleep(1)
    print("关闭软件")
    time.sleep(5)
    exeName = os.path.basename(MuMu_PATH)
    os.system(f'taskkill /im {exeName} /f')


@app.get("/qd")
def chat():
    qd()
    return "签到成功", 200


@app.route('/read-log', methods=['GET'])
def read_log_file():
    if not os.path.exists("qdLog.txt"):
        return "qdLog.txt不存在"

    try:
        with open("qdLog.txt", 'r', encoding='utf-8') as f:
            content = f.read()  # 读取整个文件内容
        return content
    except Exception as e:
        return ""

# 启动Flask应用
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)

# pyinstaller -F -i favicon.ico main.py