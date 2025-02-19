import json

class NodeParameterType:
    """Enum-like class for node parameter types."""
    string = "string"
    number = "number"
    boolean = "boolean"
    none = "none"

class NodeType:
    """Enum-like class for node types."""
    basicNode = "basicNode"
    outputNode = "outputNode"

class HardSetOptionsType:
    """Enum-like class for hard set options types."""
    selectableList = "selectableList"
    directInput = "directInput"

class ExecutionState:
    """Enum-like class for execution states."""
    pending = "pending"
    executing = "executing"
    finished = "finished"

class ExecutionResult:
    """Enum-like class for execution results."""
    success = "success"
    failure = "failure"
    unknown = "unknown"

class NodeFunctionReturnType:
    """Enum-like class for node function return types."""
    string = "string"
    number = "number"
    boolean = "boolean"
    none = "none"

class DeviceInfo:
    """
    Represents device information.

    Attributes:
        dev_info_message (str): The device information message in JSON format.
        _dev_info (dict): The parsed device information.
        _device_unique_id (str): The unique ID of the device.
        _device_name (str): The name of the device.
        _device_description (str): The description of the device.
        _device_available_nodes (AvailableNodes): The available nodes of the device.
        _device_icon_svg (str): The SVG icon of the device.
    """

    def __init__(self, dev_info_message):
        """
        Initializes a DeviceInfo instance.

        Args:
            dev_info_message (str): The device information message in JSON format.
        """
        self._dev_info = json.loads(dev_info_message)
        self._device_unique_id = self._dev_info["UNIQUE_ID"]
        self._device_name = self._dev_info["DEVICE_NAME"]
        self._device_description = self._dev_info["DEVICE_DESCRIPTION"]
        self._device_available_nodes = AvailableNodes.from_json(self._dev_info["DEVICE_AVAILABLE_NODES"])
        self._device_icon_svg = self._dev_info["DEVICE_ICON_SVG"]

    @property
    def device_unique_id(self):
        """str: The unique ID of the device."""
        return self._device_unique_id

    @property
    def device_name(self):
        """str: The name of the device."""
        return self._device_name

    @property
    def device_description(self):
        """str: The description of the device."""
        return self._device_description

    @property
    def device_available_nodes(self):
        """AvailableNodes: The available nodes of the device."""
        return self._device_available_nodes

    @property
    def device_icon_svg(self):
        """str: The SVG icon of the device."""
        return self._device_icon_svg

    @staticmethod
    def from_json(data):
        """
        Creates a DeviceInfo instance from JSON data.

        Args:
            data (dict): The JSON data.

        Returns:
            DeviceInfo: The created DeviceInfo instance.
        """
        return DeviceInfo(json.dumps(data))

    def to_json(self):
        """
        Converts the DeviceInfo instance to JSON.

        Returns:
            dict: The JSON representation of the DeviceInfo instance.
        """
        return {
            "UNIQUE_ID": self._device_unique_id,
            "DEVICE_NAME": self._device_name,
            "DEVICE_DESCRIPTION": self._device_description,
            "DEVICE_AVAILABLE_NODES": self._device_available_nodes.to_json(),
            "DEVICE_ICON_SVG": self._device_icon_svg
        }

class NodeParameter:
    """
    Represents a parameter for a node function.

    Attributes:
        name (str): The name of the parameter.
        type (NodeParameterType): The type of the parameter.
        hard_set (bool): Whether the parameter is hard set.
        hard_set_options_type (HardSetOptionsType): The type of hard set options.
        hard_set_options (list): The list of hard set options.
        value (any): The value of the parameter.
    """

    def __init__(self, name, type, hard_set=False, hard_set_options_type=HardSetOptionsType.directInput, hard_set_options=None, value=None):
        """
        Initializes a NodeParameter instance.

        Args:
            name (str): The name of the parameter.
            type (NodeParameterType): The type of the parameter.
            hard_set (bool, optional): Whether the parameter is hard set. Defaults to False.
            hard_set_options_type (HardSetOptionsType, optional): The type of hard set options. Defaults to HardSetOptionsType.DIRECT_INPUT.
            hard_set_options (list, optional): The list of hard set options. Defaults to None.
            value (any, optional): The value of the parameter. Defaults to None.
        """
        self.name = name
        self.type = type
        self.hard_set = hard_set
        self.hard_set_options_type = hard_set_options_type
        self.hard_set_options = hard_set_options if hard_set_options is not None else []
        self.value = value

    @staticmethod
    def from_json(data):
        """
        Creates a NodeParameter instance from JSON data.

        Args:
            data (dict): The JSON data.

        Returns:
            NodeParameter: The created NodeParameter instance.
        """
        return NodeParameter(
            name=data['Name'],
            type=data['Type'],
            hard_set=data.get('HardSet', False),
            hard_set_options_type=data['HardSetOptionsType'],
            hard_set_options=data.get('HardSetOptions', []),
            value=data['Value']
        )

    def to_json(self):
        """
        Converts the NodeParameter instance to JSON.

        Returns:
            dict: The JSON representation of the NodeParameter instance.
        """
        return {
            'Name': self.name,
            'Type': self.type,
            'HardSet': self.hard_set,
            'HardSetOptionsType': self.hard_set_options_type,
            'HardSetOptions': self.hard_set_options,
            'Value': self.value
        }

class NodeFunction:
    """
    Represents a function associated with a node.

    Attributes:
        command (str): The command of the function.
        return_type (NodeFunctionReturnType): The return type of the function.
        return_name (str): The return name of the function.
        parameters (list): The list of parameters for the function.
        execution_result (ExecutionResult): The execution result of the function.
        execution_state (ExecutionState): The execution state of the function.
    """

    def __init__(self, command, return_type, return_name="return", parameters=None, execution_result=ExecutionResult.unknown, execution_state=ExecutionState.pending):
        """
        Initializes a NodeFunction instance.

        Args:
            command (str): The command of the function.
            return_type (NodeFunctionReturnType): The return type of the function.
            return_name (str, optional): The return name of the function. Defaults to "return".
            parameters (list, optional): The list of parameters for the function. Defaults to None.
            execution_result (ExecutionResult, optional): The execution result of the function. Defaults to ExecutionResult.UNKNOWN.
            execution_state (ExecutionState, optional): The execution state of the function. Defaults to ExecutionState.PENDING.
        """
        self.command = command
        self.return_type = return_type
        self.return_name = return_name
        self.parameters = parameters if parameters is not None else []
        self.execution_result = execution_result
        self.execution_state = execution_state

    @staticmethod
    def from_json(data):
        """
        Creates a NodeFunction instance from JSON data.

        Args:
            data (dict): The JSON data.

        Returns:
            NodeFunction: The created NodeFunction instance.
        """
        param_list = data.get('Parameters', [])
        return NodeFunction(
            command=data['Command'],
            return_type=data['ReturnType'],
            return_name=data['ReturnName'],
            parameters=[NodeParameter.from_json(p) for p in param_list],
            execution_result=data['ExecutionResult'],
            execution_state=data['ExecutionState']
        )

    def to_json(self):
        """
        Converts the NodeFunction instance to JSON.

        Returns:
            dict: The JSON representation of the NodeFunction instance.
        """
        return {
            'Command': self.command,
            'ReturnType': self.return_type,
            'ReturnName': self.return_name,
            'Parameters': [p.to_json() for p in self.parameters],
            'ExecutionResult': self.execution_result,
            'ExecutionState': self.execution_state
        }

class Node:
    """
    Represents a node with a function.

    Attributes:
        name (str): The name of the node.
        type (NodeType): The type of the node.
        color (str): The color of the node.
        svg_icon (str): The SVG icon of the node.
        function (NodeFunction): The function associated with the node.
    """

    def __init__(self, name, type, color, svg_icon, function=None):
        """
        Initializes a Node instance.

        Args:
            name (str): The name of the node.
            type (NodeType): The type of the node.
            color (str): The color of the node.
            svg_icon (str): The SVG icon of the node.
            function (NodeFunction, optional): The function associated with the node. Defaults to None.
        """
        self.name = name
        self.type = type
        self.color = color
        self.svg_icon = svg_icon
        self.function = function

    @staticmethod
    def from_json(data):
        """
        Creates a Node instance from JSON data.

        Args:
            data (dict): The JSON data.

        Returns:
            Node: The created Node instance.
        """
        return Node(
            name=data['Name'],
            type=data['Type'],
            color=data['Color'],
            svg_icon=data['SvgIcon'],
            function=NodeFunction.from_json(data['Function']) if data.get('Function') else None
        )

    def to_json(self):
        """
        Converts the Node instance to JSON.

        Returns:
            dict: The JSON representation of the Node instance.
        """
        return {
            'Name': self.name,
            'Type': self.type,
            'Color': self.color,
            'SvgIcon': self.svg_icon,
            'Function': self.function.to_json() if self.function else None
        }

class AvailableNodes:
    """
    Manages a collection of nodes.

    Attributes:
        nodes (list): The list of nodes.
    """

    def __init__(self, nodes=None):
        """
        Initializes an AvailableNodes instance.

        Args:
            nodes (list, optional): The list of nodes. Defaults to None.
        """
        self.nodes = nodes if nodes is not None else []

    @staticmethod
    def from_json(data):
        """
        Creates an AvailableNodes instance from JSON data.

        Args:
            data (list): The JSON data.

        Returns:
            AvailableNodes: The created AvailableNodes instance.
        """
        return AvailableNodes(nodes=[Node.from_json(n) for n in data])

    def to_json(self):
        """
        Converts the AvailableNodes instance to JSON.

        Returns:
            list: The JSON representation of the AvailableNodes instance.
        """
        return [n.to_json() for n in self.nodes]