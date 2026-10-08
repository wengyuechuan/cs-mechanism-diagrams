# 测试发现修复

独立测试指出完整 JPEG 解码文案与 import 实现不一致。已改为 Image.open + Image.load 并重新导入全部 3,439 张成功；forward.md 保留测试时的发现作为记录。
