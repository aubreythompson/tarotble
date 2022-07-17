from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')

set_seed(42)

file1 = open("tarotwords.txt","r+") 
tarot_words = file1.read()

lyrics = """She was driving last Friday on her way to Cincinnati on a snow white Christmas Eve\nGoing home to see her mama and her daddy with the baby in the backseat\nFifty miles to go, and she was running low on faith and gasoline\nIt'd been a long hard year\nShe had a lot on her mind, and she didn't pay attention\nShe was going way too fast\nBefore she knew it she was spinning on a thin black sheet of glass\nShe saw both their lives flash before her eyes\nShe didn't even have time to cry\nShe was so scared\nShe threw her hands up in the air\n\nJesus, take the wheel\nTake it from my hands\n'Cause I can't do this on my own\nI'm letting go"""
gens = generator(lyrics+"\nhow", max_length=1000, num_return_sequences=1)
gentext = gens[0]['generated_text']
print(gentext)
no_lyrics = gentext.split(lyrics, 1)[1]
question = no_lyrics.split("?", 1)[0] + "?"
print(question)