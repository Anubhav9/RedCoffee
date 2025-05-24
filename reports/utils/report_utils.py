def draw_severity_icon(severity):
    """
    Visually generates a circular icon based on severity of the bug.
    Critical -> Red Color
    High -> Orange
    Medium -> Teal
    Low / Default -> Green

    Arguments
    severity : The importance of the bug detected by SonarQube
    """
    if severity == "CRITICAL":
        return "<font color='red' size='12'>&#9679;</font>"
    elif severity == "HIGH":
        return "<font color='orange' size='12'>&#9679;</font>"
    elif severity == "MEDIUM":
        return "<font color='teal' size='12'>&#9679;</font>"
    else:  # Low
        return "<font color='green' size='12'>&#9679;</font>"
