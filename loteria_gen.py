from PIL import Image, ImageDraw
import os
import random

# Paths
template_path = 'LOTERIA.png'  # Path to your template (updated to PNG)
image_dir = 'loteria/'         # Directory containing the 56 PNG images
output_pdf = 'Loteria_Tickets.pdf'

# Load template
template = Image.open(template_path)

# Get image files from directory
image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

# Ensure there are exactly 56 images
if len(image_files) != 56:
    raise ValueError(f"Expected 56 images in '{image_dir}', but found {len(image_files)}.")

# Dimensions for placing images
grid_size = (4, 4)  # 4x4 grid
grid_width, grid_height = 1225, 1415
cell_width = grid_width // grid_size[0]
cell_height = grid_height // grid_size[1]

# Centering offsets for the grid
x_offset = (template.width - grid_width) // 2
y_offset = 480  # Header space is 480 pixels

# Create tickets
tickets = []
for _ in range(25):
    # Copy template for each ticket
    ticket = template.copy()
    draw = ImageDraw.Draw(ticket)

    # Randomly select 16 unique images
    selected_images = random.sample(image_files, grid_size[0] * grid_size[1])

    # Place images into the grid with adjusted spacing
    for idx, img_file in enumerate(selected_images):
        img_path = os.path.join(image_dir, img_file)
        img = Image.open(img_path)

        # Preserve aspect ratio and resize to fit within cell dimensions
        img.thumbnail((cell_width - 10, cell_height - 10))  # Add spacing by subtracting pixels

        # Calculate position in the grid with spacing adjustments
        row, col = divmod(idx, grid_size[0])
        x = x_offset + col * cell_width + (cell_width - img.width) // 2
        y = y_offset + row * cell_height + (cell_height - img.height) // 2

        # Paste image onto the template
        ticket.paste(img, (x, y), mask=img if img.mode == 'RGBA' else None)

    # Draw the grid lines on the ticket (dark blue color)
    dark_blue = (0, 0, 139)
    for row in range(grid_size[1] + 1):
        y_line = y_offset + row * cell_height
        draw.line([(x_offset, y_line), (x_offset + grid_width, y_line)], fill=dark_blue, width=2)

    for col in range(grid_size[0] + 1):
        x_line = x_offset + col * cell_width
        draw.line([(x_line, y_offset), (x_line, y_offset + grid_height)], fill=dark_blue, width=2)

    tickets.append(ticket)

# Save all tickets as a single PDF file
tickets[0].save(output_pdf, save_all=True, append_images=tickets[1:])
print(f"Lotería tickets saved to '{output_pdf}'.")