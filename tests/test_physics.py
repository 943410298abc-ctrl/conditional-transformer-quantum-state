import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
try:
    import numpy as np
    from ctqs.physics import basis, hamiltonian, lookup, metrics, normalized, ritz
    AVAILABLE = True
except ImportError:
    AVAILABLE = False


@unittest.skipUnless(AVAILABLE, 'install requirements-research.txt for physics checks')
class TestPhysics(unittest.TestCase):
    def test_hamiltonian_against_kronecker(self):
        n, h, lam = 4, 0.37, -0.02
        x = np.array([[0., 1.], [1., 0.]])
        z = np.diag([1., -1.])
        def op(operators):
            result = np.ones((1, 1))
            for a in operators:
                result = np.kron(result, a)
            return result
        ref = np.zeros((16, 16))
        for i in range(n):
            operators = [np.eye(2) for _ in range(n)]
            operators[i] = x
            ref -= h * op(operators)
        for i in range(n-1):
            operators = [np.eye(2) for _ in range(n)]
            operators[i] = operators[i+1] = z
            ref -= op(operators)
        ref += lam * op([z] + [np.eye(2)] * (n-1))
        np.testing.assert_allclose(hamiltonian(n,h,lam), ref)

    def test_symmetry_and_covariance(self):
        for lam in [0., 0.03]:
            np.testing.assert_allclose(hamiltonian(4,.4,lam)[::-1,::-1], hamiltonian(4,.4,-lam))
        self.assertGreater(np.linalg.norm(hamiltonian(4,.4,.03)[::-1,::-1]-hamiltonian(4,.4,.03)), 0)

    def test_zero_field_degeneracy(self):
        h = hamiltonian(4,0)
        psi = np.eye(16)[:,0]
        m = metrics(h,psi,4)
        self.assertAlmostEqual(m['energy'], -3.)
        self.assertEqual(m['ground_multiplicity'], 2)
        self.assertAlmostEqual(m['ground_space_fidelity'], 1.)

    def test_ritz_rank_and_variational_bound(self):
        rng = np.random.default_rng(1)
        h = hamiltonian(4,.5)
        p = normalized(rng.normal(size=16))
        q, rank = ritz(h, [p, p.copy(), p[::-1]])
        self.assertEqual(rank,2)
        self.assertLessEqual(q@h@q, p@h@p+1e-12)
        self.assertGreaterEqual(q@h@q, np.linalg.eigvalsh(h)[0]-1e-12)

    def test_lookup_endpoints(self):
        states = np.eye(4)[:2]
        np.testing.assert_allclose(lookup(-1,[.2,.8],states), states[0])
        np.testing.assert_allclose(lookup(2,[.2,.8],states), states[1])
        self.assertAlmostEqual(np.linalg.norm(lookup(.5,[.2,.8],states)),1.)


if __name__ == '__main__':
    unittest.main()
