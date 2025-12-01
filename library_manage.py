from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    copies: int
    available_copies: int


@dataclass
class Member:
    member_id: str
    name: str


@dataclass
class BorrowRecord:
    book_id: str
    member_id: str
    borrow_date: str  # YYYY-MM-DD
    due_date: str     # YYYY-MM-DD
    returned: bool = False


# In-memory storage
books: List[Book] = []
members: List[Member] = []
borrow_records: List[BorrowRecord] = []

# Settings
MAX_LOANS = 5
FINE_PER_DAY = 100
DEFAULT_LOAN_DAYS = 7


def find_book(book_id: str) -> Optional[Book]:
    return next((b for b in books if b.book_id == book_id), None)


def find_member(member_id: str) -> Optional[Member]:
    return next((m for m in members if m.member_id == member_id), None)


def count_active_loans(member_id: str) -> int:
    return sum(1 for r in borrow_records if r.member_id == member_id and not r.returned)


def add_book(book_id: str, title: str, author: str, copies: int) -> bool:
    """Add a book. Returns True on success."""
    if find_book(book_id):
        print(f"図書ID「{book_id}」の本は既に存在します。")
        return False
    if copies <= 0:
        print("冊数は1以上を指定してください。")
        return False
    books.append(Book(book_id=book_id, title=title, author=author, copies=copies, available_copies=copies))
    print(f"図書「{title}」（ID: {book_id}, 著者: {author}, 冊数: {copies}）を追加しました。")
    return True


def list_books() -> None:
    if not books:
        print("現在、登録されている図書はありません。")
        return
    print("--- 図書一覧 ---")
    for b in books:
        print(f"ID: {b.book_id}, タイトル: {b.title}, 著者: {b.author}, 総冊数: {b.copies}, 在庫: {b.available_copies}")


def search_book(book_id: str) -> Optional[Book]:
    return find_book(book_id)


def add_member(member_id: str, name: str) -> bool:
    if find_member(member_id):
        print(f"会員ID「{member_id}」の会員は既に存在します。")
        return False
    members.append(Member(member_id=member_id, name=name))
    print(f"会員「{name}」（ID: {member_id}）を追加しました。")
    return True


def list_members() -> None:
    if not members:
        print("現在、登録されている会員はいません。")
        return
    print("--- 会員一覧 ---")
    for m in members:
        print(f"ID: {m.member_id}, 名前: {m.name}")


def borrow_book(book_id: str, member_id: str) -> bool:
    book = find_book(book_id)
    if not book:
        print(f"図書ID「{book_id}」の本は存在しません。")
        return False
    member = find_member(member_id)
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return False
    if book.available_copies <= 0:
        print(f"図書「{book.title}」は現在貸出可能な冊数がありません。")
        return False
    if count_active_loans(member_id) >= MAX_LOANS:
        print(f"貸出可能数は{MAX_LOANS}冊までです。")
        return False
    today = datetime.today()
    borrow_date = today.strftime("%Y-%m-%d")
    due_date = (today + timedelta(days=DEFAULT_LOAN_DAYS)).strftime("%Y-%m-%d")
    borrow_records.append(BorrowRecord(book_id=book_id, member_id=member_id, borrow_date=borrow_date, due_date=due_date))
    book.available_copies = max(0, book.available_copies - 1)
    print(f"図書「{book.title}」を会員「{member.name}」に貸し出しました。\n返却期限: {due_date}")
    return True


def list_borrowed_books() -> None:
    print("--- 貸出中の図書一覧 ---")
    borrow_count = 0
    for r in borrow_records:
        if r.returned:
            continue
        book = find_book(r.book_id)
        member = find_member(r.member_id)
        title = book.title if book else "(不明)"
        name = member.name if member else "(不明)"
        print(f"図書: {title}（ID: {r.book_id}）, 会員: {name}（ID: {r.member_id}）, 貸出日: {r.borrow_date}, 返却期限: {r.due_date}")
        borrow_count += 1
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")


def return_book(book_id: str, member_id: str) -> bool:
    rec = next((r for r in borrow_records if r.book_id == book_id and r.member_id == member_id and not r.returned), None)
    if not rec:
        print(f"図書ID「{book_id}」本を会員ID「{member_id}」の会員は借りていません。")
        return False
    rec.returned = True
    book = find_book(book_id)
    if book:
        book.available_copies = book.available_copies + 1
        print(f"図書「{book.title}」が返却されました。")
    else:
        print("返却処理は完了しました（図書情報が見つかりません）。")
    return True


def get_overdue_records(today: Optional[str] = None) -> List[Dict]:
    """未返却の延滞記録を構造化して返す。"""
    overdue_list: List[Dict] = []
    if today is None:
        today = datetime.today().strftime("%Y-%m-%d")
    try:
        td = datetime.strptime(today, "%Y-%m-%d")
    except Exception:
        return overdue_list
    for r in borrow_records:
        if r.returned:
            continue
        try:
            due = datetime.strptime(r.due_date, "%Y-%m-%d")
        except Exception:
            continue
        overdue_days = (td - due).days
        if overdue_days > 0:
            book = find_book(r.book_id)
            member = find_member(r.member_id)
            overdue_list.append({
                "book_id": r.book_id,
                "title": book.title if book else None,
                "member_id": r.member_id,
                "name": member.name if member else None,
                "due_date": r.due_date,
                "overdue_days": overdue_days,
                "fine": overdue_days * FINE_PER_DAY,
            })
    return overdue_list

#関数追加#


def calculate_fines() -> None:
    print("--- 延滞料金一覧 ---")
    overdue = get_overdue_records()
    if not overdue:
        print("現在、貸出中の図書はありません。")
        return
    for rec in overdue:
        print(f"図書: {rec['title']}（ID: {rec['book_id']}）, 会員: {rec['name']}（ID: {rec['member_id']}）, 延滞日数: {rec['overdue_days']}, 延滞料金: {rec['fine']}円")


def main() -> None:
    while True:
        print("図書館管理システムメニュー:")
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書を検索")
        print("4: 会員を追加")
        print("5: 会員一覧を表示")
        print("6: 図書を貸し出す")
        print("7: 貸出中の図書一覧を表示")
        print("8: 図書を返却")
        print("9: 延滞料金を計算")
        print("10: 終了")

        try:
            choice = int(input("操作を選択してください（1-10）: "))

            if choice == 1:
                book_id = input("図書IDを入力してください: ")
                title = input("タイトルを入力してください: ")
                author = input("著者名を入力してください: ")
                copies = int(input("冊数を入力してください: "))
                add_book(book_id, title, author, copies)

            elif choice == 2:
                list_books()

            elif choice == 3:
                book_id = input("検索する図書IDを入力してください: ")
                book = search_book(book_id)
                if book:
                    print(f"ID: {book.book_id}, タイトル: {book.title}, 著者: {book.author}, 総冊数: {book.copies}, 在庫: {book.available_copies}")
                else:
                    print(f"図書ID「{book_id}」の本は存在しません。")

            elif choice == 4:
                member_id = input("会員IDを入力してください: ")
                name = input("名前を入力してください: ")
                add_member(member_id, name)

            elif choice == 5:
                list_members()

            elif choice == 6:
                book_id = input("貸し出す図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                borrow_book(book_id, member_id)

            elif choice == 7:
                list_borrowed_books()

            elif choice == 8:
                book_id = input("返却する図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                return_book(book_id, member_id)

            elif choice == 9:
                calculate_fines()

            elif choice == 10:
                print("図書館管理システムを終了します。")
                break

            else:
                print("無効な選択です。1-10の数字を入力してください。")

        except ValueError as e:
            print(f"入力エラー: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    main()

def main():
    while True:
        print("図書館管理システムメニュー:")
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書を検索")
        print("4: 会員を追加")
        print("5: 会員一覧を表示")
        print("6: 図書を貸し出す")
        print("7: 貸出中の図書一覧を表示")
        print("8: 図書を返却")
        print("9: 延滞料金を計算")
        print("10: 終了")

        try:
            choice = int(input("操作を選択してください（1-10）: "))

            if choice == 1:
                book_id = input("図書IDを入力してください: ")
                title = input("タイトルを入力してください: ")
                author = input("著者名を入力してください: ")
                copies = int(input("冊数を入力してください: "))
                add_book(book_id, title, author, copies)

            elif choice == 2:
                list_books()

            elif choice == 3:
                book_id = input("検索する図書IDを入力してください: ")
                book = search_book(book_id)
                if book:
                    print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")
                else:
                    print(f"図書ID「{book_id}」の本は存在しません。")

            elif choice == 4:
                member_id = input("会員IDを入力してください: ")
                name = input("名前を入力してください: ")
                add_member(member_id, name)

            elif choice == 5:
                list_members()

            elif choice == 6:
                book_id = input("貸し出す図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                borrow_book(book_id, member_id)

            elif choice == 7:
                list_borrowed_books()

            elif choice == 8:
                book_id = input("返却する図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                return_book(book_id, member_id)

            elif choice == 9:
                calculate_fines()

            elif choice == 10:
                print("図書館管理システムを終了します。")
                break

            else:
                print("無効な選択です。1-10の数字を入力してください。")

        except ValueError as e:
            print(f"入力エラー: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main()