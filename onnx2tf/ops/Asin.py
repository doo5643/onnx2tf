import random
random.seed(0)
import numpy as np
np.random.seed(0)
import tensorflow as tf
import onnx_graphsurgeon as gs
from utils.common_functions import alternative_asin


def make_node(
    *,
    graph_node: gs.Node,
    tf_layers_dict: dict,
    **kwargs: dict,
):
    """Asin

    Parameters
    ----------
    graph_node: gs.Node
        graph_surgeon Node

    tf_layers_dict: dict
        optype, shape, dtype, tensorflow graph
    """
    graph_node_input: gs.Variable = graph_node.inputs[0]
    graph_node_output: gs.Variable = graph_node.outputs[0]
    shape = graph_node_output.shape
    dtype = graph_node_output.dtype

    replace_Asin_to_pseudo_Asin = kwargs['replace_Asin_to_pseudo_Asin']

    # Preserving Graph Structure (Dict)
    tf_layers_dict[graph_node_output.name] = {
        'optype': graph_node.op,
        'shape': shape,
        'dtype': dtype,
    }

    # Generation of TF OP
    if not replace_Asin_to_pseudo_Asin:
        tf_layers_dict[graph_node_output.name]['tf_node'] = \
            tf.math.asin(
                x=tf_layers_dict[graph_node_input.name]['tf_node'],
                name=graph_node.name,
            )
    else:
        tf_layers_dict[graph_node_output.name]['tf_node'] = \
            alternative_asin(
                input_tensor=tf_layers_dict[graph_node_input.name]['tf_node']
            )