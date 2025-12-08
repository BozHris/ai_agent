from functions.get_file_content import get_file_content




if __name__ == "__main__":
    test_one=get_file_content("calculator", "lorem.txt")

    test_two=get_file_content("calculator", "main.py")
    test_three=get_file_content("calculator", "pkg/calculator.py")
    test_four=get_file_content("calculator", "/bin/cat") 
    test_five= get_file_content("calculator", "pkg/does_not_exist.py")
    print("Test One")
    print(test_one)
    print("Test Two")
    print(test_two)
    print("Test Three")
    print(test_three)
    print("Test Four")
    print(test_four)
    print("Test Five")
    print(test_five)        