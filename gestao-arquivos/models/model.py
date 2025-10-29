import os
import datetime as dt
import hashlib
import zipfile as zf

import pandas as pd


class gteFile:
    def __init__(self):
        """Classe de arquivo base."""
        self.folderpath =''  # caminho onde o arquivo está salvo
        self.filename=''  #  nome do arquivo com a extensão
        self.name=''  # nome do arquivo
        self.extension='.'  # extensão do arquivo, com o . incluído
        self.filepath='' # caminnho

        self.folder=''
        self.datetime_creation=''
        self.datetime_acess=''
        self.datetime_modification=''
        self.size_byte=0
        self.hash_sha256=''
        self.table={}
        self.gteZip_list=[]
    
    def new_gteFile(self, folderpath, filename):
        """Define um novo arquivo com nome e pasta"""
        self.folderpath = folderpath
        self.filename = filename
        self.filepath = os.path.join(folderpath, filename)
        self.name, self.extension = os.path.splitext(filename)
        self.folder = os.path.basename(folderpath)

    def get_properties(self):
        """Recupera as propriedades do arquivo."""
        self.datetime_creation = dt.datetime.fromtimestamp(os.path.getctime(self.filepath))
        self.datetime_acess = dt.datetime.fromtimestamp(os.path.getatime(self.filepath))
        self.datetime_modification = dt.datetime.fromtimestamp(os.path.getmtime(self.filepath))
        self.size_byte = float(os.path.getsize(self.filepath))

    def generate_hashing(self):
        """Cria o Hash do conteúdo do arquivo usando o algoritmo SHA 256."""
        hash256 = hashlib.sha256()
        hash256.update(open(self.filepath, 'rb').read())
        self.hash_sha256 = hash256.hexdigest()

    def properties_to_dict(self):
        """Extrai as propriedades para um dicionario."""
        table = {"filepath": self.filepath, 
                 "folderpath": self.folderpath,
                 "filename": self.filename, 
                 "name": self.name, 
                 "extension": self.extension, 
                 "folder": self.folder, 
                 "creation_date": self.datetime_creation, 
                 "acess_date": self.datetime_acess, 
                 "modification_date": self.datetime_modification, 
                 "size_byte": self.size_byte, 
                 "hash_sha256": self.hash_sha256
                 }
        self.table = table

    def gteZip_list(self):
        """ZipFile: Listagem do conteúdo do arquivo zip."""
        if self.extension == '.zip':
            obj_zipped = zf.ZipFile(self.filepath)
            self.gteZip_list = obj_zipped.namelist()
    
    def gteZip_unzip(self):
        """ZipFile: Descompactar arquivos zip."""
        if self.extension == '.zip':
            file_zipped = zf.ZipFile(self.filepath)
            file_zipped.close()


class gteFileManagement:
    def __init__(self):
        """Gestão de arquivos diversos."""
        self.basefolder='' # caminho da pasta base
        self.paths_folder=[] # caminhos de todas as pastas incluidas na pasta base e em suas subpastas
        self.paths_files=[] # caminhos de todos os arquivos incluídos na pasta base e em suas subpastas
        self.gteFiles=[] # gte files
        self.table_properties={}

    def set_basefolder(self, basefolder):
        """Insere o caminho da pasta de referência."""
        self.basefolder=basefolder # caminho da pasta base

    def list_subfolders_files(self):
        """Lista todas as pastas e arquivos de dada pasta."""
        self.paths_folder.clear()
        self.paths_files.clear()
        for folder, subfolders, filenames in os.walk(self.basefolder):
            self.paths_folder.append([folder, subfolders])
            if filenames != []:
                for filename in filenames:
                    self.paths_files.append([folder, filename])

    def get_properties_files(self):
        """Lista as propriedades dos arquivos da pasta e subpastas."""
        self.gteFiles.clear()
        for pf in self.paths_files:
            file = gteFile()
            file.new_gteFile(pf[0], pf[1])
            file.get_properties()
            self.gteFiles.append(file)

    def properties_to_dict_files(self):
        """Extrai as propriedades de todos os arquivos para dicionarios."""
        self.table_properties.clear()
        
        for i, fp in enumerate(self.gteFiles):
            self.gteFiles[i].properties_to_dict()
        
        table_properties = {}

        for fp in self.gteFiles:
            for k, v in fp.table.items():
                if k not in table_properties:
                    table_properties[k] = []
                table_properties[k].append(v)
        
        self.table_properties = table_properties
    
    def save_table_excel(self, filepath):
        """Salva tabela de propriedades em um Excel."""
        df = pd.DataFrame.from_dict(self.table_properties)
        df.to_excel(filepath)