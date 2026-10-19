import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
try:
    import torch
    from ctqs.models import ConditionalMLP, ConditionalTransformer, state
    from ctqs.physics import basis, hamiltonian
    AVAILABLE = True
except ImportError:
    AVAILABLE = False


@unittest.skipUnless(AVAILABLE, 'install CPU PyTorch for model checks')
class TestModels(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(1)
        torch.manual_seed(11)

    def test_normalization_and_causality_in_train_and_eval(self):
        for cls in [ConditionalMLP, ConditionalTransformer]:
            for n in [4,6]:
                model = cls(n).double()
                bits = torch.tensor(basis(n), dtype=torch.float64)
                for training in [True,False]:
                    model.train(training)
                    for cond in [[.2,0.],[1.6,-.03]]:
                        with torch.no_grad():
                            p = model.psi(bits,cond)
                            self.assertLess(abs(float(p@p)-1),1e-12)
                            reference = model.logits(bits,cond)
                            for i in range(n):
                                changed = bits.clone()
                                changed[:,i:] = 1-changed[:,i:]
                                updated = model.logits(changed,cond)
                                torch.testing.assert_close(reference[:,:i+1],updated[:,:i+1],atol=1e-12,rtol=0)

    def test_even_state_and_variational_gradient(self):
        for cls in [ConditionalMLP, ConditionalTransformer]:
            model = cls(4).double()
            bits = torch.tensor(basis(4), dtype=torch.float64)
            p = state(model,bits,.4,True)
            torch.testing.assert_close(p,p.flip(0))
            h = torch.tensor(hamiltonian(4,.4))
            e = p@h@p
            e.backward()
            self.assertTrue(all(torch.isfinite(x.grad).all() for x in model.parameters() if x.grad is not None))
            # Central finite difference for one weight checks energy/autograd path.
            weight = model.read.weight if cls is ConditionalTransformer else model.net[-1].weight
            grad = float(weight.grad[0,0])
            original = float(weight.detach()[0,0])
            energies=[]
            with torch.no_grad():
                for delta in [1e-5,-1e-5]:
                    weight[0,0]=original+delta
                    q=state(model,bits,.4,True)
                    energies.append(float(q@h@q))
                weight[0,0]=original
            self.assertAlmostEqual(grad,(energies[0]-energies[1])/2e-5,places=7)


if __name__ == '__main__':
    unittest.main()
