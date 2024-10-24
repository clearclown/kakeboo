# kakeboo

## データベース設計

### 1. データベースの内容を表形式で表示

#### Receipt テーブル

| **フィールド名**     | **データ型** | **デフォルト値** | **制約**                         | **説明**                                                                                    |
| -------------------- | ------------ | ---------------- | -------------------------------- | ------------------------------------------------------------------------------------------- |
| `id`                 | SERIAL       | 自動生成         | 主キー                           | 自動で生成される内部管理用のID                                                              |
| `reciept_id`         | VARCHAR(255) | 自動生成         | 一意キー（外部キーとして使用可） | レシート固有のID                                                                            |
| `time`               | TIMESTAMP    | レシート作成時刻 | なし                             | レシートの作成日時                                                                          |
| `created_at`         | TIMESTAMP    | 現在時刻         | 自動生成                         | レシートを処理した時刻                                                                      |
| `currency_type`      | VARCHAR(3)   | "JPY"            | ISO 4217準拠                     | 通貨の種類（例: JPY, USD）                                                                  |
| `total_amount`       | Float        | 0.0              | なし                             | 合計金額                                                                                    |
| `payment_method`     | VARCHAR(255) | "-"              | なし                             | 支払い方法（例: 現金、クレジットカード、wechatpay、alipay、paypay等）                       |
| `payment_details`    | VARCHAR(255) | "-"              | なし                             | 支払い方法の詳細(例 : クレジットカードの場合は、クレジットカードの種類、カード番号の一部等) |
| `store_name`         | VARCHAR(255) | "-"              | なし                             | 店名(フルで)                                                                                |
| `store_type`         | VARCHAR(255) | "-"              | なし                             | 店の種類（例: スーパー、レストラン）                                                        |
| `store_other_info`   | JSON         | null             | なし                             | 店のその他の情報（例: 電話番号、住所、その他すべて）                                        |
| `location`           | VARCHAR(255) | "-"              | なし                             | 店の場所（国、都市などの住所）                                                              |
| `number_of_people`   | Integer      | 0                | なし                             | レシートの人数                                                                              |
| `notes`              | TEXT         | "-"              | なし                             | 備考欄                                                                                      |
| `receipt_status`     | VARCHAR(255) | "-"              | なし                             | レシートの状態                                                                              |
| `receipt_image_path` | VARCHAR(255) | "-"              | なし                             | レシート画像の保存先のパス                                                                  |

#### Item テーブル

| **フィールド名** | **データ型** | **デフォルト値** | **制約**                | **説明**                       |
| ---------------- | ------------ | ---------------- | ----------------------- | ------------------------------ |
| `id`             | SERIAL       | 自動生成         | 主キー                  | 商品の一意なID                 |
| `receipt_id`     | INTEGER      | なし             | 外部キー (`Receipt.id`) | 紐付けられたレシートのID       |
| `product_name`   | VARCHAR(255) | "-"              | なし                    | 商品名                         |
| `price`          | Float        | 0.0              | なし                    | 商品の単価                     |
| `quantity`       | Integer      | 0                | なし                    | 購入した商品の個数             |
| `discount`       | VARCHAR(255) | 0.0              | なし                    | 値引き情報                     |
| `notes`          | TEXT         | "-"              | なし                    | 備考欄（商品に関する追加情報） |

### 2. カテゴリ
#### 店の種類(タグのように複数選択)
飲食店
テイクアウト
スーパーマーケット
コンビニエスストア
オンラインサブスクリプション
ドラッグストア
病院
博物館
アミューズメント施設
娯楽施設
旅行
美容室
リラクゼーション
交通
その他

#### 商品のカテゴリ(タグのように複数選択)
住居費	家賃、住宅ローン、駐車場代などの支出項目
水道光熱費	水道代、電気代、ガス代などの支出項目
通信費	スマホ料金、インターネット料金、宅配便料金などの支出項目
保険料	生命保険や医療保険、介護保険などの支出項目
食費	外食費や食材購入費、酒代など飲食に関わる支出項目」
外食費
酒類
日用品費	掃除道具やシャンプー、ティッシュペーパーなど日用品の支出項目
被服費	洋服や靴、アクセサリーなどの支出項目
美容費	化粧品やエステなどの支出項目
交際費	デートや飲み会、友人・知人へのプレゼントなどの支出項目
趣味費	書籍代や映画チケット代など趣味に関する支出項目
交通費	電車やバスの運賃、ガソリン代などの支出項目
教育費	子どもの学費や教材の購入費などの支出項目
医療費	通院費や入院費、医薬品の購入費などの支出項目
特別費	イベントなど、毎月発生しない支出の項目
雑費	上記以外、用途不明の支出項目


```json
{
  "receipts": [
    {
      "id": 1,
      "reciept_id": "",
      "time": "",
      "created_at": "",
      "currency_type": "JPY",
      "total_amount": 2500.5,
      "payment_method": "credit_card",
      "payment_details": "VISA ****1234",
      "store_name": "Supermarket A",
      "store_type": "supermarket",
      "store_other_info": {
        "phone": "03-1234-5678",
        "address": "Tokyo, Shibuya, 123-456"
      },
      "location": "Tokyo",
      "number_of_people": 1,
      "notes": "Thanks for shopping with us!",
      "receipt_status": "completed",
      "receipt_image_path": "/receipts/2024/10/15/R123456789.jpg"
    }
  ],
  "items": [
    {
      "id": 1,
      "receipt_id": 1,
      "product_name": "Apple",
      "price": 150.0,
      "quantity": 5,
      "discount": "10% off",
      "notes": "Organic"
    }
  ]
}
```

## フォルダ構成 :
### 00notYet_backup : バックアップ
### 01notYet : 未処理ファイル
### 02current : 現在ファイル
### 03txt : 文字起こし後のフォルダ
### 04md : markdownフォルダ
### 05done : 処理完了
### 99error : エラー

### ./../log
