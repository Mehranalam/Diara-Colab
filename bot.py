from scholarly import scholarly
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import random
import os
import openai

# 33

bot_token = os.environ['BOT_TOKEN']
api_hash = os.environ['API_HASH']
api_id = os.environ['API_ID']

open_token = os.environ['OPENAI_TOKEN']

TARGET = 'DiaraArchive'

app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)


def welcome():
    keywords = [
            "Biomaterials",
            "Bioinformatics",
            "Biomedical Imaging",
            "Biomimetics",
            "Tissue Engineering",
            "Medical Devices",
            "Neuroengineering",
            "Biosensors",
            "Bioprinting",
            "Clinical Engineering",
            "Rehabilitation Engineering",
            "Bioelectrics",
            "Biomechanics",
            "Nanomedicine",
            "Regenerative Medicine",
            "Biomedical Signal Processing",
            "Genetic Engineering",
            "Pharmacokinetics",
            "Medical Robotics",
            "Wearable Health Technology",
            "Telemedicine",
            "Cardiovascular Engineering",
            "Orthopaedic Bioengineering",
            "Prosthetics and Implants",
            "Biochemical Engineering",
            "Optical Imaging",
            "Molecular Imaging",
            "Artificial Organs",
            "Cancer Bioengineering",
            "Human-Computer Interaction in Healthcare"
        ]

    selected_keyword = random.choice(keywords)
    search_query = scholarly.search_pubs(selected_keyword)
    articles = [next(search_query) for _ in range(5)]
    random_article = random.choice(articles)

    abstract = random_article['bib'].get('abstract', 'No abstract available')

    client = openai.OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"""لطفا این مقاله رو به شکل خیلی خوب و با جزيیات بررسی کن و برداشت هات رو به شکل زبان عامیانه فارسی در حد ۴ پاراگراف شرح بده و دقیقا توضیح بده این مقاله رو.

لینک مقاله: {random_article['pub_url']}"""
            }
        ]
    )

    
    return completion.choices[0].message

try:
    output = welcome()
except scholarly._proxy_generator.MaxTriesExceededException:
    print("again! :))")
    output = welcome()


async def main():
    async with app:
        await app.send_message(TARGET ,output, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

app.run(main())
