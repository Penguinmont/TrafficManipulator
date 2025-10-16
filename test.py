import numpy as np

# --- 特征类别说明 ---
# KitNET/AfterImage 框架为每个数据包提取一个包含 100 个特征的向量。
# 这些特征可以分为三大类别，所有统计数据都在 5 个不同的时间窗口（对应 5 个 Lambda 衰减率）上计算得出。
# 每个时间窗口包含 3 个核心统计量：
#   1. 权重 (weight): 时间窗口内数据点的加权计数。
#   2. 均值 (mean): 特征的加权平均值（如平均数据包大小）。
#   3. 标准差 (std): 特征的加权标准差（如数据包大小的波动性）。

# 类别 1: 数据包大小 (Packet Size) 的统计特征 (共 60 个特征)
#   这些特征描述了在不同网络“通道”中数据包大小的统计分布。
#   - 特征 0-14 (15个):   源 MAC-IP 通道 (Source MAC-IP Channel)
#       - (5个时间窗口 * 3个统计量)
#   - 特征 15-29 (15个):  源 IP 通道 (Source IP Channel)
#       - (5个时间窗口 * 3个统计量)
#   - 特征 30-44 (15个):  源-目标 IP 对通道 (Source-Destination IP Channel)
#       - (5个时间窗口 * 3个统计量)
#   - 特征 45-59 (15个):  源 IP-目标端口 对通道 (Source IP-Destination Port Channel)
#       - (5个时间窗口 * 3个统计量)

# 类别 2: 全局抖动 (Global Jitter) 的统计特征 (共 15 个特征)
#   “抖动”指的是数据包到达时间的间隔。这些特征描述了整个网络流量中数据包到达间隔的稳定性。
#   - 特征 60-74 (15个): 全局通道 (Global Channel)
#       - (5个时间窗口 * 3个统计量: weight, mean, std of inter-arrival times)

# 类别 3: 相关性 (Correlational) 的统计特征 (共 25 个特征)
#   这些特征描述了不同通道统计数据之间的相关性，这对于检测更复杂的行为模式至关重要。
#   - 特征 75-99 (25个): 5 组不同通道之间的皮尔逊相关系数 (PCC)
#       - 每组相关性都在 5 个不同的时间窗口上计算，因此 5 * 5 = 25 个特征。
#       - 这些相关性对可能包括：
#           - 源IP(包大小) vs 源MAC-IP(包大小)
#           - 源-目标IP(包大小) vs 源IP(包大小)
#           - 等等...


import numpy as np

# --- 特征类别说明 (来自您的注释) ---
# ... (您的注释保持不变) ...

def analyze_and_print_sample(sample_vector, sample_number):
    """
    分析单个100维特征向量，并以结构化的方式打印出来，所有数值保留三位小数。
    """
    print(f"--- 分析样本 #{sample_number} ---")

    # 首先，将整个向量的所有值四舍五入到小数点后三位
    formatted_vector = np.round(sample_vector, 3)

    # --- 类别 1: 数据包大小 (Packet Size) 的统计特征 (共 60 个) ---
    print("\n[类别 1: 数据包大小统计特征]")

    # 为了方便阅读，我们将每个通道的 (5个时间窗口 * 3个统计量) 结果重塑为 5x3 的矩阵
    # 每一行代表一个时间窗口，三列分别是 [权重, 均值, 标准差]
    print("  特征 0-14  (源 MAC-IP):")
    print(formatted_vector[0:15].reshape(3, 5))

    print("\n  特征 15-29 (源 IP):")
    print(formatted_vector[15:30].reshape(3, 5))

    print("\n  特征 30-44 (源-目标 IP):")
    print(formatted_vector[30:45].reshape(3, 5))

    print("\n  特征 45-59 (源 IP-目标端口):")
    print(formatted_vector[45:60].reshape(3, 5))

    # --- 类别 2: 全局抖动 (Global Jitter) 的统计特征 (共 15 个) ---
    print("\n[类别 2: 全局抖动统计特征]")
    print("  特征 60-74 (全局通道):")
    print(formatted_vector[60:75].reshape(3, 5))

    # --- 类别 3: 相关性 (Correlational) 的统计特征 (共 25 个) ---
    print("\n[类别 3: 相关性统计特征]")
    print("  特征 75-99 (5组通道间的皮尔逊相关系数):")
    # 这25个特征是5组相关性在5个时间窗口下的结果，直接打印
    print(formatted_vector[75:100].reshape(5, 5))
    print("-" * 30 + "\n")


# --- 主程序 ---
try:
    # 加载 .npy 文件
    file_path = 'example/train_ben.npy'
    data = np.load(file_path)

    # 打印数组的形状 (行数, 列数)
    print(f"数据文件 '{file_path}' 加载成功。")
    print(f"数据形状 (样本数, 特征数): {data.shape}")
    print("=" * 30)

    # 检查是否有足够的数据来打印
    num_samples_to_print = 20
    if data.shape[0] < num_samples_to_print:
        print(f"\n注意: 文件中的样本数 ({data.shape[0]}) 少于20个，将打印所有样本。")
        num_samples_to_print = data.shape[0]

    print(f"\n将详细分析前 {num_samples_to_print} 个样本:\n")

    # 循环分析并打印前20个样本
    for i in range(num_samples_to_print):
        analyze_and_print_sample(data[i], i + 1)


except FileNotFoundError:
    print("错误: 'example/train_ben.npy' 文件未找到。")
    print("请确保该文件存在于 'example' 子目录中。")
except Exception as e:
    print(f"读取或处理文件时发生错误: {e}")