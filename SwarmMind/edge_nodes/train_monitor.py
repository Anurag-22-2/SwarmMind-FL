import wandb
import random
import math

run = wandb.init(project="my-ai-training", name="first-experiment")

epochs = 10
offset = random.random() / 5

for epoch in range(2, epochs):
    acc = 1 - 2 ** -epoch - random.random() / epoch - offset
    loss = 2 ** -epoch + random.random() / epoch + offset
    
   
    wandb.log({"acc": acc, "loss": loss})
    print(f"Epoch {epoch}: acc={acc:.4f}, loss={loss:.4f}")

run.finish()