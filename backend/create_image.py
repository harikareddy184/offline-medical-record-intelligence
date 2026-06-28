from PIL import Image, ImageDraw

# Create blank image
img = Image.new('RGB', (500, 500), color=(240, 248, 255))

draw = ImageDraw.Draw(img)

# Add simple design
draw.rectangle([50, 50, 450, 450], outline="blue", width=5)
draw.text((150, 220), "Medical App", fill="black")

# Save image
img.save("image.png")

print("✅ image.png created successfully!")