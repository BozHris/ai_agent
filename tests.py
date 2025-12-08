from functions.get_files_info import get_files_info




if __name__ == "__main__":
    test_one=get_files_info("calculator", ".")

    test_two=get_files_info("calculator", "pkg")

    test_three=get_files_info("calculator", "/bin")

    test_four=get_files_info("calculator", "../")

    print("Test One")
    print(test_one)
    print("Test Two")
    print(test_two)
    print("Test Three")
    print(test_three)
    print("Test Four")
    print(test_four)