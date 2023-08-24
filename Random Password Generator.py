import random, string

password_length = int(input("Password Length (type number): "))
                      
password_characters = string.ascii_letters + string.digits + string.punctuation

password = []

for x in range (password_length):
    password.append(random.choice(password_characters))
    
print(''.join(password))
