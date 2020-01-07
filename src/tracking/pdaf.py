import numpy as np
from scipy.spatial.distance import mahalanobis as sp_mahalanobis

def pdaf(obj, gate, epoch_frame):
    """
    Generates a weighted update observation using detections in epoch frame and gate for object
    Inputs:
        obj -- tuple containing range, bearing, and type data for object
        gate -- list of tuples containing allowed rng ranges, bearing ranges, and object types
        epoch_frame -- list of detections
    Returns:
        update -- update observation based on detections within object gate (None if no detections inside gate)
        detections_used -- list of detections used in creation of observation for this object
    """
    # gate detections in epoch frame
    trimmed_epoch_frame, detections_used = gate_detections(gate, epoch_frame)

    # generate mahalanobis distance for each detection
    dist_list = [mahalanobis(obj, det) for det in trimmed_epoch_frame]

    # normalize mahalanobis distances
    norm_dists = normalize_distances(dist_list)

    # calculate update measurement
    update = (sum(rng * weight for (rng, _), weight in zip(trimmed_epoch_frame, norm_dists)), \
              sum(bearing * weight for (_, bearing), weight in zip(trimmed_epoch_frame, norm_dists)))

    # if any detections within object gate
    if len(update) != 0:
        return update, detections_used
    else:
        return (None, None), detections_used

def gate_detections(gate, epoch_frame):
    """
    Gates detections and returns trimmed list of detections for epoch frame
    Inputs:
        gate -- list of tuples containing allowed rng ranges, bearing ranges, and object types
        epoch_frame -- list of detections
    Returns:
        trimmed_epoch_frame -- gated list of detections
        detections_used -- list of detections used in creation of observation for this object
    """
    # initialize trimmed epoch frame
    trimmed_epoch_frame = [0] * len(epoch_frame)

    # initialize detections used
    detections_used = [0] * len(epoch_frame)

    # loop through detections and gate
    num_gated_dets = 0
    for ii, det in enumerate(epoch_frame):
        if (gate[0][0] < det[0] < gate[0][1]) and (gate[1][0] < det[1] < gate[1][1]) and (det[2] in gate[2]):
            # add detection to gated epoch frame
            trimmed_epoch_frame[num_gated_dets] = det
            num_gated_dets += 1

            # update detections used
            detections_used[ii] = 1

    return trimmed_epoch_frame[0:num_gated_dets], detections_used

def mahalanobis(obj, detection):
    """
    Returns mahalanobis distance between obj and detection
    Inputs:
        obj -- range and bearing data for obj
        detection -- range and bearing data for detection
    Returns:
        dist -- mahalanobis distance between obj and detection
    """
    covar_inv = [[1, 0], [0, 1]]        # Assumption: no covariance between range and bearing
    
    return sp_mahalanobis([obj[0], detection[0]], [obj[1], detection[1]], covar_inv)
    

def normalize_distances(distances):
    """
    Normalizes (to 1) the mahalanobis distances in distance array and turns association scores into costs
    Inputs:
        distances -- array of distances
    Returns:
        norm_distances -- normalized array of distances
    """

    # if detections exist within gate
    if len(distances) != 0:
        max_dist = max(distances)
        total_dist = sum(distances)
        return [(max_dist - dist) / total_dist for dist in distances]
    # else...
    else:
        return [] 
