# MachineInfomationBoard

專案構想

  原先必須要進入無塵室，觀看機台電腦才有辦法得知機台的狀態，導致機台產生錯誤導致停止做動時，無法即時得知訊息並進行應對處理，導致產生多餘的機台閒置時間產生，故開始規劃此專案生成。

目的

   1. 一目了然的機台資訊
   2. 機台異常時即時通知(信件發送)
   3. 減少機台多餘的閒置時間(效益最大化)

使用程式

  Pythone : 自動化定時撈取機台log,分析log存入資料庫,機台錯誤時信件發送
  Html,Css,Javascripes : 網頁呈現及頁面訊息更改
  Php : 後端資料處理
  使用資料庫 : Mssql
