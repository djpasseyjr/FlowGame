from absl.testing import absltest
from dynamics import FlowDynamics

class FlowDynamicsTest(absltest.TestCase):

    def test_fd_init(self):
        fd = FlowDynamics()
        self.assertLen(fd.state, 2)
        self.assertLen(fd.derivatives, 2)
        self.assertLen(fd.state_names, 2)
        self.assertLen(fd.state_history, 2)
        with self.assertRaises(ValueError):
            FlowDynamics(num_extra_states=1)

    def test_fd_dt(self):
        fd = FlowDynamics()
        dx = fd.dxdt(fd.state, 0, True)
        self.assertEqual(dx, [-1, 1])
        dx = fd.dxdt(fd.state, 0, False)
        self.assertEqual(dx, [-1, -1])

    def test_step(self):
        fd = FlowDynamics(numerical_dt=0.1)
        fd.step(False, 1.0)
        self.assertLen(fd.state_history, 11)
        self.assertEqual(fd.state_history[-1, 0], -1.0)
        self.assertEqual(fd.state_history[-1, 1], -1.0)
        self.assertEqual(fd.time_points[-1], 1.0)

        fd.step(True, 1.0)
        self.assertLen(fd.time_points, 21)
        self.assertAlmostEqual(fd.state_history[-1, 0], -2.0, delta=1e-5)
        self.assertAlmostEqual(fd.state_history[-1, 1], 0.0, delta=1e-5)
        self.assertAlmostEqual(fd.time_points[-1], 2.0, delta=1e-5)

if __name__ == "__main__":
    absltest.main()
