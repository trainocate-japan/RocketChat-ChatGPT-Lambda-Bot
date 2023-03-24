# RocketChat-ChatGPT-Lambda-Bot
RocketChatのBotでChatGPTを使用するためのAWS Lambda関数のコードです。AWS Lambda関数をデプロイして、RocketChatのBotとしてChatGPTを使用できます。  

## 依存関係
会社内のLambdaレイヤーで共有しているものを使っています。
Utilは[https://github.com/trainocate-japan/Common-Utility-Module](https://github.com/trainocate-japan/Common-Utility-Module)です。  
X-Ray SDKはオフィシャルのPython用です。  

## OpenAI APIキー

Systems Manager パラメータストアで管理しています。


