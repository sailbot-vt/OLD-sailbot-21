import numpy as np
from scipy.spatial.distance import mahalanobis as sp_mahalanobis

def joint_pdaf(object_list, gate_list, epoch_frame):
    """
    Generates a 'joint' weighted update observation using detections in epoch frame in gate for each object and weights possibility trees jointly to find a global best approach
    Inputs:
        object_list -- list of objects
        gate_list -- list of gates for each object
        epoch_frame -- list of detections
    Returns:
        update_list -- list of update observations based on detections within object gate
        detections_used -- list of detections used
    """
    # initialize assocs array
    assocs_arr = np.zeros((len(object_list), len(epoch_frame)))

    # initialize detections used
    detections_used = [0] * len(epoch_frame)

    # get association scores for each track - detection pair
    for ii, (obj, gate) in enumerate(zip(object_list, gate_list)):
        assoc_scores, detections_used_for_obj = pdaf(obj, gate, epoch_frame)

        assocs_arr[ii] = np.array(assocs)

        detections_used = [sum(uses) for uses in zip(detections_used, detections_used_for_obj)]

    # for detections shared by multiple objects, make association score 0 for all but highest associated obejct
    assocs_arr = np.where(assocs_arr < np.amax(assocs_arr, 0), 0, assocs_arr)

    # normalize rows
    for jj in range(assocs_arr.shape[0]):
        assocs_arr[jj] = np.array(normalize_distances(assocs_arr[jj].tolist()))

    # initialize update list
    update_list = [0] * len(object_list)

    # calculate update measurement
    for kk in range(len(update_list)):
        norm_assocs = assocs_arr[kk].tolist()
        # if no detections associated with object
        if sum(norm_dists) == 0:
            update_list[kk] = None
        else:
            update_list[kk] = (sum(rng * weight for (rng, _, _), weight in zip(epoch_frame, norm_assocs)), \
                           sum(bearing * weight for (_, bearing, _), weight in zip(epoch_frame, norm_assocs)))

    return update_list, detections_used


def pdaf(obj, gate, epoch_frame):
    """
    Generates a list of association scores using detections in epoch frame and gate for object
    Inputs:
        obj -- tuple containing range, bearing, and type data for object
        gate -- list of tuples containing allowed rng ranges, bearing ranges, and object types
        epoch_frame -- list of detections
    Returns:
        assoc_scores -- UNnormalized array of assoc_scores for track-detection pairs
        detections_used -- list of detections used in creation of observation for this object
    """
    # gate detections in epoch frame
    gated_epoch_frame, detections_used = gate_detections(gate, epoch_frame)

    # generate mahalanobis distance for each detection
    dists = [mahalanobis(obj, det) for det in gated_epoch_frame]

    # generate scores from distances
    max_dist = max(dists)
    assoc_scores = [max_dist - dist for dist in dists]

    return assoc_scores, detections_used

def gate_detections(gate, epoch_frame):
    """
    Gates detections and returns trimmed list of detections for epoch frame
    Inputs:
        gate -- list of tuples containing allowed rng ranges, bearing ranges, and object types
        epoch_frame -- list of detections
    Returns:
        gated_epoch_frame -- gated list of detections
        detections_used -- list of detections used in creation of observation for this object
    """
    # initialize gated epoch frame
    gated_epoch_frame = [0] * len(epoch_frame)

    # initialize detections used
    detections_used = [0] * len(epoch_frame)

    # loop through detections and gate
    for ii, det in enumerate(epoch_frame):
        if (gate[0][0] < det[0] < gate[0][1]) and (gate[1][0] < det[1] < gate[1][1]) and (det[2] in gate[2]):
            # add detection to gated epoch frame
            gated_epoch_frame[ii] = det

            # update detections used
            detections_used[ii] = 1

    return gated_epoch_frame, detections_used

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
    
    # if detection not within gate
    if detection == 0:
        return 0 

    return sp_mahalanobis([obj.rng, detection[0]], [obj.bearing, detection[1]], covar_inv)
    

def normalize_distances(distances):
    """
    Normalizes (to 1) the mahalanobis distances in distance array
    Inputs:
        distances -- array of distances
    Returns:
        norm_distances -- normalized array of distances
    """

    total_dist = sum(distances)
    return [dist / total_dist for dist in distances]
