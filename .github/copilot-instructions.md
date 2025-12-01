**Repository Purpose**

- **概要:** シンプルな図書館管理のスクリプト集。CLI操作で図書・会員を管理し、貸出・返却・延滞料金計算を行う（`main.py`, `library_manage.py`）。

**Big Picture / アーキテクチャ**

- **単一プロセスのスクリプト:** このリポジトリはモノリシックなスクリプト群で、外部サービスは使わず標準入出力（`input()` / `print()`）で操作します。
- **主要ファイル:** `main.py` がエントリポイントで `library_manage.py` にある関数（`add_book`, `borrow_book`, `return_book`, `calculate_fines` 等）を呼び出す構成。
- **データモデル:** 永続化は無く全てメモリ内のリスト（`books`, `members`, `borrow_records`）。IDや日付は文字列で扱われます。

**Developer Workflows / 実行方法**

- **仮想環境での実行（推奨）:** `env` がワークスペースにあります。実行例:

```bash
env/bin/python main.py
```

- **注意点（macOS）:** `main.py` の先頭に `from ossaudiodev import openmixer` があり、これはプラットフォーム依存（Linux向け）で import エラーを起こす可能性があります。不要であれば削除して下さい。

**Project-specific Conventions / 観察されたパターン**

- **日本語メッセージ:** CLI の出力とプロンプトは日本語で書かれているため、追加のメッセージやテキストは同言語で統一するのが良いです。
- **操作は同期的・対話的:** `input()` ベースの対話型フローを前提としているコードが多い（`main()` がループして選択肢を受け付ける）。非対話テストや自動化を行う場合は関数単位でラップして入力を注入してください。
- **日付の扱い:** 日付は文字列リテラル（例: `"2024-12-01"`）でハードコーディングされています。日付演算は単純な文字列切り出しで行われているため、正確な日付計算が必要なら `datetime` を導入してください。
- **ID と型:** `book_id`, `member_id` は文字列として扱われます。関数は現状例外を投げず `print()` でエラー報告する設計です。

**Integration Points & Dependencies**

- **依存:** 実行に必須の外部ライブラリは見当たりませんが、`main.py` に未使用かつプラットフォーム依存の `ossaudiodev` と `pip` の import があるため注意してください。
- **外部連携は無し:** 永続化や外部 API との連携コードは存在しません。拡張時はデータ永続化（SQLite/ファイル/ORM）やHTTP層を追加することになります。

**Examples & Patterns to Reference**

- 図書追加: `library_manage.add_book(book_id, title, author, copies)` — 既存IDチェック後に `books.append(...)`。
- 貸出処理: `borrow_book(book_id, member_id)` — 在庫チェック、会員存在チェック、会員の貸出冊数上限チェック（5冊）がある。
- 延滞料金: `calculate_fines()` — ハードコード日付から延滞日数を算出し、1日100円の料金を表示する短いロジック。

**What an AI agent should do first**

- 開発目的を確認（CLI改善・自動テスト追加・永続化導入など）。
- ローカルで `env/bin/python main.py` を実行して現在の動作と例外を確認する（`ossaudiodev` が原因で失敗することが多い）。
- 小さな変更は関数単位で行い、対話 I/O はモック可能にしてからリファクタを進める。

**When merging existing instructions**

- このファイルは既存の `.github/copilot-instructions.md` が無い場合の新規作成です。もし既存ファイルがあれば、上の「実行方法」「依存」「例」を優先して残してください。

---

フィードバックください: 足りない情報（テストコマンド、想定の開発ゴール、将来追加したい永続化方法など）があれば追記します。
