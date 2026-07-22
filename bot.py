import discord
from discord.ext import commands
import random

import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

#Script de identificación :D
def detect_bird(path):
  # Disable scientific notation for clarity
  np.set_printoptions(suppress=True)

  # Load the model
  model = load_model(r"converted_keras\keras_model.h5", compile=False)

  # Load the labels
  class_names = open(r"converted_keras\labels.txt", "r").readlines()

  # Create the array of the right shape to feed into the keras model
  # The 'length' or number of images you can put into the array is
  # determined by the first position in the shape tuple, in this case 1
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  # Replace this with the path to your image
  image = Image.open(path).convert("RGB")

  # resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
  image_array = np.asarray(image)

  # Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  # Load the image into the array
  data[0] = normalized_image_array

  # Predicts the model
  prediction = model.predict(data)
  index = np.argmax(prediction)
  class_name = class_names[index]
  confidence_score = prediction[0][index]

  return class_name[2:]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)
    
@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            await attachment.save(f"images/{attachment.filename}")
            local_path = f"images/{attachment.filename}"
            bird = detect_bird(local_path)
            await ctx.send(f"You sent a file called {attachment.filename} :P")
            await ctx.send(f"The image seems to have a {bird}")
            if bird.strip() == "Pigeons":
                await ctx.send("This bird eats seeds, cereals like wheat, oat or corn, legumes, leaves and berries")
            elif bird.strip() == "Sparrows":
                await ctx.send("This bird eats herb seeds, grain cereals, small fruits and small insects")
            elif bird.strip() == "Ducks":
                await ctx.send("This bird eats cereals like corn, oat and wheat, vegetables like spinach, lettuce or carrot, insects, and fruits")
            else:
                await ctx.send("There seems to be an error while trying to identify the bird")
    else:
        await ctx.send("You didn't send any files")
    
bot.run("MTQ2ODc0Mjc5MzA3NjgwNTgwOA.GoFBSu.EFa58PA7DOsyomrcWbTjxPbTYHV7Dfko09jX6E")