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
class Mail(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.mail = None  # initialize mail to None
    
    def add_phone(self, phone):
        self.phones.append(phone)
    
    def edit_phone(self, index, phone):
        self.phones[index] = phone
    
    def delete_phone(self, index):
        del self.phones[index]
    
    def set_mail(self, mail):
        self.mail = mail
    
    def get_mail(self):
        return self.mail.value if self.mail else None
    
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

address_book = AddressBook()# create global variable

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
def add_contact(name, phone, mail=None):
    name_field = Name(name)
    mail_field = Mail(mail)
    if name_field.value in address_book:
        record = address_book[name_field.value]
        record = address_book[mail_field.value]
        #record.add_phone(phone)
        if mail:
            record.set_mail(mail)
            print(f"Contact {name} with phone number {phone} was added earlier")
        else:
            record.add_phone(phone)
            print(f"Contact {name} with phone number {phone} was added earlier")
    else:
        record = Record(name_field)
        if mail:
            record.set_mail(mail)
        record.add_phone(phone)
        address_book.add_record(record)
        print(f"Contact {name} with phone number {phone} added successfully")
    return address_book
    
@input_error
def find_contact(name):
    #global address_book
    name_field = Name(name)
    found_records = address_book.find_records(name_field.value)
    if found_records:
        for record in found_records:
            print(f"{record.name.value}: {', '.join(str(phone) for phone in record.phones)}")
    else:
        print(f"No records found for {name}")

@input_error
def update_contact(name, phone):
    name_field = Name(name)
    if name_field.value in address_book:
        record = address_book[name_field.value]
        record.edit_phone(0, phone)
        print(f"Updated phone number for {name} to {phone}")
    else:
        record = Record(name_field)
        record.add_phone(phone)
        address_book.add_record(record)
        print(f"Added {name} with phone number {phone}")
    return address_book

@input_error
def show_all_contacts():
    if len(address_book.data) == 0:
        print("No contacts found")
    else:
        print("All contacts:")
        for name in address_book.data:
            record = address_book.data[name]
            email = record.get_mail()
            if email != None:
                email_str = f", {email}"
            else:
                email_str = " *******"
            print (email)
            print(f"{record.name.value}: {', '.join(str(phone) for phone in record.phones)}{email_str}")

def parse_command(command):
    parts = command.split()
    if parts[0] == "hello":
        hello()
    elif parts[0] == "add":
        if len(parts) < 3:
            try:
                raise IndexError
            except IndexError:
                print ("Command to add contact is empty, please repeat with name and number")
        else:
            add_contact(parts[1], parts[2])
    elif parts[0] == "find":
        if len(parts) < 2:
            raise IndexError
        
        find_contact(parts[1])
    elif parts[0] == "update":
        if len(parts) < 3:
            raise IndexError
        update_contact(parts[1], parts[2])
    
    elif parts[0] == "show":
        show_all_contacts()
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