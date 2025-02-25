def parse_opencore_features(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
        # Unique inputs (bus widths, handle symbolic)
        inputs = set()
        for line in code.split('\n'):
            if 'input' in line and '[' in line:
                try:
                    range_str = line.split('[')[1].split(']')[0]
                    if ':' in range_str:
                        start, end = map(int, range_str.split(':'))
                        width = abs(start - end) + 1
                        inputs.add(width)
                    else:
                        inputs.add(1)
                except (ValueError, IndexError):
                    inputs.add(4)
        fan_in = sum(inputs) if inputs else max(code.count('['), 2)

        # Gate counts (only in assign statements, now including comparisons and ternaries)
        assign_code = ''.join(line for line in code.split('\n') if 'assign' in line)
        and_count = assign_code.count('&')
        or_count = assign_code.count('|')
        xor_count = assign_code.count('^')
        not_count = assign_code.count('~')
        shift_count = assign_code.count('<<') + assign_code.count('>>') + assign_code.count('<<<') + assign_code.count(
            '>>>')
        comp_count = assign_code.count('>') + assign_code.count('<') + assign_code.count('==')  # Comparisons
        ternary_count = assign_code.count('?')  # Ternaries
        total_gates = and_count + or_count + xor_count + not_count + shift_count + comp_count + ternary_count
        gate_mix = (and_count + or_count) / total_gates if total_gates > 0 else 1.0
        op_count = total_gates

        # Nesting (only in assign)
        nest_depth = assign_code.count('(') - assign_code.count(')')  # Balanced nesting
        if nest_depth < 0: nest_depth = 0  # Safety

        # Dependency chain (wires beyond outputs)
        dep_chain = code.count('wire') - 1 if code.count('wire') > 0 else 0

        # Register proximity (assume inputs from flops unless clear otherwise)
        reg_prox = 1 if "always @" in code else 1  # Keep 1 for consistency

    return [fan_in, op_count, nest_depth, dep_chain, gate_mix, reg_prox]
file_path = "verilog file on local system.v"  # Save your code as this file
features = parse_opencore_features(file_path)
print("Extracted Features:", features)