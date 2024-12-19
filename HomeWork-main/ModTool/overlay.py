from itertools import product
from PIL import Image
import os


# 配置类
class Config:
    def __init__(self):
        self.output_base = "./output_/"
        self.assets_base = "./assets/"

        # 图层配置：背景、角色、图标（未来可能扩展）
        self.layers = {
            "background": "./assets/background/",
            "character": "./assets/character/",
            # "icon": "./assets/icon/"  # 未来可能添加的icon图层
        }

        # 背景和角色的列表
        self.bgs = ["Atgm", "Command", "Engineer", "FullSquad", "HalfSquad", "Hmg", "Manpad", "Scout", "Rcl"]
        self.chars = ["M16", "M16Young", "AKM"]
        # self.icons = ["icon1", "icon2"]  # 示例icon

        # 叠加规则：每个图层的大小、位置和透明度
        self.overlay_rules = {
            "background": {"resize": 1.0, "position": [0, 0], "alpha": 1.0},
            "character": {"resize": 0.27, "position": [0, -0.06], "alpha": 1.0},
            "icon": {"resize": 0.2, "position": [0.8, 0.8], "alpha": 0.7},
        }


# 叠加图像的辅助函数
def overlay_image(base_image, overlay_image, position_x, position_y, resize=1.0):
    """
    叠加一个图像到基准图像上
    :param base_image: 基准图像
    :param overlay_image: 叠加图像
    :param position_x: 叠加图像的位置（x坐标）
    :param position_y: 叠加图像的位置（y坐标）
    :param resize: 叠加图像的缩放比例
    :return: 合成后的图像
    """
    overlay_image = overlay_image.resize(
        (int(overlay_image.width * resize), int(overlay_image.height * resize))
    )

    # 计算位置
    x_pos = int(base_image.width * position_x)
    y_pos = int(base_image.height * position_y)

    # 创建临时图像用于叠加
    temp_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    temp_image.paste(overlay_image, (x_pos, y_pos), overlay_image)

    # 返回合成后的图像
    return Image.alpha_composite(base_image, temp_image)


# 合成图像的主函数
def combine_images(config):
    """
    根据配置合成所有可能的图像组合
    :param config: 配置对象
    :return: 生成的所有图像路径列表
    """
    result_images = []

    # 遍历所有背景和角色组合
    for bg, char in product(config.bgs, config.chars):
        char_folder_path = os.path.join(config.layers["character"], char)

        if os.path.exists(char_folder_path):
            for attachment in os.listdir(char_folder_path):
                if attachment.endswith(".png"):  # 确保是png文件
                    overlay_path_bg = os.path.join(config.layers["background"], f"{bg}.png")
                    overlay_path_char = os.path.join(char_folder_path, attachment)

                    if os.path.exists(overlay_path_bg) and os.path.exists(overlay_path_char):
                        # 获取叠加规则
                        bg_rule = config.overlay_rules["background"]
                        char_rule = config.overlay_rules["character"]

                        # 打开图像并应用透明度
                        base_image = Image.open(overlay_path_bg).convert("RGBA")
                        base_image = Image.blend(
                            Image.new("RGBA", base_image.size, (255, 255, 255, 0)),
                            base_image,
                            bg_rule["alpha"],
                        )

                        overlay_image_char = Image.open(overlay_path_char).convert("RGBA")
                        overlay_image_char = Image.blend(
                            Image.new("RGBA", overlay_image_char.size, (255, 255, 255, 0)),
                            overlay_image_char,
                            char_rule["alpha"],
                        )

                        # 叠加角色图像
                        base_image = overlay_image(
                            base_image,
                            overlay_image_char,
                            char_rule["position"][0],
                            char_rule["position"][1],
                            char_rule["resize"]
                        )

                        # 生成输出文件名并保存
                        output_image_name = f"{char}_{bg}_{attachment.split('.')[0]}.png"
                        output_image_path = os.path.join(config.output_base, output_image_name)
                        base_image.save(output_image_path)
                        result_images.append(output_image_path)

    return result_images


# 配置初始化并合成图像
config = Config()
generated_images = combine_images(config)

print(f"生成的图像路径：{generated_images}")
