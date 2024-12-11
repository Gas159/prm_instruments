# А роза упала на лапу Азора
#
#
letters = " А роза  Азора"


def polindrom(letter: str) -> bool:
    crn_string = letter.strip().replace(" ", "").lower()
    print(crn_string)
    for i in range(len(crn_string)):
        print(i, -i - 1)
        print(crn_string[i], crn_string[-i - 1])
        print()
        if crn_string[i] != crn_string[-i - 1]:
            print("not polindrom")
            # return False
        # print(i, i - 1)
    print(crn_string)
    print("polindrom")
    return True


print(polindrom(letters))
