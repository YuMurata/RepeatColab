from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess as sp
from datetime import datetime, timedelta, timezone
import urllib3
import time

from driver import init_driver
from colab_file import ColabFile, RuntimeMode

from logger import Logger

logger = Logger(__name__, log_file_path='logs/repeat_colab.log')


class Accessor():
    def __init__(self, self_file: ColabFile, another_file: ColabFile):
        self.driver = init_driver()

        self.self_file = self_file
        self.another_file = another_file

    def click_runall(self):
        '''
        「すべてのセルを実行」をクリックする関数
        '''
        select_dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'runtime-menu-button')))
        select_dropdown.click()
        time.sleep(1)
        select_dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, ':1s')))
        select_dropdown.click()

    def click_change_runtime(self, mode: RuntimeMode):
        '''
        ランタイムのタイプを変更する関数
        '''
        # ランタイムクリック
        select_dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'runtime-menu-button')))
        select_dropdown.click()
        logger.debug('click runtime')

        # ランタイムのタイプ変更クリック
        select_dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, ':25')))
        select_dropdown.click()
        logger.debug('click change runtime type')

        # ドロップダウンクリック
        select_dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'input-4')))
        select_dropdown.click()
        logger.debug('click accelerator')

        # 待たずにクリックしてしまうことがあるので
        time.sleep(1)

        # XPATH避けたい
        # ランタイム選択
        select_dropdown = \
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[@id='accelerator']/[@value='{mode}']")))
        select_dropdown.click()
        logger.debug('click runtime type')

        # 保存ボタンクリック
        select_dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'ok')))
        select_dropdown.click()
        logger.debug('click preserve')

        logger.debug('change runtime')

    def check_time(self):
        '''
        インスタンス起動時間[Hour]を返す関数
        '''
        # インスタンスを起動してからの時間を返す
        res = sp.Popen(['cat', '/proc/uptime'], stdout=sp.PIPE)
        # 単位はHour
        use_time = float(sp.check_output(
            ['awk', '{print $1 /60 /60 }'], stdin=res.stdout).decode().replace('\n', ''))
        return use_time

    def access_another(self):
        '''
        引数のpathに設定されたページを取得し, (Colaboratory前提なので)実行する関数
        '''

        self.driver.execute_script('window.open()')  # make new tab
        self.driver.switch_to.window(
            self.driver.window_handles[-1])  # switch new tab
        self.driver.get(self.another_file.path)
        # ページの要素が全て読み込まれるまで待機
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located)
        logger.debug('open window')

        # 指定のURLにアクセスできているか確認(認証ページに飛ばされていないか確認)
        cur_url = self.driver.current_url
        logger.debug(f'opened url: {cur_url}')

        # ランタイムのタイプを変更する
        self.click_change_runtime(self.another_file.mode)

        # 全てのセルを実行する
        self.click_runall()

        logger.info('access another')

    def access_self(self):
        '''
        引数のpathに設定されたページを取得するだけの関数
        '''
        try:
            # 新規タブを開いて更新処理
            self.driver.execute_script('window.open()')  # make new tab
            self.driver.switch_to.window(
                self.driver.window_handles[-1])  # switch new tab
            self.driver.get(self.self_file.path)
            # ページの要素が全て読み込まれるまで待機
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located)
            logger.debug('open window')

            # 指定のURLにアクセスできているか確認(認証ページに飛ばされていないか確認)
            cur_url = self.driver.current_url
            logger.debug(f'opened url: {cur_url}')

            self.click_change_runtime(self.self_file.mode)
            time.sleep(30)

            logger.info('access self')

        except urllib3.exceptions.NewConnectionError as e:
            print(str(e))
            print('********Portal New connection timed out***********')
            time.sleep(30)

        except urllib3.exceptions.MaxRetryError as e:
            print(str(e))
            time.sleep(30)
            print('*********Portal Max tries exceeded************')

    # def git_push(self):
    #     '''
    #     addしてcommitしてpushする関数
    #     '''
    #     try:
    #         repo = git.Repo.init()
    #         repo.index.add(self.store_path)
    #         repo.index.commit('add elapsed_time.txt')
    #         origin = repo.remote(name='origin')
    #         origin.push()
    #         return 'Success'

    #     except:
    #         return 'Error'

    def main(self):

        while True:
            elapsed_time = self.check_time()
            print(elapsed_time)

            # 検証用の処理
            jtime = self.get_japan_time()
            append_text = 'File A : ' + \
                str(elapsed_time) + ' Hour (' + \
                str(jtime.strftime('%H:%M:%S')) + ')\n'
            self.append_time_file(append_text)

            # 11時間越えたら
            if elapsed_time > 11:
                # GitHubにプッシュ
                result = self.git_push()
                self.set_mode('None')
                # ColaboratoryファイルBを開く
                self.access_another_colabo(self.access_path)

                self.set_mode('GPU')
                self.auto_access(self.access_path_2)
                break

            else:
                self.set_mode('GPU')
                self.auto_access(self.access_path_2)
                # 60分ごとにチェック
                time.sleep(3600)

        print('Done.')
