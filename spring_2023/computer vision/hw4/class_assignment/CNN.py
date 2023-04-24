{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import time\n",
    "import torch\n",
    "import torch.nn as nn\n",
    "import torchvision\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from torchvision import transforms\n",
    "from tqdm.notebook import trange, tqdm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Downloading https://data.vision.ee.ethz.ch/cvl/food-101.tar.gz to ../Data/Food101/food-101.tar.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|██████████| 4996278331/4996278331 [2:05:11<00:00, 665154.72it/s]  \n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Extracting ../Data/Food101/food-101.tar.gz to ../Data/Food101\n"
     ]
    },
    {
     "ename": "TypeError",
     "evalue": "Food101.__init__() got an unexpected keyword argument 'train'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[3], line 6\u001b[0m\n\u001b[1;32m      1\u001b[0m root_path \u001b[39m=\u001b[39m \u001b[39m\"\u001b[39m\u001b[39m../Data/Food101\u001b[39m\u001b[39m\"\u001b[39m\n\u001b[1;32m      3\u001b[0m train_dataset \u001b[39m=\u001b[39m torchvision\u001b[39m.\u001b[39mdatasets\u001b[39m.\u001b[39mFood101(root_path, download\u001b[39m=\u001b[39m\u001b[39mTrue\u001b[39;00m, transform\u001b[39m=\u001b[39mtransforms\u001b[39m.\u001b[39mCompose([\n\u001b[1;32m      4\u001b[0m     transforms\u001b[39m.\u001b[39mToTensor(),\n\u001b[1;32m      5\u001b[0m ]))\n\u001b[0;32m----> 6\u001b[0m test_dataset \u001b[39m=\u001b[39m torchvision\u001b[39m.\u001b[39;49mdatasets\u001b[39m.\u001b[39;49mFood101(root_path, train\u001b[39m=\u001b[39;49m\u001b[39mFalse\u001b[39;49;00m, download\u001b[39m=\u001b[39;49m\u001b[39mTrue\u001b[39;49;00m)\n",
      "\u001b[0;31mTypeError\u001b[0m: Food101.__init__() got an unexpected keyword argument 'train'"
     ]
    }
   ],
   "source": [
    "root_path = \"../Data/Food101\"\n",
    "\n",
    "train_dataset = torchvision.datasets.Food101(root_path, download=True, transform=transforms.Compose([\n",
    "    transforms.ToTensor(),\n",
    "]))\n",
    "test_dataset = torchvision.datasets.Food101(root_path, train=False, download=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def show(imgs):\n",
    "    if not isinstance(imgs, list):\n",
    "        imgs = [imgs]\n",
    "    fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)\n",
    "    for i, img in enumerate(imgs):\n",
    "        img = img.detach()\n",
    "        img = transforms.functional.to_pil_image(img)\n",
    "        axs[0, i].imshow(np.asarray(img))\n",
    "        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])\n",
    "\n",
    "samples = []\n",
    "for i in range(64):\n",
    "    samples.append(train_dataset[i][0])\n",
    "grid = torchvision.utils.make_grid(samples)\n",
    "show(grid)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
    "# hyper parameter\n",
    "num_epochs = 5\n",
    "batch_size = 8\n",
    "learning rate = 0.001"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "cse4310",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
