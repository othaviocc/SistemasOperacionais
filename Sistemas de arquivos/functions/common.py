import os

from exceptions import *

class Common:
    def __init__(self, control):
        self.control = control

    def mv(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #move ou renomeia arquivos e diretorios
        # <-::- Manipular Arquivo 1 -::->
        if len(args) != 2: raise WrongParameters('Você deve passar dois parâmetros para esta função! Use mv [arquivo1] [arquivo2]')
        dir1, dir2 = args
        dir1 = dir1.split('/')
        if dir1[-1] in ['.', '..', '']: raise CantMoveParent('Use ../ para mover esta pasta')
        t1_cwd = self.control.change_dir(file, cwd[0], dir1[0:-1], inodes_array)      # Entra no diretório onde o arquivo de origem está localizado
        folder_dict1 = self.control.read_blocks(file, t1_cwd, inodes_array)    # Lê o conteúdo do diretório de origem
        # Pega o índice do inode do arquivo a mover e remove-o do diretório antigo
        index = folder_dict1[dir1[-1]] 
        del folder_dict1[dir1[-1]]

        # <-::- Manipular Arquivo 2 -::->
        dir2 = dir2.split('/')
        if dir2[-1] in ['.', '..', '']: raise CantMoveParent('Não é possível utilizar este tipo de caminho')
        t2_cwd = self.control.change_dir(file, cwd[0], dir2[0:-1], inodes_array)     # Entra no diretório de destino
        folder_dict2 = self.control.read_blocks(file, t2_cwd, inodes_array)    # Lê o conteúdo do diretório de destino
         # Impede sobrescrever um arquivo existente
        if dir2[-1] in folder_dict2: raise FileAlreadyExists('O diretório final já existe!')
        # Adiciona a entrada do arquivo no diretório de destino, alem de atualizar o nome do inode para o novo destino
        folder_dict2[dir2[-1]] = index
        inode = self.control.read_inode(inodes_array, index)
        inode.name = dir2[-1]

        # <-::- Gravar alterações -::->
        self.control.save_inode(inodes_array, inode) 
        # Regrava o diretório de origem (sem o arquivo) e o de destino (com o arquivo)
        self.control.rewrite(file, t1_cwd, inodes_array, folder_dict1, blocks_bitmap)
        self.control.rewrite(file, t2_cwd, inodes_array, folder_dict2, blocks_bitmap)       
        
    def ln(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #cria links simbolicos entre arquivos/diretorios
        # <-::- Manipular Arquivo 1 -::->
        if len(args) != 2: raise WrongParameters('Você deve passar dois parâmetros para esta função! Use "ln [arquivo1] [arquivo2]"')
        dir1, dir2 = args
        dir1 = dir1.split('/')
        if dir1[-1] in ['.', '..', '']: raise CantMoveParent('Use ../ para linkar esta pasta')
        t1_cwd = self.control.change_dir(file, cwd[0], dir1[0:-1], inodes_array)    # Entra no diretório onde está o arquivo original
        folder_dict1 = self.control.read_blocks(file, t1_cwd, inodes_array)    # Lê o conteúdo do diretório de origem
        org_inode = self.control.read_inode(inodes_array, folder_dict1[dir1[-1]])    # Lê o inode do arquivo original (que será linkado)

        # <-::- Manipular Arquivo 2 -::->
        dir2 = dir2.split('/')
        if dir2[-1] in ['.', '..', '']: raise CantMoveParent('Não é possível criar um link em uma pasta pai')
        t2_cwd = self.control.change_dir(file, cwd[0], dir2[0:-1], inodes_array)    # Entra no diretório onde o link será criado
        folder_dict2 = self.control.read_blocks(file, t2_cwd, inodes_array)    # Lê o conteúdo do diretório de destino
        # Impede sobrescrever um arquivo/link existente
        if dir2[-1] in folder_dict2: raise FileAlreadyExists('O diretório/arquivo final já existe!')
        inode = self.control.create_link_inode(dir2[-1], org_inode, inodes_bitmap)    # Cria o novo inode de link que aponta para o arquivo original
        folder_dict2[inode.name] = inode.index    # Adiciona o link simbólico ao diretório de destino

        # <-::- Gravar alterações -::->
        self.control.save_inode(inodes_array, inode)
        # Regrava o diretório de origem (sem o arquivo) e o de destino (com o arquivo) no disco
        self.control.rewrite(file, t1_cwd, inodes_array, folder_dict1, blocks_bitmap)
        self.control.rewrite(file, t2_cwd, inodes_array, folder_dict2, blocks_bitmap)       

    def clear(*args):
        # Clear
        os.system('cls')

    def exit(*args):
        #exit
        exit(0)