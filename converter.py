from asm_xml_parser import ConditionBox, DecisionBox, StateBox, parse_asm_chart

class CodeBlock():
    def __init__(self):
        self.code = ""
        
    def get_code(self):
        return self.code[:-1] if self.code and self.code[-1] == "\n" else self.code
    
    def add_code(self, new_code, tabs = 0):
        self.code = self.code + "\n".join(["    " * tabs + line for line in new_code.split("\n")]) + "\n"
        
    def empty_line(self):
        self.code += "\n"

def get_variables_block(variables):
    variables_block = CodeBlock()
    
    # Add module variables
    for variable in variables.values():
        type_block = "input reg" if variable.is_input else "output reg" if variable.is_output else "reg"
        if variable.size > 1:
            variables_block.add_code(f"{type_block} [{variable.size - 1}:0] {variable.name};")
        else:
            variables_block.add_code(f"{type_block} {variable.name};")
    
    # Add clock and state variables
    variables_block.add_code("reg clk;")
    variables_block.add_code("integer state;")
    
    return variables_block.get_code()

def get_decision_block(decision, all_nodes):
    decision_block = CodeBlock()
    
    # Add condition
    decision_block.add_code(f"if ({decision.condition}) begin")
    
    # Add true destination
    true_destination_node = all_nodes.get(decision.true_destination)
    decision_block.add_code(get_next_node_block(true_destination_node, all_nodes), 1)
    
    # Add else statement
    decision_block.add_code("end else begin")
    
    # Add false destination   
    false_destination_node = all_nodes.get(decision.false_destination)
    decision_block.add_code(get_next_node_block(false_destination_node, all_nodes), 1)
    
    # End block
    decision_block.add_code("end", 0)
    
    return decision_block.get_code()

def get_state_block(state, all_nodes):
    state_block = CodeBlock()
    
    # Add state name
    state_block.add_code(f"{state.id}: begin")
    
    # Add state statements
    for statement in state.statements:
        state_block.add_code(statement, 1)
    
    # Add destination node
    destination_node = all_nodes.get(state.destination)
    state_block.add_code(get_next_node_block(destination_node, all_nodes), 1)

    # End block
    state_block.add_code("end", 0)
    
    return state_block.get_code()

def get_condition_block(condition, all_nodes):
    condition_block = CodeBlock()
    
    # Add statements
    for statement in condition.statements:
        condition_block.add_code(statement, 1)
    
    # Add destination node
    destination_node = all_nodes.get(condition.destination)
    condition_block.add_code(get_next_node_block(destination_node, all_nodes), 1)
        
    return condition_block.get_code()

def get_next_node_block(node, all_nodes):
    node_block = CodeBlock()
    
    # Generate code based on node type
    if isinstance(node, StateBox):
        node_block.add_code(f"state <= {node.id};")
    elif isinstance(node, ConditionBox):
        node_block.add_code(get_condition_block(node, all_nodes))
    elif isinstance(node, DecisionBox):
        node_block.add_code(get_decision_block(node, all_nodes))
        
    return node_block.get_code()
    

def get_verilog(asm_chart):
    main_block = CodeBlock()
    current_tab = 0
    
    # Extract ASM chart details
    name = asm_chart.name
    all_variables = asm_chart.variables
    all_nodes = asm_chart.nodes
    start_id = asm_chart.start_id
    
    # Add module declaration
    main_block.add_code(f"module {name} (" + ", ".join([f"{var.name}" for var in all_variables.values() if var.is_input or var.is_output]) + ");")
    current_tab += 1
    
    # Add reg declarations
    main_block.add_code(get_variables_block(all_variables), current_tab)
    main_block.empty_line()
    
    # Add initial block
    main_block.add_code("initial begin", current_tab)
    main_block.add_code("clk = 0;", current_tab + 1)
    main_block.add_code(f"state = {start_id};", current_tab + 1)
    main_block.add_code("end", current_tab)
    main_block.empty_line()
    
    # Add always block for clock generation
    main_block.add_code("always begin", current_tab)
    main_block.add_code("clk = ~clk;", current_tab + 1)
    main_block.add_code("#5;", current_tab + 1)
    main_block.add_code("end", current_tab)
    main_block.empty_line()
    
    # Add always block for state machine
    main_block.add_code("always @(posedge clk) begin", current_tab)
    current_tab += 1
    main_block.add_code("case (state)", current_tab)
    main_block.empty_line()
    current_tab += 1
    
    # Add state cases
    for node in all_nodes.values():
        if isinstance(node, StateBox):
            main_block.add_code(get_state_block(node, all_nodes), current_tab)
            main_block.empty_line()
    current_tab -= 1
    main_block.add_code("endcase", current_tab)
    
    # End always block
    current_tab -= 1
    main_block.add_code("end", current_tab)
    main_block.empty_line()
    
    # End module
    current_tab -= 1
    main_block.add_code("endmodule")
    
    return main_block.get_code()

def main():
    while True:
        file_path = input("Enter the path to the ASM chart XML file: ").strip()
            
        try:
            with open(file_path, "r") as file:
                asm_xml_str = file.read()
            break
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found. Please check the path and try again.")

    asm_chart = parse_asm_chart(asm_xml_str)
    with open("asm.v", "w") as file:
        file.write(get_verilog(asm_chart))
        
if __name__ == "__main__":
    main()