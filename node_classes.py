"""
This module defines classes that represent nodes, functions, and parameters for a system of available nodes.

Classes:
- Parameter: Represents a parameter for a function, including its name and type.
- Function: Represents a function associated with a node, including the command, return type, return name, and parameters.
- Node: Represents a node that can contain a function, including its name, type, color, SVG icon, and an optional function.
- AvailableNodes: Manages a collection of nodes, allowing for adding, setting, and retrieving nodes, as well as converting the node collection to a dictionary.

Usage:
- Define individual nodes with functions and parameters.
- Add nodes to an AvailableNodes instance to manage and convert the entire set to a dictionary representation.

The code supports conversion of each of the classes to dictionary format, allowing for easier serialization or further processing.
"""


class Parameter:
    """
    A class representing a parameter for a function.

    Attributes:
    Name (str): The name of the parameter.
    Type (str): The type of the parameter (e.g., 'int', 'string').
    """
    def __init__(self, name, param_type):
        """
        Initializes a Parameter instance with a name and type.

        Args:
        name (str): The name of the parameter.
        param_type (str): The type of the parameter.
        """
        self.Name = name
        self.Type = param_type
    
    def to_dict(self):
        """
        Converts the Parameter instance to a dictionary.

        Returns:
        dict: A dictionary representation of the Parameter instance.
        """
        return {
            "Name": self.Name,
            "Type": self.Type
        }

class Function:
    """
    A class representing a function associated with a node.

    Attributes:
    Command (str): The command or action that the function represents.
    ReturnType (str or None): The type of the value that the function returns (optional).
    ReturnName (str): The name of the value that the function returns.
    Parameters (list of Parameter): A list of Parameter instances for the function (optional).
    """
    def __init__(self, command, return_type=None, return_name=None, parameters=None):
        """
        Initializes a Function instance with command, optional return type, optional return name, 
        and optional parameters.

        Args:
        command (str): The command or action of the function.
        return_type (str, optional): The return type of the function (default is None).
        return_name (str, optional): The return name of the function (default is None).
        parameters (list of dict, optional): A list of dictionaries representing function parameters 
                                              (default is an empty list if not provided).
        """
        self.Command = command
        self.ReturnType = return_type
        self.ReturnName = return_name
        # Default parameters to an empty list if not provided
        self.Parameters = parameters if parameters else []

    
    def to_dict(self):
        """
        Converts the Function instance to a dictionary.

        Returns:
        dict: A dictionary representation of the Function instance.
        """
        return {
            "Command": self.Command,
            "ReturnType": self.ReturnType,
            "ReturnName": self.ReturnName,
            "Parameters": [param.to_dict() for param in self.Parameters]
        }

class Node:
    """
    A class representing a node with a function.

    Attributes:
    Name (str): The name of the node.
    Type (str): The type of the node (e.g., 'device', 'action').
    Color (str): The color of the node.
    SvgIcon (str): The SVG icon representing the node.
    Function (Function): The function associated with the node, if any.
    """
    def __init__(self, name, node_type, color, svg_icon, function):
        """
        Initializes a Node instance with its attributes and an optional function.

        Args:
        name (str): The name of the node.
        node_type (str): The type of the node.
        color (str): The color of the node.
        svg_icon (str): The SVG icon representing the node.
        function (dict, optional): A dictionary representing the function associated with the node.
        """
        self.Name = name
        self.Type = node_type
        self.Color = color
        self.SvgIcon = svg_icon  # Assuming the SVG icon is passed as a string.
        self.Function = function if function else None

    def to_dict(self):
        """
        Converts the Node instance to a dictionary.

        Returns:
        dict: A dictionary representation of the Node instance.
        """
        node_dict = {
            "Name": self.Name,
            "Type": self.Type,
            "Color": self.Color,
            "SvgIcon": self.SvgIcon,
        }
        if self.Function:
            node_dict["Function"] = self.Function.to_dict()
        return node_dict

class AvailableNodes:
    """
    A class representing a collection of available nodes.

    Attributes:
    _nodes (list of Node): A list of Node instances that are available.
    """
    def __init__(self):
        """
        Initializes an empty list of nodes.
        """
        self._nodes = []

    @property
    def nodes(self):
        """
        Returns the list of nodes.

        Returns:
        list of Node: The list of nodes.
        """
        return self._nodes

    @nodes.setter
    def nodes(self, new_nodes):
        """
        Sets the list of nodes, ensuring all elements are of type Node.

        Args:
        new_nodes (list of Node): A list of Node instances to set.

        Raises:
        TypeError: If the input is not a list, or if not all elements are of type Node.
        """
        if not isinstance(new_nodes, list):
            raise TypeError("Must be a list")
        if not all(isinstance(node, Node) for node in new_nodes):
            raise TypeError("All elements must be of type Node")
        self._nodes = new_nodes

    def add_node(self, node):
        """
        Adds a Node instance to the list of available nodes.

        Args:
        node (Node): The Node instance to add.

        Raises:
        TypeError: If the input is not a Node instance.
        """
        if not isinstance(node, Node):
            raise TypeError("Only instances of Node can be added")
        self._nodes.append(node)

    def to_dict(self):
        """
        Converts the AvailableNodes instance to a dictionary.

        Returns:
        list of dict: A list of dictionary representations of the Node instances.
        """
        return [node.to_dict() for node in self._nodes]
