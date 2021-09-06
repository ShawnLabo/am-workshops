# コンテナ入門 ハンズオン

## Google Cloud Platform プロジェクトの選択

ハンズオンを行う Google Cloud プロジェクトを選択して **Start** をクリックしてください。

<walkthrough-project-setup>
</walkthrough-project-setup>

## ハンズオンの内容

下記の内容をハンズオン形式で学習します。

1. 環境準備：10 分
2. Cloud Shell 上での Docker の基本操作：15分
3. 仮想マシン上での Docker コンテナの実行：15分

<!-- ********************************
*
* ハンズオン1 環境の準備
*
******************************** -->

## ハンズオン1 環境の準備

<walkthrough-tutorial-duration duration=10></walkthrough-tutorial-duration>

最初に、ハンズオンを進めるための環境準備を行います。

下記の設定を進めていきます。

- gcloud コマンドラインツール設定
- Google Cloud サービス有効化


## gcloud コマンドラインツール設定

Google Cloud は、CLI や GUI から操作が可能です。
ハンズオンでは主に CLI で作業を行いますが、GUI で確認する URL も合わせて掲載します。

### gcloud コマンドラインツールとは?

gcloud は Google Cloud の主要な CLI ツールです。
gcloud を使用するとコマンドラインから Google Cloud を操作できます。
またはスクリプトに組み込んだり様々な自動化ツールと組み合わせることにより、多くのタスクを実行できます。

たとえば、gcloud を使用して、以下のようなものを作成・管理できます。

- Google Compute Engine 仮想マシン
- Google Kubernetes Engine クラスタ
- Cloud SQL インスタンス

**ヒント**: gcloud コマンドラインツールについての詳細は[こちら](https://cloud.google.com/sdk/gcloud?hl=ja)をご参照ください。


### デフォルトプロジェクトの設定

gcloud コマンドでは操作の対象とするプロジェクトの指定が必要です。

gcloudのデフォルトプロジェクトとして、操作対象のプロジェクトを設定しておきます。

```bash
gcloud config set project {{project-id}}
```

## Google Cloud サービス有効化

Google Cloud では利用したいサービスごとに有効化が必要です。

以降のハンズオンで利用する機能を事前に有効化しておきます。

```bash
gcloud services enable compute.googleapis.com cloudbuild.googleapis.com sourcerepo.googleapis.com artifactregistry.googleapis.com cloudresourcemanager.googleapis.com container.googleapis.com stackdriver.googleapis.com 
```

約2分かかります。

**GUI**: [APIダッシュボード](https://console.cloud.google.com/apis/dashboard?hl=ja&project={{project-id}})

<walkthrough-footnote>必要な機能が使えるようになりました。以上で環境準備は完了です。</walkthrough-footnote>


<!-- ********************************
*
* ハンズオン2 Docker の基本操作
*
******************************** -->

## Docker の基本操作

<walkthrough-tutorial-duration duration=15></walkthrough-tutorial-duration>

続いて、Cloud Shell 上で Docker の基本的な操作を実施してみます。

- Docker コンテナの実行
- Docker コンテナイメージの不変性の確認
- Docker コンテナのビルドと Artiface Registry への登録

## Cloud Shell の Docker 環境の確認

### Docker サービスの起動確認

### まず Docker サービスが起動していることを確認

serviceコマンドを実行します。

```bash
service docker status
```

万が一下記が表示された場合は起動していません。

```
[FAIL] Docker is not running ... failed!
```

起動していなかった場合は次のコマンドで起動してください。

```bash
sudo service docker start
```

## docker コマンドの基本的な使い方

### docker

`docker` コマンドを引数なしで実行すると、サブコマンドの一覧が出力されます。

```bash
docker
```

Cloud Shell には docker コマンドの補完の設定がされています。
コマンドを途中まで入力してタブを押すことで入力の支援ができます。

### docker ps

`docker ps` で起動中のコンテナを確認できます。

```bash
docker ps
```

今は実行中のコンテナはありません。

## nginx コンテナの実行

Docker Hub から nginx コンテナイメージをダウンロードして実行します。

```bash
docker run -it nginx:1.20
```

コンテナイメージ（nginx:1.20）が現在のマシン上にない場合は、自動でダウンロード (`docker pull`) します。
そして、フォアグラウンドで nginx コンテナが実行されます。
標準出力にログが出力されます。

一旦 `Ctrl + C` を数回押してコンテナを停止します。

## nginx コンテナをオプション付きで実行

```bash
docker run -d -p 8080:80 --name my-nginx --rm nginx:1.20
```

ここでは下記のオプションを付けています

- `-d`: バックグラウンドで実行します
- `-p <ホストのポート>:<コンテナのポート>`: 指定したホストのポートをコンテナのポートに転送します
- `--name <コンテナ名>`: コンテナの名前を指定しています
- `--rm`: コンテナが終了状態になった時にコンテナを削除します

今回はすでにコンテナイメージがマシンに存在しているため高速に起動します。

`docker ps` で起動していることを確認します。

```bash
docker ps
```

`my-nginx`コンテナが起動していることや、ローカルマシンの TCP ポート `8080` 番を、nginx コンテナの TCP ポート `80` 番に転送していることが確認できます。

## nginx コンテナの動作確認

### my-nginx コンテナにアクセス

画面右上にあるアイコン <walkthrough-web-preview-icon></walkthrough-web-preview-icon> をクリックして「ポート 8080 でプレビュー」を選択します。

ブラウザで新しいタブが開いて Cloud Shell で実行した `my-nginx` コンテナにアクセスできます。
正常に動作している場合は Nginx のデフォルトのページが確認できます。


### ログの確認

アクセスログが出力されていることを確認します

```bash
docker logs -f my-nginx
```

`my-nginx` で出力されているログが表示されます。

 確認できたら `Ctrl + C` で停止します。

<walkthrough-footnote>ここまでで、docker コマンドによるコンテナの実行や、コンテナ内へのポート転送について実施しました。続いて、コンテナの特徴である Immutability（不変性）について、実際に変更を加えて試してみます。</walkthrough-footnote>


## コンテナイメージの不変性を確認

コンテナを再作成すると、それまでコンテナに対して行った変更がリセットされてコンテナイメージの初期状態に戻ることを確認します。

### コンテナの内容を変更

先ほど実行した `my-nginx` コンテナのシェルを起動します。

```bash
docker exec -it my-nginx bash
```

このシェルで `my-nginx` コンテナの内部を操作できます。

### コンテナ内で実行されているプロセスを確認

`ps` コマンドをインストールします。

```bash
apt update ; apt install -y procps
```

`ps` コマンドを実行します。

```bash
ps aux
```

`my-nginx` コンテナ内で複数のプロセスが実行されていることが確認できます。

### index.html を変更

`my-nginx` コンテナの `index.html` を書き換えます。

```bash
echo "<h1>Test</h1>" > /usr/share/nginx/html/index.html
```

`Ctrl + D` でシェルから脱出します。

### index.html の変更を確認

先ほど <walkthrough-web-preview-icon></walkthrough-web-preview-icon> から開いたプレビューページを再度開いてリロードします。

ページの内容が 'Test' に変更されていることがわかります。

### my-nginx コンテナの再作成

コンテナを停止します。

```bash
docker stop my-nginx
```

再度、同じコマンドで起動します。

```bash
docker run -d -p 8080:80 --name my-nginx --rm nginx:1.20
```

### 変更のリセットを確認

再度 <walkthrough-web-preview-icon></walkthrough-web-preview-icon> から Nginx にアクセスしてリロードします。

nginx のデフォルトページに戻っていることが確認できます。

コンテナを再作成すると変更がリセットされて初期状態に戻ることが確認できました。

### my-nginx コンテナを停止

起動したコンテナを停止しておきます。

```bash
docker stop my-nginx
```

## 独自コンテナイメージのビルド

### Dockerfile の確認

Cloud Shell エディタの左側のフォルダツリーから `python-app` ディレクトリを開いてください。

以下のファイルをクリックして開いて内容を確認します。

- main.py
- Dockerfile

特に `Dockerfile` の内容をよく確認してください。

### コンテナイメージのビルド

先ほど確認した `Dockerfile` を使って、`docker build` コマンドでコンテナイメージをビルドします。

```bash
cd ~/cloudshell_open/am-workshops/container-basic/python-app/
docker build -t python-app .
```

コンテナイメージの名前 (タグ) を `python-app` としています。

### python-app イメージからコンテナを起動

ビルドした `python-app` イメージからコンテナを起動します。

```bash
docker run -d -p 8080:8080 --name python-app --rm python-app
```


### python-app コンテナの動作確認

画面右上にあるアイコン <walkthrough-web-preview-icon></walkthrough-web-preview-icon> をクリックして「ポート 8080 でプレビュー」を選択します。
Nginx のページが表示される場合はリロードしてください。

「Hello, GCP」が表示されていれば正常に動作しています。

### python-app コンテナのログを確認

`python-app` コンテナのログを確認します。

```bash
docker logs -f python-app
```

ログが確認できたら `Ctrl + C` で終了します。

## コンテナイメージを Artifact Registry に Push

### コンテナリポジトリを作成

Google Cloud のコンテナレジストリサービスである Artifact Registry に新しい Docker リポジトリを作成します。

```bash
gcloud artifacts repositories create docker-training --repository-format=docker \
--location=asia-northeast1 --description="Docker repository for Hands-on"
```

### python-app イメージに別名を設定

Artifact Registry におけるコンテナイメージの名前は次のようなパスで表現されます。

```
# <ロケーション名>-docker.pkg.dev/<プロジェクトID>/<リポジトリ名>/
asia-northeast1-docker.pkg.dev/{{project-id}}/docker-training/
```

`python-app` イメージにこちらのルールに従った別名をつけます。

```bash
docker tag python-app asia-northeast1-docker.pkg.dev/{{project-id}}/docker-training/container-handson:v1
```

### python-app イメージを Push

Cloud Shell から Artifact Registry に Push するための認証設定を行います。

```bash
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
```

「Do you want to continue (Y/n)?」と聞かれたら `y` を入力してください。

コンテナイメージを Artifact Registry に Push します。

```bash
docker push asia-northeast1-docker.pkg.dev/{{project-id}}/docker-training/container-handson:v1
```

**GUI**: [コンテナレジストリ](https://console.cloud.google.com/artifacts/docker/{{project-id}}/asia-northeast1/docker-training/container-handson?hl=ja&project={{project-id}})

コンテナイメージを Artifact Registry に保存できました。
これで、Google Kubernetes Engine や Cloud Run、または Google Cloud 外の様々な場所からコンテナイメージを利用できるようになりました。

<!-- ********************************
*
* ハンズオン3 WordPress の起動
*
******************************** -->

## WordPress の起動

<walkthrough-tutorial-duration duration=15></walkthrough-tutorial-duration>

今度は、Cloud Shell 上ではなく、仮想マシン（Google Compute Engine）を作成し、そこに Docker と Docker Compose の実行環境を作成して、コンテナを実行してみましょう。

- 仮想マシンの作成
- 仮想マシンへの Docker のインストール
- 仮想マシンへの Docker Compose のインストール
- docker-compose による WordPress アプリの実行
- Artifact Registryに Push したコンテナイメージの実行

## Google Compute Engine で仮想マシンの作成

Google Compute Engine (GCE) は Google Cloud の仮想マシンサービスです。

### 仮想マシンの作成

`docker-vm` という名前で Ubuntu の仮想マシンを作成します。

```bash
gcloud compute instances create \
  --image=ubuntu-minimal-1804-bionic-v20200703a \
  --machine-type=n1-standard-1 \
  --image-project=ubuntu-os-cloud \
  --tags=http-server \
  --metadata=startup-script-url=https://raw.githubusercontent.com/ShawnLabo/am-workshops/main/container-basic/startup-script.sh \
  --zone asia-northeast1-c \
  docker-vm
```

作成まで待ちます（10秒程度）。
GCE の作成は非常に高速です。

**GUI**: [Compute Engine](https://console.cloud.google.com/compute/instances?project={{project-id}})


### ファイアウォール ルールの作成

80番ポートへのアクセスを許可するファイアウォール ルールを作成します。

```bash
gcloud compute firewall-rules create allow-http \
--direction=INGRESS --priority=1000 --network=default \
--action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-tags=http-server
```

**GUI**: [ファイアウォール](https://console.cloud.google.com/networking/firewalls/list?project={{project-id}})

## 作成された docker-vm に接続

### ターミナルのタブの [+]マークをクリックして、もうひとつターミナルを開く

ターミナルが2つになり、タブをクリックすることで切り替えることができます

### 新しいタブでデフォルトプロジェクトを改めて設定

```bash
gcloud config set project {{project-id}}
```

### docker-vm に SSH で接続

docker-vm に SSH で接続します。
gcloud コマンドで接続することが可能です。

```bash
gcloud compute ssh docker-vm --zone asia-northeast1-c
```

最初に SSH キーのパスワードを設定しますので、適当なパスワードを設定してください。

以降、docker-vm （GCE） で実行するコマンドには`[docker-vm]`、Cloud Shell で実行するコマンドは `[Cloud Shell]` というコメントをつけています。

## Docker / Docker Compose のインストール

**docker-vm のタブで操作してください**

### Docker インストール

Docker をインストールします。

```bash
sudo apt update
sudo apt install -y docker.io
# [docker-vm]
```

Docker を起動します

```bash
sudo systemctl start docker
# [docker-vm]
```

### Docker Compose インストール

Docker Compose をインストールします。

```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-Linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# [docker-vm]
```

### インストールの確認

`docker` コマンドが正常に実行できることを確認します。

```bash
docker version
# [docker-vm]
```

バージョン情報が返ってこれば OK です。

続いて、`docker-compose` についても同様に確認してみます。

```bash
docker-compose version
# [docker-vm]
```

同じく、バージョン情報が表示されれば OK です。

<walkthrough-footnote>以上で、仮想マシン上でコンテナを実行する準備が整いました。</walkthrough-footnote>


## Docker Compose で WordPress を起動

**docker-vm のタブで操作してください**

### docker-compose.yamlの確認

今回は、[起動スクリプト](https://cloud.google.com/compute/docs/startupscript?hl=ja)によって `/tmp/wordpress-app` に `docker-compose.yaml` を作成しています。

内容を確認します。

```bash
cd /tmp/wordpress-app/
cat docker-compose.yaml
# [docker-vm]
```

`mysql`コンテナと`wordpress`コンテナの設定が書かれていることを確認してください。

### WordPress の起動

```bash
sudo docker-compose up -d
# [docker-vm]
```

※ `sudo` なしで `docker` コマンドを実行できるように設定することも可能です

### コンテナの状態を確認

```bash
sudo docker-compose ps
# [docker-vm]
```

`mysql`コンテナと`wordpress`コンテナの2つが起動している (`Up` になっている) ことがわかります。


## WordPress の動作確認

### WordPress にアクセス

**Cloud Shell のタブで操作してください**

以下のコマンドで docker-vm の IP アドレスを取得して WordPress の URL を表示します。

```bash
WWW=$(gcloud compute instances describe docker-vm --zone asia-northeast1-c --format=json | jq .networkInterfaces[].accessConfigs[].natIP -r)
echo http://$WWW
# [Cloud Shell]
```

URLをクリックしてください。
WordPress の初期設定画面が表示されることを確認してください。

### WordPress の停止

**docker-vm のタブで操作してください**

動作確認ができたら、`docker-vm` に SSH しているタブに戻ってコンテナを停止します。

```bash
cd /tmp/wordpress-app
sudo docker-compose down
# [docker-vm]
```

<walkthrough-footnote>docker-compose で DockerHub から取得したイメージを実行してみました。続いて、先ほど Artifact Registry に登録した独自コンテナイメージを実行してみましょう。</walkthrough-footnote>

## Artifact Registry に保存した python-app を実行

### docker-vm に Artifact Registry の権限を付与

**Cloud Shell のタブで操作してください**

docker-vm から Artifact Registry に対して `docker pull` できるように権限を付与する必要があります。
今回は、Compute Engine のサービスアカウントに、Artifact Registry の読み取り権限を付与します。

```bash
SERVICE_ACCOUNT=$(gcloud compute instances describe docker-vm --zone asia-northeast1-c --format=json | jq .serviceAccounts[].email -r)
gcloud projects add-iam-policy-binding {{project-id}} \
--member="serviceAccount:$SERVICE_ACCOUNT" --role='roles/artifactregistry.reader'
# [Cloud Shell]
```

**GUI**: [IAM](https://console.cloud.google.com/iam-admin/iam?project={{project-id}}&supportedpurview=project)

### docker-vm から Artifact Registry を利用するための設定

**docker-vm のタブで操作してください**

```bash
sudo gcloud auth configure-docker asia-northeast1-docker.pkg.dev
# [docker-vm]
```

Do you want to continue (Y/n)?

と聞かれたら、yを入力してください

### container-handson コンテナイメージの実行

**docker-vm のタブで操作してください**

Artifact Registryにある `container-handson` イメージでコンテナを起動します。
これは、元々 `python-app` イメージとしてビルドして Artifact Registry に Push したものです。

```bash
sudo docker run -d -p 80:8080 --restart always asia-northeast1-docker.pkg.dev/{{project-id}}/docker-training/container-handson:v1
# [docker-vm]
```

### python-app の動作確認

**Cloud Shell のタブで操作してください**

docker-vm の IP アドレスを取得して URL を表示します。

```bash
echo http://$WWW
# [Cloud Shell]
```

表示された URL をクリックしてください。
Hello, GCP と表示されることを確認してください。

<walkthrough-footnote>自分でビルドして Artifact Registry に Push したイメージを docker-vm で起動してアクセスできることが確認できました。</walkthrough-footnote>

## クリーンアップ

追加の課金を避けるため、作成したプロジェクトを削除します。
作成したリソースを個別に削除する場合は、こちらのページの手順を実施せずに次のページに進んで下さい。

### デフォルトプロジェクト設定の削除

```bash
# Cloud Shell
gcloud config unset project
```

### プロジェクトの削除

```bash
# Cloud Shell
gcloud projects delete {{project-id}}
```

プロジェクトの削除には適切な権限が必要です。
削除できない場合は、オーナー権限のアカウントをお持ちの方に依頼してください。

## Congraturations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>
これにて コンテナ入門のハンズオンは完了です！！

