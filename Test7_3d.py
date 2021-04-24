from builtins import *
import numpy as np
# 画图会用到
import plotly.graph_objs as go
import pandas as pd

z_dict = dict()
fig = go.Figure()


# 提取CSV表格数据
def get_Z_Dict():
    data = pd.read_csv('Trackpad Heatmap data demo.csv', header=1)
    df = pd.DataFrame(data)
    x = list()
    y = list()

    for i in range(len(data)):
        newdata = df.iloc[i]['RebootLoop_x1 Trackpad':'RebootLoop_x50 Trackpad']
        list1 = list(newdata.array)
        if 1 in list1:
            x1 = list1.index(1.0)  # 返回第一次出现1的下标值
            y1 = list1.count(1.0)  # 返回出现1的总次数
            x.append(x1)
            y.append(y1)
        else:
            pass
    z_tuples = list(zip(x, y))  # 生成(x,y)，字典的key的list
    for (i, j) in z_tuples:
        b = (i, j)
        xy_tuples = z_tuples.count(b)
        z_dict[b] = xy_tuples  # 生成z_dict字典，形式为((x, y), z)


def get_3D():
    z_max = max(z_dict.values())
    fig.add_trace(go.Mesh3d(
        x=[50],
        y=[50],
        z=[0],
        hoverinfo='none',
        opacity=0,
        flatshading=False,
    ))
    fig.add_trace(go.Mesh3d(
        x=[50],
        y=[50],
        z=[0],
        hoverinfo='none',
        opacity=0,
        flatshading=False,

        # 复用这个trace, 设置 colorbar
        intensity=[1, z_max],  # 设置 colorbar 取值范围
        coloraxis='coloraxis',  # 设置 colorbar 颜色
    ))
    for x2, y2 in z_dict.keys():
        if (x2, y2) in z_dict.keys():
            z2 = z_dict.get((x2, y2))

            fig.add_trace(go.Mesh3d(

                x=[x2, x2, x2 + 1, x2 + 1, x2, x2, x2 + 1, x2 + 1],
                y=[y2, y2 + 1, y2 + 1, y2, y2, y2 + 1, y2 + 1, y2],
                z=[0, 0, 0, 0, z2, z2, z2, z2],
                alphahull=0,
                opacity=1,
                flatshading=False,
                # Intensity of each vertex, which will be interpolated and color-coded
                intensity=[0, 0, 0, 0, z2, z2, z2, z2],
                coloraxis='coloraxis',

            ))
    fig.update_layout(
        width=650,
        height=700,
        title_text='3D Bar Chart',
        title_x=0.5,
        scene=dict(
            camera_eye_x=-1.25,
            camera_eye_y=1.25,
            camera_eye_z=1.25,
            zaxis=dict(title='Count of failed units', nticks=z_max + 2 if z_max < 5 else None),
            xaxis=dict(title='First failed iteration', nticks=12),
            yaxis=dict(title='Total failed times', nticks=12),
        ),
        coloraxis=dict(
            colorbar=dict(
                ticks="outside",
                tickvals=[i for i in range(z_max + 1)],
                title='Count of failed units',
            ),

        ),

    )

    fig.show()


if __name__ == '__main__':
    get_Z_Dict()
    get_3D()

