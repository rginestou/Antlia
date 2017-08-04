def outer():
    L = []
    def inner():
        nonlocal L
        L.append("yolo")
    inner()
    return L

print(outer())
