#!/usr/bin/env python
import rospy
import py_trees_ros
import py_trees
import std_msgs
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def crear_arbol():
    nodo_recoger_datos = py_trees.composites.Sequence("Recoger Datos")
    topic_abortar_a_bb = py_trees_ros.subscribers.ToBlackboard(
        name="/abort_mission -> bb",
        topic_name="/abort_mission",
        topic_type=std_msgs.msg.Bool,
        blackboard_variables = {'abort': None}
    )
    nodo_recoger_datos.add_child(topic_abortar_a_bb)
    nodo_abortar_mision = py_trees.composites.Selector("Abortar Mision")
    nodo_sigue_mision = py_trees.blackboard.CheckBlackboardVariable(
        name="Sigue la mision?",
        variable_name="abort",
        expected_value=False
    )
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 2.0
    goal.target_pose.pose.position.y = 2.0
    goal.target_pose.pose.orientation.w = 1.0
    nodo_home = py_trees_ros.actions.ActionClient(
        name="Ir a la base",
        action_namespace="/move_base",
        action_spec=MoveBaseAction,
        action_goal=goal
    )
    nodo_abortar_mision.add_child(nodo_sigue_mision)
    nodo_abortar_mision.add_child(nodo_home)
    raiz = py_trees.composites.Sequence("Arbol")
    raiz.add_child(nodo_recoger_datos)
    raiz.add_child(nodo_abortar_mision)

    arbol = py_trees_ros.trees.BehaviourTree(raiz)
    arbol.setup(5000)
    return arbol

def main():
    rospy.init_node("arbol_simple")
    arbol = crear_arbol()
    rospy.on_shutdown = arbol.interrupt
    arbol.tick_tock(500)


if __name__ == "__main__":
    main()
