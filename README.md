# Rasberry-Pi-Car
The code of Raberry-Pi Car. Start with the simple use case of raspberry pie, record the learning experiment process of raspberry pie.  
项目是学校项目设计的课程项目，要求使用基于树莓派的小车实现部分功能。

在该实验中实现了 **小车的避障、单线巡线、颜色追踪任务**，后文会附出已实现功能的实现过程和代码，在参考的资料中有部分有待实现的内容以供参考，如有需要的同学可以参考本博客和参考教程实现树莓派小车各种功能的控制。

* 避障：使用红外和超声波传感器组合实现避障；
* 单线巡线：使用摄像头，基于视觉进行单线巡线；
* 颜色追踪：使用摄像头，基于视觉对蓝色（可以后续更改）物体进行追踪；

学校提供的小车的商家是[慧净电子](http://www.hlmcu.com/)，商家提供了一些使用教程，适合初学，基于C语言，实现了一些简单的红外避障、红外寻迹、超声波避障和摄像头调用。

项目使用Python作为编程语言，我建议使用Python实现，尤其是希望实现复杂功能的同学：首先，相较于C++，Python更容易上手，可以更方便实现各种功能；其次，Python有很多集成好的深度学习框架，如Tensorflow、Pytorch，对于一些复杂的功能可以很好地实现。但是同时，Python在运行速度方面存在劣势。
