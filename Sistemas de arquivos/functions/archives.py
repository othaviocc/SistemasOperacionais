from exceptions import *

# <-::- FUNÇÕES DE ARQUIVOS -::->

class Archives():
    def __init__(self, control):
        self.control = control

    def touch(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #cria um arquivo vazio
        if len(args) != 1: raise WrongParameters('Você deve passar um parâmetro para esta função! Use touch [arquivo]')
        dir = args[0].split('/') # dir[-1] --> Filename
        if dir[-1] in ['.', '..', '']: raise NotAcceptableFileName('Nome do arquivo inválido')
        cwd = self.control.change_dir(file, cwd[0], dir[0:-1], inodes_array) #guarda inode do diretorio pai
        self.control.create_file(file, dir[-1], inodes_array, inodes_bitmap, cwd, blocks_bitmap)# Cria um novo arquivo no diretório atual, alocando um i-node e atualizando os bitmaps
            #self.control.add_in_folder(file, file_inode, inodes_array, cwd, blocks_bitmap)

    def rm(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #remove um arquivo do sistema e libera seu espaço
        if len(args) != 1: raise WrongParameters('Você deve passar um parâmetro para esta função! Use rm [arquivo]')
        dir = args[0].split('/')
        if dir[-1] in ['.', '..']: raise CantRemove('Nao é permitido remover diretorios especiais')
        cwd = self.control.change_dir(file, cwd[0], dir[0:-1], inodes_array)    #guarda inode do diretorio pai
        folder_dict = self.control.read_blocks(file, cwd, inodes_array)  #le o conteudo do diretorio atual
        f_inode = self.control.read_inode(inodes_array, folder_dict[dir[-1]])  # pega inode do arquivo q vai ser removido

        if f_inode.permissions[0] == '-':  #se eh um arquivo comum
            for block in f_inode.block_pointers: #libera blocos
                blocks_bitmap[block] = 0
            inodes_bitmap[f_inode.index] = 0  #libera inode
            del folder_dict[dir[-1]]   #remove nome do diretorio
            self.control.save_bitmap(file, blocks_bitmap, inodes_bitmap)  #salva no disco os bitmaps atualizados
            self.control.rewrite(file, cwd, inodes_array, folder_dict, blocks_bitmap)  #regrava o diretorio sem o arquivo removido

    def echo(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        # ercreve conteudo em um arquivo
        if len(args) != 3: raise WrongParameters('Você deve passar três parâmetros para esta função! Use echo ["mensagem"] [>, >>] [arquivo]')
        dir = args[2].split('/') # dir[-1] --> Filename
        if dir[-1] in ['.', '..', '']: raise NotAcceptableFileName('Nome arquivo invalido')
        cwd = self.control.change_dir(file, cwd[0], dir[0:-1], inodes_array)    #guarda inode do diretorio pai
        folder_dict = self.control.read_blocks(file, cwd, inodes_array) #le o conteudo do diretorio atual
        match args[1]:
            case '>': #se ja existe substitui, caso não, cria arquivo
                if dir[-1] in folder_dict:
                    (self.control.rewrite, self.control.read_inode(inodes_array, folder_dict[dir[-1]]), inodes_array, args[0], blocks_bitmap)
                else:
                    self.control.create_file(file, dir[-1], inodes_array, inodes_bitmap, cwd, blocks_bitmap, args[0])
            case '>>': #se ja existe /n, caso não, cria arquivo
                if dir[-1] in folder_dict:
                    file_content = self.control.read_blocks(file, self.control.read_inode(inodes_array, folder_dict[dir[-1]]), inodes_array)
                    self.control.rewrite(file, self.control.read_inode(inodes_array, folder_dict[dir[-1]]), inodes_array, (file_content  + '\n' + args[0]) if file_content else args[0], blocks_bitmap)
                else:
                    self.control.create_file(file, dir[-1], inodes_array, inodes_bitmap, cwd, blocks_bitmap, args[0])

    def cat(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #exibe conteudo arquivo
        if len(args) != 1: raise WrongParameters('Você deve passar um parâmetro para esta função! Use cat [arquivo]')
        dir = args[0].split('/') # dir[-1] --> Filename
        if dir[-1] in ['.', '..', '']: raise NotAcceptableFileName('Nome invalido para leitura')
        cwd = self.control.change_dir(file, cwd[0], dir[0:-1], inodes_array)   #guarda inode do diretorio pai
        folder_dict = self.control.read_blocks(file, cwd, inodes_array)  #le o conteudo do diretorio atual
        file_inode = self.control.read_inode(inodes_array, folder_dict[dir[-1]])   # Obtém o i-node do arquivo que será lido
        content = self.control.read_blocks(file, file_inode, inodes_array)   # Lê o conteúdo armazenado nos blocos desse arquivo
        print('<-::- FILE CONTENT -::->')
        print(content.replace("\\n", '\n'))
        print('<-::- END OF FILE -::->')

    def cp(self, file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, *args):
        #copia conteudo de um arquivo pro outro
        # <-::- Manipular Arquivo 1 -::->
        if len(args) != 2: raise WrongParameters('Você deve passar dois parâmetros para esta função! Use cp [origem] [destino]')
        dir1, dir2 = args
        dir1 = dir1.split('/')
        if dir1[-1] in ['.', '..', '']: raise NotAcceptableFileName('Parametros incorretos')
        t_cwd = self.control.change_dir(file, cwd[0], dir1[0:-1], inodes_array)       # Muda para o diretório onde o arquivo original está localizado
        folder_dict = self.control.read_blocks(file, t_cwd, inodes_array)   #le o conteudo do diretorio atual
        content = self.control.read_blocks(file, self.control.read_inode(inodes_array, folder_dict[dir1[-1]]), inodes_array)   # Lê o conteúdo real do arquivo original

        # <-::- Copiar Arquivo 2 -::->
        # Cria o novo arquivo no destino e escreve nele o conteúdo copiado no modo '>' que eh sobrescreve/cria)
        self.echo(file, cwd, inodes_array, blocks_bitmap, inodes_bitmap, content, '>', dir2)
        