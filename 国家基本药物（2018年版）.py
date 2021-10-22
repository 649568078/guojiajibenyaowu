import pyautogui
import pyperclip
import win32gui
import win32con
import win32clipboard as w
import time
from pynput.keyboard import Controller, Key, Listener, GlobalHotKeys
import sys
import math


# 获取当前屏幕分辨率
def get_screenpoint():
    # screenWidth, screenHeight = pyautogui.size()  # 获取屏幕的尺寸
    # print(screenWidth, screenHeight)
    x, y = pyautogui.position()  # 获取当前鼠标的位置
    print('坐标已复制' + str(x) + ',' + str(y))
    pyperclip.copy(str(x) + ',' + str(y))


def run():
    rturn = (395, 429)  # rturn位置
    tiaozhuan = (1410, 756)  # 跳转位置
    go = (1499, 749)  # go位置
    fanhui = (1572, 193)  # 返回位置
    all_title = 685  # 总条数
    everypage_title = 15  # 每页条数
    page = math.ceil(all_title / everypage_title)  # 总页数（向上取整）

    # 当前title条数
    c = int(open('count.txt', 'r', encoding='utf-8').read())

    # 当前页  当前title / 每页title
    current_page = math.ceil(c / everypage_title)
    if current_page < 1:
        current_page = 1
    #print(current_page)

    # 定位药品位置
    num_list = []
    for i in range(everypage_title):
        pianyi = 34
        a = (594, 220 + pianyi * i)
        num_list.append(a)

    #循环每一页
    for go_num in range(current_page, page+1):
        flag_page = "0"
        while flag_page != "1":
            # 跳到某一页
            #print('pyautogui.moveTo(tiaozhuan[0], tiaozhuan[1], duration=0.1)')
            pyautogui.moveTo(tiaozhuan[0], tiaozhuan[1], duration=0.1)
            pyautogui.doubleClick()
            pyautogui.typewrite(message='{}'.format(go_num), interval=0.5)
            pyautogui.moveTo(go[0], go[1], duration=0.1)
            pyautogui.click()

            # 确认当前的药品位置 当前条数 除以 每页条数取余数，假设每页最多有15条，当前药品位置在[0,14]之间
            current_location = c % everypage_title

            #如果被整除余0则是最后一条，要变为最大数量
            if current_location == 0:
                current_location = everypage_title

            # 循环当前页每一条
            for i2 in range(current_location,everypage_title+1):
                time.sleep(5)
                print('当前循环为' + str(c))
                print('current_location' + str(current_location))
                flag = "0"
                while flag != "1":
                    # 清理剪贴板
                    pyperclip.copy('')
                    # 如果存在next_page，证明网页正常刷新
                    time.sleep(1)
                    page_judge = pyautogui.locateCenterOnScreen('判断是否正常刷新.png')
                    print("判断是否正常刷新" + str(page_judge))
                    # 如果网页没有正常刷新,重新跳两次
                    if page_judge is None:
                        pyautogui.moveTo(int(rturn[0]), int(rturn[1]), duration=0.1)
                        pyautogui.click()
                        time.sleep(1)
                        pyautogui.moveTo(tiaozhuan[0], tiaozhuan[1], duration=0.1)
                        pyautogui.doubleClick()
                        pyautogui.typewrite(message='{}'.format(go_num), interval=0.5)
                        pyautogui.moveTo(go[0], go[1], duration=0.1)
                        pyautogui.click()
                        time.sleep(1)
                        continue
                    #因为列表是从0开始取的，所以这里i2余数需要-1
                    pyautogui.moveTo(int(num_list[i2-1][0]), int(num_list[i2-1][1]), duration=0.1)
                    pyautogui.click()
                    time.sleep(3)
                    pzmc = pyautogui.locateCenterOnScreen('品种名称.png')
                    print("品种名称" + str(pzmc))
                    if pzmc is not None:
                        x1, y1 = pzmc
                        pyautogui.moveTo(x1 + 500, y1, duration=0.1)
                        pyautogui.click()
                        pyautogui.keyDown('shift')
                        # 这里是左上角的位置，需要调整
                        pyautogui.moveTo(622, 217)
                        pyautogui.click()
                        pyautogui.keyUp('shift')
                        time.sleep(0.5)
                        pyautogui.hotkey('ctrl', 'c')
                        if pyperclip.paste() == '':
                            # 如果剪贴板没东西，重新本次循环
                            continue
                        with open('1-685.txt', 'a+', encoding='utf-8') as f:
                            f.write("第" + str(c) + "条")
                            f.write("\n")
                            f.write(pyperclip.paste())
                            f.write("\n" + "*************************")
                        # 点击返回，返回列表页
                        pyautogui.moveTo(fanhui[0], fanhui[1], duration=0.1)
                        pyautogui.click()
                        #print('# 点击返回，返回列表页')
                        c += 1
                        with open('count.txt', 'w', encoding='utf-8') as f:
                            f.write(str(c))
                        flag = '1'
                    else:
                        continue
            flag_page = "1"


if __name__ == '__main__':
    # 直接绑定快捷键
    with GlobalHotKeys({'<alt>+1': get_screenpoint,
                        '<alt>+2': run,
                        }
                       ) as h:
        h.join()
