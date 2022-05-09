# disocrd_bot
discord上で以下3つのBotを提供します．
- Schedule Announcement Bot
    - 授業スケジュールを毎日授業15分前にアナウンス
- Text to Speech Bot
    - 特定のチャンネルに投稿したメッセージをVCに流す
- Pay off Bot
    - 立替の割り勘を算出してメンションを行う
    
※ `TOKEN`や`URL`など別ファイルに分けて呼び出している為，このリポジトリをcloneしても動きません．

## 必要環境
### Python
- Pipenv + Pyenv(Python 3.10.0)
- Google Cloud Platform Text-to-Speech

## 必要ライブラリ
### Python
※ **Pipfile**を参照

## 必要ソフトウェア
- FFmpeg