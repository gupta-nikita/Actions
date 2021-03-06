import math
import torch.nn as nn
from torch.autograd import Variable


# Create Model
class ModelDef(nn.Module):
    """
    Generate model architecture
    """

    def __init__(self, n_inp, n_classes, rnn_type='RNN'):
        """
        Model initialization

        :param i_height: height of input image
        :type i_height: int
        :param i_width: width of input image
        :type i_width: int
        :param rnn_type: RNN or LSTM/GRU cell
        :type rnn_type: str
        """
        super(ModelDef, self).__init__()
        self.n_inp = n_inp
        self.n_layers = 1
        self.n_classes = n_classes

        self.rnn_type = rnn_type + 'Cell'
        if rnn_type == 'RNN':
            self.rnn = nn.RNNCell(self.n_inp, self.n_classes, nonlinearity='tanh')
        else:
            self.rnn = getattr(nn, self.rnn_type)(self.n_inp, self.n_classes)

    def forward(self, x, h0, c0):
        if self.rnn_type in ['RNNCell', 'GRUCell']:
            hn = self.rnn(x, h0)
            return hn
        else:
            hn, cn = self.rnn(x, (h0, c0))
            return (hn, cn)

    def init_hidden(self, bsz):
        weight = next(self.parameters()).data

        return Variable(weight.new(bsz, self.n_classes).zero_())
