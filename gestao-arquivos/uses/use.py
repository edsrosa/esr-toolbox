from models.model import gteFileManagement

def list_folder(basefolder):
    """Pasta para gerenciar os arquivos."""
    management = gteFileManagement()
    management.set_basefolder(basefolder=basefolder)
    management.list_subfolders_files()
    management.get_properties_files()
    return management

def export_xlsx(list_folder, filepath):
    """Exporta a listagem para um arquivo xlsx."""
    list_folder.properties_to_dict_files()
    list_folder.save_table_excel(filepath)
