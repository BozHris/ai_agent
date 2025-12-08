from functions.write_file import write_file

if __name__ == "__main__":
    test_one=write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    test_two=write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    test_three=write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Test One")
    print(test_one)         
    print("Test Two")
    print(test_two) 
    print("Test Three")
    print(test_three)   