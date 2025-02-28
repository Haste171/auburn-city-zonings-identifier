from PIL import Image
import logging
import argparse
import sys
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def replace_colors(image_path: str, target_hex_list: List[str], replacement_hex: str, output_path: str) -> None:
    """
    Replace multiple colors in an image with a single replacement color.
    
    Args:
        image_path (str): Path to the input image
        target_hex_list (list): List of hex color codes to replace
        replacement_hex (str): Hex color code to replace with
        output_path (str): Path to save the output image
    """
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()

    target_hex_list = [hex.upper() for hex in target_hex_list]
    replacement_hex = replacement_hex.upper()

    logger.info(f"Replacing colors {target_hex_list} with {replacement_hex}")

    target_rgbs = []
    for target_hex in target_hex_list:
        if not target_hex.startswith("#"):
            target_hex = f"#{target_hex}"
        target_rgb = (
            int(target_hex[1:3], 16),
            int(target_hex[3:5], 16),
            int(target_hex[5:7], 16)
        )
        target_rgbs.append(target_rgb)
        logger.info(f"Target RGB: {target_rgb}")

    if not replacement_hex.startswith("#"):
        replacement_hex = f"#{replacement_hex}"
    
    replacement_rgb = (
        int(replacement_hex[1:3], 16),
        int(replacement_hex[3:5], 16),
        int(replacement_hex[5:7], 16),
        255
    )
    logger.info(f"Replacement RGB: {replacement_rgb}")

    color_counts = {}
    sample_size = min(100000, len(data))
    for i in range(0, len(data), len(data)//sample_size):
        if i >= len(data):
            break
        rgb = data[i][:3]
        if rgb in color_counts:
            color_counts[rgb] += 1
        else:
            color_counts[rgb] = 1

    most_common = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    logger.info(f"Most common RGB values in image sample: {most_common}")

    actual_colors = [color for color, _ in most_common]
    for target in target_rgbs:
        for actual in actual_colors:
            if max(abs(target[i] - actual[i]) for i in range(3)) < 20:
                if actual not in target_rgbs:
                    target_rgbs.append(actual)
                    logger.info(f"Added detected color variation: {actual}")

    tolerance = 8
    new_data = []
    total_replaced = 0

    for pixel in data:
        r, g, b, a = pixel
        is_target_color = any(
            abs(r - target_rgb[0]) <= tolerance and 
            abs(g - target_rgb[1]) <= tolerance and 
            abs(b - target_rgb[2]) <= tolerance
            for target_rgb in target_rgbs
        )

        if is_target_color:
            new_data.append(replacement_rgb)
            total_replaced += 1
        else:
            new_data.append(pixel)

    new_img = Image.new("RGBA", img.size)
    new_img.putdata(new_data)
    new_img.save(output_path)

    logger.info(f"Total replaced: {total_replaced} pixels out of {len(data)}")

def create_zone_group_mapping(zone_data: Dict[str, Dict[str, Any]], zone_codes: List[str]) -> Dict[str, str]:
    """Create a mapping from zone codes to hex colors, ensuring correct format and uppercase."""
    mapping = {}
    for zone in zone_codes:
        if zone in zone_data:
            color = zone_data[zone]["color"]
            if not color.startswith("#"):
                color = f"#{color}"
            mapping[zone] = color
        else:
            logger.warning(f"Zone code '{zone}' not found in zone data")
    return mapping

def load_zone_data() -> Dict[str, Dict[str, Any]]:
    """Load zoning data from zone_data.py."""
    try:
        from data.zones import zone_data
        logger.info(f"Loaded {len(zone_data)} zone definitions from zone_data.py")
        return zone_data
    except ImportError:
        logger.error("Could not import zone_data.py. Make sure it exists in the same directory.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Replace colors in zoning map images")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Replace colors command
    replace_parser = subparsers.add_parser("replace", help="Replace colors in an image")
    replace_parser.add_argument("--image", "-i", required=True, help="Path to input image")
    replace_parser.add_argument("--output", "-o", required=True, help="Path to output image")
    replace_parser.add_argument("--colors", "-c", nargs="+", required=True, help="List of hex colors to replace")
    replace_parser.add_argument("--replacement", "-r", required=True, help="Replacement hex color")

    # Zone group command
    zone_parser = subparsers.add_parser("zone-group", help="Replace colors for a group of zones")
    zone_parser.add_argument("--image", "-i", required=True, help="Path to input image")
    zone_parser.add_argument("--output", "-o", required=True, help="Path to output image")
    zone_parser.add_argument("--zones", "-z", nargs="+", required=True, help="List of zone codes to replace")
    zone_parser.add_argument("--replacement", "-r", required=True, help="Replacement hex color")

    args = parser.parse_args()
    zone_data = load_zone_data()

    if args.command == "replace":
        replace_colors(
            image_path=args.image,
            target_hex_list=args.colors,
            replacement_hex=args.replacement,
            output_path=args.output
        )

    elif args.command == "zone-group":
        mapping = create_zone_group_mapping(zone_data, args.zones)
        if not mapping:
            logger.error("No valid zone codes found")
            sys.exit(1)

        logger.info(f"Replacing zones: {', '.join(mapping.keys())}")
        hex_list = list(mapping.values())

        replace_colors(
            image_path=args.image,
            target_hex_list=hex_list,
            replacement_hex=args.replacement,
            output_path=args.output
        )

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
