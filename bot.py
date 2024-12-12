from scholarly import scholarly
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import random
import google.generativeai as genai
import os

bot_token = os.environ['BOT_TOKEN']
api_hash = os.environ['API_HASH']
api_id = os.environ['API_ID']
# ...
open_token = os.environ['OPENAI_TOKEN']

TARGET = 'DiaraToken'

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


    RESUKLT = f"Title: **{random_article['bib']['title']}**\n\n" \
            f"Abstract: {abstract}\n\n" \
            f"Author(s): **{random_article['bib']['author']}**\n\n" \
            f"Year: {random_article['bib']['pub_year']}\n" \
            f"Link: {random_article['pub_url']}\n\n" \
            "🥇 This message was generated by **[DiaraColab search engine](https://github.com/Mehranalam/Diara-Colab)** and the articles were received from google scholar.\n\n" \
            "**🌊 تمام مقالات ارسالی توسط ربات داخل کانال @DiaraToken برای دسترسی بهتر آرشیو خواهد شد.**"
    
    return RESUKLT


def mind(result):
    genai.configure(api_key=open_token)

    model = genai.GenerativeModel("gemini-1.5-flash")
    content = f"""لطفا این مقاله رو به شکل خیلی خوب و با جزيیات بررسی کن و برداشت هات رو به شکل زبان عامیانه فارسی به‌طور کامل شرح بده بطور علمی و دقیق با فرمولها و دلایل حرفه‌ای و دقیقا توضیح بده این مقاله رو.

لینک مقاله و خلاصه‌ای ازش: {result}

لطفا انتهای پست هم رفرنس بزار و ارجاع بده.
اگه هم فایل PDF بود و دسترسی نداشتی یک خبر درمورد مهندسی پزشکی بفرست یه خبر علمی
"""
    response = model.generate_content(content)

    rtl = response.text
    uio = rtl.replace("#", "")
    
    return uio


try:
    resukt = welcome()
    maintain = mind(resukt)
except:
    print("again! :))")
    resukt = welcome()
    maintain = mind(resukt)

async def main():
    async with app:
        sent_message = await (app.send_message(TARGET ,resukt, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN))
        await app.send_message(TARGET ,maintain , reply_to_message_id=sent_message.id)

app.run(main())
