# コンテナ入門 ハンズオン

## Google Cloud Platform（GCP）プロジェクトの選択

ハンズオンを行う GCP プロジェクトを選択し、 **Start** をクリックしてください。

<walkthrough-project-setup>
</walkthrough-project-setup>

## ハンズオンの内容

下記の内容をハンズオン形式で学習します。

1. 環境準備：10 分
2. CloudShell 上での Docker の基本操作：15分
3. 仮想マシン上での Docker コンテナの実行：15分

## 環境準備

<walkthrough-tutorial-duration duration=10></walkthrough-tutorial-duration>

最初に、ハンズオンを進めるための環境準備を行います。

下記の設定を進めていきます。

- gcloud コマンドラインツール設定
- GCP 機能（API）有効化設定


## gcloud コマンドラインツール

GCP は、CLI、GUI から操作が可能です。ハンズオンでは主に CLI を使い作業を行いますが、GUI で確認する URL も合わせて掲載します。

### gcloud コマンドラインツールとは?

gcloud コマンドライン インターフェースは、GCP でメインとなる CLI ツールです。このツールを使用すると、コマンドラインから、またはスクリプトや他の自動化により、多くの一般的なプラットフォーム タスクを実行できます。

たとえば、gcloud CLI を使用して、以下のようなものを作成、管理できます。

- Google Compute Engine 仮想マシン
- Google Kubernetes Engine クラスタ
- Google Cloud SQL インスタンス

**ヒント**: gcloud コマンドラインツールについての詳細は[こちら](https://cloud.google.com/sdk/gcloud?hl=ja)をご参照ください。


## gcloud コマンドラインツール設定 - プロジェクト

gcloud コマンドでは操作の対象とするプロジェクトの設定が必要です。

### GCP のプロジェクト ID を環境変数に設定

環境変数 `GOOGLE_CLOUD_PROJECT` に GCP プロジェクト ID を設定します。

```bash
export GOOGLE_CLOUD_PROJECT="{{project-id}}"
```

### CLI（gcloud コマンド） から利用する GCP のデフォルトプロジェクトを設定

操作対象のプロジェクトを設定します。

```bash
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

<walkthrough-footnote>これで、gcloud コマンドを実行する際に、毎回プロジェクトを指定しなくて済むようになりました。続いて、API の有効化を行います。</walkthrough-footnote>

## GCP 環境設定

GCP では利用したい機能ごとに、有効化を行う必要があります。
ここでは、以降のハンズオンで利用する機能を事前に有効化しておきます。

### ハンズオンで利用する GCP の API を有効化する

```bash
gcloud services enable compute.googleapis.com cloudbuild.googleapis.com sourcerepo.googleapis.com artifactregistry.googleapis.com cloudresourcemanager.googleapis.com container.googleapis.com stackdriver.googleapis.com 
```

約2分かかります。

**GUI**: [APIダッシュボード](https://console.cloud.google.com/apis/dashboard?hl=ja&project={{project-id}})

<walkthrough-footnote>必要な機能が使えるようになりました。次にリージョン・ゾーンの設定を行います。</walkthrough-footnote>


## gcloud コマンドラインツール設定 - リージョン、ゾーン

### デフォルトリージョンを設定

コンピュートリソースを作成するデフォルトのリージョンとして、日本リージョン（asia-northeast1）を指定します。

```bash
gcloud config set compute/region asia-northeast1
```

### デフォルトゾーンを設定

コンピュートリソースを作成するデフォルトのゾーンとして、日本リージョン内の 1 ゾーン（asia-northeast1-c）を指定します。

```bash
gcloud config set compute/zone asia-northeast1-c
```

<walkthrough-footnote>以上で環境準備は完了です。</walkthrough-footnote>


## CloudShell 上での Docker の基本操作

<walkthrough-tutorial-duration duration=15></walkthrough-tutorial-duration>

続いて、CloudShell 上で Docker の基本的な操作を実施してみます。

- Docker コンテナの実行
- Docker コンテナの Immutability（不変性）の確認
- Docker コンテナのビルドと Artiface Registry への登録

## CloudShell 上の Docker の確認

### Docker サービスの起動確認

### まず Docker が起動していることを確認

serviceコマンドを実行します。

```bash
service docker status
```

万が一下記が表示された場合は起動していません。

```
[FAIL] Docker is not running ... failed!
```

下記コマンドで起動してください。

```
sudo service docker start
```

## docker コマンドの基本的な使い方

### docker コマンドを引数なしで実行

dockerのサブコマンドの一覧が出力されます。

```bash
docker
```

Cloud Shellにはdockerコマンドの補完の設定がされています。

コマンドを途中まで入力してタブを押すことで入力の支援ができます。

### コンテナの起動を確認

```bash
docker ps
```

何も実行中のコンテナはありません。

## nginx コンテナの実行

```bash
docker run -it nginx:1.20
```

DockerHub から nginx イメージ（nginx:1.20）が pull されて、フォアグラウンドで nginx コンテナが実行されます。
標準出力にログの情報が出ています。

このままではWebサーバとして機能しないので、`Ctrl+c` を数回押して停止します。

## nginx コンテナのオプション付き実行

```bash
docker run -d -p 8080:80 --name my-nginx --rm nginx:1.20
```

ここでは下記のオプションを付けています

- `-d`: バックグラウンドで実行します
- `-p <ホストのポート>`:コンテナのポート: 指定したホストのポートをコンテナのポートに転送します
- `--name <コンテナ名>`: コンテナの名前を指定しています
- `--rm`: コンテナが終了状態になった時に、コンテナを削除します

キャッシュが利用されるため、起動は高速です。

実行後に、起動を確認します。

```bash
docker ps
```

Cloud Shell のマシン（開発マシン）の TCP ポート `8080` 番を、nginx コンテナの TCP ポート `80` 番に転送していることが確認できます。

## 実行した nginx コンテナへの Web アクセス

### CloudShell の機能を利用し、起動したアプリケーションにアクセス

画面右上にあるアイコン <walkthrough-web-preview-icon></walkthrough-web-preview-icon> をクリックし、"プレビューのポート: 8080"を選択します。

これによりブラウザで新しいタブが開き、Cloud Shell 上で起動しているコンテナにアクセスできます。

正しくアプリケーションにアクセスできると、Nginx のデフォルトのページが確認できます。


### ログの確認

アクセスログが出力されていることを確認します

```bash
docker logs -f my-nginx
```

上記のコマンドは `docker ps` でコンテナIDを確認して、それを引数に `logs` サブコマンドを実行しています。

確認後、`Ctrl+c` で停止します

<walkthrough-footnote>ここまでで、docker コマンドによるコンテナの実行や、コンテナ内へのポート転送について実施しました。続いて、コンテナの特徴である Immutability（不変性）について、実際に変更を加えて試してみます。</walkthrough-footnote>


## コンテナの Immutablility （不変性）を確認

### コンテナの内容を変更

先ほど実行した my-nginx コンテナのシェルにログインします。

```bash
docker exec -it my-nginx bash
```

これで my-nginx コンテナ内のシェル環境にログインできました。

### コンテナ内で実行されているプロセスを確認

`ps` コマンドをインストールします。

```bash
apt update ; apt install -y procps
```

`ps` コマンドを実行します。

```bash
ps aux
```

数個のプロセスが実行されていることが確認できます。

### ログイン後 index.html を変更

```bash
echo "<h1>Test</h1>" > /usr/share/nginx/html/index.html
```

`Ctrl+d` でシェルから脱出します。

### Web アクセスして index.html 変更の反映を確認

先ほど <walkthrough-web-preview-icon></walkthrough-web-preview-icon> から開いたプレビューページを再度開き、画面をリロードします。

ページの内容が 'Test' に変更されていることがわかります。

## コンテナの Immutablility （不変性）を確認（続き）

一時的に手動で変更された index.html の内容について、コンテナを再起動すると、変更が破棄されて nginx コンテナの初期状態に戻ることを確認します。

### コンテナを停止してから再度実行

コンテナを停止します。

```bash
docker stop my-nginx
```

再度、同じコマンドで起動します。

```bash
docker run -d -p 8080:80 --name my-nginx --rm nginx:1.20
```

### 再度、アプリケーションにアクセス、更新

nginx のデフォルトページに戻っていることが確認できます。

これで、コンテナは Immutable であり、実行時の変更を永続化しないことがわかりました。

### nginx コンテナを停止

```bash
docker stop my-nginx
```


## 独自コンテナアプリのビルド

### エディタの起動

Cloud Shell タブの上部の [エディタを開く] をクリックして、エディタを起動します。
このエディタ画面で、ファイルの確認、編集が可能です。

### ディレクトリを移動して、ファイルの内容を確認

左側のフォルダツリーから、ディレクトリを移動します。

```
python-app/
```

- main.py
- Dockerfile

を確認します。

特に Dockerfileの内容をよく確認してください。


## コンテナをビルド

### docker build コマンドでビルド実行

先ほど確認した `Dockerfile` を使って、`docker build` コマンドからコンテナをビルドしてみましょう。

```bash
cd ~/cloudshell_open/am-workshops/container-basic/python-app/
docker build -t python-app .
```

コンテナイメージの名前を `python-app` としています。

### ビルドしたコンテナを実行

```bash
docker run -d -p 8080:8080 --name python-app --rm python-app
```

`my-nginx` コンテナと同様に TCP ポート `8080`を、`python-app` の TCP ポート `8080` に転送しています。


### CloudShell の機能を利用して、起動したアプリケーションにアクセス

画面右上にあるアイコン <walkthrough-web-preview-icon></walkthrough-web-preview-icon> をクリックし、"プレビューのポート: 8080"を選択します。
Nginxのページが表示される場合はリロードしてください。


### 前と同様の手順でログを確認

```bash
docker logs -f python-app
```

`Ctrl+c` で終了します。

## コンテナイメージをコンテナリポジトリ (Artifact Registry) に転送

### 新しいコンテナリポジトリを作成

Google Cloud のコンテナレジストリサービスである Artifact Registry に、自分専用の Docker リポジトリを作成します。

```bash
gcloud artifacts repositories create docker-training --repository-format=docker \
--location=asia-northeast1 --description="Docker repository for Hands-on"
```

### コンテナレジストリ (Artifact Registry) にコンテナイメージを転送

今作成したコンテナレジストリの領域は以下のパスで表現されます。

```
# <ロケーション名>-docker.pkg.dev/<プロジェクトID>/<リポジトリ名>/
asia-northeast1-docker.pkg.dev/{{project-id}}/docker-training/
```

### ローカルでビルドしたイメージに、コンテナレジストリの名前をタグづけ

```bash
docker tag python-app asia-northeast1-docker.pkg.dev/{{project-id}}/docker-training/container-handson:v1
```

v1というタグをつけて、バージョン管理しています。

### コンテナイメージをレジストリにプッシュ

まずは、CloudShell からコンテナレジストリにプッシュするための認証設定を行います。

```bash
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
```

Do you want to continue (Y/n)?

と聞かれたら、yを入力してください

コンテナイメージを、作成したコンテナレジストリに Push します。

```bash
docker push asia-northeast1-docker.pkg.dev/{{project-id}}/docker-training/container-handson:v1
```

**GUI**: [コンテナレジストリ](https://console.cloud.google.com/artifacts/docker/{{project-id}}/asia-northeast1/docker-training/container-handson?hl=ja&project={{project-id}})

コンテナをコンテナレジストリに保存して、GKEなどから利用する準備ができました。


## 仮想マシン上での Docker コンテナの実行

<walkthrough-tutorial-duration duration=15></walkthrough-tutorial-duration>

今度は、CloudShell 上ではなく、仮想マシン（Google Compute Engine）を作成し、そこに Docker / docker-compose の実行環境を作成して、コンテナを実行してみましょう。

- 仮想マシンの作成
- 仮想マシンへの Docker / docker-compose のインストール
- docker-compose による Wordpress アプリの実行
- コンテナレジストリに登録したコンテナイメージの実行

## Google Compute Engine で仮想マシンの作成

Google Compute Engine (GCE) は Google Cloud の仮想マシンサービスです。

### 仮想マシンの作成

`docker-vm` という名前で、ubuntu ベースの仮想マシンを作成します。
下記コマンドを実行します。

```bash
gcloud compute instances create \
  --image=ubuntu-minimal-1804-bionic-v20200703a \
  --machine-type=n1-standard-1 \
  --image-project=ubuntu-os-cloud \
  --tags=http-server \
  --metadata=startup-script-url=https://raw.githubusercontent.com/ShawnLabo/am-workshops/main/container-basic/startup-script.sh \
  docker-vm
```

作成まで待ちます（10秒程度）。
GCE の作成は非常に高速です。

**GUI**: [Compute Engine](https://console.cloud.google.com/compute/instances?project={{project-id}})


### GCE に適用するファイアウォールを作成

tcp:80、tcp:8000 について、全ての接続を許可します。

```bash
gcloud compute firewall-rules create default-allow-http \
--direction=INGRESS --priority=1000 --network=default \
--action=ALLOW --rules=tcp:80,tcp:8000 --source-ranges=0.0.0.0/0 --target-tags=http-server
```

<!-- 次に、tcp:22 について、Identity-Aware Proxy (IAP) からの接続のみを許可します。

```bash
gcloud compute firewall-rules create allow-ssh-ingress-from-iap \
  --direction=INGRESS \
  --action=allow \
  --rules=tcp:22 \
  --source-ranges=35.235.240.0/20
``` -->

**GUI**: [ファイアウォール](https://console.cloud.google.com/networking/firewalls/list?project={{project-id}})

## 作成された docker-vm に接続

### ターミナルのタブの [+]マークをクリックして、もうひとつターミナルを開く

ターミナルが2つになり、タブをクリックすることで、切り替えることができます

### 新しいタブで、gcloud のデフォルトのゾーンを改めて設定

```bash
gcloud config set compute/zone asia-northeast1-c
```

### gcloud コマンドを利用した SSH 接続

<!-- `--tunnel-through-iap` オプションを指定することで、IAP 経由で安全に SSH 接続が可能です。

```bash
gcloud compute ssh docker-vm --tunnel-through-iap
``` -->

```bash
gcloud compute ssh docker-vm
```

最初にsshのキーのパスワードを設定しますので、適当なパスワードを設定してください。

※ 今後、docker-vm（GCE）上で実行するコマンドは、[GCE] というタグをSubjectにつけています。

## Docker / docker-compose のインストール

### [GCE] docker.io と vim パッケージ

```bash
sudo apt update; sudo apt install -y docker.io vim
```

dockerdを起動します

```bash
sudo systemctl start docker
```

### docker-compose

```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-Linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### docker / docker-compose の動作確認

`docker` コマンドが正常に実行できることを確認します。

```bash
docker version
```

バージョン情報が返ってこれば OK です。

続いて、`docker-compose` についても同様に確認してみます。

```bash
docker-compose version
```

同じく、バージョン情報が表示されれば OK です。

<walkthrough-footnote>以上で、仮想マシン上でコンテナを実行する準備が整いました。</walkthrough-footnote>


## WordPressアプリケーションを、docker-composeで起動

### [GCE] docker-compose.yamlの確認

今回は、仮想マシン作成時に startup script を指定することにより、自動的に `/tmp/wordpress-app` に `docker-compose.yaml` を準備しています。

内容を確認します。

```bash
cd /tmp/wordpress-app/
cat docker-compose.yaml
```

### [GCE] docker-compose で複数のコンテナを一気に起動

```bash
sudo docker-compose up -d
```

※ 現在ログイン中のユーザでは、dockerd の unix ドメインソケットに接続できないため、`sudo` をつけます

### [GCE] コンテナの起動を確認

```bash
sudo docker-compose ps
```

wordpress と mysql の Official イメージを pull して実行されていることがわかります。


## WordPress への Web アクセス確認

### 仮想マシンの URL を取得して Web アクセス

**CloudShell のタブを元の方に切り替えてから**、以下のコマンドで仮想マシンの IP アドレスを取得して、URL を表示します。

```bash
WWW=$(gcloud compute instances describe docker-vm --format=json | jq .networkInterfaces[].accessConfigs[].natIP -r)
echo http://$WWW:8000
```

URLをクリックしてアクセスして、WordPress のセットアップ画面が表示されることを確認してください。

### [GCE] 確認が終わったら停止

`docker-vm` に SSH しているタブに戻って、下記を実行してコンテナを停止します。

```bash
cd /tmp/wordpress-app
sudo docker-compose down
```

<walkthrough-footnote>docker-compose で DockerHub から取得したイメージを実行してみました。続いて、先ほど Artifact Registry に登録した独自コンテナイメージを実行してみましょう。</walkthrough-footnote>

## コンテナレジストリに保存した python-app を実行

### docker-vm で使われるサービスアカウントに Artifact Registry の権限を付与

docker-vm から Artifact Registry に対して `docker pull` する場合、Compute Engine 用に作成されたサービスアカウントに、Artifact Registry の読み取り権限を付与する必要があります。

**CloudShell のタブを元の方に切り替えてから**、以下のコマンドを実行して、権限の付与を行います。

```bash
SERVICE_ACCOUNT=$(gcloud compute instances describe docker-vm --format=json | jq .serviceAccounts[].email -r)
gcloud projects add-iam-policy-binding {{project-id}} \
--member="serviceAccount:$SERVICE_ACCOUNT" --role='roles/artifactregistry.reader'
```

**GUI**: [IAM](https://console.cloud.google.com/iam-admin/iam?project={{project-id}}&supportedpurview=project)

### [GCE] docker-vm から Artifact Registry を利用するための設定

docker-vm に SSH しているタブに戻って、下記を実行してください

```bash
sudo gcloud auth configure-docker asia-northeast1-docker.pkg.dev
```

Do you want to continue (Y/n)?

と聞かれたら、yを入力してください

### [GCE] コンテナを pull して実行

```bash
sudo docker run -d -p 80:8080 --restart always asia-northeast1-docker.pkg.dev/{{project-id}}/docker-training/container-handson:v1
```


### python-app へのアクセスを確認

現在のタブを、もう片方（CloudShell）に切り替えてください。
IPアドレスを取得して、URLを表示します。

```bash
echo http://$WWW
```

仮想マシンの 80 番ポートで、python-app のアプリに接続できることが確認できました。

## Congraturations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>
これにて コンテナ入門のハンズオンは完了です！！

<!-- ## クリーンアップ（プロジェクトを削除）

作成したリソースを個別に削除する場合は、こちらのページの手順を実施せずに次のページに進んで下さい。

### GCP のデフォルトプロジェクト設定の削除

```bash
gcloud config unset project
```

### プロジェクトの削除
```bash
gcloud projects delete {{project-id}}
```

プロジェクトの削除には適切な権限が必要です。
削除できない場合は、オーナー権限のアカウントをお持ちの方に依頼してください。
 -->
