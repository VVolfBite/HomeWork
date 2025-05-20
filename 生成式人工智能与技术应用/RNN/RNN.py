import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset

print("Starting data loading...")

# =======================
# 1. 读取与处理数据
# =======================
try:
    df = pd.read_csv("stock_dataset_2.csv")
    print(f"Successfully loaded data with shape: {df.shape}")
    print("\nFirst few rows of data:")
    print(df.head())
    print("\nData columns:", df.columns.tolist())
    df['date'] = pd.to_datetime(df['date'])
except Exception as e:
    print(f"Error reading data file: {e}")
    exit(1)

feature_cols = ['open', 'close', 'low', 'high', 'volume', 'money', 'change']
target_col = 'label'

# 验证数据列是否存在
missing_cols = [col for col in feature_cols + [target_col] if col not in df.columns]
if missing_cols:
    print(f"Missing columns in dataset: {missing_cols}")
    exit(1)

print("\nFeature statistics before scaling:")
print(df[feature_cols].describe())

print("\nStarting feature scaling...")
# 特征归一化
scaler = StandardScaler()
features = scaler.fit_transform(df[feature_cols].values)
labels = df[target_col].values.reshape(-1, 1)
print(f"Features shape: {features.shape}, Labels shape: {labels.shape}")

print("\nFeature statistics after scaling:")
print(pd.DataFrame(features, columns=feature_cols).describe())

# =======================
# 2. 构建时间序列
# =======================
print("\nCreating sequences...")
SEQ_LEN = 30

def create_sequences(features, labels, seq_len):
    x, y = [], []
    for i in range(len(features) - seq_len):
        x.append(features[i:i+seq_len])
        y.append(labels[i+seq_len])
    return np.array(x), np.array(y)

X, y = create_sequences(features, labels, SEQ_LEN)
print(f"Sequences created. X shape: {X.shape}, y shape: {y.shape}")

# 划分训练与测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)
print(f"\nTrain set shape: {X_train.shape}, Test set shape: {X_test.shape}")

# 转为 Tensor
X_train = torch.tensor(X_train).float()
y_train = torch.tensor(y_train).float()
X_test = torch.tensor(X_test).float()
y_test = torch.tensor(y_test).float()

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=64, shuffle=True)
test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=64)

# =======================
# 3. 构建模型
# =======================
print("\nBuilding model...")

class LstmRNN(nn.Module):
    def __init__(self, stock_count, lstm_size=128, num_layers=1, num_steps=30, 
                 input_size=7, embed_size=None, dropout=0.0):
        """
        LSTM RNN Model with optional embedding for multiple stocks.

        Args:
            stock_count (int): Number of stock symbols
            lstm_size (int): Hidden units in each LSTM layer
            num_layers (int): Number of LSTM layers
            num_steps (int): Time steps for input sequence
            input_size (int): Dimensionality of input features
            embed_size (int): If provided, use embedding for stock symbols
            dropout (float): Dropout rate applied to LSTM layers
        """
        super().__init__()
        self.use_embed = embed_size is not None and embed_size > 0
        self.embed_size = embed_size or -1
        self.stock_count = stock_count
        self.num_steps = num_steps
        self.input_size = input_size

        # 如果使用嵌入层
        if self.use_embed:
            self.embedding = nn.Embedding(stock_count, self.embed_size)
            input_size = input_size + self.embed_size

        # 创建LSTM层
        self.lstm_layers = nn.ModuleList()
        for i in range(num_layers):
            return_sequences = (i < num_layers - 1)
            self.lstm_layers.append(nn.LSTM(
                input_size if i == 0 else lstm_size,
                lstm_size,
                batch_first=True,
                dropout=dropout if i < num_layers - 1 else 0
            ))

        # 输出层
        self.dense = nn.Linear(lstm_size, 1)

    def forward(self, x, symbol_ids=None):
        """
        Forward pass for the model.

        Args:
            x: Input tensor of shape (batch_size, num_steps, input_size)
            symbol_ids: Optional tensor of shape (batch_size,) containing stock symbol indices
        Returns:
            output: Tensor of shape (batch_size, 1)
        """
        if self.use_embed and symbol_ids is not None:
            # 处理嵌入
            if len(symbol_ids.shape) == 2 and symbol_ids.shape[-1] == 1:
                symbol_ids = symbol_ids.squeeze(-1)
            
            # 获取嵌入并扩展维度
            embed = self.embedding(symbol_ids)  # (batch_size, embed_size)
            embed = embed.unsqueeze(1).expand(-1, self.num_steps, -1)  # (batch_size, num_steps, embed_size)
            x = torch.cat([x, embed], dim=-1)  # (batch_size, num_steps, input_size + embed_size)

        # 通过LSTM层
        out = x
        for lstm in self.lstm_layers:
            out, _ = lstm(out)

        # 通过输出层
        output = self.dense(out[:, -1, :])  # 只使用最后一个时间步的输出
        return output

# 检查是否有可用的GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\nUsing device: {device}")

# 创建模型实例
model = LstmRNN(
    stock_count=1,  # 当前只有一个股票
    lstm_size=128,
    num_layers=3,
    num_steps=SEQ_LEN,
    input_size=len(feature_cols),
    dropout=0.2
).to(device)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# 打印模型参数
print("\nModel parameters:")
for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")

# =======================
# 4. 模型训练
# =======================
print("\nStarting training...")
loss_list = []
EPOCHS = 50

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    batch_count = 0
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        pred = model(xb)
        loss = criterion(pred, yb)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        batch_count += 1
        
        # 打印第一个batch的预测结果
        if epoch == 0 and batch_count == 1:
            print("\nFirst batch prediction sample:")
            print("Input shape:", xb[0].shape)
            print("True value:", yb[0].item())
            print("Predicted value:", pred[0].item())
    
    avg_loss = total_loss / len(train_loader)
    loss_list.append(avg_loss)
    print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {avg_loss:.6f}")

# =======================
# 5. 可视化训练损失
# =======================
print("\nPlotting training loss...")
plt.figure(figsize=(10, 6))
plt.plot(loss_list)
plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.grid(True)
plt.savefig('training_loss.png')
plt.close()

# =======================
# 6. 测试集评估
# =======================
print("\nEvaluating on test set...")
model.eval()
predictions = []
true_values = []

with torch.no_grad():
    for xb, yb in test_loader:
        xb = xb.to(device)
        pred = model(xb)
        predictions.append(pred.cpu().numpy())
        true_values.append(yb.numpy())

predictions = np.concatenate(predictions, axis=0)
true_values = np.concatenate(true_values, axis=0)

# 打印一些预测样本
print("\nPrediction samples (first 5):")
for i in range(5):
    print(f"Sample {i+1}:")
    print(f"True value: {true_values[i][0]:.2f}")
    print(f"Predicted value: {predictions[i][0]:.2f}")
    print(f"Absolute error: {abs(true_values[i][0] - predictions[i][0]):.2f}")

# 计算评估指标
mse = np.mean((predictions - true_values) ** 2)
rmse = np.sqrt(mse)
mae = np.mean(np.abs(predictions - true_values))

print(f"\nTest Set Metrics:")
print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")

# 绘制预测结果
print("\nPlotting prediction results...")
plt.figure(figsize=(12, 6))
plt.plot(true_values, label="True", alpha=0.7)
plt.plot(predictions, label="Predicted", alpha=0.7)
plt.legend()
plt.title("True vs Predicted (Test Set)")
plt.grid(True)
plt.savefig('prediction_results.png')
plt.close()

# 保存预测结果到CSV
print("\nSaving prediction results to CSV...")
results_df = pd.DataFrame({
    'True_Value': true_values.flatten(),
    'Predicted_Value': predictions.flatten(),
    'Absolute_Error': np.abs(true_values.flatten() - predictions.flatten())
})

# 添加日期列
test_dates = df['date'].values[-len(true_values):]
results_df['Date'] = test_dates

# 重新排列列顺序
results_df = results_df[['Date', 'True_Value', 'Predicted_Value', 'Absolute_Error']]

# 保存到CSV
results_df.to_csv('prediction_results.csv', index=False)
print("Prediction results saved to 'prediction_results.csv'")

print("\nDone!")
