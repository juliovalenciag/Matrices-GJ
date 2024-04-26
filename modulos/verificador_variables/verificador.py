def verificador_de_variables(soluciones: list[list[str]]) -> tuple[list[str], list[str]]:
    variables_infinitas : list[str] = []
    variables : list[str] = []
    for solucion in soluciones:
        for i,valor in enumerate(solucion):
            if not valor in variables:
                variables.append(valor)
                
            if i == 0:
                continue
            else:
                if valor in variables_infinitas:
                    continue
                else:
                    variables_infinitas.append(valor)
            
    print(variables_infinitas)
    return variables_infinitas, variables