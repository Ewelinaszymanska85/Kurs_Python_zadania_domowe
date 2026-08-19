# Diagram mermaid:
# graph TD
#     A --> B
#     A --> C
#     B --> D
#     C --> E
#     D --> F
#     E --> F

class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B):
    pass

class E(C):
    pass

class F(D, E):
    pass

# Moje przewidywanie MRO dla klasy F (przed sprawdzeniem):
# F -> D -> B -> E -> C -> A -> object

# Sprawdzenie:
print(F.mro()) 