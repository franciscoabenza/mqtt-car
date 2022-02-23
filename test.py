
import getch

def Read_Key():
    count=0
    limit=1000
    while  count < limit:
        count = count + 1
        print(count)

    key = getch.getch()

    if key == 'q':
        return 'q'
    elif key == 'w':
        return 'Arrow_Up'
    elif key == 's':
        return 'Arrow_Down'
    elif key == 'd':
        return 'Arrow_Right'
    elif key == 'a':
        return 'Arrow_Left'
    else:
        print("YOU GOT A REALEASE 🎉")
        return 'p'

print(Read_Key())