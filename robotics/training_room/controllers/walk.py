"""ZMP walking planner — the "walk" rung of the body curriculum.

Implements Kajita's preview control for biped walking (the LIPM + ZMP method
the Asimov-1 video cites): given a footstep sequence, generate a center-of-mass
trajectory that keeps the zero-moment point inside the support polygon.

This is the *planner* layer only — it outputs reference trajectories (CoM,
footsteps, swing feet). The *tracking* layer (inverse kinematics + whole-body
force→torque) maps those references onto the 28 joints, and is the next rung.

References:
  S. Kajita et al., "Biped Walking Pattern Generation by using Preview Control
  of Zero-Moment Point", ICRA 2003.
"""
from __future__ import annotations

import numpy as np


class ZMPPreviewPlanner:
    """Generate a CoM trajectory that tracks a ZMP reference via preview control.

    State  x = [com, com_vel, com_acc]
    LIPM   com_acc = (g / z_c) * (com - zmp)
    """

    def __init__(self, z_c: float = 0.78, g: float = 9.81, dt: float = 0.005,
                 preview_s: float = 1.6, Qe: float = 1.0, R: float = 1e-6):
        self.z_c = z_c
        self.g = g
        self.dt = dt
        self.N = int(preview_s / dt)  # preview horizon (steps)

        # discrete LIPM
        T = dt
        self.A = np.array([[1.0, T, T * T / 2.0],
                           [0.0, 1.0, T],
                           [0.0, 0.0, 1.0]])
        self.b = np.array([[T ** 3 / 6.0], [T ** 2 / 2.0], [T]])
        self.c = np.array([[1.0, 0.0, -z_c / g]])  # p = com - (z_c/g)*acc

        # solve Riccati + compute feedback and preview gains
        self.K, self.f = self._gains(Qe, R)

    def _gains(self, Qe: float, R: float):
        A, b, c = self.A, self.b, self.c
        Q = c.T @ c * Qe  # state cost (on ZMP error)
        # Riccati (iterative, N iterations is plenty for convergence)
        P = np.zeros((3, 3))
        for _ in range(2000):
            P_next = A.T @ P @ A - A.T @ P @ b @ np.linalg.inv(R + b.T @ P @ b) @ b.T @ P @ A + Q
            if np.max(np.abs(P_next - P)) < 1e-12:
                P = P_next
                break
            P = P_next
        # feedback gain
        K = np.linalg.inv(R + b.T @ P @ b) @ (b.T @ P @ A)
        # closed-loop
        Ac = A - b @ K
        # preview gains f[j] for j = 1..N steps ahead
        f = np.zeros(self.N)
        invBT = np.linalg.inv(R + b.T @ P @ b) @ b.T  # (1,3)
        for j in range(1, self.N + 1):
            M = np.linalg.matrix_power(Ac.T, j - 1)  # (3,3)
            f[j - 1] = float((invBT @ M @ c.T)[0, 0]) * Qe
        return K, f

    def plan(self, zmp_ref: np.ndarray, com0: np.ndarray, horizon: int) -> np.ndarray:
        """Generate a CoM trajectory tracking a ZMP reference.

        Args:
            zmp_ref: (horizon,) desired ZMP x-position at each step
            com0:    initial [com_x, com_vel_x]
            horizon: number of steps to plan
        Returns:
            (horizon,) CoM x-position trajectory
        """
        x = np.array([com0[0], com0[1], 0.0])
        traj = np.zeros(horizon)
        for k in range(horizon):
            u = -float((self.K @ x)[0])
            for j in range(self.N):
                idx = k + j + 1
                ref = zmp_ref[idx] if idx < horizon else zmp_ref[-1]
                u += self.f[j] * ref
            x = self.A @ x + self.b.flatten() * u
            traj[k] = x[0]
        return traj


def footstep_sequence(n_steps: int, step_length: float, step_width: float,
                      start_x: float = 0.0) -> np.ndarray:
    """Generate alternating left/right footstep positions (x only, sagittal).

    Returns an array of (n_steps,) foot x-positions; the ZMP reference during
    double-support is the midpoint of the stance foot.
    """
    feet = []
    x = start_x
    for i in range(n_steps):
        x += step_length
        feet.append(x)
    return np.array(feet)


def zmp_from_footsteps(feet: np.ndarray, dt: float, step_s: float) -> np.ndarray:
    """Build a ZMP x-reference from footstep positions (piecewise stance)."""
    steps_per_step = int(step_s / dt)
    horizon = steps_per_step * len(feet)
    zmp = np.zeros(horizon)
    for i, fx in enumerate(feet):
        s = i * steps_per_step
        e = min((i + 1) * steps_per_step, horizon)
        zmp[s:e] = fx
    return zmp
