import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.tracking.pdaf import joint_pdaf, pdaf, gate_detections, mahalanobis, normalize_distances
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
        truth_norm_dists = [1/31., 5/31., 10/31., 15/31]

        # call normalize_distances
        norm_dists = normalize_distances(dists)

        # check for correct behavior
        for truth_dist, dist in zip(truth_norm_dists, norm_dists):
            self.assertAlmostEqual(truth_dist, dist)

        # create empty list of distances
        dists = []

        # check that empty list is returned
        truth_norm_dists = []

        self.assertEqual(truth_norm_dists, normalize_distances(dists))

    def test_mahalanobis(self):
        """Tests mahalanobis method"""
        # generate test object
        test_obj = MagicMock(rng=5, bearing=5)

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
        truth_trimmed_epoch_frame = [0] * len(test_detects)
        truth_trimmed_epoch_frame[gated_idx] = test_detects[gated_idx]
        truth_detections_used = [0] * num_detects
        truth_detections_used[gated_idx] = 1

        # call gate_detections
        trimmed_frame, dets_used = gate_detections((rng_gate, bearing_gate, type_gate), test_detects)

        # check for correct behavior
        self.assertEqual(truth_trimmed_epoch_frame, trimmed_frame)
        self.assertEqual(truth_detections_used, dets_used)

    @patch('src.tracking.pdaf.gate_detections')
    @patch('src.tracking.pdaf.mahalanobis')
    def test_pdaf(self, mock_mahal, mock_gate):
        """Tests pdaf method"""
        # number of test cases
        num_cases = 4

        # mock normalize_distances return values
        truth_weights = [[0.7, 0.3], [0.55, 0.45], [], [1, 0]]

        # mock detections used return value from gate_detections
        truth_dets_used = [[1, 1], [1, 1], [0, 0], [1, 0]]

        # loop through test cases
        for ii in range(num_cases):
            # set normalize_distances and gate_detections return values
            mock_mahal.side_effect = truth_weights[ii]
            mock_gate.return_value = [0] * len(truth_weights[ii]), truth_dets_used[ii]

            # call pdaf
            dists, dets_used = pdaf(None, None, None)        # args do not matter

            # check for correct behavior
            self.assertEqual(truth_weights[ii], dists)
            self.assertEqual(truth_dets_used[ii], dets_used)

            mock_mahal.reset_mock()

    @patch('src.tracking.pdaf.pdaf')
    def test_joint_pdaf(self, mock_pdaf):
        """Tests joint pdaf method"""
        # number of test cases
        num_cases = 3

        # initialize obj_list_list
        obj_list_list = [0] * num_cases

        # initalize gate_list_list
        gate_list_list = [0] * num_cases

        # initialize epoch_frame_list
        epoch_frame_list = [0] * num_cases

        # initialize norm_dists_lists
        norm_dists_lists = [0] * num_cases

        # initialize truth_update_list 
        truth_update_list = [0] * num_cases

        # initialize dets_used_list
        dets_used_list = [0] * num_cases

        # initialize truth_detsdets_used
        truth_dets_used = [0] * num_cases

        # test 1 -- one object, multiple detections
        obj_list_list[0]     = [MagicMock(rng = 5, bearing = 5, objectType=ObjectType.BUOY)]
        gate_list_list[0]    = ((0, 10), (2.5, 7.5), (ObjectType.BUOY, ObjectType.NONE))
        epoch_frame_list[0]  = [(4, 4, ObjectType.BUOY), (8, 6, ObjectType.NONE)]
        norm_dists_lists[0]  = [[0.75, 0.25]]
        truth_update_list[0] = [(5, 4.5)]
        dets_used_list[0]    = [[1, 1]]
        truth_dets_used[0]   = [1, 1]
        # test 2 -- two objects, multiple detections for each (no overlapping detections)
        obj_list_list[1]     = obj_list_list[0] + [MagicMock(rng = 15, bearing = 30, objectType = ObjectType.BUOY)]
        gate_list_list[1]    = gate_list_list[0] + ((12, 18), (20, 40), (ObjectType.BUOY, ObjectType.NONE))
        epoch_frame_list[1]  = epoch_frame_list[0] + [(13, 25, ObjectType.NONE), (16, 28, ObjectType.NONE)]
        norm_dists_lists[1]  = [[0.75, 0.25, 0, 0], [0, 0, 0.45, 0.55]]
        truth_update_list[1] = truth_update_list[0] + [(14.65, 26.65)]
        dets_used_list[1]    = [[1, 1, 0, 0], [0, 0, 1, 1]]
        truth_dets_used[1]   = [1, 1, 1, 1]
        # test 3 -- two objects, multiple detections for each w/ ONE overlapping detection
        obj_list_list[2]     = obj_list_list[1]
        gate_list_list[2]    = (((0, 15), (0, 20), (ObjectType.BUOY, ObjectType.NONE)), ((8, 22), (16, 44), (ObjectType.NONE)))
        epoch_frame_list[2]  = epoch_frame_list[1] + [(10, 18, ObjectType.NONE)]
        norm_dists_lists[2]  = [[0.55, 0.25, 0, 0, 0.2], [0, 0, 0.4, 0.5, 0.1]]
        truth_update_list[2] = [(6.2, 7.3), (14.66666666, 26.666666666)]
        dets_used_list[2]    = [[1, 1, 0, 0, 1], [0, 0, 1, 1, 0]]
        truth_dets_used[2]   = [1, 1, 1, 1, 1]

        # loop through test cases
        for obj_list, gate_list, epoch_frame, norm_dists_list, dets_used, \
            truth_update, truth_dets_used in zip(obj_list_list, gate_list_list, epoch_frame_list, \
                                                 norm_dists_lists, dets_used_list, truth_update_list, truth_dets_used):
            # set up PDAF mock return value
            mock_pdaf.side_effect = zip(norm_dists_list, dets_used)

            # call joint pdaf
            update, dets_used = joint_pdaf(obj_list, gate_list, epoch_frame)

            # check for correct behavior
            for truth_update_val, update_val in zip(truth_update, update):
                for truth_val, val in zip(truth_update_val, update_val):
                    self.assertAlmostEqual(truth_val, val)

            self.assertEqual(truth_dets_used, dets_used)
