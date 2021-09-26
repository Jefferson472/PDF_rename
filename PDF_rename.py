import os
import re
import shutil
import pdfplumber

# ACESSAR DIRETÓRIO E LER SOMENTE ARQUIVOS .PDF
main_folder = os.getcwd()
print(main_folder)



# ACESSA O ARQUIVO PDF E LÊ AS PALAVRAS NAS POSIÇÕES [9], [11] E [12] E RETORNA ESTA INFORMAÇÃO
def ler_pdf(path_pdf):
    path = main_folder + '\\' + path_pdf
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        text = page.extract_words()
    try:
        po_number = text[9]['text']
        forn_name = text[11]['text'].replace('-', '') + ' ' + text[12]['text']
        return f'{po_number} - {forn_name}'
    except:
        log_event = open('log_event.txt', 'a')
        log_event.write(f'Não foi possível ler o arquivo: {path} \n')
        pass


if __name__ == '__main__':
    # VERIFICA ARQUIVO POR ARQUIVO DO DIRETÓRIO ATUAL, CASO SEJA UM .PDF INICIA A EXECUÇÃO DE LEITURA E RENOMEIA O ARQUIVO 
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if re.search(r'\.pdf$', file):
                file_name, file_extension = os.path.splitext(file)
                new_name = ler_pdf(file)

                if new_name is not None:
                    new_name = 'PO ' + new_name + file_extension
                    old_file_full_path = os.path.join(root, file)
                    new_file_full_path = os.path.join(root, new_name)
                    print(f'Movendo arquivo "{file}" para "{new_name}"')
                    try:
                        shutil.move(old_file_full_path, new_file_full_path)
                    except:
                        log_event = open('log_event.txt', 'a')
                        log_event.write(f'Não foi possível renomear o arquivo: {file} \n')
                        pass
