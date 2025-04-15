from PIL import Image
import os
import json

WIDTH, HEIGHT = 1920, 1080
FRAME_FOLDER = "frames"
OUTPUT_FILE = "FrameData2.json"

print("start")

def get_pixel_index(x, y, width):
    return y * width + x

def convert_image_to_frame_data(image_path):
    print(f"처리 중: {image_path}")  # 처리 중인 이미지 파일 출력
    image = Image.open(image_path).convert("RGBA")
    pixels = image.load()

    order = "xy"
    colors = {}

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a < 10:
                continue
            grayscale = round((r + g + b) / 3)
            index = get_pixel_index(x, y, WIDTH)
            if grayscale not in colors:
                colors[grayscale] = []
            colors[grayscale].append(index)

    frame_data = [order]
    for color, indexes in colors.items():
        indexes.sort()
        ranges = []
        start = end = indexes[0]
        for idx in indexes[1:]:
            if idx == end + 1:
                end = idx
            else:
                ranges.append(f"{start:X}/{end:X}")
                start = end = idx
        ranges.append(f"{start:X}/{end:X}")
        frame_data.append([color] + ranges)
    return frame_data

def main():
    files = sorted(os.listdir(FRAME_FOLDER))
    result = {}

    total_files = len(files)
    print(f"총 {total_files}개의 이미지 파일이 있습니다.")

    for idx, file in enumerate(files):
        if file.endswith(".png"):
            path = os.path.join(FRAME_FOLDER, file)
            frame_data = convert_image_to_frame_data(path)
            result[idx + 1] = frame_data

            # 진행 상태 출력
            progress = (idx + 1) / total_files * 100
            print(f"진행 상황: {progress:.2f}% ({idx + 1}/{total_files})")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f)

    print(f"프레임 데이터가 {OUTPUT_FILE} 파일로 저장되었습니다.")

if __name__ == "__main__":
    main()
