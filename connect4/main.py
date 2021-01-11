from connect4.board import Board


def main():
    b = Board()
    print(b)
    b.play(player=2, column=3)
    print(b)

    for _ in range(3):
        b.play(player=1, column=3)
        print(b)

    b.play(player=2, column=3)
    print(b)

    print(f"Winner = {b.check_win()}")

    for i in range(4):
        b.play(player=2, column=i + 1)
        print(b)
        print(f"Winner = {b.check_win()}")


if __name__ == "__main__":
    main()
