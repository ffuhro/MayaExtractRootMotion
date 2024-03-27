# v 1.0 
#
#


import maya.cmds as cmds

def create_joint():
    # Get selected bone
    selected_bones = cmds.ls(selection=True, type='joint')
    if not selected_bones:
        cmds.warning("No joint selected. Please select a joint.")
        return
    elif len(selected_bones) > 1:
        cmds.warning("More than one joint selected. Please select only one joint.")
        return
    selected_bone = selected_bones[0]

    # Deselect all items
    cmds.select(clear=True)

    # Create a new joint named 'root'
    new_joint = cmds.joint(name='root')

    # Constrain the new joint to the selected joint, limiting to X and Z translate channels
    point_constraint = cmds.pointConstraint(selected_bone, new_joint, maintainOffset=True)
    cmds.setAttr(point_constraint[0] + '.offsetX', lock=True)
    cmds.setAttr(point_constraint[0] + '.offsetZ', lock=True)

    print("New joint 'root' created and constrained to '{}' on X and Z translate channels.".format(selected_bone))

    # Add orient constraint from selected bone to new joint
    # orient_constraint = cmds.orientConstraint(selected_bone, new_joint, maintainOffset=True)
    # Bake rotation attributes
    # cmds.bakeResults(new_joint, attribute=['rx', 'ry', 'rz'], simulation=True, time=(cmds.playbackOptions(minTime=True, query=True), cmds.playbackOptions(maxTime=True, query=True)))
    # cmds.delete(orient_constraint)
    # cmds.cutKey(selected_bone, attribute='rx', clear=True)
    # cmds.cutKey(selected_bone, attribute='ry', clear=True)
    # cmds.cutKey(selected_bone, attribute='rz', clear=True)
    # print("Rotation channels removed from selected bone '{}'.".format(selected_bone))

    # Bake translateX and translateZ attributes

    cmds.bakeResults(new_joint, attribute=['tx', 'tz'], simulation=True, time=(cmds.playbackOptions(minTime=True, query=True), cmds.playbackOptions(maxTime=True, query=True)))

    cmds.delete(point_constraint)

    cmds.cutKey(selected_bone, attribute='tx', clear=True)
    cmds.cutKey(selected_bone, attribute='tz', clear=True)

    print("Translate X and Z channels removed from selected bone '{}'.".format(selected_bone))

    cmds.parent(selected_bone, new_joint)

    # Confirm reparenting
    print("Selected bone '{}' reparented under 'root' joint.".format(selected_bone))


# Run the function
create_joint()
