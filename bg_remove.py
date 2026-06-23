from rembg import remove

def remove_bg(input_path, output_path):
    with open(input_path, "rb") as inp:
        result = remove(inp.read())

    with open(output_path, "wb") as out:
        out.write(result)