import sys
import os
import csv
import re
import pickle

class Person:

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee id:", self.id)
        print(self.first, self.mi, self.last)
        print(self.phone, "\n")

def method1(filepath):
    employee_list = {}

    with open(os.path.join(os.getcwd(), filepath), 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)

        for lines in csv_reader:

            # Last: 0, First: 1, Middle Initial: 2, ID: 3, Office phone: 4
            lines[0] = lines[0].capitalize()
            lines[1] = lines[1].capitalize()

            # Replace middle initial if neccessary
            if lines[2]:
                lines[2] = lines[2].capitalize()
            else:
                lines[2] = 'X'
            

            # Check id and phone numbers
            regex_id = re.search("[a-zA-Z]{2}\d{4}", lines[3])
            regex_phone = re.search("\d{3}[-.\\s]?\d{3}[-.\\s]?\d{4}", lines[4])

            while regex_id is None:
                print("ID invalid:", lines[3])
                print("ID is two letters followed by 4 digits")
                txt = input("Please enter a valid id: ")

                regex_id = re.search("[a-zA-Z]{2}\d{4}", txt)
                lines[3] = txt

            while regex_phone is None:
                print("Phone", lines[4], "is invalid")
                print("Enter phone number in form 123-456-7890")
                txt = input("Enter phone number: ")

                regex_phone = re.search("\d{3}[-.\\s]?\d{3}[-.\\s]?\d{4}", lines[4])
                lines[4] = txt

            # Reformat Phone Numbers
            lines[4] = re.sub(r'(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})', r'\1-\2-\3',lines[4])


            if lines[3] not in employee_list.keys():
                employee_list[lines[3]] = Person(lines[0], lines[1], lines[2], lines[3], lines[4])
            else:
                print("Error: id", lines[3], "already exists. Not being added to dict")

    return employee_list
            


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        employee_list = method1(fp)

        # save the pickle file
        pickle.dump(employee_list, open('dict.p', 'wb'))  # write binary

        # read the pickle file
        dict_in = pickle.load(open('dict.p', 'rb'))  # read binary

        print("\n\nEmployee List:\n")

        for p in dict_in.values():
            p.display()