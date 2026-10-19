"""Normalized autoregressive models. No exact states or energies are inputs."""
import torch
from torch import nn
from torch.nn import functional as F


class AutoregressiveState(nn.Module):
    def psi(self, bits, condition):
        logits = self.logits(bits, condition)
        logp = -F.softplus(torch.where(bits.bool(), -logits, logits)).sum(-1)
        return torch.exp(logp / 2)


class ConditionalMLP(AutoregressiveState):
    def __init__(self, n, width=32):
        super().__init__()
        self.register_buffer('prefix_mask', torch.tril(torch.ones(n, n), diagonal=-1))
        self.register_buffer('positions', torch.eye(n))
        self.net = nn.Sequential(nn.Linear(2 * n + 2, width), nn.Tanh(),
                                 nn.Linear(width, width), nn.Tanh(), nn.Linear(width, 1))

    def logits(self, bits, condition):
        k, n = bits.shape
        prefix = bits[:, None, :] * self.prefix_mask[None, :, :]
        condition = torch.as_tensor(condition, dtype=bits.dtype, device=bits.device)
        inputs = torch.cat((prefix, self.positions[None].expand(k, -1, -1),
                            condition.reshape(1, 1, 2).expand(k, n, 2)), dim=-1)
        return self.net(inputs).squeeze(-1)


class ConditionalTransformer(AutoregressiveState):
    """Explicit condition token + BOS + right-shifted spin sequence; dropout=0."""
    def __init__(self, n, width=16, heads=2):
        super().__init__()
        self.embed = nn.Embedding(3, width)
        self.positions = nn.Embedding(n + 1, width)
        self.condition = nn.Linear(2, width)
        layer = nn.TransformerEncoderLayer(width, heads, dim_feedforward=2 * width,
                                           dropout=0.0, activation='gelu', batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, 1, enable_nested_tensor=False)
        self.read = nn.Linear(width, 1)
        self.register_buffer('causal', torch.triu(torch.ones(n + 1, n + 1, dtype=torch.bool), diagonal=1))

    def logits(self, bits, condition):
        k, n = bits.shape
        tokens = torch.cat((torch.full((k, 1), 2, dtype=torch.long, device=bits.device),
                            bits[:, :-1].long()), dim=1)
        condition = torch.as_tensor(condition, dtype=bits.dtype, device=bits.device)
        cond = self.condition(condition).reshape(1, 1, -1).expand(k, 1, -1)
        hidden = torch.cat((cond, self.embed(tokens)), dim=1)
        hidden = hidden + self.positions(torch.arange(n + 1, device=bits.device))[None]
        return self.read(self.encoder(hidden, mask=self.causal)[:, 1:]).squeeze(-1)


def state(model, bits, h, even=False, lam=0.0):
    psi = model.psi(bits, [h, lam])
    if even:
        if lam != 0:
            raise ValueError('even training is only justified at lambda=0')
        psi = psi + psi.flip(0)
        psi = psi / torch.linalg.vector_norm(psi)
    return psi
