
from aitextgen import aitextgen
# With your trained model, you can reload the model at any time by
# providing the folder containing the pytorch_model.bin model weights + the config, and providing the tokenizer.
ai2 = aitextgen(model_folder="trained_model",
               tokenizer_file="aitextgen.tokenizer.json")


lyrics = """She was driving last Friday on her way to Cincinnati on a snow white Christmas Eve\nGoing home to see her mama and her daddy with the baby in the backseat\nFifty miles to go, and she was running low on faith and gasoline\nIt'd been a long hard year\nShe had a lot on her mind, and she didn't pay attention\nShe was going way too fast\nBefore she knew it she was spinning on a thin black sheet of glass\nShe saw both their lives flash before her eyes\nShe didn't even have time to cry\nShe was so scared\nShe threw her hands up in the air\n\nJesus, take the wheel\nTake it from my hands\n'Cause I can't do this on my own\nI'm letting go"""
lines = [2]
for line in lines:
    nline = lyrics.split("\n")[line]
    gentext = ai2.generate_one(prompt=nline+"\n")
    no_lyrics = gentext.split("\n")[1:]
    print("\n".join(no_lyrics))
