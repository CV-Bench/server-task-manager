import json


def get_state_array(current_state, content, step):
    if step == 0:
        current_state = [content] * 3

    elif step == 1:
        current_state[2] = content

    else:
        current_state[1] = current_state[2]
        current_state[2] = content

    return current_state


def extract_infos_from_train_states(states):
    new_states = [{
        "iter": 0, 
        "lr": 0, 
        "memory": 0, 
        "data_time": 0, 
        "loss_rpn_cls": 0, 
        "loss_rpn_bbox": 0, 
        "loss_cls": 0, 
        "acc": 0, 
        "loss_bbox": 0, 
        "loss": 0, 
        "time": 0
    }] * 3
    
    for index, state in enumerate(states):
        new_states[index] = {
            "iter": state["iter"], 
            "lr": state["lr"], 
            "memory": state["memory"], 
            "data_time": state["data_time"], 
            "loss_rpn_cls": state["loss_rpn_cls"], 
            "loss_rpn_bbox": state["loss_rpn_bbox"], 
            "loss_cls": state["loss_cls"], 
            "acc": state["acc"], 
            "loss_bbox": state["loss_bbox"], 
            "loss": state["loss"], 
            "time": state["time"]
        }

    return new_states


def extract_infos_from_val_states(states):
    new_states = [{
        "iter": 0, 
        "lr": 0, 
        "bbox_mAP": 0, 
        "bbox_mAP_50": 0, 
        "bbox_mAP_75": 0, 
        "bbox_mAP_s": 0, 
        "bbox_mAP_m": 0, 
        "bbox_mAP_l": 0
    }] * 3
    
    for index, state in enumerate(states):
        new_states[index] = {
            "iter": state["iter"], 
            "lr": state["lr"], 
            "bbox_mAP": state["bbox_mAP"], 
            "bbox_mAP_50": state["bbox_mAP_50"], 
            "bbox_mAP_75": state["bbox_mAP_75"], 
            "bbox_mAP_s": state["bbox_mAP_s"], 
            "bbox_mAP_m": state["bbox_mAP_m"], 
            "bbox_mAP_l": state["bbox_mAP_l"]
        }

    return new_states


def get_train_stats(path):
    """prints the first, last and current mAP of a log file

    Args:
        path (str): the path to the log file

    Returns:
        tuple: (first mAP, last mAP, current mAP) as floats. If the log file is empty, all values are 0. If the log file contains only one line, all values are the last value, if the log file contains only two lines, the first and last value are the same, and the current value is the second value.
    """

    # first line contains the header
    # last line is empty
    with open(path, "r") as file:
        ## Get First Training and Val Data
        lines = file.readlines()

        # print(lines)

        train_steps = []
        val_steps = []

        train_log_step = 0
        val_log_step = 0

        current_epoch = 0

        # Find first Training and Val
        for line in lines[1:]:
            content = json.loads(line)
            
            if content["mode"] == "train":
                train_steps = get_state_array(train_steps, content, train_log_step)
                train_log_step += 1

            if content["mode"] == "val":
                val_steps = get_state_array(val_steps, content, val_log_step)
                val_log_step += 1

            current_epoch = content["epoch"]

        return {
            "train": extract_infos_from_train_states(train_steps), 
            "val": extract_infos_from_val_states(val_steps),
            "current_epoch": current_epoch
        }