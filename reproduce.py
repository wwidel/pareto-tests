import sys
import tests


def get_i():
    try:
        i = int(sys.argv[1])
    except IndexError:
        print('No argument provided. Try\n\n\t python reproduce.py i\n\nwith "i" being an integer satisfying 0 < i < 33.')
        return
    except ValueError:
        print('The argument provided should be an integer. Try\n\n\t python reproduce.py i\n\nwith "i" being an integer satisfying 0 < i < 33.')
        return

    if i not in range(1, 33):
        print(
            'The argument provided should be an integer from the set {1, 2, ..., 32}. Try\n\n\t python reproduce.py i\n\nwith "i" being an integer satisfying 0 < i < 33.')
        return

    return i


def main():
    i = get_i()
    if i == None:
        return
    #
    tests.main([i], 1)
    return

if __name__ == '__main__':
    main()
