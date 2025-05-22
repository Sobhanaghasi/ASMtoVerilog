from typing import List, Dict, Optional, Union, Tuple
import xml.etree.ElementTree as ET

class ASMChart:
    def __init__(self, name: str, variables: Dict[str, 'Variable'], nodes: Dict[str, 'Node'], start_id: int):
        self.name: str = name
        self.variables: Dict[str, 'Variable'] = variables
        self.nodes: Dict[str, 'Node'] = nodes
        self.start_id: int = start_id

class Variable:
    def __init__(self, name: str, size: int, is_input: bool = False, is_output: bool = False):
        self.name: str = name
        self.size: int = size
        self.is_input: bool = is_input
        self.is_output: bool = is_output

class Node:
    def __init__(self, node_id: int, name: str):
        self.id: int = node_id
        self.name: str = name


class StateBox(Node):
    def __init__(self, node_id: str, name: str, statements: List[str], destination: Optional[int]):
        super().__init__(node_id, name)
        self.statements: List[str] = statements
        self.destination: Optional[int] = destination


class DecisionBox(Node):
    def __init__(self, node_id: str, condition: str, true_destination: int, false_destination: int):
        # Note: name is optional/not specified for DecisionBox in example, so store id as name
        super().__init__(node_id, node_id)
        self.condition: str = condition
        self.true_destination: int = true_destination
        self.false_destination: int = false_destination


class ConditionBox(Node):
    def __init__(self, node_id: str, name: str, statements: List[str], destination: Optional[int]):
        super().__init__(node_id, name)
        self.statements: List[str] = statements
        self.destination: Optional[int] = destination
        

# === Function to parse ASM chart XML ===
def parse_asm_chart(xml_string: str) -> Tuple[str, Dict[str, Variable], Dict[str, Node]]:
    root = ET.fromstring(xml_string) 
    name = root.attrib.get("name", "ASM_Chart")

    variables: Dict[str, Variable] = {}
    nodes: Dict[str, Node] = {}

    # Parse Variables
    vars_tag = root.find("Variables")
    if vars_tag is not None:
        for var_el in vars_tag.findall("Variable"):
            name = var_el.attrib.get("name")
            size = int(var_el.attrib.get("size"))
            var_type = var_el.attrib.get("type", "").lower()
            is_input = var_type == "input"
            is_output = var_type == "output"
            variables[name] = Variable(name, size, is_input, is_output)

    # Parse StateBoxes
    state_boxes_tag = root.find("StateBoxes")
    if state_boxes_tag is not None:
        for sb_el in state_boxes_tag.findall("StateBox"):
            node_id = int(sb_el.attrib["id"])
            name_el = sb_el.find("Name")
            name = name_el.text.strip() if name_el is not None else node_id

            statements = []
            stmts_el = sb_el.find("Statements")
            if stmts_el is not None:
                for stmt_el in stmts_el.findall("Statement"):
                    if stmt_el.text:
                        statements.append(stmt_el.text.strip())

            dest_el = sb_el.find("Destination")
            destination = int(dest_el.text.strip()) if dest_el is not None else None

            nodes[node_id] = StateBox(node_id, name, statements, destination)

    # Parse DecisionBoxes
    decision_boxes_tag = root.find("DecisionBoxes")
    if decision_boxes_tag is not None:
        for db_el in decision_boxes_tag.findall("DecisionBox"):
            node_id = int(db_el.attrib["id"])
            cond_el = db_el.find("Condition")
            condition = cond_el.text.strip() if cond_el is not None else ""

            true_dest_el = db_el.find("TrueDestination")
            false_dest_el = db_el.find("FalseDestination")
            true_destination = int(true_dest_el.text.strip()) if true_dest_el is not None else None
            false_destination = int(false_dest_el.text.strip()) if false_dest_el is not None else None

            if true_destination is None or false_destination is None:
                raise ValueError(f"DecisionBox {node_id} missing TrueDestination or FalseDestination")

            nodes[node_id] = DecisionBox(node_id, condition, true_destination, false_destination)

    # Parse ConditionBoxes
    condition_boxes_tag = root.find("ConditionBoxes")
    if condition_boxes_tag is not None:
        for cb_el in condition_boxes_tag.findall("ConditionBox"):
            node_id = int(cb_el.attrib["id"])
            name_el = cb_el.find("Name")
            name = name_el.text.strip() if name_el is not None else node_id

            statements = []
            stmts_el = cb_el.find("Statements")
            if stmts_el is not None:
                for stmt_el in stmts_el.findall("Statement"):
                    if stmt_el.text:
                        statements.append(stmt_el.text.strip())

            dest_el = cb_el.find("Destination")
            destination = int(dest_el.text.strip()) if dest_el is not None else None

            nodes[node_id] = ConditionBox(node_id, name, statements, destination)
    
    start_id = root.find("StartState")
    if start_id is not None:
        start_id = int(start_id.text.strip())
    else:
        raise ValueError("StartState not found in XML")

    return ASMChart(name, variables, nodes, start_id)