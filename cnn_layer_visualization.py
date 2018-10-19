import os
import cv2
import numpy as np
import torch
from torch.optim import Adam
from torchvision import models
from torch.autograd import Variable


class CNNLayerVisualization:
    def __init__(self, image, model, selected_layer, selected_filter):
        self.image = Variable(image.unsqueeze(0))
        self.model = model
        self.selected_layer = selected_layer
        self.selected_filter = selected_filter
        self.conv_output = 0

    def hook_layer(self):
        def hook_function(module, grad_in, grad_out):
            self.conv_output = grad_out[0, self.selected_filter]
        self.model[self.selected_layer].register_forward_hook(hook_function)

    def visualise_layer_with_hooks(self, img_id):
        self.hook_layer()
        for i in range(0, 35):
            # optimizer.zero_grad()
            # Assign create image to a variable to move forward in the model
            x = self.image
            for index, layer in enumerate(self.model):
                if not os.path.exists('D:/generated/' + 'layer'+str(index)):
                    os.makedirs('D:/generated/'+'layer'+str(index))
                print('network-architecture-index', index)
                print('network-architecture-layer', layer)
                x = layer(x.cuda())
                if index == self.selected_layer:
                    break

                # for i in range(x.shape[1]):
                # img = x.detach().numpy()[0, i, :, :]
                # if i == self.selected_filter:
                img = x.data.cpu().numpy()[0, i, :, :]
                #######################
                ymax = 255
                ymin = 0
                xmax = img.max()
                xmin = img.min()
                img = torch.round_(torch.Tensor((ymax - ymin) * (img - xmin) / (xmax - xmin) + ymin))
                #######################

                # a = cv2.cvtColor(img.cpu().numpy(), cv2.COLOR_BGR2GRAY)
                c = img.cpu().numpy().astype(np.uint8)
                b = cv2.equalizeHist(c)
                cv2.imwrite('D:/generated/' + 'layer'+str(index)+'/' + img_id[-1]+'----' + 'layer' +
                            str(index) + '-filter' + str(i)+'.png', b)



