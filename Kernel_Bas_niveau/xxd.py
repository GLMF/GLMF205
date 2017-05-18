import sys
import binascii


def dump(filename):
    try:
        with open(filename, 'rb') as fic:
            line = 0
            newline = True
            block = ''
            nb_block = 0
            strline = ''
            while True:
                if newline:
                    print(str(line).zfill(7) + ': ', end='')
                    newline = False
                    line += 10
                car = fic.read(1)
                if car == b'':
                    break
                if len(block) == 4:
                    print(block, end=' ')
                    block = ''
                    nb_block += 1
                if nb_block == 8:
                    nb_block = 0
                    newline = True
                    print('  ' + strline)
                    strline = ''
                hexa = binascii.hexlify(car).decode('utf-8')
                block += hexa
                int_val = int(hexa, 16)
                if int_val < 32 or int_val > 127:
                    int_val = 46 # correspond à 0x2e, le code ASCII du point
                strline += chr(int_val)
            if block != '':
                print(block, end=' ')
                if len(block) == 2:
                    print('  ', end='')
                add_block = 0
                for i in range(9 - nb_block):
                    print('  ', end='')
                    add_block += 1
                    if add_block % 2 == 0:
                        print('  ', end='')
                print(strline)
    except Exception as e:
        print('Erreur lors de l\'ouverture/lecture du fichier {}'.format(filename))
        print(e)
        exit(1)

def reverse_dump(filename):
    try:
        with open(filename, 'r') as fic:
            newline = ''
            for line in fic:
                newline += line[9:][:-19].replace(' ', '')
            print(binascii.unhexlify(newline).decode('utf-8'), end='')
    except Exception as e:
        print('Erreur lors de l\'ouverture/lecture du fichier {}'.format(filename))
        print(e)
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Syntax: xxd.py [dump|reverse_dump] <filename>')
        exit(2)
    if sys.argv[1] == 'dump':
        dump(sys.argv[2])
    elif sys.argv[1] == 'reverse_dump':
        reverse_dump(sys.argv[2])
