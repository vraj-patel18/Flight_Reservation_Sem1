import csv
import os

SEAT_FOLDER = "seat_matrices"

def create_seat_file(flight_no, rows, columns):
    if not os.path.exists(SEAT_FOLDER):
        os.mkdir(SEAT_FOLDER)
    filename = flight_no + ".csv"
    path = os.path.join(SEAT_FOLDER, filename)
    letters = "ABCDEF"[:columns]
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Row"] + list(letters))
        for row in range(1, rows + 1):
            writer.writerow([row] + ["Available"] * columns)
    return filename

def read_seats(filename):
    path = os.path.join(SEAT_FOLDER, filename)
    with open(path, "r", newline="") as file:
        return list(csv.reader(file))

def show_seats(filename):
    for row in read_seats(filename):
        print(row)

def update_seat(filename, seat_no, status):
    seats = read_seats(filename)
    row_number = int(seat_no[:-1])
    letter = seat_no[-1].upper()
    letters = seats[0][1:]
    if row_number < 1 or row_number >= len(seats) or letter not in letters:
        return False
    column = letters.index(letter) + 1
    seats[row_number][column] = status
    path = os.path.join(SEAT_FOLDER, filename)
    with open(path, "w", newline="") as file:
        csv.writer(file).writerows(seats)
    return True
