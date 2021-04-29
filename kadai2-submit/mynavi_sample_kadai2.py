# import os
# from selenium.webdriver import Chrome, ChromeOptions
from selenium import  webdriver
import time
import pandas as pd

# 課題７　ログファイル出力　まだ良く分かっていませんので、引き続き調べます。
import logging
logging.basicConfig(filename="app.log",level=logging.WARNING)
logging.debug('debug')
logging.info('info')
logging.warning('warnig')
logging.error('error')
logging.critical('critical')

# Chromeを起動する関数　　　恐縮ですが、自分のMacで動くようにコメントアウトさせて頂きました。

# def set_driver(driver_path, headless_flg):
#     # Chromeドライバーの読み込み
#     options = ChromeOptions()

#     # ヘッドレスモード（画面非表示モード）の設定
#     if headless_flg == True:
#         options.add_argument('--headless')

#     # 起動オプションの設定
#     options.add_argument(
#         '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
#     # options.add_argument('log-level=3')
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('--ignore-ssl-errors')
#     options.add_argument('--incognito')          # シークレットモードの設定を付与

#     # ChromeのWebDriverオブジェクトを作成する。
#     return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

def main():

    # # driverを起動
    # if os.name == 'nt': #Windows
    #     driver = set_driver("chromedriver.exe", False)
    # elif os.name == 'posix': #Mac
    #     driver = set_driver("chromedriver", False)

    # 課題４　キーワードをコンソールから入力
    search_keyword = input("検索キーワードを入力してください >>> ")
    # search_keyword = "高収入"
    driver = webdriver.Chrome()
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    try:
    # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
    # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()


    exp_only_name_list = []
    exp_status_list = []
    exp_condition_list = []

    # 課題６　エラー処理
    try:
        # 課題３　全ページの情報を取得（高収入のページ数に合わせました。
        # 検索キーワードが変わるとページ数も変わりますが、
        # ページ数の変更にどのようにフレキシブルに対応するかは、まだ分かっておりません。
        for page in range(1,12):
            url = 'https://tenshoku.mynavi.jp/list/kw%E9%AB%98%E5%8F%8E%E5%85%A5/pg{}/?jobsearchType=14&searchType=18'.format(page)
            driver.get(url)
            #timesleep(1)

        # 検索結果の一番上の会社名を取得
            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

        #課題１　キャッチコピーを除いた会社名のみを表示
            for name in name_list:
                only_name = name.text
                exp_only_name_list.append(only_name.split('|')[0])

        # 課題２　正社員・契約社員　情報取得   
            status_list = driver.find_elements_by_class_name("cassetteRecruit__copy")

            for status_label in status_list:
                status = status_label.find_element_by_class_name("labelEmploymentStatus")
                exp_status_list.append(status.text)

        #課題２　初年度年収/給与　情報取得    
            condition_list = driver.find_elements_by_class_name("tableCondition")

            for condition_body in condition_list:
                conditions = condition_body.find_elements_by_class_name("tableCondition__body")
                conditions.reverse()
                exp_condition_list.append(conditions[0].text)
    except:
        pass

    #　「高収入」の新規案件の年収・給与を囲むdivタグのclass名について、284件目に、タイプミスがあるため、
    # 注目案件と新規案件で異なるタグ名を指定することが出来ず、共通のタグ名を使わざるを得ないので、
    # 新規案件のみに統一するため、一番最初に位置する注目案件の要素を削除する必要がある。
    # ただし、検索キーワードが変わると、注目案件が無くなる場合もあるので、
    # ここでは、「高収入」の年収と月給を会社名と雇用形態と合わせてファイル出力するための対応。
    exp_condition_list.pop(0)

    # 課題５　csvファイルに出力
    # 課題６　エラー処理
    try:
        df = pd.DataFrame()
        df['会社名'] = exp_only_name_list
        df['雇用形態'] = exp_status_list
        df['年収/給与'] = exp_condition_list

        df.to_csv('table_totals.csv')
        df.to_csv('table_totals2.csv',index=False)
    except:
        pass

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
