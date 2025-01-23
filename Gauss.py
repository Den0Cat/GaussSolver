def parse_linear(linear: str) -> list[dict]:
    variables = list(set(map(lambda symbol: symbol if symbol.isalpha() else '', linear)))
    variables += ['=']
    if '' in variables: variables.remove('')
    linear = linear.split('\n')
    variables_book = [{var:0 for var in variables} for i in range(len(linear))]
    for ind in range(len(linear)):
        linear[ind] = ''.join(linear[ind].split())
        linear[ind] = linear[ind].replace("*","")
        for k in range(len(linear[ind])):
            symbol = linear[ind][k]
            if not symbol.isdigit() and symbol not in "+-" and (k==0 or linear[ind][k-1] in "+-"):
                linear[ind] = linear[ind].replace(symbol, '1'+symbol, 1)
        linear[ind] = linear[ind].replace("-","+-").replace("=+-","=-")
        if linear[ind][0] == "+": linear[ind] = linear[ind].replace("+","",1)
        divide = linear[ind].split('=')
        variables_book[ind]['='] = int(divide[1])
        equation = divide[0]
        for element in equation.split('+'):
            variables_book[ind][element[-1]] = int(element[:-1])
    return [variables, variables_book]


def linear_to_matrix(variables: list[str], variables_book: list[dict]) -> list[list[int]]:
    matrix = [[0 for _ in range(len(variables))] for _ in range(len(variables_book))]
    for line in range(len(variables_book)):
        for element in range(len(variables)):
            matrix[line][element] = variables_book[line][variables[element]]
    return matrix


def print_matrix(variables: list[str], matrix: list[list[int]]) -> None:
    print(*variables, sep='\t')
    for i in range(len(matrix)):
        print(*matrix[i], sep='\t')
    return None


def gauss_elimination(matrix: list[list[int]]) -> list[list[int]]:
    for j in range(len(matrix[0])):
        if len(matrix)-1 < j:
            break
        source = matrix[j][j]
        src_i = j
        src_j = j
        for i in range(len(matrix)):
            if i!=j and source!=0:
                element = matrix[i][j]
                k = -element/source
                for j1 in range(j,len(matrix[0])):
                    matrix[i][j1] += matrix[src_i][j1]*k
    for line in range(len(matrix)-1, -1, -1):
        check = correct_check(matrix[line][:-1], matrix[line][-1])
        if check == "REDUNDANT LINE":
            matrix.pop(line)
    return matrix


def correct_check(line: list[int], answer: int) -> str:
    zeros = 0
    for item in line:
        if item == 0: zeros += 1
    if zeros == len(line)-1: return "OK"
    else: 
        if zeros == len(line) and answer != 0: return "NO SOLUTION"
        if zeros == len(line) and answer == 0: return "REDUNDANT LINE"
        if zeros <= len(line)-2: return "TWO OR MORE VARIABLES"


def last_check(matrix_gauss: list[list[int]], variables: list[str], ans_dict: dict[str:float]) -> bool:
    eps = 0.01
    for line in range(len(matrix_gauss)):
        ans = matrix_gauss[line][-1]
        sum_vars = 0
        for item in range(len(matrix_gauss[0])-1):
            sum_vars += ans_dict[variables[item]]*matrix_gauss[line][item]
        if abs(sum_vars-ans)>eps:
            return False
    return True


def gauss_ans(variables: list[str], matrix_gauss: list[list[int]]) -> dict[str:float]:
    free_vars = []
    ans_dict = {var:None for var in variables}
    for line in range(len(matrix_gauss)-1, -1, -1):
        check = correct_check(matrix_gauss[line][:-1], matrix_gauss[line][-1])
        if check == "OK":
            element = matrix_gauss[line][line]
            ans_dict[variables[line]] = matrix_gauss[line][-1]/element
        elif check == "NO SOLUTION":
            return None
        elif check == "REDUNDANT LINE":
            continue
        elif check == "TWO OR MORE VARIABLES":
            non_zeros = 0
            for item in range(len(matrix_gauss[0])-1):
                if matrix_gauss[line][item] != 0:
                    non_zeros += 1
            sum_vars = 0
            for item in range(len(matrix_gauss[0])-2,-1,-1):
                var = variables[item]
                if ans_dict[var] == None and matrix_gauss[line][item]!=0:
                    if non_zeros > 1:
                        ans_dict[var] = 1
                        free_vars.append(var)
                        sum_vars += matrix_gauss[line][item]
                        non_zeros -= 1
                    else:
                        ans_dict[var] = (matrix_gauss[line][-1] - sum_vars) / matrix_gauss[line][item]
                        non_zeros -= 1
                elif ans_dict[var] != None:
                    sum_vars += matrix_gauss[line][item]*ans_dict[var]
                    non_zeros -= 1
                    
    return [ans_dict,free_vars]


def main():
    linear = open("linear.txt", "r").read()

    print(f"{"REQUESTED SYSTEM OF LINEAR EQUATIONS":=^50}")
    print(linear)
    print(f"{"=":=^50}")

    parsed = parse_linear(linear)
    variables = parsed[0]
    variables_book = parsed[1]
    matrix = linear_to_matrix(variables, variables_book)

    print(f"{"MATRIX OF LINEAR EQUATIONS":=^50}")
    print_matrix(variables, matrix)
    print(f"{"=":=^50}")

    matrix_gauss = gauss_elimination(matrix)

    print(f"{"MATRIX OF LINEAR EQUATIONS AFTER GAUSS":=^50}")
    print_matrix(variables, matrix_gauss)
    print(f"{"=":=^50}")

    gauss = gauss_ans(variables, matrix_gauss)
    if gauss != None and gauss[1]==[]:
        print("ANSWER:", end=' ')
        for var in range(len(variables)-1):
            print(variables[var], '=', gauss[0][variables[var]], sep='', end=", " if var < len(variables)-2 else '.')
    elif gauss != None and gauss[1]!=[]:
        ans = last_check(matrix_gauss, variables, gauss[0])
        if ans:
            print("ANSWER:", end=' ')
            for var in range(len(variables)-1):
                print(variables[var], '=', gauss[0][variables[var]] if variables[var] not in gauss[1] else str(gauss[0][variables[var]])+"(FREE)", sep='', end=", " if var < len(variables)-2 else '.')
            print('\n'+"INFINITE SOLUTIONS FOR FREE VARIABLES")
        else:
            print("ANSWER: NO SOLUTIONS")
    else:
        print("ANSWER: NO SOLUTIONS")


if __name__ == '__main__':
    main()