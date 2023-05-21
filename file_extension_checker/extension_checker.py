import magic

print(magic.from_file("Test.jpg", mime=True))
print(magic.from_file("Test.png", mime=True))
