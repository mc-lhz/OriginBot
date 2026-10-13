# OriginBot

OriginBot 智能小车项目 —— 车道线保持 + 红绿灯识别 + 激光雷达避障，基于 ROS2 与 Horizon Robotics BPU 平台。

2025 年 OriginBot 项目相关资产备份。

## 项目结构

```
.
├── codes/                 散装脚本与配置文件
│   ├── lanedetection.py           车道线控制节点（订阅 /pct_vel，转发 /cmd_vel）
│   ├── dnn_node_yolo.launch.py    拉起 dnn_node_example，加载 traffice.json 做红绿灯推理
│   ├── simple.launch.py           多节点 launch 编写示例
│   ├── topic_helloworld_pub/sub.py ROS2 话题发布/订阅入门示例
│   ├── view_traffic.py            订阅 /traffice_sign，打印红绿灯识别结果
│   ├── view_lidar.py              订阅 /scan，筛选 0.12~0.3m 的近距回波
│   ├── picker_pic.py              按回车抓拍 /image，存到 /userdata/pictures/img
│   ├── picker_end.py              端到端数据采集：裁剪车道线 ROI 并按 /cmd_vel 打标
│   ├── videorecord.py             录制 /image 为 avi 视频
│   ├── pic_seg.py                 数据集按 8:1:1 划分（图片与标签配对检查）
│   ├── mydata.yaml                YOLOv5 数据集配置：红/蓝/绿灯 3 类
│   ├── yolov5x_config.yaml        Horizon hb_mapper 量化转换配置（nv12 / bayes-e）
│   ├── traffice.txt               交通标志类别文本
│   └── originbot-云-端 .ipynb     云端 notebook
├── lanedetection/         ROS2 功能包
│   ├── lanedetection.py           主控节点：红绿灯停车、雷达避障、车道线行驶
│   ├── obstacle_detection.py      雷达检测正前方障碍物，发布 /has_obs
│   ├── package.xml / setup.py / setup.cfg / test/
├── models/                模型与推理配置
│   ├── best.onnx                          YOLOv5x 导出的浮点模型
│   ├── yolov5x_672x672_nv12.bin           上板量化模型（672×672 / nv12）
│   ├── resnet18_224x224_nv12.bin          图像分类模型
│   ├── traffice.json                      dnn_node 推理配置
│   └── predefined_classes.txt             预定义类别
├── book/                  《实战…》教程 PDF（第三方教材，注意版权）
├── programs/              环境安装资料（安装包与驱动不入库）
└── 文档/                  项目过程截图
```

## 核心流程

```
相机 /image ──► dnn_node (yolov5x_672x672_nv12.bin)
                  └─► /traffice_sign (ai_msgs/PerceptionTargets)
雷达 /scan  ──► obstacle_detection ──► /has_obs (Bool)
模型推理    ──► /pct_vel (Twist)
                            │
                            ▼
                    lanedetection 节点
                            │
                            └─► /cmd_vel ──► 底盘

决策优先级：红灯停车 > 前方障碍物右转避让(angular.z=6.4) > 正常车道线循迹
```

`lanedetection.py:47` 的 `pct_callback` 实现了上述优先级：检测到 `red_light`（置信度 > 0.5）时速度与角速度清零；否则若 `/has_obs` 为真则以固定角速度右转；否则按 `linear.x = 1.3 × 0.32`、`angular.z = 2.6 × pct.angular.z` 循迹。

## 环境准备

| 用途 | 软件 |
| --- | --- |
| 上位机远程操作 | MobaXterm |
| 开发环境 | Anaconda3 |
| 虚拟化 | VMware Workstation 17 Pro |
| 串口驱动 | CH340（`programs/Uart drive（CH340）/`） |
| 代码编辑器 | Sublime Text |

安装包体积过大（Anaconda 约 914MB），已通过 `.gitignore` 排除，请自行从官方渠道下载。详见 `programs/预装软件.pdf` 与 `book/` 教程。

## 使用方式

```bash
# 编译并加载功能包
cd ~/catkin_ws/src
git clone https://github.com/mc-lhz/OriginBot.git
cd ~/catkin_ws && colcon build && source install/setup.bash

# 拉起红绿灯识别
ros2 launch codes/dnn_node_yolo.launch.py
# 模型需放在开发板 /userdata/yolov5/traffice.json 同级路径

# 单独运行节点
ros2 run lanedetection lanedetection.py
```

数据集重新划分与模型转换：

```bash
python3 codes/pic_seg.py          # 划分 8:1:1 并检查图片/标签配对
hb_mapper checker  codes/yolov5x_config.yaml
hb_mapper convert  codes/yolov5x_config.yaml
```

## 许可

代码部分仅供学习参考；`book/` 内 PDF 为第三方出版物版权归原出版方所有；模型与 `yolov5x_config.yaml` 版权归 Horizon Robotics 所有。