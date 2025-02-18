from PIL import Image
import os

# Paths
image_dir = 'loteria/'  # Directory containing the 56 PNG images
output_pdf = 'Loteria_Reference.pdf'

# Get image files from directory
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')], key=lambda x: int(x.split('.')[0]))

# Ensure there are exactly 56 images
if len(image_files) != 56:
    raise ValueError(f"Expected 56 images in '{image_dir}', but found {len(image_files)}.")

# A4 dimensions in pixels (at 300 DPI)
a4_width, a4_height = 2480, 3508

# Grid dimensions for reference layout
grid_size = (8, 7)  # 8 columns x 7 rows (to fit all 56 images)
tile_width, tile_height = a4_width // grid_size[0], a4_height // grid_size[1]

# Create a blank A4-sized image (white background)
reference_image = Image.new('RGB', (a4_width, a4_height), 'white')

# Place images into the grid in numerical order
for idx, img_file in enumerate(image_files):
    img_path = os.path.join(image_dir, img_file)
    img = Image.open(img_path)

    # Preserve aspect ratio and resize to fit within each tile
    img.thumbnail((tile_width - 10, tile_height - 10))  # Add spacing by subtracting pixels

    # Calculate position in the grid
    row, col = divmod(idx, grid_size[0])
    x = col * tile_width + (tile_width - img.width) // 2
    y = row * tile_height + (tile_height - img.height) // 2

    # Paste image onto the reference image
    reference_image.paste(img, (x, y))

# Save the reference image as a PDF
reference_image.save(output_pdf, "PDF", resolution=300)
print(f"Lotería reference PDF saved to '{output_pdf}'.")
