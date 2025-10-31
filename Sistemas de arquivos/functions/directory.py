from exceptions import *

class Directory:
    def __init__(self, control):
        self.control = control

    def mkdir(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        # cria um novo diretorio dentro do diretorio atual
        if len(args) != 1: raise WrongParameters('Uso correto: mkdir <diretorio>')
        dir = args[0].split('/')
        if dir[-1] in ['.', '..', '']: raise NotAcceptableDirName(f"A pasta não pode se chamar {dir[-1]}")
        cwd = self.control.change_dir(file, cwd[0], dir[0:-1], inodes_array)   # Entra no diretório onde a nova pasta será criada
        self.control.create_folder(file, dir[-1], inodes_array, inodes_bitmap, cwd, blocks_bitmap)   # Cria a nova pasta, aloca i-node e atualiza bitmaps
        #self.control.add_in_folder(file, folder, inodes_array, cwd, blocks_bitmap)

    def rmdir(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #remove um diretorio vazio do sistema
        if len(args) != 1: raise WrongParameters('Uso correto: rmdir <diretorio>')
        dir = args[0].split('/')
        if dir[-1] in ['.', '..']: raise CantRemove('Não é permitido remover diretórios especiais')
        cwd = self.control.change_dir(file, cwd[0], dir, inodes_array)  # Entra na pasta que será removida
        folder_dict = self.control.read_blocks(file, cwd, inodes_array) #le o conteudo da pasta
        if len(folder_dict) == 2: #verifica se o diretorio esta 'vazio'
            for block in cwd.block_pointers:
                blocks_bitmap[block] = 0   # Libera os blocos usados pela pasta
            inodes_bitmap[cwd.index] = 0   # Libera o i-node da pasta
            cwd = self.control.read_inode(inodes_array, folder_dict['..'])  # Volta para o diretório pai
            folder_dict = self.control.read_blocks(file, cwd, inodes_array)  # Lê o conteúdo do diretório pai
            del folder_dict[dir[-1]]  #remove a referencia da pasta apagada
            self.control.save_bitmap(file, blocks_bitmap, inodes_bitmap)  #salva bitmaps atualizados no disco
            self.control.rewrite(file, cwd, inodes_array, folder_dict, blocks_bitmap)   #regrava o diretorio pai sem a pasta que foi removida

    def ls(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #lista o conteudo
        if len(args) != 0 and len(args) != 1: raise WrongParameters 
        dir = args[0].split('/') if len(args) != 0 else []  # Se foi passado um caminho, divide em partes, caso nao, lista o diretório atual
        cwd = self.control.change_dir(file, cwd[0], dir[0:-1], inodes_array)   #entra no diretorio 
        folder_dict = self.control.read_blocks(file, cwd, inodes_array)   #le o conteudo do diretorio

        # <-::- Formatar saida -::->
        del folder_dict['.'], folder_dict['..']   #remove entradas especiais
        #ordena a saida, primeiro diretorios(permissao d), depois arquivos
        formatted_output = sorted(folder_dict, key=lambda x: (self.control.read_inode(inodes_array, folder_dict[x]).permissions[0], x))
        for item in formatted_output:  #imprime diretorios em vermelho e arquivos em branco
            if self.control.read_inode(inodes_array, folder_dict[item]).permissions[0] == 'd':
                print(f'\033[1;31m{item}/ ', end='')
            else:
                print(f'\033[37m{item} ', end='')
        if len(folder_dict) > 0: print('\033[0m')

    def cd(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #altera o diretorio
        if len(args) != 1: raise WrongParameters('Parametros incorretos, uso correto: cd <diretorio>')
        dir = args[0].split('/')   #divide o caminho em partes
        cwd[0] = self.control.change_dir(file, cwd[0], dir, inodes_array)   #atualiza o diretorio atual para o destino informado
