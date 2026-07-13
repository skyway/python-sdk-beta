# SkyWay Python SDK

SkyWay Python SDK は、Python で作成されたアプリケーションから SkyWay を利用するための SDK です。本 SDK を利用することで、Python のアプリケーションでリアルタイムに映像・音声データを受信し、任意のデータ送信を行うことができます。

> 💡 **NOTE**
>
> **提供状況**
>
> Python SDKは現在、β版として機能を限定して提供しています。そのため、他のSDKで利用できる機能の一部が含まれていない場合があります。また、 **API仕様が予告なく変更される可能性があります。** あらかじめご了承ください。
>
> β版の提供期間中は、SDKの品質改善および機能追加に継続して取り組んでまいります。
>
> ご利用後に気になる点がございましたら、お気軽に[お問合せフォーム](https://support.skyway.ntt.com/hc/ja/requests/new?ticket_form_id=14615614124185)よりご連絡ください。

## 利用シーンの例

本SDKを組み込むことで実現可能なサービスの一例です。

**AIと連携したリアルタイム接客システム**

本SDKを用いてエンドユーザーの映像・音声をリアルタイムに受信し、マルチモーダルAIと連携させることで、低遅延な対話型接客を実現できます。

**LLMを活用したリアルタイム議事録**

本SDKを用いて会議の音声や画面共有映像などをリアルタイムに受信し、外部AIサービスで分析することで、会議内容を即時に記録・整理するエージェントを開発できます。

## インストール方法

pip コマンドを用いて、PyPI からインストールできます。

```bash
pip install skyway-room
```

## ドキュメント

- [Python SDK β版 APIリファレンス](https://python-sdk.api-reference.skyway.ntt.com/room/)
- [ユーザーガイド](https://skyway.ntt.com/ja/docs/user-guide/python-sdk/)

## サンプルコード

- [P2PRoomでの映像と音声の受信、データの送信を行うサンプルコード](https://github.com/skyway/python-sdk/tree/main/examples/quickstart)

## ライセンス

- [MIT License](https://github.com/skyway/python-sdk/tree/main/LICENSE)
