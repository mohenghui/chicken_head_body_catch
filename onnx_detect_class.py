import onnxruntime as ort
import numpy as np
import cv2
import random
class OnnxDetector():
    def __init__(self,weight):
        # self.names=names
        # self.colors={name:tuple([random.randint(0, 255) for _ in range(3)]) for i,name in enumerate(names)}
        # pass
        cuda=True if ort.get_device() =="GPU" else False
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
        self.session = ort.InferenceSession(weight, providers=providers)
        self.outname = [i.name for i in self.session.get_outputs()]
        self.inname = [i.name for i in self.session.get_inputs()]
    # def init_weigth(self,w):

        
    def letterbox(self,im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, r, (dw, dh)
    def listint(self,list):
        return [int(i)for i in list]
    # def get_in
    def beint(self,tuple_list):
        return tuple([int(i) for i in tuple_list])
    def run(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        image = img.copy()
        image, ratio, dwdh = self.letterbox(image, auto=False)
        image = image.transpose((2, 0, 1))
        image = np.expand_dims(image, 0)
        image = np.ascontiguousarray(image)

        im = image.astype(np.float32)
        im /= 255
        inp = {self.inname[0]:im}
        outputs = self.session.run(self.outname, inp)[0]
        ori_images = [img.copy()]
        info_list=[]
        for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(outputs):
            # info=[]
            image = ori_images[int(batch_id)]
            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio
            box = self.listint(box.round().astype(np.int32).tolist())
            cls_id = int(cls_id)
            box.append(cls_id)
            info_list.append(box)
        return info_list 
            # score = round(float(score),3)
            # print(color)
            # cv2.rectangle(image,self.beint(box[:2]),self.beint(box[2:]),color,2)
            # cv2.putText(image,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2)  
        # return cv2.cvtColor(ori_images[0],cv2.COLOR_RGB2BGR)
        # return 
if __name__ == "__main__":
    names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 
            'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 
            'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 
            'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 
            'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 
            'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 
            'hair drier', 'toothbrush']

    onnx_Detector=OnnxDetector(names=names)
    onnx_Detector.init_weigth(w="./yolov7-tiny.onnx")
    img=cv2.imread(".\\inference\\images\\horses.jpg")
    loop_start = cv2.getTickCount()
    out=onnx_Detector.detecct(img=img)
    loop_time = cv2.getTickCount() - loop_start
    total_time = loop_time/(cv2.getTickFrequency()) # 使用getTickFrequency()更加准确
    print(total_time)
    running_FPS = int(1/total_time) # 帧率取整
    print("running_FPS:",running_FPS)
    cv2.imshow("mypic",out)
    cv2.waitKey(0)