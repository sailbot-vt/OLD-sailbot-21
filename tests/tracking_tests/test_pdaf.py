import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.tracking.pdaf import pdaf, gate_detections, mahalanobis, normalize_distances
from src.tracking.classification_types import ObjectType

import numpy as np
import time

class PDAFTests(unittest.TestCase):
    """Tests the methods in PDAF"""
    def test_normalize_distances(self):
        """Tests normalize distances method"""
        # create list of distances
        dists = [1, 5, 10, 15]

        # create truthed normalized list
        truth_norm_dists = [14/31., 10/31., 5/31., 0]

        # call normalize_distances
        norm_dists = normalize_distances(dists)

        # check for correct behavior
        for truth_dist, dist in zip(truth_norm_dists, norm_dists):
            self.assertAlmostEqual(truth_dist, dist)

    def test_mahalanobis(self):
        """Tests mahalanobis method"""
        # generate test object
        test_obj = (5, 5)

        # generate test detections
        num_detects = 3
        test_detects = [(5, 5), (10, 25), (40, -30)]

        # create truth mahalanobis distances
        truth_m_dists = [0, abs(5 - 20), abs(35 - (-35))]

        # call mahalanobis function
        m_dists = [0] * num_detects
        for ii, det in enumerate(test_detects):
            m_dists[ii] = mahalanobis(test_obj, det)

        # check for correct behavior
        for truth_dist, dist in zip(truth_m_dists, m_dists):
            self.assertAlmostEqual(truth_dist, dist)

    def test_gate_detections(self):
        """Tests gate detections method"""
        # generate test detections
        num_detects = 3
        test_detects = [(5, 5, ObjectType.BUOY), (10, 25, ObjectType.BUOY), (40, -30, ObjectType.BOAT)]

        # create range gate (one detect will pass through, others blocked
        rng_gate = (0, 10)
        bearing_gate = (0, 15)
        type_gate = (ObjectType.NONE, ObjectType.BUOY)

        # created truth trimmed epoch frame and detections_used
        gated_idx = 0
        truth_trimmed_epoch_frame = [test_detects[gated_idx]]
        truth_detections_used = [0] * num_detects
        truth_detections_used[gated_idx] = 1

        # call gate_detections
        trimmed_frame, dets_used = gate_detections((rng_gate, bearing_gate, type_gate), test_detects)

        # check for correct behavior
        self.assertEqual(truth_trimmed_epoch_frame, trimmed_frame)
        self.assertEqual(truth_detections_used, dets_used)
