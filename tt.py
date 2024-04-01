#%%
import numpy as np
import matplotlib.pyplot as plt

# 生成矢量場的坐標
x = np.linspace(0, 2, 10)
y = np.linspace(0, 1, 5)
X, Y = np.meshgrid(x, y)

# 生成矢量場的矢量值
U = np.cos(X)
V = np.sin(Y)

# 繪製矢量場
plt.quiver(X, Y, U, V, scale=20)

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Quiver Plot')

plt.show()

# %%
import matplotlib.pyplot as plt
import numpy as np

# 创建一些示例数据
data = np.random.random((10, 10))

# 绘制图表
plt.imshow(data, cmap='viridis')
# cbar = plt.colorbar(orientation='horizontal')  # 使用 orientation 参数设置颜色条的方向

# 或者，可以显式指定颜色条的相关参数
cbar = plt.colorbar(ticks=[0, 0.5, 1], orientation='horizontal', label='Colorbar Label')

# 可以设置颜色条的标签
#cbar.set_label('Custom Label')

# 隐藏颜色条的边框
cbar.outline.set_visible(False)

# 设置颜色条的格式
cbar.formatter.set_powerlimits((0, 0))
cbar.update_ticks()

# 调整颜色条的位置
cbar.ax.set_position([0.1, 0.1, 0.8, 0.05])

# 显示图表
plt.show()

# %%
