import os
import json
import re
import shutil


def merge_configs_from_folder(config_folder):
    """
    从指定文件夹中读取所有JSON配置文件，并合并成一个列表。
    """
    all_configs = []
    for filename in os.listdir(config_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(config_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_configs.extend(data)  # 将当前文件的配置合并到总列表中
    return all_configs


def select_picture_for_configs(configs, picture_folder):
    """
    根据配置中的背景、角色和附件信息，选择匹配的图片。
    """
    result = []
    for config in configs:
        search_terms = [config.get("background"), config.get("character")] + config.get("attachments", [])
        matching_images = find_matching_images(search_terms, picture_folder)
        
        if len(matching_images) == 1:
            config["replace"] = matching_images[0]
            result.append(config)
        else:
            raise ValueError(f"配置 {config} 所描述的图片数量不正确，当前匹配到的图片有: {matching_images}")
    
    return result


def find_matching_images(search_terms, picture_folder):
    """
    根据搜索条件在指定文件夹中查找匹配的图片。
    """
    matching_images = []
    for filename in os.listdir(picture_folder):
        name, ext = os.path.splitext(filename)
        if ext.lower() in [".png", ".jpg", ".jpeg"]:
            name_parts = name.split("_")
            if all(term in name_parts for term in search_terms) and len(name_parts) == len(search_terms):
                matching_images.append(filename)
    return matching_images


def select_unit_for_configs(configs, mod_file):
    """
    根据配置中的单位信息，从mod文件中选择对应的图片路径。
    """
    result = []
    with open(mod_file, 'r', encoding='utf-8') as file:
        mod_content = file.read()

    for config in configs:
        units = config.get('units', [])
        selected_images = []

        for unit in units:
            pattern = re.compile(r'"([^"]*' + re.escape(unit) + r'[^"]*)"\s*[^"]*FileName\s*=\s*"([^"]+\.(png|jpg|jpeg|bmp|gif))"')
            matches = pattern.findall(mod_content)

            # 添加匹配到的图片路径
            selected_images.extend(match[1] for match in matches)

        if selected_images:
            config["origin"] = selected_images
            result.append(config)
        else:
            raise ValueError(f"配置 {config} 所描述的单位并不存在。")

    return result


def generate_mod_file(configs, mod_file_path, output_dir, picture_folder):
    """
    生成新的mod文件，将图片路径替换并保存修改后的文件。
    """
    with open(mod_file_path, 'r', encoding='utf-8') as file:
        mod_file_content = file.read()

    new_mod_file_content = mod_file_content
    for config in configs:
        replace_filename = config["replace"]
        for origin_path in config["origin"]:
            image_filename = origin_path.split("/")[-1]
            folder_path = "/".join(origin_path.split("/")[:-1])
            new_image_path = origin_path.replace(image_filename, replace_filename)

            # 替换mod文件中的图片路径
            pattern = re.compile(re.escape(origin_path))
            new_mod_file_content = pattern.sub(new_image_path, new_mod_file_content)

            # 生成目标文件夹路径
            target_folder_path = os.path.join(output_dir, folder_path.replace("GameData:", "").lstrip("/"))
            os.makedirs(target_folder_path, exist_ok=True)

            # 复制图片文件到目标文件夹
            picture_source_path = os.path.join(picture_folder, replace_filename)
            if os.path.exists(picture_source_path):
                shutil.copy(picture_source_path, os.path.join(target_folder_path, replace_filename))
            else:
                print(f"警告：图片 {replace_filename} 未找到在指定的图片文件夹：{picture_folder}")

    # 保存修改后的mod文件
    new_mod_file_path = os.path.join(output_dir, "modified_mod_file.txt")
    with open(new_mod_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(new_mod_file_content)

    print(f"替换后的mod文件已保存至: {new_mod_file_path}")


def main():
    output_folder = "./output/"
    config_folder = "./config/"
    picture_folder = "./assets/combined/"
    mod_path = "mod.txt"

    try:
        merged_configs = merge_configs_from_folder(config_folder)
        result = select_picture_for_configs(merged_configs, picture_folder)
        result = select_unit_for_configs(result, mod_path)
        generate_mod_file(result, mod_path, output_folder, picture_folder)
    except ValueError as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
