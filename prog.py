class Program:
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"

    def __init__(self):
        self.id = 0
        self.acc = 0
        self.pc = 0
        self.code = []
        self.data = {}
        self.arrival_time = 0
        self.period = 0
        self.execution_time = 0
        self.remaining_time = 0  # Renomeado de times_executed para remaining_time
        self.state = Program.WAITING
        self.start_time = None
        self.end_time = None
        self.deadline = 0
        
    def __str__(self):
        return f"Program ID {self.id}|State: {self.state}| Remaining_time: {self.remaining_time}, PC: {self.pc}|\nwith Arrival_time: {self.arrival_time}, Period: {self.period}, Execution_time: {self.execution_time},"

    def set_code(self, new_code):
        self.code = new_code
 
           
    def calculate_deadline(self, current_time):
        time_since_last_period_start = current_time % self.period
        if time_since_last_period_start == 0:
            self.deadline = self.period
            self.remaining_time = self.execution_time
            return True
        else:
            self.deadline = self.period - time_since_last_period_start
            return False

    def is_finished(self, current_time):
        x = len(self.code) 
        if self.state != Program.FINISHED and self.pc >= x:
            self.state = Program.FINISHED
            self.end_time = current_time
            return True
        else:
            return False
        
    def is_started(self, current_time):
        if self.state == Program.RUNNING and self.pc == 0:
            self.start_time = current_time

    def update_remaining_time(self): 
        if self.remaining_time > 0:
            self.remaining_time -=  1
            return False
        elif self.remaining_time == 0:
            return True


def execute_instruction(program, mnemonic, instr_input):
    if mnemonic == "load":
        if instr_input.startswith("#"):
            program.acc = int(instr_input[1:])  # Modo imediato
        elif instr_input in program.data:
            program.acc = program.data[instr_input]  # Modo direto
        else:
            print(f"Erro: Variável {instr_input} não encontrada em dados.")
            return

    elif mnemonic == "add":
        if instr_input.startswith("#"):
            program.acc += int(instr_input[1:])  # Modo imediato
        elif instr_input in program.data:
            program.acc += program.data[instr_input]  # Modo direto
        else:
            print(f"Erro: Variável {instr_input} não encontrada em dados.")
            return
        
    elif mnemonic == "sub":
        if instr_input.startswith("#"):
            program.acc -= int(instr_input[1:])  # Modo imediato
        elif instr_input in program.data:
            program.acc -= program.data[instr_input]  # Modo direto
        else:
            print(f"Erro: Variável {instr_input} não encontrada em dados.")
            return

    elif mnemonic == "mult":
        if instr_input.startswith("#"):
            program.acc *= int(instr_input[1:])  # Modo imediato
        elif instr_input in program.data:
            program.acc *= program.data[instr_input]  # Modo direto
        else:
            print(f"Erro: Variável {instr_input} não encontrada em dados.")
            return

    elif mnemonic == "div":
        if instr_input.startswith("#"):
            program.acc //= int(instr_input[1:])  # Modo imediato (divisão inteira)
        elif instr_input in program.data:
            program.acc //= program.data[instr_input]  # Modo direto
        else:
            print(f"Erro: Variável {instr_input} não encontrada em dados.")
            return
        
    elif mnemonic == "store":
        if instr_input in program.data:
            program.data[instr_input] = program.acc
        else:
            print(f"Erro: Variável {instr_input} não encontrada em dados.")
            return

    elif mnemonic == "brany":
        target_line = next((index for index, line in enumerate(program.code) if line[2] == instr_input), None)
        if target_line is not None:
            program.pc = target_line - 1
        else:
            print(f"Erro: Label {instr_input} não encontrada no código.")
            return
        
    elif mnemonic in ["brpos", "brzero", "brneg"]:
        target_line = next((index for index, line in enumerate(program.code) if line[2] == instr_input), None)
        if target_line is not None:
            if (mnemonic == "brpos" and program.acc > 0) or \
               (mnemonic == "brzero" and program.acc == 0) or \
               (mnemonic == "brneg" and program.acc < 0):
                program.pc = target_line - 1
        else:
            print(f"Erro: Label {instr_input} não encontrada no código.")
            return

    elif mnemonic == "syscall":
        if instr_input == "0":
            program.pc = len(program.code) 
        elif instr_input == "1":
            print(program.acc)
        elif instr_input == "2":
            value = input("Digite um valor: ")  # Renomeado para evitar conflito
            program.acc = int(value)
        else:
            print(f"Erro: SYSCALL com argumento {instr_input} não reconhecido.")
            return

    program.pc += 1

def run_program(program):
    if program.pc < len(program.code):
        instruction = program.code[program.pc]
        mnemonic = instruction[1]
        input_value = instruction[2] if len(instruction) > 2 else None
        execute_instruction(program, mnemonic, input_value)
        
# Atualizando a função edf_scheduler para evitar um loop infinito
def edf_scheduler(programs):
    current_time = -1
    n = 0
    i = 0
    t = Program()
    r = Program()

    while not all(p.state == Program.FINISHED for p in programs):
        for program in programs:  
            program.calculate_deadline(current_time)
        
        #Filas que tem o prog em waiting ou running
        #Fila de programas q o rem..._t... > 0
        waiting = [o for o in programs if o.remaining_time > 0 and o.state != Program.FINISHED and current_time >= o.arrival_time]
        #Fila de programas que n terminaram e com arr..._t... >= c..._t... para comparacao
        vi = [r for r in programs if r.state != Program.FINISHED and current_time >= r.arrival_time]
        #Fila de programas q o rem..._t... == 0
        notf = [k for k in programs if k.remaining_time == 0 and k.state != Program.FINISHED and current_time >= k.arrival_time]
        a = [a for a in programs if a.state != Program.FINISHED]
        lnof = len(notf) - 1
        true = False
    
        print(f"Current Time: {current_time}")
        print(f"Waiting: {len(waiting)}")
        print(f"Vi: {len(vi)}")
        print(f"Notf: {len(notf)}")
        print(f"Current Time: {current_time}")

        # Inicio do EDF Contando que o programa tem que executar no minimo de vezes dita pelo Execution_time, dentro do periodo/deadline

        if len(waiting) > 0:
            r = t  #salva o t
            t = min(waiting, key=lambda p: p.deadline) #pega o com menor deadline
            if t != r and r.state !=Program.FINISHED and current_time !=0: #se mudou o t colocca o programa anterior em waiting (t != r or t!=notf[i]) 
                r.state = Program.WAITING
                print(r)
            t.state = Program.RUNNING
            t.is_started(current_time)
            print(t)
            run_program(t)
            t.update_remaining_time()
            if t.is_finished(current_time):# se tiver terminado
                print(t)
            current_time += 1

        #se for comecar o fifo e nao comecar pelo que estava em running, bloqueia 
        if len(waiting) == 0 and len(vi) > 0 and len(notf) > 0:
            if t != notf[i] and t.state !=Program.FINISHED:
                t.state = Program.WAITING
                print(f"Current Time: {current_time}")
                print(t)

        #Inicio de um Fifo se todos os programas ja estiverem executado o execution time
        while len(notf) == len(vi) and len(vi) > 0: # se todos os programas em waiting sao zero
            if i > lnof:
                i = 0
            if i <= lnof: 
                if notf[i].execution_time != n:
                    notf[i].state = Program.RUNNING
                    notf[i].is_started(current_time) # verifica se é a primeira vez q executa 
                    run_program(notf[i])
                    print(f"Current Time: {current_time}")
                    print(notf[i])
                    n += 1
                if notf[i].is_finished(current_time):
                    i = 0
                    n = 0
                    print(f"Current Time: {current_time}")
                    print(notf[i])
                    current_time += 1
                    break
                current_time += 1
                if notf[i].execution_time == n and notf[i].state != Program.FINISHED:
                    notf[i].state = Program.WAITING
                    print(f"Current Time: {current_time}")
                    print(notf[i])
                    i += 1
                    n = 0
                # Condicao para sair do fifo, para voltar a ser EDF
                # se pelo menos um tiver o o remaining time !=0 vai pra EDF
                for program in vi:  
                    if program.calculate_deadline(current_time) == True:
                        i = 0
                        true = True
                        break
                if true == True:
                    break

        #ate chegar num arrivle_time   
        if len(waiting) == 0 and len(notf) == 0 and len(a)!=0:
            current_time += 1

        



def read_assembly_file(filename):
    program = Program()

    with open(filename, 'r') as file:
        lines = file.readlines()

    # Separar as seções .code e .data
    code_section = lines[lines.index(".code\n")+1:lines.index(".endcode\n")]
    data_section = lines[lines.index(".data\n")+1:lines.index(".enddata\n")]

    # Processar a seção .code
    for index, line in enumerate(code_section):
        if line.strip():  # Ignorar linhas vazias
            instruction = line.strip().split()
            program.code.append([index] + instruction)

    # Processar a seção .data
    for line in data_section:
        if line.strip():  # Ignorar linhas vazias
            variable, value = line.strip().split()
            program.data[variable] = int(value)

    return program

def main():
    filenames = ["C:\\Users\\bruno\\Desktop\\prog1.txt", 
                 "C:\\Users\\bruno\\Desktop\\prog2.txt", 
                 "C:\\Users\\bruno\\Desktop\\prog3.txt"]
    
    programs = [read_assembly_file(filename) for filename in filenames]

    for idx, prog in enumerate(programs):
       prog.arrival_time = int(input(f"Digite o arrival time para o Programa {idx + 1}: "))
       prog.execution_time = int(input(f"Digite o tempo de execução para o Programa {idx + 1}: "))
       prog.period = int(input(f"Digite o período (deadline) para o Programa {idx + 1}: "))
       prog.remaining_time = prog.execution_time
       prog.id = idx + 1

    edf_scheduler(programs)

    print("\n" + "-"*50 + "\n")
    for idx, prog in enumerate(programs):
        print(f"\n{prog}:\n")
        print(f"acc: {prog.acc}")
        print(f"pc: {prog.pc}")
        print(f"arrival_time: {prog.arrival_time}")
        print(f"period: {prog.period}")
        print(f"execution_time: {prog.execution_time}")
        print("\nCode:")
        for line in prog.code:
            print(line)
        print("\nData:")
        for var, value in prog.data.items():
            print(f"{var}: {value}")
        print("\n" + "-"*50 + "\n")

    # Imprime os resultados
    for prog in programs:
        print(f"Program ID-{prog.id}:")
        print(f"Start time: {prog.start_time}")
        print(f"End time: {prog.end_time}")
        print(f"Total computation time: {prog.end_time - prog.start_time + 1}")
        print("-" * 50)


if __name__ == "__main__":
    main()