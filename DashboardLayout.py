# This file contains the layout of the dashboard for the game BaghChal
# The dashboard is displayed in the console
def print_board_with_layout(board):
    print("\n")
    for i, row in enumerate(board):
        row_display = "  |  ".join(f"{cell:^3}" for cell in row)

        print(f"   {row_display}  ")
        if i < len(board) - 1:
            print("  " + "-" * (len(row_display) + 4))
    print("\n")