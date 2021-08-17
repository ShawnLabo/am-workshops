# Cloud Run入門 ハンズオン

## Google Cloud Platform（GCP）プロジェクトの選択

ハンズオンを行う GCP プロジェクトを選択し、 **Start** をクリックしてください。

<walkthrough-project-setup>
</walkthrough-project-setup>

## ハンズオンの内容

下記の内容をハンズオン形式で学習します。

- 環境準備：10 分
  - gcloud コマンドラインツール設定
  - GCP 機能（API）有効化設定

- [Cloud Run（フルマネージド）](https://console.cloud.google.com/run?) を用いたアプリケーション開発：50 分

## 環境準備


<walkthrough-tutorial-duration duration=10></walkthrough-tutorial-duration>

最初に、ハンズオンを進めるための環境準備を行います。

下記の設定を進めていきます。

- gcloud コマンドラインツール設定
- GCP 機能（API）有効化設定
- サービスアカウント設定


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

## GCP 環境設定

GCP では利用したい機能ごとに、有効化を行う必要があります。
ここでは、以降のハンズオンで利用する機能を事前に有効化しておきます。

### ハンズオンで利用する GCP の API を有効化する

```bash
gcloud services enable cloudbuild.googleapis.com sourcerepo.googleapis.com artifactregistry.googleapis.com cloudresourcemanager.googleapis.com container.googleapis.com stackdriver.googleapis.com cloudtrace.googleapis.com cloudprofiler.googleapis.com logging.googleapis.com sqladmin.googleapis.com run.googleapis.com sql-component.googleapis.com vision.googleapis.com
```

**GUI**: [APIライブラリ](https://console.cloud.google.com/apis/library?project={{project-id}})



## サービスアカウントの作成、権限設定

アプリケーションから他の GCP サービスを利用する場合、個々のエンドユーザーではなく、専用の Google アカウント（サービスアカウント）を作ることを強く推奨しています。

### ハンズオン向けのサービスアカウントを作成する

`my-cloudrun` という名前で、ハンズオン専用のサービスアカウントを作成します。

```bash
gcloud iam service-accounts create my-cloudrun --display-name "Cloud Run Service Account"
```

**ヒント**: サービスアカウントについての詳細は[こちら](https://cloud.google.com/iam/docs/service-accounts)をご参照ください。

### サービスアカウント名を保存しておきます
```bash
SERVICE_ACCOUNT=my-cloudrun@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
```

**GUI**: [サービスアカウント](https://console.cloud.google.com/iam-admin/serviceaccounts?project={{project-id}})

## サービスアカウントに権限（IAM ロール）を割り当てる

作成したサービスアカウントには GCP リソースの操作権限がついていないため、ここで必要な権限を割り当てます。

下記の権限を割り当てます。

- Cloud SQL Clientロール (roles/cloudsql.client)
- Cloud pubsub Editorロール（roles/pubsub.editor）

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT  --member serviceAccount:$SERVICE_ACCOUNT --role roles/cloudsql.client
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT  --member serviceAccount:$SERVICE_ACCOUNT --role roles/pubsub.editor
```
**GUI**: [IAM](https://console.cloud.google.com/iam-admin/iam?project={{project-id}})



## Cloud Runを使ったアプリケーション開発

<walkthrough-tutorial-duration duration=40></walkthrough-tutorial-duration>

コンテナ、Cloud Runを利用したアプリケーション開発を体験します。

下記の手順で進めていきます。

- サンプルアプリケーションのコンテナ化
- Cloud SQL の作成
- コンテナの [Artifact Registry](https://cloud.google.com/artifact-registry/) への登録
- Cloud Run のデプロイ

## サンプルアプリケーションの確認

画面右上にあるアイコン <walkthrough-cloud-shell-editor-icon></walkthrough-cloud-shell-editor-icon> をクリックし、Cloud Shell エディタを開きます。
すでにエディタが開いている場合は必要ありません。
右側のファイルツリーからファイルをクリックして、内容を表示、編集できます。

### アプリケーションのコード、Dockerfileを確認します
下記ディレクトリに移動します。
```
~/gcp-handson
  -> cloud-run-basic
    -> web-db
```
2つのファイルを確認します。
- main.py
- Dockerfile

## パラメータの設定
```bash
export DB_NAME=mydb
export DB_PASS=Himitsupass
export DB_USER=root
export CLOUD_SQL=my-cloud-sql
export CLOUD_SQL_CONNECTION_NAME=$PROJECT:$REGION:$CLOUD_SQL
```

## Cloud SQLインスタンスの作成
### 下記コマンドを実行して、Cloud SQLインスタンス（MySQL）を作成します
```bash
gcloud sql instances create $CLOUD_SQL --database-version=MYSQL_5_7 --tier=db-n1-standard-1       --region=asia-northeast1 --root-password=$DB_PASS
```
約5分かかります

**GUI**: [Cloud SQL](https://console.cloud.google.com/sql/instances?project={{project-id}})

### データベースを作成します

```bash
gcloud sql databases create --instance=$CLOUD_SQL $DB_NAME
```

## サンプルアプリケーションのビルドとレジストリ登録

### 新しいコンテナリポジトリを作成

Google Cloud のコンテナレジストリサービスである Artifact Registry に、自分専用の Docker リポジトリを作成します。

```bash
gcloud artifacts repositories create cloud-run-training --repository-format=docker \
--location=asia-northeast1 --description="Docker repository for Hands-on"
```

### コンテナのタグ名を設定

コンテナレジストリ (Artifact Registry) のルールに則ったタグ名を環境変数に用意しておきます。

```bash
export AR_IMAGE=asia-northeast1-docker.pkg.dev/{{project-id}}/cloud-run-training/web-db:v1
```

### コンテナを作成する

Pythonで作成されたサンプル Web アプリケーションをコンテナ化します。
同時にコンテナレジストリに登録します。

```bash
cd ~/gcp-handson/cloud-run-basic/web-db/
gcloud builds submit -t $AR_IMAGE
```

**GUI**: [コンテナレジストリ](https://console.cloud.google.com/artifacts/docker/{{project-id}}/asia-northeast1/cloud-run-training/container-handson?hl=ja&project={{project-id}})


## Cloud Runにコンテナをデプロイする

### gcloudコマンドで、Cloud Runを作成し、コンテナをデプロイします
Cloud Runの名前はweb-dbにしています。

```bash
gcloud run deploy --set-cloudsql-instances=$CLOUD_SQL --image=$AR_IMAGE --set-env-vars=DB_USER=$DB_USER,DB_NAME=$DB_NAME,DB_PASS=$DB_PASS,CLOUD_SQL_CONNECTION_NAME=$GOOGLE_CLOUD_PROJECT:asia-northeast1:$CLOUD_SQL --service-account=$SERVICE_ACCOUNT --platform=managed --region=asia-northeast1 --allow-unauthenticated web-db
```

**参考**: デプロイが完了するまで、1〜2分程度かかります。

**GUI**: [Cloud Run](https://console.cloud.google.com/run?project={{project-id}})

### URLを取得して、アプリケーションの動作を確認します

```bash
URL=$(gcloud run services describe --format=json --region=asia-northeast1 --platform=managed web-db | jq .status.url -r)
echo $URL

```

**GUI**: [Cloud Run](https://console.cloud.google.com/run?hl=ja&project={{project-id}})

## Cloud Runのログを確認します

### コンテナのログを確認
**GUI**: [Cloud Run ログ](https://console.cloud.google.com/run/detail/asia-northeast1/web-db/logs?project={{project-id}})

アクセスログを確認します。

## アプリケーションをアップデートします

### [エディタを開く]をクリックしてエディタを開き、左側のディレクトリツリーをクリックし、以下のディレクトリに移動します。
```
gcp-handson
  -> cloud-run-basic
    -> web-db
      -> templates
```

index.html をクリックします。

## アプリケーションの変更
### index.htmlの25行目を変更します

変更前
```
<nav class="red lighten-1">
```
変更後
```
<nav class="blue lighten-1">
```

変更後、[File]メニューから[Save]を選択して、変更を保存します。


### コンテナのイメージ名を設定
```bash
export AR_IMAGE=asia-northeast1-docker.pkg.dev/{{project-id}}/cloud-run-training/web-db:v2
```

### コンテナを再ビルド、登録（プッシュ）します
```bash
cd ~/gcp-handson/cloud-run-basic/web-db/
gcloud builds submit -t $AR_IMAGE
```

## Cloud Runの新しいリビジョンをデプロイします
### 下記コマンドを実行します
```bash
gcloud run deploy --no-traffic --set-cloudsql-instances=$CLOUD_SQL --image=$AR_IMAGE --set-env-vars=DB_USER=$DB_USER,DB_NAME=$DB_NAME,DB_PASS=$DB_PASS,CLOUD_SQL_CONNECTION_NAME=$GOOGLE_CLOUD_PROJECT:asia-northeast1:$CLOUD_SQL --service-account=$SERVICE_ACCOUNT --platform=managed --region=asia-northeast1 --allow-unauthenticated web-db
```
--no-trafficを指定しているため、まだ以前のリビジョンがトラフィックを処理しています。

### 最新のリビジョンを取得します
```bash
LATEST=$(gcloud run revisions list --platform=managed --region=asia-northeast1 --service=web-db --format=json | jq .[].metadata.name -r | sort -rn | head -n 1)
```
確認します
```bash
echo $LATEST
```

**GUI**: [Cloud Run 変更内容（リビジョン）](https://console.cloud.google.com/run/detail/asia-northeast1/web-db/revisions?hl=ja&project={{project-id}})


### トラフィックの50%を新バージョンに振り分けます
```bash
gcloud run services update-traffic --to-revisions=$LATEST=50 --platform=managed --region=asia-northeast1 web-db
```
## アプリケーションにアクセスして、トラフィックの確認をします

### URLに何度かアクセスして、50%ずつ振り分けられていることを確認します

```bash
echo $URL
```




### すべてのトラフィックを新バージョンに振り分けます
```bash
gcloud run services update-traffic --to-latest --platform=managed --region=asia-northeast1 web-db
```

**GUI**: [Cloud Run 変更内容（リビジョン）](https://console.cloud.google.com/run/detail/asia-northeast1/web-db/revisions?hl=ja&project={{project-id}})
## アプリケーションにアクセスして、トラフィックの確認をします

### URLを表示します
```bash
echo $URL
```
何度かアクセスして、完全にリビジョンの切り替えが完了していることを確認します。

## [追加] Cloud Build によるビルド、デプロイの自動化

Cloud Build を利用し今まで手動で行っていたアプリケーションのビルド、コンテナ化、リポジトリへの登録、Cloud Run へのデプロイを自動化します。

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

上で取得したサービスアカウントに Cloud Build から自動デプロイをさせるため Cloud Run 管理者の権限を与えます。

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT  --member serviceAccount:$CB_SA --role roles/run.admin
```

Cloud Runサービスアカウントに、Cloud BuildサービスアカウントをIAMサービスアカウント権限を付与して追加します
```bash
gcloud iam service-accounts add-iam-policy-binding $SERVICE_ACCOUNT --member=serviceAccount:$CB_SA --role=roles/iam.serviceAccountUser
```

**GUI**: [IAM](https://console.cloud.google.com/iam-admin/iam?project={{project-id}})

***@cloudbuild.gserviceaccount.com のアカウントを探し、[Cloud Run管理者]権限がついていることを確認します。


## Cloud Source Repository（CSR）に Git レポジトリを作成

今回利用しているソースコードを配置するためのプライベート Git リポジトリを、Cloud Source Repository（CSR）に作成します。

```bash
gcloud source repos create container-handson
```

**GUI**: [Source Repository](https://source.cloud.google.com/{{project-id}}/container-handson): 作成前にアクセスすると拒否されます。


## Cloud Build トリガーを作成

Cloud Build に前の手順で作成した、プライベート Git リポジトリに push が行われたときに起動されるトリガーを作成します。

```bash
gcloud beta builds triggers create cloud-source-repositories --description="cloud-run" --repo=container-handson --branch-pattern=".*" --build-config="cloud-run-basic/cloudbuild.yaml"
```

**GUI**: [ビルドトリガー](https://console.cloud.google.com/cloud-build/triggers?project={{project-id}})



## Git クライアント設定

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


## Git リポジトリ設定

CSR を Git のリモートレポジトリとして登録します。

```bash
cd ~/gcp-handson
git remote add google https://source.developers.google.com/p/$GOOGLE_CLOUD_PROJECT/r/container-handson
```

以前の手順で作成した CSR のリポジトリと、Cloud Shell 上にある資材を紐付けました。次にその資材をプッシュします。


### [エディタを開く]をクリックしてエディタを開き、左側のディレクトリツリーをクリックし、以下のディレクトリに移動します。
```
gcp-handson
  -> cloud-run-basic
    -> web-db
      -> templates
```
index.html をクリックします。

## アプリケーションの変更
### index.htmlの25行目を変更します

変更前
```
<nav class="blue lighten-1">
```
変更後
```
<nav class="black lighten-1">
```

変更後、[File]メニューから[Save]を選択して、変更を保存します。

### git にコミットします
```bash
git commit -va -m modify
```

## CSR へのコードのプッシュ

以前の手順で作成した CSR は空の状態です。
git push コマンドを使い、CSR に資材をプッシュします。

```bash
git push google master
```
**GUI**: [Source Repository](https://source.cloud.google.com/{{project-id}}/container-handson) から資材がプッシュされたことを確認できます。



## Cloud Build トリガーの動作確認
### Cloud Build の自動実行を確認

[Cloud Build の履歴](https://console.cloud.google.com/cloud-build/builds?project={{project-id}}) にアクセスし、git push コマンドを実行した時間にビルドが実行されていることを確認します。

## アプリケーションにアクセスして、変更の確認をします

### URLを表示します
```bash
echo $URL
```
何度かアクセスして、完全にリビジョンの切り替えが完了していることを確認します。
## Congraturations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>
これにて Cloud Runの入門ハンズオンは全て完了です！！

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