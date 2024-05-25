"""
[USAGE] 
python main.py <directory> -f <formats>

There are currently four file formats that it can be converted to: 
- jpeg
- png
- webp
- tiff

[Example]
python main.py C:\path\to\directory -f jpeg png webp tiff
"""

import os
import rawpy
import imageio
import concurrent.futures
import argparse

def process_file(raw_path, jpeg_dir, png_dir, tiff_dir, webp_dir):
    try:
        with rawpy.imread(raw_path) as raw:
            print("Raw path: ", raw_path)
            rgb = raw.postprocess()

            # Save as JPEG
            if jpeg_dir:
                jpeg_path = os.path.join(jpeg_dir, os.path.splitext(os.path.basename(raw_path))[0] + '.jpg')
                imageio.imsave(jpeg_path, rgb)

            # Save as PNG
            if png_dir:
                png_path = os.path.join(png_dir, os.path.splitext(os.path.basename(raw_path))[0] + '.png')
                imageio.imsave(png_path, rgb)

            # Save as TIFF
            if tiff_dir:
                tiff_path = os.path.join(tiff_dir, os.path.splitext(os.path.basename(raw_path))[0] + '.tiff')
                imageio.imsave(tiff_path, rgb)

            # Save as WebP
            if webp_dir:
                webp_path = os.path.join(webp_dir, os.path.splitext(os.path.basename(raw_path))[0] + '.webp')
                imageio.imsave(webp_path, rgb)

            print(f'Converted {raw_path} to {jpeg_path if jpeg_dir else ""}, {png_path if png_dir else ""}, {tiff_path if tiff_dir else ""}, {webp_path if webp_dir else ""}')
    except Exception as e:
        print(f'Failed to convert {raw_path}: {e}')

def convert_raw_to_images(directory, formats):
    jpeg_dir = png_dir = tiff_dir = webp_dir = None

    if 'jpeg' in formats:
        jpeg_dir = os.path.join(directory, 'jpeg')
        os.makedirs(jpeg_dir, exist_ok=True)
    if 'png' in formats:
        png_dir = os.path.join(directory, 'png')
        os.makedirs(png_dir, exist_ok=True)
    if 'tiff' in formats:
        tiff_dir = os.path.join(directory, 'tiff')
        os.makedirs(tiff_dir, exist_ok=True)
    if 'webp' in formats:
        webp_dir = os.path.join(directory, 'webp')
        os.makedirs(webp_dir, exist_ok=True)

    raw_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.lower().endswith(('.nef', '.cr3', '.cr2', '.arw', '.dng', '.rw2', '.orf'))]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, raw_path, jpeg_dir, png_dir, tiff_dir, webp_dir) for raw_path in raw_files]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Error occurred: {e}')

def main():
    parser = argparse.ArgumentParser(description='Convert RAW images to JPEG, PNG, TIFF, and WebP formats.')
    parser.add_argument('directory', type=str, help='The directory containing RAW files to convert.')
    parser.add_argument('-f', '--formats', type=str, nargs='+', choices=['jpeg', 'png', 'tiff', 'webp'], default=['jpeg'], help='The output formats (default: jpeg).')

    args = parser.parse_args()
    convert_raw_to_images(args.directory, args.formats)

if __name__ == '__main__':
    main()
