import random
class_names = ["Maahir AHMED",
               "Malcolm Chi",
               "Raehaan Goswami",
               "Akshat Joshi",
               "Arjun Kaul",
               "Jordan Liew",
               "Dylan Lu",
               "Aaron Macadangdang",
               "Hari Modha",
               "Viet Truong Nguyen",
               "Kabir Parmar",
               "Gokul Koushik Ramu",
               "Gurtej Sambhy",
               "Aditya Singh",
               "Monark Soni",
               "Raghav Tiwari"
]
# class_names = ["aa", "ab", "ba", "bb"]
random.shuffle(class_names)

def convert_ASCII(arr):
    output = []
    for i in range(len(arr)):
        output.append([ord(c) for c in arr[i]])
    return output

def convert_Str(arr):
    output = []
    for i in arr:
        string = ""
        for j in i:
            string += chr(j)
        output.append(string)
    return output
    
def method_error():
    print("The method you entered is invalid, please select a number from 1 to 3.")

def insertion_sort(arr):
    for i in range(1, len(arr)):
        j = i
        n = 0
        while arr[j - 1][n] >= arr[j][n] and j > 0:
            if arr[j - 1][n] > arr[j][n]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                j -= 1
                n = 0
            if arr[j - 1][n] == arr[j][n]:
                n += 1

def selection_sort(arr):
    for i in range(0, len(arr) - 1):
        cur_min = i
        for j in range(i+1, len(arr)):
            n = 0
            while True:
                if arr[j][n] < arr[cur_min][n]:
                    cur_min = j
                    break
                elif arr[j][n] == arr[cur_min][n]:
                    n += 1
                elif arr[j][n] > arr[cur_min][n]:
                    break
        arr[i], arr[cur_min] = arr[cur_min], arr[i]

def bubble_sort(arr):
    for i in range(0, len(arr) - 1):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

print(f"Unordered List: {class_names}")
method = input("Which sorting method to use?\n(1)Insertion\n(2)Selection\n(3)Bubble\n")
print("\n")

converted_names = convert_ASCII(class_names)
print(converted_names)
if method == "1":
    insertion_sort(converted_names)
    class_names = convert_Str(converted_names)
    print(f"Ordered List: {class_names}")
elif method == "2":
    selection_sort(converted_names)
    class_names = convert_Str(converted_names)
    print(f"Ordered List: {class_names}")
elif method == "3":
    bubble_sort(converted_names)
    class_names = convert_Str(converted_names)
    print(f"Ordered List: {class_names}")
else:
    method_error()