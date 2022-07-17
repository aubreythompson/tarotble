
from aitextgen import aitextgen
# With your trained model, you can reload the model at any time by
# providing the folder containing the pytorch_model.bin model weights + the config, and providing the tokenizer.
ai2 = aitextgen(model_folder="trained_model",
               tokenizer_file="aitextgen.tokenizer.json")

lyrics = """baby I'm faded but you will be waiting \n"""
ai2.generate(1, prompt=lyrics+"\nhow")
no_lyrics = gentext.split(lyrics, 1)[1]
question = no_lyrics.split("?", 1)[0] + "?"
print(question)