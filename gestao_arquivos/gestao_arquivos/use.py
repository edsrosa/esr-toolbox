from .models import gteFileManagement

def list_folder(basefolder):
    """Pasta para gerenciar os arquivos."""
    management = gteFileManagement()
    management.list_properties(basefolder)
    return management

def export_xlsx(list_folder, filepath):
    """Exporta a listagem para um arquivo xlsx."""
    list_folder.properties_to_dict_files()
    list_folder.save_table_excel(filepath)
