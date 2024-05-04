#modelsは、データを保存するための仕組みを提供する
from django.db import models
#Userは、Djangoであらかじめ用意されている「ユーザー」を表すもの。WEBアプリをつくるとき、ユーザーの情報を管理する。
from django.contrib.auth.models import User

#Taksという名前のモデルを定義している。
#モデル=Djangoでデータを保存するための設計図のようなもの。
'''
Class…オブジェクト指向プログラミング（OOP）の基本的な概念。型枠や設計図。
例えば「車のクラス」…エンジンやタイヤ、ドアなどの部品。また走ったり止まったりするような動作

プログラミングにおいては、クラスを使って以下を定義することができる。
①データ（属性）定義：例）車の色、車種、速度などのデータを持たせる。
②関数（メソッドの定義）：動作の定義。例）車の加速、ブレーキ、曲がる　など

クラスからオブジェクトを作成（インスタンス化）
車のっクラスなら、My Car、Your Carなど具体的な車のインスタンスを提供。
'''
class Task(models.Model):
    #CASCADEはユーザー削除したらTaskも削除するようにする
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    createDate = models.DateTimeField(auto_now_add=True)

    #DB管理パネルで上記変数名でデータをみられるようになる
    #これをつけないとPythonのデフォルトのメモリアドレスが返されてしまう。
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["completed"]
        #日付で並び替えをしたい場合はordering = ["createDate"]とする

#ちなみにmodels.pyを作成しただけではテーブルは作成されない。
#DBに反映させるにいは、make migration／マイグレートする作業が必要。

