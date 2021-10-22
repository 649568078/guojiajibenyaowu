import pyautogui
import pyperclip
import win32gui
import win32con
import win32clipboard as w
import time
from pynput.keyboard import Controller, Key, Listener, GlobalHotKeys
import sys

# 获取当前屏幕分辨率
def get_screenpoint():
    # screenWidth, screenHeight = pyautogui.size()  # 获取屏幕的尺寸
    # print(screenWidth, screenHeight)
    x, y = pyautogui.position()  # 获取当前鼠标的位置
    print('坐标已复制' + str(x) + ',' + str(y))
    pyperclip.copy(str(x) + ',' + str(y))


def run():
    # 找到rturn位置
    rturn = (395, 429)
    # 跳转位置
    tiaozhuan = (1410, 756)
    go = (1499, 749)
    fanhui = (1572, 193)

    c = int(open('count.txt', 'r', encoding='utf-8').read())

    for go_num in range(40, 47):
        flag_page = "0"
        while flag_page != "1":
            # 跳到某一页
            print('pyautogui.moveTo(tiaozhuan[0], tiaozhuan[1], duration=0.1)')
            pyautogui.moveTo(tiaozhuan[0], tiaozhuan[1], duration=0.1)
            pyautogui.doubleClick()
            pyautogui.typewrite(message='{}'.format(go_num), interval=0.5)
            pyautogui.moveTo(go[0], go[1], duration=0.1)
            pyautogui.click()

            # 定位15个药品位置
            num_list = []
            for i in range(15):
                pianyi = 34
                a = (594, 220 + pianyi * i)
                num_list.append(a)

            # 循环当前页所有药品标签

            for i2 in num_list:
                time.sleep(5)
                print('当前循环为'+str(c))
                flag = "0"
                while flag != "1":
                    if c >= 151:
                        sys.exit()
                    # 清理剪贴板
                    pyperclip.copy('')
                    # 如果存在next_page，证明网页正常刷新
                    time.sleep(1)
                    page_judge = pyautogui.locateCenterOnScreen('判断是否正常刷新.png')
                    print("判断是否正常刷新"+str(page_judge))
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

                    pyautogui.moveTo(int(i2[0]), int(i2[1]), duration=0.1)
                    pyautogui.click()
                    time.sleep(3)
                    pzmc = pyautogui.locateCenterOnScreen('品种名称.png')
                    print("品种名称"+str(pzmc))
                    if pzmc is not None:
                        x1, y1 = pzmc
                        pyautogui.moveTo(x1 + 500, y1, duration=0.1)
                        pyautogui.click()
                        pyautogui.keyDown('shift')
                        #这里是左上角的位置，需要调整
                        pyautogui.moveTo(622,217)
                        pyautogui.click()
                        pyautogui.keyUp('shift')
                        time.sleep(0.5)
                        pyautogui.hotkey('ctrl', 'c')
                        if pyperclip.paste() == '':
                            # 如果剪贴板没东西，重新本次循环
                            continue
                        with open('40-46.txt', 'a+', encoding='utf-8') as f:
                            f.write("第" + str(c) + "条")
                            f.write("\n")
                            f.write(pyperclip.paste())
                            f.write("\n" + "*************************")
                        # 点击返回，返回列表页
                        pyautogui.moveTo(fanhui[0], fanhui[1], duration=0.1)
                        pyautogui.click()
                        print('# 点击返回，返回列表页')
                        c += 1
                        with open('count.txt', 'w', encoding='utf-8') as f:
                            f.write(str(c))
                        flag = '1'
                    else:
                        continue
                flag_page = "1"
            else:
                pyautogui.moveTo(int(rturn[0]), int(rturn[1]), duration=0.1)
                pyautogui.click()
                time.sleep(2)


if __name__ == '__main__':
    # 直接绑定快捷键
    with GlobalHotKeys({'<alt>+1': get_screenpoint,
                        '<alt>+2': run,
                        }
                       ) as h:
        h.join()
