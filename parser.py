import asyncio
import os

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup

import data


async def get_max_page(url) -> int:
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(url)
            soup_max = BeautifulSoup(await response.text(), "lxml")
            list_page = soup_max.find_all("a", class_="page larger")
            if list_page:
                max_page = list_page[-1].text
                return int(max_page)
            else:
                return 0
        except Exception as ex:
            print(ex)


async def gather_data():
    async with aiohttp.ClientSession() as session:

        for model in data.models:
            for body_type in data.body_types:
                url_body = f"https://3dmodels.org/ru/3d-models/vehicles/{model}/{body_type}"
                max_page = await get_max_page(url_body)
                for page in range(1, max_page + 1):
                    url = f"https://3dmodels.org/ru/3d-models/vehicles/{model}/{body_type}/page/{page}/"
                    print(url)
                    name_img = await parse_all_image_url(url, model, body_type)
                    print(name_img)
                    save_file(model, body_type, name_img)


async def parse_all_image_url(url, model, body_type):
    name_img: dict = {}
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), "lxml")
        img_link = soup.find_all("img", class_="lazyload")
        span_car = soup.find_all("span", class_="list-bottom")

        for img in img_link:
            url = (img.get("src"))
            if model in url:
                ln = url.split("/")[-2].split("_")
                ln.pop(0)
                model, *marka, year = ln
                car_name = f"{model}_{"-".join(marka)}_{body_type}_{year}"
                name_img[car_name] = url

        return name_img


def save_file(model, body_type, name_img: dict):
    c = 0
    for name, url in name_img.items():
        print(f"File: {name} Download {c + 1}")
        file_url = f"images/{model}/{body_type}"
        if not os.path.exists(file_url):
            os.makedirs(file_url)

        response = requests.get(url)
        with open(f"{file_url}/{name}.jpg", "wb") as file:
            file.write(response.content)


async def main():
    await gather_data()


if __name__ == '__main__':
    asyncio.run(main())
