

func = lambda v: all(ch.isalnum() or ch.isspace() for ch in v)

print(func("Hello World"))  # True
print(func("Hello-World"))  # True
print(func("!!!"))          # False
print(func("!fdsf   "))         # False