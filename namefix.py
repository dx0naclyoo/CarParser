import io
import os
from PIL import Image

file_path = "images/vw-make/"
file_name = os.listdir(file_path)


def get_correct_modify(model: list) -> str:

    new_model = []
    if len(model) == 1:
        return "".join(model)

    if len(model) > 1:
        for x in model:
            if int(len(x)) < 4:
                new_model.append(x)
        return "-".join(new_model)

    else:
        return "-".join(model)

    return "-".join(model)



for name in file_name:

    list_name = name.split("_")
    if len(list_name) < 3:
        print(list_name)
    else:
        marka, *model, body, year = name.split("_")

        if "hatchback-car" in body:
            body = "hatchback"


        model = model[0].split("-")


        new_model = model.pop(0)
        modify = get_correct_modify(model)
        if not modify:
            new_name = f"{marka}_{new_model}_{body}_{year}".lower()
        else:
            new_name = f"{marka}_{new_model}_{modify}_{body}_{year}".lower()

        print(new_name)

        byteImgIO = io.BytesIO()
        with Image.open(f"{file_path}{name}") as file:
            file.save(byteImgIO, "PNG")

            # указатель файла в начало
            byteImgIO.seek(0)

            # читаем байты в переменную
            # (это изображение, представленное как строка байтов)
            byteImg = byteImgIO.read()

            with open(f"{file_path}new_img/{new_name}", "wb") as new_file:
                new_file.write(byteImg)



