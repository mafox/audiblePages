fruits = ["Apple", "Mango", "Banana", "Peach"]
[print(fruit + " juice") for fruit in fruits]

fruits = ["  Apple   ", "   Mango  ", "      Banana  ", " Peach  "]
[print(fruit.strip()) for fruit in fruits]
fruits = [fruit.strip() for fruit in fruits]

print(fruits)

fruits_stripped = (fruit.strip() for fruit in fruits)
print(f'fruits_stripped: {fruits_stripped}')
fruits_list = [fruit for fruit in fruits_stripped if fruit]
print(f'fruits_list: {fruits_list}')

fruits = [ fruit for fruit in [ fruit.strip() for fruit in fruits ] if fruit ]
print(f'fruits: {fruits}')

authors = ['Neil Gaiman', 'Terry Pratchett']
authors = [ author for author in [ author.strip() for author in authors ] if author ]
narrators= ['Rebecca Front', 'Michael Sheen', 'David Tennant']
narrators = [ narrator for narrator in [ narrator.strip() for narrator in narrators ] if narrator ]

book_title ="    the book    "
book_title = book_title.strip()
print(f'*{book_title}*')

print(f'fruits: {fruits}')
