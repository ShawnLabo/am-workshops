# コンテナ入門 ハンズオン

## Google Cloud Platform（GCP）プロジェクトの選択

ハンズオンを行う GCP プロジェクトを選択し、 **Start** をクリックしてください。

<walkthrough-project-setup>
</walkthrough-project-setup>


## ハンズオンの内容
下記の内容をハンズオン形式で学習します。

- 環境準備：10 分
  - gcloud コマンドラインツール設定
  - GCP 機能（API）有効化設定


## 環境準備

<walkthrough-tutorial-duration duration=10></walkthrough-tutorial-duration>

最初に、ハンズオンを進めるための環境準備を行います。

下記の設定を進めていきます。

- gcloud コマンドラインツール設定
- GCP 機能（API）有効化設定

## gcloud コマンドラインツール

GCP は、CLI、GUI から操作が可能です。ハンズオンでは主に CLI を使い作業を行いますが、GUI で確認する URL も合わせて掲載します。


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

<walkthrough-footnote>CLI（gcloud）を利用する準備が整いました。次にハンズオンで利用する機能を有効化します。</walkthrough-footnote>


## GCP 環境設定

GCP では利用したい機能ごとに、有効化を行う必要があります。
ここでは、以降のハンズオンで利用する機能を事前に有効化しておきます。

### ハンズオンで利用する GCP の API を有効化する

```bash
gcloud services enable compute.googleapis.com cloudbuild.googleapis.com sourcerepo.googleapis.com containerregistry.googleapis.com cloudresourcemanager.googleapis.com container.googleapis.com stackdriver.googleapis.com 
```
約2分かかります。

**GUI**: [APIダッシュボード](https://console.cloud.google.com/apis/dashboard?hl=ja&project={{project-id}})

<walkthrough-footnote>必要な機能が使えるようになりました。次にサービスアカウントの設定を行います。</walkthrough-footnote>

## Cloud ShellでDockerサービスおよびdockerコマンドの確認

### Dockerサービスの起動確認

### まずDockerが起動していることを確認します
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

## dockerコマンドの基本的な使い方

### dockerコマンドを引数なしで実行します
dockerのサブコマンドの一覧が出力されます。
```bash
docker
```
Cloud Shellにはdockerコマンドの補完の設定がされています。

コマンドを途中まで入力してタブを押すことで入力の支援ができます。

### コンテナの起動を確認します
```bash
docker ps
```
何も実行中のコンテナはありません。

## nginxコンテナを実行します
```bash
docker run -it nginx:1.19
```
DockerHubからnginxイメージ（nginx:1.19）がpullされて、フォアグラウンドでnginxコンテナが実行されます。
標準出力にログの情報が出ています。

このままではWebサーバとして機能しないので、Ctrl + cで停止します。

## nginxコンテナをバックグラウンドで、かつポート転送を指定して起動します
```bash
docker run -d -p 8080:80 --name my-nginx --rm nginx:1.19
```
ここでは下記のオプションを付けています
- -d: バックグラウンドで実行します
- -p ホストのポート:コンテナのポート: 指定したホストのポートをコンテナのポートに転送します
- --name コンテナ名: コンテナの名前を指定しています
- --rm: コンテナが終了状態になった時に、コンテナを削除します

キャッシュが利用されるため、起動は高速です。

実行後に、起動を確認します。
```bash
docker ps
```
Cloud Shellのマシン（開発マシン）のTCPポート8080番を、nginxコンテナのTCPポート80版に転送していることが確認できます。

## 開発マシンで起動しているnginxコンテナにアクセスします

### CloudShell の機能を利用し、起動したアプリケーションにアクセスする

画面右上にあるアイコン <walkthrough-web-preview-icon></walkthrough-web-preview-icon> をクリックし、"プレビューのポート: 8080"を選択します。
これによりブラウザで新しいタブが開き、Cloud Shell 上で起動しているコンテナにアクセスできます。

正しくアプリケーションにアクセスできると、Nginxのデフォルトのページが確認できます。


### ログの確認
アクセスログが出力されていることを確認します

```bash
docker logs -f my-nginx
```
上記のコマンドはdocker psでコンテナIDを確認して、それを引数にlogsサブコマンドを実行しています。

確認後、Ctrl+cで停止します

## コンテナのImmutableの特性を確認します

### コンテナの内容を変更します
コンテナのシェルにログインします。
```bash
docker exec -it my-nginx bash
```
これでコンテナのシェル環境にログインできました。

### コンテナのプロセスを確認します
psコマンドを入れます。
```bash
apt update ; apt install -y procps
```
psコマンドを実行します。
```bash
ps aux
```
数個のプロセスが実行されていることが確認できます。

### ログイン後、index.htmlを変更します。
```bash
echo "<h1>Test</h1>" > /usr/share/nginx/html/index.html
```
Ctrl + d でシェルから脱出します。

### 再度、アプリケーションにアクセス、更新します
ページの内容が 'Test' に変更されていることがわかります


## コンテナのImmutableの特性を確認します（続き）
### コンテナを停止、再度実行します
コンテナを停止します。
```bash
docker stop my-nginx
```
再度、同じコマンドで起動します。
```bash
docker run -d -p 8080:80 --name my-nginx --rm nginx:1.19
```

### 再度、アプリケーションにアクセス、更新します
nginxのデフォルトページに戻っていることが確認できます。

これで、コンテナはImmutableであり、実行時の変更を永続化しないことがわかりました。

### nginxコンテナを停止します
```bash
docker stop my-nginx
```


## 独自のコンテナアプリのビルド
### Cloud Shellタブの上部の[エディタを開く]をクリックして、エディタを起動します
このエディタ画面で、ファイルの確認、編集が可能です。

### ディレクトリを移動して、ファイルの内容を確認します
左側のフォルダツリーから、ディレクトリを移動します。
```
gcp-handson/
  -> container-basic/
    -> python-app/
```
- main.py
- Dockerfile

を確認します。

特に Dockerfileの内容をよく確認してください。


## コンテナをビルドします
### ファイル（コード）の準備ができたので、コンテナイメージ作成のためにビルドします
```bash
cd ~/gcp-handson/container-basic/python-app/
docker build -t python-app .
```
コンテナの名前は python-appとしています。
### ビルドが完了した後に、python-appを実行します
```bash
docker run -d -p 8080:8080 --name python-app --rm python-app
```
nginxコンテナと同様に TCPポート8080を、python-appのTCPポート8080に転送しています。


### CloudShell の機能を利用し、起動したアプリケーションにアクセスする

画面右上にあるアイコン <walkthrough-web-preview-icon></walkthrough-web-preview-icon> をクリックし、"プレビューのポート: 8080"を選択します。


### 前の手順同様、ログを確認してみてください
```bash
docker logs -f python-app
```
Ctrl + cで終了します。


## コンテナをレジストリに転送します
### コンテナレジストリ Google Container Registry（GCR）にコンテナイメージを転送します
コンテナレジストリの領域はプロジェクトごとに作成され、名前が決められています。
```
# gcr.io/プロジェクト名/
gcr.io/{{project-id}}/
```

### ローカルでビルドしたイメージに、コンテナレジストリの名前をタグづけします
```bash
docker tag python-app gcr.io/{{project-id}}/container-handson:v1
```
v1というタグをつけて、バージョン管理しています。

### コンテナレジストリにプッシュします
```bash
docker push gcr.io/{{project-id}}/container-handson:v1
```
**GUI**: [コンテナレジストリ](https://console.cloud.google.com/gcr/images/{{project-id}}?project={{project-id}})

コンテナをコンテナレジストリに保存して、GKEなどから利用する準備ができました。
## Congraturations!
<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>
これにて コンテナのハンズオンは完了です！！

講師の説明をお待ちください。

## Google Kubernetes Engine を用いたアプリケーション開発


コンテナ、Kubernetes を利用したアプリケーション開発を体験します。


## GKE クラスターの作成、設定

コンテナレジストリに登録したコンテナを動かすための、GKE 環境を準備します。

### GKE クラスターを作成する

```bash
gcloud beta container clusters create "k8s-container-handson"  \
--scopes "https://www.googleapis.com/auth/cloud-platform" \
--enable-stackdriver-kubernetes \
--enable-ip-alias \
--num-nodes 2 \
--enable-autoscaling --min-nodes "2" --max-nodes "3"
```

**参考**: クラスターの作成が完了するまでに、5分から最大10分程度時間がかかることがあります。


### 作成中のGKEクラスターを確認しましょう
**GUI**: [GKEクラスター](https://console.cloud.google.com/kubernetes/list?project={{project-id}})

### GKEクラスターを構成するノードも確認しましょう
**GUI**: [Compute Engine](https://console.cloud.google.com/compute/instances?project={{project-id}})

### コマンドが完了するまで待ちます。


<walkthrough-footnote>クラスターが作成できました。次にクラスターを操作するツールの設定を行います。</walkthrough-footnote>


## GKEクラスターのKubernetesに対して アクセス設定を行います

Kubernetes には専用の [コマンド（kubectl）](https://kubernetes.io/docs/reference/kubectl/overview/)が用意されており、Cloud Shellには予めインストールされています。

認証情報を取得し、作成したクラスターを操作できるようにします。

```bash
gcloud container clusters get-credentials k8s-container-handson
```
## Kubernetesの世界へようこそ！
ここからはKubernetesで統一化された操作が可能です。
Cloud Shellには、kubectlコマンドが用意されています。

### ノードを確認します(Kubernetes上の管理)
```bash
kubectl get nodes
```

### 起動しているpodを確認します
```bash
kubectl get pods
```
何も表示されていないはずです。

### 管理用のpodを覗いてみます
-n で管理用の名前空間を指定しています。
```bash
kubectl get pods -n kube-system
```

<walkthrough-footnote>kubectl コマンドから作成したクラスターを操作できるようになりました。次に作成済みのコンテナをクラスターにデプロイします。</walkthrough-footnote>


## コンテナの GKE へのデプロイ、外部公開

### Kubernetesのmanifestを確認します
エディタを使って、gke-configディレクトリの配下を確認してください。

ファイルツリーから、下記のディレクトリに移動して、各ファイルをクリックします。
```
gcp-handson
 -> container-basic
   -> python-app
     -> gke-config
```
1つはdeploymentのテンプレートとして用意しています。


### テンプレートを使って、マニフェストを作成します。
下記は、linuxのenvsubstコマンドを使って、$GOOGLE_CLOUD_PROJECT 環境変数を置き換えています。
（エディタで直接置き換えても大丈夫です。）
```bash
envsubst < gke-config/deployment.yaml.tpl > gke-config/deployment.yaml
```

### コンテナを Kubernetes クラスターへデプロイする
```bash
kubectl apply -f gke-config/
```

このコマンドにより、Kubernetes の 3 リソースが作成され、インターネットからアクセスできるようになります。

**GUI**: [Deployment](https://console.cloud.google.com/kubernetes/workload?project={{project-id}}), [Service/Ingress](https://console.cloud.google.com/kubernetes/discovery?project={{project-id}})


## kubectlコマンドで確認します

- Pod
```bash
kubectl get pods
```
- Service
```bash
kubectl get service
```

<walkthrough-footnote>コンテナを GKE にデプロイし、外部公開できました。次にデプロイしたアプリケーションにアクセスします。</walkthrough-footnote>


## コンテナの GKE へのデプロイ、外部公開 - 動作確認

### アクセスするグローバル IP アドレスの取得

デプロイしたコンテナへのアクセスを待ち受ける Service の IP アドレスを確認します。

```bash
kubectl get service container-handson-loadbalancer
```
EXTERNAL-IP（グローバルIP）が'Pending'と表示される場合は、まだIPアドレスが割り当てられていません。
割り当てられるまで何度か実行してください。
(1分程度かかります。)

### コンテナへアクセス

下記のコマンドを実行し出力された URL をクリックし、アクセスします。

```bash
export SERVICE_IP=$(kubectl get service container-handson-loadbalancer -o json | jq .status.loadBalancer.ingress[0].ip -r); echo "http://${SERVICE_IP}/"
```
(上記はハンズオンをしやすくするためのもので必須ではありません)



## スケールアウト

### 下記を実行し、Podが単一であることを確認してください。
```bash
kubectl get pods -o wide
```
### 下記URLにアクセスすると、Podのホスト名が確認できます。
再読み込みを繰り返して、ホスト名が変わらないことを確認してください。
```bash
echo http://$SERVICE_IP/hostname
```

### 次のコマンドを実行して、Podをスケールアウトします
```bash
kubectl scale deployment container-handson-deployment --replicas=3
```
### Podの増加を確認します
下記を実行することで、Podのノードへの配置も確認できます。
```bash
kubectl get pods -o wide
```

### 再度URLにアクセスして、3つのPodにロードバランスされていることを確認します
```bash
echo http://$SERVICE_IP/hostname
```
(上記はハンズオンをしやすくするためのもので必須ではありません)

ページをリロードするたびに、ロードバランスで別々のPodにアクセスされて、ホスト名が変わることが確認できます。


## Operations（旧名 Stackdriver） を利用したアプリケーションの運用

<walkthrough-tutorial-duration duration=10></walkthrough-tutorial-duration>

- [Cloud Logging](https://cloud.google.com/logging/) によるログ管理

## Cloud Logging によるログ管理

サンプルアプリケーションでは標準出力にログを出力しています。
それらは自動的に Cloud Logging に連携され、表示、検索などをすることが可能です。

**GUI**: [ロギング](https://console.cloud.google.com/logs/viewer?&project={{project-id}}&resource=k8s_container)

Logging のページに遷移し、コンテナのアプリケーションから出力されたログが表示されていることを確認します。


![Logging](https://storage.googleapis.com/devops-handson-for-github/StackdriverLogging.png)

クラスターのログ（マスター）も確認可能です。

**GUI**: [クラスターのログ](https://console.cloud.google.com/logs/viewer?project={{project-id}}&resource=k8s_cluster)

<walkthrough-footnote>Cloud Logging からアプリケーション、その他のログを確認しました。</walkthrough-footnote>


- 水平オートスケーリング
## [追加] 水平オートスケーリング
Compute Engineと連携した 水平オートスケーリングを確認します。

podが自動的にスケールし、加えてノードとなっているCompute Engineも自動的に増減します。

## Horizontal Pod AutoScaler(HPA)を有効にします
### 下記コマンドを実行して、HPAを適用します
```bash
cd ~/gcp-handson/container-basic/python-app
kubectl apply -f hpa
```

### 適用された設定内容を確認します
```bash
kubectl get hpa
```

## 負荷をかけて、スケーリングを試します
### Cloud Shell にabコマンドをインストールします
```bash
sudo apt update
sudo apt install -y apache2
```

### abコマンドを使って、負荷をかける専用のURLに連続アクセスを実行します
```bash
ab -c 20 -n 300 http://$SERVICE_IP/fuka
```
約30秒から1分程度で終了します。

### 負荷状況を確認します
```bash
kubectl get hpa
```

## 自動でスケールアウトしている状況を確認します
### podが自動で増えていることを確認します
```bash
kubectl get pod
```

### ノードとなるGCEもスケールして増えていることを確認します
```bash
kubectl get nodes
```

GCP側でもCompute Engineが増えていることを確認します。

**GUI**: [Compute Engine](https://console.cloud.google.com/compute/instances?project={{project-id}})

### pod およびノードの自動スケールが実行されていることを確認できたら、完了となります

## Congraturations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

これにて GKE の基本ハンズオンは完了です！！


### 追加のハンズオンを実施する方は、次に進んでください。

ここで終了する方は、末尾までスキップして、リソースの削除の手順を実行してください。
## 追加ハンズオンの流れ
- IngressによるL7ロードバランサ
- Cloud Build によるビルド、デプロイの自動化


## IngressによるL7ロードバランサ
L7ロードバランサであるIngressをデプロイすると、Google Cloud Load Balancerがデプロイされます。
ここでは、URLのパスによるアプリケーションの振り分けを試します。

### Ingressの確認

前の手順で、実はService の作成と同時に、Ingress も作成しています。

### Ingressの一覧
```bash
kubectl get ingress
```


### Ingress へのアクセス
```bash
INGRESS_IP=$(kubectl get ingress container-handson-ingress -o json | jq .status.loadBalancer.ingress[].ip -r)
echo http://$INGRESS_IP/
```
(上記はハンズオンをしやすくするためのもので必須ではありません。)

Ingressのデプロイは時間がかかるため、現在はまだアクセスができない可能性があります。


## phpアプリのデプロイ
### ディレクトリを移動します
```bash
cd ~/gcp-handson/container-basic/php-app
```

### コンテナをビルドし、コンテナレジストリ（Google Container Registry）へ登録（プッシュ）する
今回は、gcloudコマンドを利用して、ビルド、登録を同時に行います。
```bash
gcloud builds submit -t gcr.io/{{project-id}}/php-app:v1
```

## パスによる振り分け
### テンプレートを使って、マニフェストを作成します。
下記コマンドは、linuxのenvsubstコマンドを使って、$GOOGLE_CLOUD_PROJECT 環境変数を置き換えています。
```bash
envsubst < gke-config/deployment.yaml.tpl > gke-config/deployment.yaml
```

### phpアプリとIngressの変更をデプロイします
```bash
kubectl apply -f gke-config/
```

### 作成されたリソースを確認します
```bash
kubectl get pods,services,ingress
```

## アクセスして振り分けの動作を確認します
メインのページ
```bash
echo http://$INGRESS_IP/
echo http://$INGRESS_IP/hostname
```
追加したpodのページ
```bash
echo http://$INGRESS_IP/php/
```
Ingressへの反映は5〜10分程度時間がかかる場合があります。
しばらくは404 Not found、または502 Server Errorが表示されます。




## [追加] Cloud Build によるビルド、デプロイの自動化


<walkthrough-tutorial-duration duration=30></walkthrough-tutorial-duration>

Cloud Build を利用し今まで手動で行っていたアプリケーションのビルド、コンテナ化、リポジトリへの登録、GKE へのデプロイを自動化します。

下記の手順で進めていきます。

- [Cloud Source Repositories](https://cloud.google.com/source-repositories/) へのリポジトリの作成
- [Cloud Build トリガー](https://cloud.google.com/cloud-build/docs/running-builds/automate-builds) の作成
- Git クライアントの設定
- ソースコードの Push をトリガーにした、アプリケーションのビルド、GKE へのデプロイ


## Cloud Build サービスアカウントへの権限追加

Cloud Build を実行する際に利用されるサービスアカウントを取得し、環境変数に格納します。

```bash
export CB_SA=$(gcloud projects get-iam-policy $GOOGLE_CLOUD_PROJECT | grep cloudbuild.gserviceaccount.com | uniq | cut -d ':' -f 2)
```

上で取得したサービスアカウントに Cloud Build から自動デプロイをさせるため Kubernetes 管理者の権限を与えます。

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT  --member serviceAccount:$CB_SA --role roles/container.admin
```

**GUI**: [IAM](https://console.cloud.google.com/iam-admin/iam?project={{project-id}})

***@cloudbuild.gserviceaccount.com のアカウントを探し、[Kubernetes管理者]権限がついていることを確認します。

<walkthrough-footnote>Cloud Build で利用するサービスアカウントに権限を付与し、Kubernetes に自動デプロイできるようにしました。次に資材を格納する Git リポジトリを作成します。</walkthrough-footnote>


## Cloud Source Repository（CSR）に Git レポジトリを作成

今回利用しているソースコードを配置するためのプライベート Git リポジトリを、Cloud Source Repository（CSR）に作成します。

```bash
gcloud source repos create container-handson
```

**GUI**: [Source Repository](https://source.cloud.google.com/{{project-id}}/container-handson): 作成前にアクセスすると拒否されます。

<walkthrough-footnote>資材を格納する Git リポジトリを作成しました。次にこのリポジトリに更新があったときにそれを検知し、処理を開始するトリガーを作成します。</walkthrough-footnote>


## Cloud Build トリガーを作成

Cloud Build に前の手順で作成した、プライベート Git リポジトリに push が行われたときに起動されるトリガーを作成します。

```bash
gcloud beta builds triggers create cloud-source-repositories --description="containerhandson" --repo=container-handson --branch-pattern=".*" --build-config="container-basic/cloudbuild.yaml"
```

**GUI**: [ビルドトリガー](https://console.cloud.google.com/cloud-build/triggers?project={{project-id}})

<walkthrough-footnote>リポジトリの更新を検知するトリガーを作成しました。次にリポジトリを操作する Git クライアントの設定を行います。</walkthrough-footnote>


## Git クライアント設定

### ディレクトリを移動します
```bash
cd ~/gcp-handson/container-basic/python-app
```
### 認証設定

Git クライアントで CSR と認証するための設定を行います。

```bash
git config --global credential.https://source.developers.google.com.helper gcloud.sh
```

**ヒント**: git コマンドと gcloud で利用している IAM アカウントを紐付けるための設定です。

### git設定

- USERNAME を自身のユーザ名に置き換えて実行し、利用者を設定します。
```bash
git config --global user.name USERNAME
```
- USERNAME@EXAMPLE.com を自身のメールアドレスに置き換えて実行し、利用者のメールアドレスを設定します。

```bash
git config --global user.email USERNAME@EXAMPLE.com
```
<walkthrough-footnote>Git クライアントの設定を行いました。次に先程作成した CSR のリポジトリと、Cloud Shell 上にある資材を紐付けます。</walkthrough-footnote>


## Git リポジトリ設定

CSR を Git のリモートレポジトリとして登録します。

```bash
cd ~/gcp-handson
git remote add google https://source.developers.google.com/p/$GOOGLE_CLOUD_PROJECT/r/container-handson
```

<walkthrough-footnote>以前の手順で作成した CSR のリポジトリと、Cloud Shell 上にある資材を紐付けました。次にその資材をプッシュします。</walkthrough-footnote>


## CSR へのコードのプッシュ

以前の手順で作成した CSR は空の状態です。
git push コマンドを使い、CSR に資材をプッシュします。

```bash
git push google master
```

**GUI**: [Source Repository](https://source.cloud.google.com/{{project-id}}/container-handson) から資材がプッシュされたことを確認できます。

<walkthrough-footnote>Cloud Shell 上にある資材を CSR のリポジトリにプッシュしました。次に資材の更新をトリガーに処理が始まっている Cloud Build を確認します。</walkthrough-footnote>


## Cloud Build トリガーの動作確認

### Cloud Build の自動実行を確認

[Cloud Build の履歴](https://console.cloud.google.com/cloud-build/builds?project={{project-id}}) にアクセスし、git push コマンドを実行した時間にビルドが実行されていることを確認します。

### 新しいコンテナのデプロイ確認

ビルドが正常に完了後、以下コマンドを実行し、Cloud Build で作成したコンテナがデプロイされていることを確認します。

```bash
kubectl describe deployment/container-handson-deployment | grep Image
```

`error: You must be logged in to the server (Unauthorized)` というメッセージが出た場合は、再度コマンドを実行してみてください。

コマンド実行結果の例。

```
    Image:        gcr.io/{{project-id}}/container-handson:COMMITHASH
```

Cloud Build 実行前は Image が `gcr.io/{{project-id}}/container-handson:v1` となっていますが、実行後は `gcr.io/{{project-id}}/container-handson:COMMITHASH` になっている事が分かります。
実際は、COMMITHASH には Git のコミットハッシュ値が入ります。

<walkthrough-footnote>資材を更新、プッシュをトリガーとしたアプリケーションのビルド、コンテナ化、GKE へのデプロイを行うパイプラインが完成しました。</walkthrough-footnote>


## アプリケーションの修正

/ にアクセスをすると"Hello, GCP"が表示されます。

この文字列を変更して、自動でGKEにデプロイしてみましょう。

```bash
echo "http://$INGRESS_IP/"
```
(上記はハンズオンをしやすくするためのもので必須ではありません)

### ソースコードの修正
エディタのフォルダツリーで、ディレクトリを移動します。
```
gcp-handson
  -> container-basic
    -> python-app
```
main.py がアプリケーションのソースコードです。
messageの変数を好きな文字列に置き換えてみてください。
（変更後、[File]メニューから、[Save]します。）

### Git に修正をコミット、CSR にpush

今行った修正を git コマンドを使い、コミット、CSR にpushします。

変更をコミット、プッシュします。
```bash
cd ~/gcp-handson
git commit -va -m modify
git push google master
```


## Cloud Build の自動実行を確認

[Cloud Build の履歴](https://console.cloud.google.com/cloud-build/builds?project={{project-id}}) にアクセスし、git push コマンドを実行した時間にビルドが実行されていることを確認します。

### Kubernetesのローリングアップデートの確認 ###
デプロイ後、サービスが停止することなく、新しいバージョンに入れ替わる様子が確認できます。
```bash
kubectl get pods -w
```
Ctrl+cで停止します

### アプリケーションにアクセスし、変更した文字列を確認してください。

```bash
echo "http://$INGRESS_IP/"
```
(上記はハンズオンをしやすくするためのもので必須ではありません)


## Congraturations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

これにて コンテナ/Kubernetesの入門ハンズオンは全て完了です！！

次の手順でクリーンアップを行って下さい。

## クリーンアップ（プロジェクトを削除）

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