from sql import query, prepare_statement, generate_types


prepare_statement("SELECT * FROM users WHERE id = ?")
prepare_statement("INSERT INTO users (id, name) VALUES(?, ?)")
query("SELECT * FROM users WHERE id = ?", ())

if __name__ == "__main__":
    generate_types()
