# RepeatColab

RepeatColabは[GoogleColaboratory](https://colab.research.google.com/notebooks/welcome.ipynb)の時間制限問題を無視して1日中動かし続けるプロジェクトです。

***まだ動きません***

## Requirement
* Tool
    * python3.8
    * Chrome
    * ChromeDriver
* module
    * selenium
    * pydrive

pipenv用意したかったけどなんかできなかったからあきらめた

## Install
`git clone https://github.com/purin52002/RepeatColab.git`

## 現段階での事前処理
1. Chromeをインストール
2. Chromeを開きGoogleにログイン
3. [GoogleColaboratory](https://colab.research.google.com/notebooks/welcome.ipynb)で適当にファイルを作る
2. アドレスバーに`chrome://version/`を入力
3. [ここ](https://chromedriver.chromium.org/downloads)から4.の**GoogleChrome:** と同じバージョンの`chromedriver`をダウンロード
4. ダウンロードした`chromedriver`を`RepeatColab/`に置く
5. 4.の**プロフィールパス:** から`User Data`を`RepeatColab/`にコピーし名前を`user_plofile`にする
6. `RepeatColab/config.py`の`ColabPath.train`に3.で作ったファイルのURLを代入

## 現段階での不具合
`python sandbox.py`を実行することで、
1. Chromeを開く
2. `ColabPath.train`で設定されたcolabファイルを開く
3. `ランタイム`をクリック
4. `ランタイムのタイプを変更`をクリック
5. `ハードウェアアクセラレータ`をクリック

まで行われる。

本来なら次に`GPU`がクリックされるはずだが、されない。プログラムの該当行は`accessor.py`の64行目

有識者求む

## Licence

[MIT](https://github.com/purin52002/RepeatColab/blob/master/LICENSE)

## Author

[YuMurata](https://github.com/YuMurata)