### Freely のバックエンド

>**Warning** <br />
>Heroku有料化のため、Firebaseへ移行しました。(2022/11/28~) <br />
>[現在のアプリはこちらを参照ください](https://github.com/Masaya-Matsushita/freely-frontend)


### 🏗 アプリ構成(~2022/11/28)
<img src="https://user-images.githubusercontent.com/97160510/197398576-e0150a21-61ca-4b86-a705-9d64e55d375c.png" width="600px" />

|領域|用途|使用技術|
|:---:|:---:|:---:|
|フロントエンド|言語・FW <br /> UI <br /> Deploy|TypeScript, React, Next.js <br /> TailwindCSS, Mantine <br /> Vercel|
|バックエンド|言語・FW <br /> ORM <br /> Deploy <br /> 環境構築|Python, FastAPI <br /> SQLAlchemy <br /> Heroku(PostgreSQL) <br /> Docker(FastAPI公式Image)|
|周辺技術|デザイン <br /> BFF・プロキシサーバ <br /> フェッチ・ポーリング <br /> 状態管理 <br />　エラーUI <br /> 画像トリミング <br />　グラフ描画 <br />　QRコード <br />　アイコン <br />　リンター / フォーマッター |Figma <br /> Node.js (Next.js API Route) <br /> SWR <br /> Recoil <br /> react-error-boundary <br /> react-easy-crop <br /> react-chartjs-2 <br /> next-qrcode <br /> tabler-icons, react-icons <br /> ESLint / Prettier |
<br />
