from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def edit_phone(self, index, phone):
        self.phones[index] = phone

    def delete_phone(self, index):
        del self.phones[index]

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def edit_record(self, name, record):
        self.data[name.value] = record

    def delete_record(self, name):
        del self.data[name.value]

    def find_records(self, name):
        found_records = []
        for key in self.data:
            if name.lower() in key.lower():
                found_records.append(self.data[key])
        return found_records

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print("Name not found in contacts")
    
    return inner

def hello():
    print("""Hello, I'm a bot. I will help you use the program.
        - For add contact to directory input <<< add 'name' 'number'>>> use a space without a comma
        - For find contact in directory input <<< find 'name'  >>> use a space without a comma
        - For show all contacts in directory input <<< show >>> 
        - For update contact in directory input <<< update 'name' 'new number'  >>> use a space without a comma
        - To exit the program input <<<exit>>> or <<<bye>>>""")

@input_error
def add_contact(address_book, name, phone):
    name_field = Name(name)
    if name_field.value in address_book:
        record = address_book[name_field.__value]
        record.add_phone(phone)
        print(f"Added phone number {phone} to {name}")
    else:
        record = Record(name_field)
        record.add_phone(phone)
        address_book.add_record(record)
        print(f"Added {name} with phone number {phone}")

@input_error
def find_contact(address_book, name):
    name_field = Name(name)
    found_records = address_book.find_records(name_field.value)
    if found_records:
        for record in found_records:
            print(f"{record.name.value}: {', '.join(str(phone) for phone in record.phones)}")
    else:
        print(f"No records found for {name}")


@input_error

def update_contact(address_book, name, phone):
    name_field = Name(name)
    if name_field.__value in address_book:
        record = address_book[name_field.__value]
        record.edit_phone(0, phone)
        print(f"Updated phone number for {name} to {phone}")
    else:
        record = Record(name_field)
        record.add_phone(phone)
        address_book.add_record(record)
        print(f"Added {name} with phone number {phone}")

@input_error
def show_all_contacts(address_book):
    if len(address_book.data) == 0:  
        print("No contacts found")
    else:
        print("All contacts:")
        for name in address_book.data:  
            record = address_book.data[name]  
            print(f"{record.name.__value}: {', '.join(str(phone) for phone in record.phones)}")

def parse_command(command):
    address_book = AddressBook()
    parts = command.split()
    if parts[0] == "hello":
        hello()
    elif parts[0] == "add":
        if len(parts) < 3:
            raise IndexError
        add_contact(address_book, parts[1], parts[2])
    elif parts[0] == "find":
        if len(parts) < 2:
            raise IndexError
        find_contact(address_book, parts[1])
    elif parts[0] == "update":
        if len(parts) < 3:
            raise IndexError
        update_contact(address_book, parts[1], parts[2])
    elif parts[0] == "show":
        show_all_contacts(address_book)
    else:
        print("Invalid command")
        
        
def main():
    while True:
        command = input("Enter command: ")
        if command == "exit" or command == "bye":
            print("The program is finished")
            break
        else:
            parse_command(command)
            
if __name__ == '__main__':
    main()
