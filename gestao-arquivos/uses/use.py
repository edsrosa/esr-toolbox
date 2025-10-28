from models.model import gteFileManagement

def folder(basefolder):
    """Pasta para gerenciar os arquivos."""
    management = gteFileManagement()
    management.set_basefolder(basefolder=basefolder)
    management.list_subfolders_files()
    management.get_properties_files
    return management
