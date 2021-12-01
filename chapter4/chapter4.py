# -*- coding: utf-8 -*-
import torch
import torch.utils.data as Data
import torch.nn.functional as F
from torch.autograd import Variable
import matplotlib.pyplot as plt
import numpy as np
import pdb


# 1.加载数据
torch.manual_seed(1)  # 确定随机种子，保证结果可重复

LR = 0.01
BATCH_SIZE = 20
EPOCH = 10

# 生成数据
x = torch.unsqueeze(torch.linspace(-1,1,1500), dim = 1)
y = x.pow(3) + 0.1*torch.normal(torch.zeros(*x.size()))

# 数据画图
plt.scatter(x.numpy(),y.numpy())
plt.show()

# 把数据转化为torch类型
torch_dataset = Data.TensorDataset(x,y)
loader = Data.DataLoader(dataset = torch_dataset,batch_size=BATCH_SIZE,shuffle=True,drop_last=True)

# 2.配置模型和优化器
class Net(torch.nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.hidden = torch.nn.Linear(1,20)  #隐含层
        self.predict = torch.nn.Linear(20,1) #输出层
        
    def forward(self,x):
        #pdb.set_trace()
        x = F.relu(self.hidden(x))
        x = self.predict(x)
        
# 不同的网络模型
net_SGD = Net()
net_Momentum = Net()
net_RMSprop = Net()
net_AdaGrad = Net()
net_Adam = Net()

nets = [net_SGD,net_Momentum,net_AdaGrad,net_RMSprop,net_Adam]

# 不同的优化器
opt_SGD = torch.optim.SGD(net_SGD.parameters(),lr= LR)
opt_Momentum = torch.optim.SGD(net_Momentum.parameters(),lr=LR,momentum=0.8)
opt_RMSprop = torch.optim.RMSprop(net_RMSprop.parameters(),lr=LR,alpha=0.9)
opt_AdaGrad = torch.optim.Adagrad(net_AdaGrad.parameters(),lr=LR)
opt_Adam = torch.optim.Adam(net_Adam.parameters(),lr=LR,betas=(0.9,0.99))

optimizers = [opt_SGD,opt_Momentum,opt_AdaGrad,opt_RMSprop,opt_Adam]

loss_func = torch.nn.MSELoss()

losses_his = [[],[],[],[],[]]

# 模型训练
for epoch in range(EPOCH):
    print('EPOCH:',epoch)
    for step,(batch_x,batch_y) in enumerate(loader):
        b_x = Variable(batch_x)
        b_y = Variable(batch_y)
        
        for net,opt,l_his in zip(nets,optimizers,losses_his):
            output = net(b_x)             #前向算法的结果
            pdb.set_trace()
           
            loss = loss_func(output,b_y)  #计算loss
            opt.zero_grad()               #梯度清零
            
            loss.backward()               #后向算法，计算梯度
            opt.step()                    #应用梯度
            l_his.append(loss.data.item())
            
labels = ['SGD','Momentum','AdaGrad','RMSprop','Adam']
for i,l_his in enumerate(losses_his):
    plt.plot(l_his,label = labels[i])
plt.legend(los='best')
plt.xlabel('steps')
plt.ylabel('Loss')
plt.ylim(0,0.2)
plt.show























