from assets import open_asset, generate_types


with open_asset("a.txt") as f:
    print(f.read())

if __name__ == "__main__":
    generate_types()
