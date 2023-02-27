# 鸡头，鸡身抓取客户端   
通过YOLOv7实现鸡头/鸡身坐标跟踪   
# 总体设计思想   
该方案有四套抓鸡方案   
第一套抓鸡方案   
python demo_onnx.py   

第二套抓鸡方案   
python demo_onnx_chop.py  
![image](https://user-images.githubusercontent.com/52809781/221510970-6b06b8cc-4c53-4fe9-82ed-575b088615c1.png)    
第三套抓鸡方案   
python demo_onnx_chop_new.py    
![image](https://user-images.githubusercontent.com/52809781/221511138-caaeb288-c60a-4fde-8d23-fc31d7d0f9d9.png)

第四套抓鸡方案   
python demo_onnx_chop_over.py   
通过驱动器控制电机实现电机运动   
控制电机原理通过脉冲信号控制电机正转，反转，转速等控制   

与[抓鸡服务器](https://github.com/mohenghui/catchServer)配套使用
# 里面用到的数据集和权重   
可通过[百度网盘](https://pan.baidu.com/s/1qX9RGKTKYfYbGKpdd8iuLw)进行下载
